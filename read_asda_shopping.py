#!/usr/bin/python
# -*- coding: utf-8 -*-

# Reads the HTML page from ASDA's shopping basket
# Writes to an excel spreadsheet in three columns item, quantity, price

# TODO: Obtain the HTML page by making a GET request.

from html.parser import HTMLParser
from optparse import OptionParser
import logging
from openpyxl import Workbook

HTML_PAGE = "shopping_basket.htm"
LOG_FILE = "htmlparser.log"

logger = logging.getLogger(__name__)

def convert_to_pounds(string):
    """
    :return: string
             The money value expressed in pounds that was entered in the string.
    
    :param string: A string with one of the following formats:
                       ?£a - a '£' in the string, and the amount from the 
                           third character)
                       ap - the last character of the string is p, the amount is
                            then divided by 100 to make the result in pounds.
    
    Utility function which extracts the amount in pounds from an appropriately
    formatted string.
    """
    # TODO: Return a number rather than a string!
    
    rc = string
    # Determines if '£' is in the string.
    if "£" in string:
        # Returns from the third character.
        # TODO: ASDA prices start like Â£. I assume this is to do with the
        #       format of the string. We could improve the logic here to read
        #       the string in a better way, so that it start with '£'.
        # TODO: Just because the string has a '£' in it doesn't mean that the
        #       string is in the correct format. Extra checks should be made
        #       here.
        rc = string[2:]
    # Determines if the string ends in 'p'
    elif string[-1] == "p":
        # Returns except the last character in pounds.
        # TODO: Should check the format of the string more carefully, items that
        #       are 5p will come out as £0.5.
        rc = "0." + string[:-1]
    else:
        logger.error("Incorrect format for string: %s", string)
        
    return rc
        

class Product():
    """
    Provides a container for each product. Stores name, quantity, price and
    amount.
    """
    def __init__(self):
        # Initialise the member variables.
        self.name = ""
        self.quantity = ""
        self.price = ""
        self.amount = ""
    
    # Getters and setters.
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

class ShoppingParser(HTMLParser):
    def __init__(self, logfile):
        HTMLParser.__init__(self)
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

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-l", "--log_file", dest="filename", help="The file name "
                      "that the logs should be written to")
                      
    (options, args) = parser.parse_args()
    print(options)
    print(args)
    logging.basicConfig(filename=logfile, level=logging.INFO, filemode="w")
    with open(HTML_PAGE, "r") as myfile:
        data = myfile.read().replace('\n','')

    parser = ShoppingParser()
    parser.feed(data)
    print(parser.to_string())
    parser.create_workbook()

