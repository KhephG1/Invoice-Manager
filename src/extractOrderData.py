from pdfquery import PDFQuery
#pdf query can be used to run jquery like commands on the data of a pdf
pdf = PDFQuery('test.pdf')
pdf.load()
# pdf.tree.write("testxml.xml",pretty_print = True, encoding = "utf-8")
label = pdf.pq('LTTextLineHorizontal:contains("Customer PO #")')
left_corner = float(label.attr('x0'))
bottom_corner = float(label.attr('y0'))
name = pdf.pq('LTTextLineHorizontal:in_bbox("%s,%s,%s,%s")' % (left_corner, bottom_corner-30, left_corner+150, bottom_corner)).text()
print(name)












