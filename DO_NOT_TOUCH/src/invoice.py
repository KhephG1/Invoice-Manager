from pdfquery import PDFQuery
from log_status import log_status
#pdf query can be used to run jquery like commands on the data of a pdf

class Invoice:

    def __init__(self,filename):
        self.invoice_number = ""
        self.order_number=""
        self.pages = []
        self.filename = filename
        self.receipt_num = None

    def parse_page(self,page_num,pdf):
        pdf.load(page_num)

        item_labels = pdf.pq('LTTextLineHorizontal:overlaps_bbox("520,0,560,800")')

        items = []

        for label in item_labels:
            text = pdf.pq(label).text()

            if not text or text[0] != '$':
                continue

            end_flag = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s,%s,%s,%s")' % (
                430, float(label.attrib['y0']) - 3, 467, float(label.attrib['y1']) + 3)).text()
            
            if end_flag == "Subtotal:":
                break

            y0, y1 = float(label.attrib['y0']), float(label.attrib['y1'])
            x0, x1 = float(label.attrib['x0']), float(label.attrib['x1'])

            price = get_text_inbbox(x0-3, y0-3, x1+3, y1+3,pdf)

            number = get_text_inbbox(10, y0 - 3, 50, y1 + 3,pdf)

            description = get_text_inbbox(65, y0 - 3, 269, y1 + 3, pdf)

            quantity = get_text_inbbox(376, y0 - 3, 383, y1 + 3, pdf)

            mfg_raw = get_text_inbbox(137, y0 - 21, 245, y1 - 20, pdf)
            mfg_words = mfg_raw.split()
            manufacturer = " ".join(mfg_words[1:]) if len(mfg_words) > 1 else ""

            lot_text = get_text_inbbox(71, y0 - 35, 162, y1 - 35, pdf)
            lot_number = lot_text.replace("Lot Number: ", "") if "Lot Number:" in lot_text else ""

            exp_text = get_text_inbbox(285, y0 - 35, 386, y1 - 35, pdf)
            expiry_date = exp_text.replace("Expiry Date:", "") if "Expiry Date:" in exp_text else ""

            items.append(Item(number, description, quantity, manufacturer, lot_number, expiry_date, price))

        return items

    def parse(self, status_text):
        try:
            pdf = PDFQuery(self.filename)
        except TypeError:
            pass

        pdf.load(0)
        label = pdf.pq('LTTextLineHorizontal:contains("Invoice #")')
        invoice_x0 = float(label[0].attrib['x0'])
        invoice_y0 = float(label[0].attrib['y0'])
     
        #extract the actual invoice number based on the coordinates of the label
        self.invoice_number = get_text_inbbox(invoice_x0-10,invoice_y0-20,invoice_x0+40,invoice_y0-10,pdf)
        self.order_number = self.invoice_number[-3:]
        num_pages = len(pdf.doc.catalog['Pages'].resolve()['Kids'])

        for i in range(num_pages):
            self.pages.append(self.parse_page(i, pdf))

        log_status(self.__str__(), status_text)
        return self.pages
    
    def __str__(self):
        output = [f"Invoice Number: {self.invoice_number}"]
        output.append(f"\nOrder Number: {self.order_number}")
        for page_num, items in enumerate(self.pages):
            output.append(f"\nPage {page_num + 1}:")
            if items:
                for item in items:
                    output.append(f"  {item}")
            else:
                output.append("  (No items found on this page)")
        return "\n".join(output)


class Item:
    def __init__(self,number,description,quantity, manufacturer,lot_number,expiry_date, price):
        self.number = number
        self.quantity = quantity
        self.description = description
        self.manufacturer = manufacturer
        self.lot_number = lot_number
        self.expiry_date = expiry_date
        self.price = price
        self.type = None

    def __str__(self):
        return f"{self.number}: {self.description} x {self.quantity} ({self.manufacturer} - {self.price})"

def get_text_inbbox(x0,y0,x1,y1,pdf):
    return pdf.pq(f'LTTextLineHorizontal:overlaps_bbox("{x0},{y0},{x1},{y1}")').text()





        











