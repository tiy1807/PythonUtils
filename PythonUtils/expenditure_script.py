from record_expenditure import ExpenditureFile
import logging

logging.basicConfig(filename="expenditure.log", level=logging.INFO, filemode="w")
logger = logging.getLogger('expenditure')

file = ExpenditureFile("expenditure.csv")
file.run()
