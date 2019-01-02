from os import walk
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader


def get_pdf_list():
    r = []
    l = []
    for (dirpath, dirnames, filenames) in walk("./left-watermarker"):
        l.extend(filenames)
        break

    for (dirpath, dirnames, filenames) in walk("./right-watermarker"):
        r.extend(filenames)
        break
    return r, l


canvas_width = 566

# Create the watermark from an image
c = canvas.Canvas('right-watermark.pdf')
c.drawImage('sneeds-logo.png', canvas_width - 4, 2, width=30, height=30, mask='auto', preserveAspectRatio=True)
c.drawString(canvas_width - 73, 12, "SNEEDS.IR")
c.save()

c = canvas.Canvas('left-watermark.pdf')
c.drawImage('sneeds-logo.png', 2, 2, width=30, height=30, mask='auto')
c.drawString(37, 12, "SNEEDS.IR")
c.save()

right_pdf_list, left_pdf_list = get_pdf_list()

# Solving mac problem
if right_pdf_list[0] == ".DS_Store":
    del (right_pdf_list[0])

if left_pdf_list[0] == ".DS_Store":
    del (left_pdf_list[0])

print("\nLEFT PDFs : ")
for booklet_name in right_pdf_list:
    watermark = PdfFileReader(open("right-watermark.pdf", "rb"))
    output_file = PdfFileWriter()
    input_file = PdfFileReader(open("right-watermarker/" + booklet_name, "rb"))

    page_count = input_file.getNumPages()

    # Go through all the left-watermarker file pages to add a watermark to them
    for page_number in range(page_count):
        print(booklet_name + ": Watermarking page {} of {}".format(page_number, page_count - 1))

        input_page = input_file.getPage(page_number)
        input_page.mergePage(watermark.getPage(0))

        output_file.addPage(input_page)

    with open("output/" + booklet_name, "wb") as outputStream:
        output_file.write(outputStream)

print("\nLEFT PDFs : ")
for booklet_name in left_pdf_list:
    watermark = PdfFileReader(open("left-watermark.pdf", "rb"))
    output_file = PdfFileWriter()
    input_file = PdfFileReader(open("left-watermarker/" + booklet_name, "rb"))

    page_count = input_file.getNumPages()

    # Go through all the left-watermarker file pages to add a watermark to them
    for page_number in range(page_count):
        print(booklet_name + ": Watermarking page {} of {}".format(page_number, page_count - 1))

        input_page = input_file.getPage(page_number)
        input_page.mergePage(watermark.getPage(0))

        output_file.addPage(input_page)

    with open("output/" + booklet_name, "wb") as outputStream:
        output_file.write(outputStream)
