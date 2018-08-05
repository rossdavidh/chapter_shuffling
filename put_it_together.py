# Merge PDFs
import os
import sys
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger


def audit_command_line_inputs(argv):
    # e.g. python put_it_together.py list_of_chapters.csv newbook.pdf
    output_msg          = None
    inputs              = {}
    input_labels        = ['list_of_chapters_path','output_filename']
    if len(argv) != (1 + len(input_labels)):
        print('lenargv',len(argv),'leninputlabels',len(input_labels))
        output_msg = 'arguments should be: '
        for label in input_labels:
            output_msg += label
            output_msg += ', '
        output_msg      = output_msg[:-2] #chop off last ', '
    elif (argv[1][-4:] != '.txt'):
        output_msg      = 'first argument must be the pathname of the text file of chapter files to put together'
    elif (not os.path.exists(argv[1])):
        output_msg      = 'cannot find file for list of chapters '+argv[1]
    elif (argv[2][-4:] != '.pdf'):
        output_msg      = 'second argument should be the filename for the output pdf, with the pdf suffix'
    else:
        for index,key in enumerate(input_labels):
            inputs[key] = argv[index+1]
    return output_msg,inputs

def load_chapter_pdfs(inputs):
    list_of_chapters = []
    with open(inputs['list_of_chapters_path']) as f:
        list_of_chapters = list(f)
    list_of_chapters = [("./"+c.strip()) for c in list_of_chapters if c.strip()]
    pdfChapters = [PdfFileReader(open(c,"rb")) for c in list_of_chapters]
    return pdfChapters

def calculate_numbers(pdfChapters):
    print('nbr of pdfs put together is: ',str(len(pdfChapters)))
    totalPagesInBook = 0
    for chapter in pdfChapters:
        totalPagesInBook += chapter.getNumPages()
    print('total non-blank pages in book is: ',totalPagesInBook)
    numBlankPages = 16 - (totalPagesInBook % 16) #one signature is 4 11x17 sheets folded in half (x2) on both sides (x2 again) = 16
    print('blank pages we had to add to get a number divisible by 16: ',numBlankPages)
    numStartBlankPages = 2 #magic number! But, it does insure that the first printed page is an odd one, so images are on the left when printed
    numEndBlankPages = numBlankPages - numStartBlankPages
    #NOTE: I should have also made sure that we have at least a few blank pages at the end,
    #      but perhaps just stick in a mini-signature of two sheets if there aren't any
    return numStartBlankPages,numEndBlankPages

def add_pages_to_output(numStartBlankPages,pdfChapters,numEndBlankPages):
    output = PdfFileWriter()
    blankPageFile = open("./blankPage.pdf", "rb")
    blankPagePdf = PdfFileReader(blankPageFile)
    for blankpage in range(0,numStartBlankPages):
        output.addPage(blankPagePdf.getPage(0))
    totPageNumberSoFar = numStartBlankPages
    for chapter in pdfChapters:
        chapterPages = chapter.getNumPages()
        print('chapterPages',chapterPages)
        for page in range(0,chapterPages):
            totPageNumberSoFar += 1
            output.addPage(chapter.getPage(page))
    for blankpage in range(0,numEndBlankPages):
        output.addPage(blankPagePdf.getPage(0))
    return output

if __name__ == '__main__':
    output_msg,inputs                        = audit_command_line_inputs(sys.argv)
    if output_msg:
        print(output_msg)
        sys.exit(127)
    pdfChapters                              = load_chapter_pdfs(inputs)
    numStartBlankPages,numEndBlankPages      = calculate_numbers(pdfChapters)
    output                                   = add_pages_to_output(numStartBlankPages,pdfChapters,numEndBlankPages)
    outputStream                             = open(inputs['output_filename'], "wb")
    output.write(outputStream)
    outputStream.close()
     
