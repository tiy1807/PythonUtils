# ------------------------------------------------------------------------------
# Record Expenditure
#
# Produces records of expenditure in a text file.
# ------------------------------------------------------------------------------

# Used to open notepad to edit the csv file
import subprocess

# Used to find the current day
import datetime

from user_input import UserInput
from option import Option
from option_input import OptionInput
from text_input import TextInput
from multiple_inputs import MultipleInput
from storer import Store
from options_list import OptionList
from list_input import ListInput
from petrol_record import PetrolRecord

OUTPUT_LOCATION = ""

def string_to_date(date_string):
    values = date_string.split("/")
    return datetime.date(int(values[2]),int(values[1]),int(values[0]))

# ------------------------------------------------------------------------------
# Class ExpenditureRecord:
#
# Gains the user input to create the text.
# Note there is no error checking.
# ------------------------------------------------------------------------------
class ExpenditureRecord:
    def __init__(self, data, access):
        self.valid = False

        if access == 'w':
            today = datetime.date.today().strftime('%d/%m/%Y')

            tui_date = TextInput("When did you spend it?", today)
            tui_amount = TextInput("How much have you spent?")
            tui_where = TextInput("Where did you spend it?")

            tui_type = OptionInput("What type of expenditure was it?", data.object_list)

            tui_inputs = MultipleInput([tui_date,tui_amount,tui_where,tui_type], self.set_attrs)
            tui_inputs.request_inputs()

            # Triggers record specific actions
            if tui_type.get_answer() == "Petrol":
                self.record_petrol()

        elif access == 'r':
            data = data.rstrip()
            properties = data.split(",")
            self.set_attrs(*properties)
        else:
            print("Something has gone wrong ...")

    def set_attrs(self, date, amount, where, type):
        self.valid = True
        self.date = date
        self.amount = amount
        self.where = where
        self.type = type

    def append_to_file(self, file):
        # Opens the file and writes the line
        file_handler = open(file,'a')
        file_handler.write(self.to_string() + "\n")
        print("Added " + self.to_string() + " to " + file)
        file_handler.close()

    def to_string(self):
        properties = [self.date, self.amount, self.where, self.type]
        return ",".join(properties)

    def record_petrol(self):
        # This is extra functionallity when recording petrol expenditure, which
        # asks additional questions and saves that information in the petrol
        # log.
        tui_litres = TextInput("How many litres did you buy?")
        tui_miles = TextInput("What is the mileage on the car?")
        tui = MultipleInput([tui_litres, tui_miles], self._record_petrol)
        tui.request_inputs()

    def _record_petrol(self, litres, miles):
        petrol_store = Store(OUTPUT_LOCATION + "petrol_spending.csv", PetrolRecord)
        petrol_store.write_new_record([self.date,self.amount,litres,miles])

# ------------------------------------------------------------------------------
# Class ExpenditureFile
#
# Holds the file where the expenditure is written. Has two properties:
# - file    - This is the full file path to the csv where the expenditure data
#             is stored.
# - type_store - Store object with the valid types in it as Option objects.
# - records - This contains a list of expenditure record objects. This reads all
#             of the records.
# ------------------------------------------------------------------------------
class ExpenditureFile:
    def __init__(self, file):
        self.file = file
        self.type_store = Store(OUTPUT_LOCATION + "expenditure_config.csv", Option, OptionList)

        # Read all the records in the expenditure file
        self.records = []
        file_handler = open(self.file,'r')
        for line in file_handler.readlines():
            record = ExpenditureRecord(line,'r')
            #print(record.to_string())
            self.records.append(record)
        file_handler.close()

    def add_type(self):
        valid_types = self.type_store.read_to_container()
        valid_types.add_option()
        self.type_store.write(valid_types)

    # Adds a new record
    def add_record(self):
        new_record = ExpenditureRecord(self.type_store.read_to_container(), 'w')
        if new_record.valid:
            new_record.append_to_file(self.file)
            self.records.append(new_record)
        else:
            print("Record invalid. Adding aborted")

    def summary(self, **properties):
        # properties contains key words that allow filtering of the records by
        # their attributes. Currently will print the totals for a list of types
        # supplied. There is no error checking so if the type is not present in
        # a record then will print 0.
        print("Summary started with properties " + str(properties))
        types = None
        start_date = None
        end_date = None
        dates = None
        total = 0

        type_filter = ("types" in properties.keys())
        date_filter = ("dates" in properties.keys())

        if type_filter:
            types = properties.get("types")

        if date_filter:
            dates = properties.get("dates")
            if len(dates) == 2:
                start_date = string_to_date(dates[0])
                end_date = string_to_date(dates[1])

        for key in properties.keys():
            if key not in ["dates","types"]:
                print("Error: Invalid key - " + str(key))

        for record in self.records:
            record_counted = True
            if type_filter and record.type not in types:
                record_counted = False
            if date_filter:
                record_date = string_to_date(record.date)
                if start_date and record_date < start_date and end_date and record_date > end_date:
                    record_counted = False

            if record_counted:
                total += float(record.amount)

        print("The total amount you have spent is " + str(total))

    def print_all_records(self):
        file_handler = open(self.file,'r')
        print(file_handler.read())
        file_handler.close()

    def print_last_record(self):
        file_handler = open(self.file,'r')
        print(file_handler.readlines()[-1])
        file_handler.close()

    def open_csv(self):
        subprocess.check_output('notepad ' + self.file)

    def selective_summary(self):
        tui_type = OptionInput("Which type would you like to total?", self.type_store.read())
        tui_type_list = ListInput(tui_type, ListInput.REPEAT_TILL_TERMINATED)
        tui_start_date = TextInput("From which date?")
        tui_end_date = TextInput("To which date?",default=datetime.date.today().strftime('%d/%m/%Y'))

        tui = MultipleInput([tui_type_list, tui_start_date, tui_end_date], self._selective_summary)
        tui.request_inputs()

    def _selective_summary(self, types, start_date, end_date):
        self.summary(types=types,dates=[start_date,end_date])

    def run(self):
        add = Option("add","a","Add an item of expenditure",self.add_record)
        quit = Option("quit","q","Quits the program")
        print_records = Option("print","p","Prints all recorded expenditure",self.print_all_records)
        last = Option("last","l","Prints the last record",self.print_last_record)
        edit = Option("edit","e","Opens the records in notepad for manual editing",self.open_csv)
        total = Option("total","t","Prints the total expenditure",self.selective_summary)
        add_type = Option("add type","at","Adds another valid type",self.add_type)

        options = [add,quit,print_records,last,edit,total,add_type]

        keep_going = True
        while keep_going:
            tui = OptionInput("What would you like to do?",options,"a")
            tui.request_input()
            if tui.chosen_option == quit.name:
                keep_going = False
