from pdfquery import PDFQuery
#pdf query can be used to run jquery like commands on the data of a pdf
try:
    pdf = PDFQuery('test2.pdf')
except TypeError:
    raise RuntimeError("The program failed to open the file")


num_pages = len(pdf.doc.catalog['Pages'].resolve()['Kids'])

for i in range(num_pages):
    pdf.load(i)
    # pdf.tree.write("testxml.xml",pretty_print = True, encoding = "utf-8")
    #pdf.pq returns an xml tree within a pyquery wrapper. Query's are provided to the pq method as strings


    #extract the coordinates of the Invoice # label
    print(f"Page {i+1}")
    print("")
    label = pdf.pq('LTTextLineHorizontal:contains("Invoice #")')
    invoice_x0 = float(label[0].attrib['x0'])
    invoice_y0 = float(label[0].attrib['y0'])

    #extract the actual invoice number based on the coordinates of the label
    invoice_num = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s,%s,%s,%s")' % (invoice_x0-10,invoice_y0-20,invoice_x0+40,invoice_y0-10)).text()


    #use the $ symbol as the label for each item entry. The bbox dimensions ensure all $ characters are captured
    item_label = pdf.pq('LTTextLineHorizontal:overlaps_bbox("520,0,560,800")')

    item_nums = []
    amnt_invoiced = []
    lot_nums = []
    quants = []
    exp_dates = []
    item_descs = []
    mfgs = []
    Ext_prices = []
    for label in item_label:
        if pdf.pq(label).text() and pdf.pq(label).text()[0]=='$':
            if pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s,%s,%s,%s")' % (430,float(label.attrib['y0'])-3,467,float(label.attrib['y1'])+3)).text() == "Subtotal:":
                break
            Ext_prices.append(pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s,%s,%s,%s")' % (float(label.attrib['x0'])-3,float(label.attrib['y0'])-3,float(label.attrib['x1'])+3,float(label.attrib['y1'])+3)).text())
            item_nums.append(pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s,%s,%s,%s")' % (10,float(label.attrib['y0'])-3,50,float(label.attrib['y1'])+3)).text())
            item_descs.append(pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s,%s,%s,%s")' % (65,float(label.attrib['y0'])-3,269,float(label.attrib['y1'])+3)).text())
            quants.append(pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s,%s,%s,%s")' % (376,float(label.attrib['y0'])-3,383,float(label.attrib['y1'])+3)).text())
            mfgs.append(pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s,%s,%s,%s")' % (137,float(label.attrib['y0'])-21,245,float(label.attrib['y1'])-20)).text())
            if "Lot Number:" in pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s,%s,%s,%s")' % (71,float(label.attrib['y0'])-35,162,float(label.attrib['y1'])-35)).text():
                lot_nums.append(pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s,%s,%s,%s")' % (71,float(label.attrib['y0'])-35,162,float(label.attrib['y1'])-35)).text())
            else:
                lot_nums.append("")

            if "Expiry Date:" in pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s,%s,%s,%s")' % (285,float(label.attrib['y0'])-35,386,float(label.attrib['y1'])-35)).text():
                exp_dates.append(pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s,%s,%s,%s")' % (285,float(label.attrib['y0'])-35,386,float(label.attrib['y1'])-35)).text())
            else:
                exp_dates.append("")
            


    #remove "Lot Number:" string from the date field
    for i in range(len(lot_nums)):
        lot_nums[i] = lot_nums[i].replace("Lot Number: ", "")



    #parse manufacturer data (we only want the company name which is after the company number)
    mfgs_filtered = []
    for s in mfgs:
        words = s.split()
        if len(words) > 1:
            mfgs_filtered.append(" ".join(words[1:]))  # everything except the first word
        else:
            mfgs_filtered.append("")  # handle strings with only one word

    #remove "Expiry Date:" string from the date field
    for i in range(len(exp_dates)):
        exp_dates[i] = exp_dates[i].replace("Expiry Date:", "")

    for num in item_nums: print(num)

    for desc in item_descs: print(desc)

    for quant in quants: print(quant)

    for mfg in mfgs_filtered: print(mfg)

    for num in lot_nums: print(num)

    for date in exp_dates: print (date)

    for price in Ext_prices: print(price)

    print("")











