from record_expenditure import ExpenditureFile
import logging

logging.basicConfig(filename="expenditure.log", level=logging.DEBUG, filemode="w")
logger = logging.getLogger('expenditure')

file = ExpenditureFile("expenditure.csv")
file.run()
