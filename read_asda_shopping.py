# Reads the HTML page from ASDA's shopping basket
# Writes to an excel spreadsheet in three columns item, quantity, price

from html.parser import HTMLParser
import logging
from openpyxl import Workbook

HTML_PAGE = "shopping_basket.htm"
LOG_FILE = "htmlparser.log"

def convert_to_pounds(string):
    if "£" in string:
        return string[2:]
    elif string[-1] == "p":
        return "0." + string[:-1]
    else:
        print("Incorrect format %s" % string)
        return string
        

class Product():
    def __init__(self):
        self.name = ""
        self.quantity = ""
        self.price = ""
        self.amount = ""
    def add_name(self, name):
        self.name = name
    def add_amount(self, amount):
        self.amount = amount
    
    def add_quantity(self, amount):
        self.quantity = amount
    def add_price(self, price):
        self.price = price
    def get_name(self):
        return self.name
    def to_string(self):
        return ", ".join(self.get_attrs())
    def get_attrs(self):
        return [self.name, self.amount, self.quantity, self.price]

class MyHTMLParser(HTMLParser):
    def __init__(self, logfile):
        HTMLParser.__init__(self)
        logging.basicConfig(filename=logfile, level=logging.INFO, filemode="w")
        self.logger = logging.getLogger(__name__)
        self.product_list = []
        self.product = None
        self.product_title = False
        self.is_quantity = False
        self.is_price = False
        self.is_sub_title = False
    def handle_starttag(self, tag, attrs):
        self.logger.debug("Encountered a start tag: %s with attrs: %s", tag, attrs)
        if attrs:
            attrs = dict(attrs)
            if attrs.get('class') == 'product':
                self.logger.info("Creating new product")
                self.product = Product()
            elif tag == 'span' and attrs.get('class') and attrs.get('class') == 'title productTitle':
                self.logger.debug("Starting product title")
                self.product_title = True
            elif tag == 'span' and attrs.get('class') and attrs.get('class') == 'qtyTxt':
                self.logger.debug("Starting quantity")
                self.is_quantity = True
            elif tag == 'span' and attrs.get('class') and attrs.get('class') == 'price':
                self.logger.debug("Starting price")
                self.is_price = True
            elif tag == 'span' and attrs.get('class') and attrs.get('class') == 'subTitle':
                self.logger.debug("Starting subtitle")
                self.is_sub_title = True
            elif tag == 'div' and attrs.get('class') and attrs.get('class') == 'delSubs column':
                self.logger.info("End of product: %s", self.product.get_name())
                self.product_list.append(self.product)
                self.product = Product()
        
    def handle_endtag(self, tag):
        self.logger.debug("Encountered an end tag : %s", tag)
        if tag == 'span':
            if self.is_quantity:
                self.is_quantity = False
            if self.product_title:
                self.product_title = False
            if self.is_price:
                self.is_price = False
            if self.is_sub_title:
                self.is_sub_title = False
  
    def handle_data(self, data):
        self.logger.debug("Encountered some data  : %s", data)
        if self.product_title:
            newname = self.product.get_name() + " " + data
            self.logger.info("Product name = %s", newname)
            self.product.add_name(newname)
        if self.is_quantity:
            self.product.add_quantity(data)
        if self.is_price and data != "Now":
            self.product.add_price(convert_to_pounds(data))
        if self.is_sub_title:
            self.product.add_amount(data)
            
    def to_string(self):
        str = ""
        for product in self.product_list:
            str += product.to_string()
            str += "\n"
        return str
        
    def create_workbook(self):
        wb = Workbook()
        ws = wb.active
        for row_num in range(len(self.product_list)):
            attrs = self.product_list[row_num].get_attrs()
            for col_num in range(len(attrs)):
                cell = ws.cell(row=row_num+1, column=col_num+1, value=attrs[col_num])
        wb.save("shoppinglist.xlsx")
            
with open(HTML_PAGE, "r") as myfile:
    data = myfile.read().replace('\n','')

parser = MyHTMLParser("asda.log")
parser.feed(data)
print(parser.to_string())
parser.create_workbook()

