import os
import sys
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger

'''
For a pdf of, for example, 32 pages, this will create separate pdf's
for the front and back pages of the first 'signature' (pages 1-16),
and additional separate pdf's of the front and back pages of the
second signature (pages 17-32).  The expectation is that these will
be printed out using sheets of paper twice the size of the pages (e.g.
11x17 paper for pages which are 8.5x11), on a printer which does not
flip the pages for you (hence separate pdf's so that you can print
one out, then manually reinsert the same sheets of paper to print
on the other side).
'''

FRONT_SIDE_PAGE_NBRS  = [8,9,6,11,4,13,2,15]
BACK_SIDE_PAGE_NBRS   = [16,1,14,3,12,5,10,7]

def audit_command_line_inputs(argv):
    # e.g. python shuffle.py newbook.pdf signatures
    output_msg          = None
    inputs              = {}
    input_labels        = ['input_pdf_path','dir_for_sigs']
    if len(argv) != (1 + len(input_labels)):
        print('lenargv',len(argv),'leninputlabels',len(input_labels))
        output_msg = 'arguments should be: '
        for label in input_labels:
            output_msg += label
            output_msg += ', '
        output_msg      = output_msg[:-2] #chop off last ', '
    elif (argv[1][-4:] != '.pdf'):
        output_msg      = 'first argument must be the pathname of the input pdf file'
    elif (not os.path.exists(argv[1])):
        output_msg      = 'cannot find input pdf file '+argv[1]
    elif (not os.path.isdir(argv[2])):
        output_msg      = 'second argument must be a directory to put the signature pdfs in'
    else:
        for index,key in enumerate(input_labels):
            inputs[key] = argv[index+1]
    return output_msg,inputs

def inspect_input_pdf(pdfInOrder):
    output                = PdfFileWriter()
    how_many_pages        = pdfInOrder.getNumPages()
    nbr_sigs              = int(how_many_pages / 16)
    return how_many_pages,nbr_sigs

def sig_number_generator(twice_sig_nbr):
    is_odd = twice_sig_nbr % 2
    if is_odd:
        sig_nbr = (twice_sig_nbr / 2) - 0.5
        return [int(p + (sig_nbr*16)) for p in BACK_SIDE_PAGE_NBRS]
    else:
        sig_nbr = twice_sig_nbr / 2
        return [int(p + (sig_nbr*16)) for p in FRONT_SIDE_PAGE_NBRS]

def plan_signatures(nbr_sigs):
    sig_side_page_numbers = [sig_number_generator(nbr) for nbr in list(range(0,2*nbr_sigs))]
    front_side            = lambda x: 'sig'+str(x)+'FrontSide'
    back_side             = lambda x: 'sig'+str(x)+'BackSide'
    sig_side_filenames    = [f(x+1) for x in range(nbr_sigs) for f in (front_side,back_side)]
    return sig_side_page_numbers,sig_side_filenames


if __name__ == '__main__':
    output_msg,inputs                        = audit_command_line_inputs(sys.argv)
    if output_msg:
        print(output_msg)
        sys.exit(127)

    pdfInOrder                               = PdfFileReader(open( inputs['input_pdf_path'], "rb"))
    how_many_pages,nbr_sigs                  = inspect_input_pdf(pdfInOrder)
    print('how_many_pages',how_many_pages)
    if how_many_pages % 16 != 0:
        print('expecting a pdf with a number of pages that is a multiple of 16')
        sys.exit(127)
    print('number signatures: ',nbr_sigs)

    sig_side_page_numbers,sig_side_filenames = plan_signatures(nbr_sigs) 


    for filenameIndex,pageNumbers in enumerate(sig_side_page_numbers):
        tempPdfWriter = PdfFileWriter()
        for page in pageNumbers:
            tempPdfWriter.addPage(pdfInOrder.getPage(page-1))
        fn = sig_side_filenames[filenameIndex]+'.pdf'
        pn = os.path.join(inputs['dir_for_sigs'],fn)
        tempOutputStream = open(pn, "wb")
        tempPdfWriter.write(tempOutputStream)
        print(pn)
        tempOutputStream.close()


