# ------------------------------------------------------------------------------
# Record Expenditure
#
# Produces records of expenditure in a text file.
# ------------------------------------------------------------------------------

# Used to open notepad to edit the csv file
import subprocess

# Used to find the current day
import datetime

import logging
import json
from sys import platform

from boolean_input import BooleanInput
from user_input import UserInput
from option import Option
from option_input import OptionInput
from text_input import TextInput
from multiple_inputs import MultipleInput
from storer import Store
from options_list import OptionList
from list_input import ListInput
from petrol_record import PetrolRecord
from live_info.live_email import EmailInfo

OUTPUT_LOCATION = ""

def string_to_date(date_string):
    values = date_string.split("/")
    return datetime.date(int(values[2]),int(values[1]),int(values[0]))

def decrement_day_by_one(date_string):
    date = string_to_date(date_string)
    decrement = datetime.timedelta(days=-1)
    new_date = date + decrement
    return new_date.strftime('%d/%m/%Y')

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
            rc = tui_inputs.request_inputs()

            # Triggers record specific actions
            if rc == UserInput.SUCCESS and tui_type.get_answer() == "Petrol":
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
        file_handler = open(file,'a',encoding='latin-1')
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
        petrol_store.sort(PetrolRecord.get_date)
        petrol_store.write_new_record([self.date,self.amount,litres,miles])

    def __eq__(self, second_record):
        rc = ((self.date == second_record.date) and
              (self.amount == second_record.amount) and
              (self.where == second_record.where) and
              (self.type == second_record.type))
        return rc
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
        self.logger = logging.getLogger('expenditure')
        self.file = file
        self.type_store = Store(OUTPUT_LOCATION + "expenditure_config.csv", Option, OptionList)
        self._reload_file()

    def _reload_file(self):
        self.records = []
        file_handler = open(self.file,'r',encoding="latin-1")
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
        self.add_created_record(new_record)

    def add_created_record(self, new_record):
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
        self.logger.info("Summary started with properties " + str(properties))
        types = None
        start_date = None
        end_date = None
        dates = None
        total = 0

        type_filter = ("types" in properties.keys())
        date_filter = ("dates" in properties.keys())

        if type_filter:
            types = properties.get("types")
            if types == []:
                # In this case no types were set so treat as all types
                type_filter = False

        if date_filter:
            dates = properties.get("dates")
            if len(dates) == 2:
                start_date = string_to_date(dates[0])
                end_date = string_to_date(dates[1])

        for key in properties.keys():
            if key not in ["dates","types"]:
                print("Error: Invalid key - " + str(key))

        self.logger.debug("Start Date " + str(start_date))
        self.logger.debug("End Date " + str(end_date))
        self.logger.debug("Types " + str(types))
        for record in self.records:
            self.logger.debug("Starting: %s", record.to_string())
            record_counted = True
            if type_filter and record.type not in types:
                self.logger.debug("Record incorrect type")
                record_counted = False
            if date_filter:
                record_date = string_to_date(record.date)
                if (start_date) and (record_date < start_date):
                    self.logger.debug("Record before date range")
                    record_counted = False
                if (end_date) and (record_date > end_date):
                    self.logger.debug("Record after date range")
                    record_counted = False

            if record_counted:
                self.logger.debug("Record counted")
                total += round(float(record.amount),2)
            else:
                self.logger.debug("Record ignored")
        return round(total,2)

    def print_records(self):
        self.date_and_types_input(self._print_records)

    def _print_records(self, start_date, end_date, types=[]):
        self.logger.info(f"Printing records from {start_date} to {end_date}, in {types}")
        self.logger.info(f"Filtering by type? {types}")
        start_date = string_to_date(start_date)
        end_date = string_to_date(end_date)
        self.records.sort(key=lambda record:string_to_date(record.date))
        for record in self.records:
            record_date = string_to_date(record.date)
            if (record_date >= start_date) and (record_date <= end_date):
                if types == []:
                    print(record.to_string())
                else:
                    if record.type in types:
                        print(record.to_string())


    def print_last_record(self):
        file_handler = open(self.file,'r',encoding='latin-1')
        print(file_handler.readlines()[-1])
        file_handler.close()

    def open_csv(self):
        if platform == "linux":
            subprocess.call(['vim', '+', self.file])
        elif platform == "win32" or platform == "win64":
            subprocess.call('notepad ' + self.file)
        self._reload_file()

    def date_and_types_input(self, callback_function):
        questions = []

        tui_start_date = TextInput("From which date?",regex="[0-3][0-9]\/[0-1][0-9]\/20[1-3][0-9]")
        tui_end_date = TextInput("To which date?",default=datetime.date.today().strftime('%d/%m/%Y'),regex="[0-3][0-9]\/[0-1][0-9]\/20[1-3][0-9]")
        questions.append(tui_start_date)
        questions.append(tui_end_date)

        tui_type_option = BooleanInput("Would you like to filter by type?")
        valid_input = tui_type_option.request_input()
        if valid_input == UserInput.SUCCESS:
            if tui_type_option.get_answer():
                tui_type = OptionInput("Which type are you interested in?", self.type_store.read())
                tui_type_list = ListInput(tui_type, ListInput.REPEAT_TILL_TERMINATED)
                questions.append(tui_type_list)

            tui = MultipleInput(questions, callback_function)
            tui.request_inputs()

    def selective_summary(self):
        self.date_and_types_input(self._selective_summary)

    def _selective_summary(self, types, start_date, end_date):
        value = self.summary(types=types,dates=[start_date,end_date])
        print("The total value is: %s" % value)

    def recent_budget_report(self):
        current_month = datetime.date.today().month

    def create_budgeting_periods(self, start_date, end_date):
        budget_data = json.load(open("budget_mapping.json"))
        general_periods = budget_data["periods"]
        start_date = string_to_date(start_date)
        end_date = string_to_date(end_date) + datetime.timedelta(days=32)
        budgeting_periods = []

        for year in range(start_date.year, end_date.year + 1):
            for period in general_periods:
                period_date = datetime.date(year, int(period[-2:]), int(period[:2]))
                if (period_date > start_date) and (period_date < end_date):
                    budgeting_periods.append(period_date)

        return budgeting_periods

    def complete_budget_report(self):
        start_date = self.records[0].date
        end_date = self.records[-1].date
        self.budget_report(start_date, end_date)

    def recent_budget_report(self):
        start_date = (string_to_date(self.records[-1].date) - datetime.timedelta(days=100)).strftime('%d/%m/%Y')
        end_date = self.records[-1].date
        self.budget_report(start_date, end_date)


    def budget_report(self, start_date, end_date):
        self.logger.info(f"Creating budget report from {start_date} to {end_date}")
        budget_data = json.load(open("budget_mapping.json"))
        budget_map = budget_data["mapping"]
        budgeting_periods = self.create_budgeting_periods(start_date, end_date)

        total_budget = {}

        for period_id, period_start_date in list(enumerate(budgeting_periods))[:-1]:
            spend_totals = {}
            print(period_start_date)
            period_end_date = budgeting_periods[period_id + 1] - datetime.timedelta(days=1)
            for key in budget_map.keys():
                value = self.summary(types=budget_map[key],dates=[period_start_date.strftime('%d/%m/%Y'), period_end_date.strftime('%d/%m/%Y')])
                spend_totals[key] = value
            total_budget[period_start_date] = spend_totals

        output_string = "Headings,"
        for start_date in budgeting_periods[:-1]:
            output_string += start_date.strftime('%d/%m/%Y') + ","
        output_string += "\n"

        for category in budget_map.keys():
            output_string += category + ","

            for start_date in budgeting_periods[:-1]:
                output_string += str(total_budget[start_date][category]) + ","
            output_string += "\n"

        with open("output.csv","w") as output_handler:
            output_handler.write(output_string)

    def read_email(self):
        email = EmailInfo(10, 10)
        settings = json.load(open("budget_mapping.json"))
        msgs = email.get_messages(10, 'to:' + settings['expenditure_email'])
        if msgs['resultSizeEstimate'] > 0:
            msg_list = msgs['messages']
            #print(msg_list)
            for msg in msg_list:
                message = email.get_message_body(msg['id'])
                print(message)
                records = message.splitlines()
                print(records)
                for record in records:
                    print(record)
                    if len(record.split(",")) == 4:
                        exp_record = ExpenditureRecord(record, "r")
                        if exp_record not in self.records:
                            self.add_created_record(exp_record)
                    else:
                        print(f"Invalid record: {record}")
        else:
            print("No messages recieved that matched the pattern for expenditure")

    def run(self):
        email = Option("read email","email","Reads supplied email for any expenditure additions",self.read_email)
        add = Option("add","a","Add an item of expenditure",self.add_record)
        quit = Option("quit","q","Quits the program")
        print_records = Option("print","p","Prints all recorded expenditure between two dates",self.print_records)
        last = Option("last","l","Prints the last record",self.print_last_record)
        edit = Option("edit","e","Opens the records in notepad for manual editing",self.open_csv)
        total = Option("total","t","Prints the total expenditure",self.selective_summary)
        add_type = Option("add type","at","Adds another valid type",self.add_type)
        budget_report = Option("budget","b","Produces budget report for approx last 3 months",self.recent_budget_report)
        full_budget_report = Option("full budget","fb","Produces budget report for entire history",self.complete_budget_report)

        options = [add,quit,print_records,last,edit,total,add_type,email,budget_report,full_budget_report]

        keep_going = True
        while keep_going:
            self.logger.info("Asking user question")
            tui = OptionInput("What would you like to do?",options,"a")
            tui.request_input()
            if tui.chosen_option == quit.name:
                keep_going = False
