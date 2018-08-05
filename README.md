# chapter_shuffling
stitch pdfs together into one book pdf, then split it apart again into pdfs for the signatures

Put a plain text file in the directory with the programs from this repo, that is simply a list of the pdf's you wish to
join together, with one pdf filename per line.  So, something like:

table_of_contents.pdf
chapter_1.pdf
chatper_2.pdf
appendix.pdf

Also put the chapter pdf's (in this case, table_of_contents.pdf, chapter_1.pdf, etc.) in the directory.  Then, at the command
line, issue the command:

python put_it_together.py list_of_chapters.txt newbook.pdf

The file newbook.pdf will be a single combined PDF file, but if you want to turn it into a bookbinding project, you may want to
shuffle the pages some.  To do that, after making sure there is a subdirectory called "signatures", issue this command:

python shuffle.py newbook.pdf signatures

The signature pdf's will be made for printing 16-page signatures on 8 sheets of paper, in a printer that does not turn the pages
over for you (so the front and back pages of each signature will be in separate 8-page pdf's).
