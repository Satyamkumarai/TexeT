# import PyPDF2 as pp
# pdf_file = "./split/1.pdf"
# pdf = pp.PdfFileReader(pdf_file)

# page1=  pdf.getPage(0)
# def expand(d):
    
#     for k in d:
#         print(k , d[k],sep="\t",end="\n"+'-'*10+ '\n')
        
# # print(page1)
# # for k in page1:
# #     print(k , page1[k],sep="\t",end="\n\n")
# resources = page1['/Resources']
# # expand(resources)
# xObject = resources['/XObject']
# expand(xObject)
# for i in xObject:
#     expand(xObject[i]['/Resources'])

from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

packet = io.BytesIO()
# create a new PDF with Reportlab
can = canvas.Canvas(packet, pagesize=letter)
can.drawString(10, 100, "Hello world")
can.save()

#move to the beginning of the StringIO buffer
packet.seek(0)
new_pdf = PdfFileReader(packet)
# read your existing PDF
existing_pdf = PdfFileReader(open("original.pdf", "rb"))
output = PdfFileWriter()
# add the "watermark" (which is the new pdf) on the existing page
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)
# finally, write "output" to a real file
outputStream = open("destination.pdf", "wb")
output.write(outputStream)
outputStream.close()