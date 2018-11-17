from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader

# Create the watermark from an image
c = canvas.Canvas('watermark.pdf')

# Draw the image at x, y. I positioned the x,y to be where i like here
c.drawImage('sneeds-logo.png', 2, 2, width=30, height=30, mask='auto')
c.drawString(37, 12, "SNEEDS.IR")
c.save()

watermark = PdfFileReader(open("watermark.pdf", "rb"))
output_file = PdfFileWriter()
input_file = PdfFileReader(open("test.pdf", "rb"))

page_count = input_file.getNumPages()

# Go through all the input file pages to add a watermark to them
for page_number in range(page_count):
    print("Watermarking page {} of {}".format(page_number, page_count))
    # merge the watermark with the page
    input_page = input_file.getPage(0)
    input_page.mergePage(watermark.getPage(0))
    # add page from input file to output document
    output_file.addPage(input_page)
    if page_number > 5:
        break

# finally, write "output" to document-output.pdf
with open("document-output.pdf", "wb") as outputStream:
    output_file.write(outputStream)
