from os import walk
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader


def get_pdf_list():
    f = []
    for (dirpath, dirnames, filenames) in walk("./input"):
        f.extend(filenames)
        break
    return f


canvas_width = 566

# Create the watermark from an image
c = canvas.Canvas('watermark.pdf')

# Draw the image at x, y. I positioned the x,y to be where i like here
c.drawImage('sneeds-logo.png', canvas_width-4, 2, width=30, height=30, mask='auto', preserveAspectRatio=True)
c.drawString(canvas_width-73, 12, "SNEEDS.IR")
c.save()

pdf_list = get_pdf_list()

for booklet_name in pdf_list:
    watermark = PdfFileReader(open("watermark.pdf", "rb"))
    output_file = PdfFileWriter()
    input_file = PdfFileReader(open("input/" + booklet_name, "rb"))

    page_count = input_file.getNumPages()

    # Go through all the input file pages to add a watermark to them
    for page_number in range(page_count):
        print(booklet_name + ": Watermarking page {} of {}".format(page_number, page_count))
        # merge the watermark with the page
        input_page = input_file.getPage(page_number)
        input_page.mergePage(watermark.getPage(0))
        # add page from input file to output document
        output_file.addPage(input_page)

    # finally, write "output" to document-output.pdf
    with open("output/" + booklet_name, "wb") as outputStream:
        output_file.write(outputStream)
