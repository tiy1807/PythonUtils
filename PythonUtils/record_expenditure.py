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
from collections import OrderedDict
from sys import platform
from pathlib import Path

from PythonUtils.boolean_input import BooleanInput
from PythonUtils.user_input import UserInput
from PythonUtils.option import Option
from PythonUtils.option_input import OptionInput
from PythonUtils.text_input import TextInput
from PythonUtils.multiple_inputs import MultipleInput
from PythonUtils.storer import Store
from PythonUtils.record import Record
from PythonUtils.options_list import OptionList
from PythonUtils.list_input import ListInput
from PythonUtils.petrol_record import PetrolRecord
from PythonUtils.live_info.live_email import EmailInfo
from PythonUtils.date_input import DateInput

OUTPUT_LOCATION = ""

def string_to_date(date_string):
    values = date_string.split("/")
    return datetime.date(int(values[2]), int(values[1]), int(values[0]))

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
class ExpenditureRecord(Record):
    def __init__(self, *data):
        super().__init__(*data)

    @property
    def date(self):
        return self.value_tuple[0]

    @property
    def amount(self):
        return self.value_tuple[1]

    @property
    def where(self):
        return self.value_tuple[2]

    @property
    def type(self):
        return self.value_tuple[3]

    def compare_to(self, comparison):
        # {'start-date': '01/01/2020', 'end-date': 02/01/2020', 'min-amount': '1.00', 'max-amount': '5.00',
        #  'where': [a, b, c], 'type': [x, y, z]}
        matches = True
        if ((comparison.get('start-date') and string_to_date(comparison['start-date']) > string_to_date(self.date)) or
            (comparison.get('end-date') and string_to_date(self.date) > string_to_date(comparison['end-date'])) or
            (comparison.get('min-amount') and float(comparison['min-amount']) > float(self.amount)) or
            (comparison.get('max-amount') and float(comparison['max-amount']) > float(self.amount)) or
            (comparison.get('where') and self.where not in comparison['where']) or
            (comparison.get('type') and self.type not in comparison['type'])):
            matches = False
        return matches

    def to_string(self):
        return ",".join(self.to_csv())


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
class ExpenditureFile(Store):
    def __init__(self, settings_file="expenditure_config.json"):
        self.logger = logging.getLogger('expenditure')

        with open(settings_file) as f:
            settings = json.load(f)
            self.file = settings["files"]["expenditure"]
            super().__init__(self.file, ExpenditureRecord)

            self.type_store = Store(settings["files"]["categories"], Option, OptionList)
            self.petrol_store = Store(settings["files"]["petrol"], PetrolRecord)

    @property
    def records(self):
        return self.read()

    def add_type(self):
        valid_types = self.type_store.read_to_container()
        valid_types.add_option()
        self.type_store.write(valid_types)

    # Adds a new record
    def add_record(self):
        today = datetime.date.today().strftime('%d/%m/%Y')

        tui_date = DateInput(text="When did you spend it?", default=today)
        tui_amount = TextInput("How much have you spent?")
        tui_where = TextInput("Where did you spend it?")

        tui_type = OptionInput("What type of expenditure was it?", self.type_store.read_to_container().object_list)

        tui_inputs = MultipleInput([tui_date, tui_amount, tui_where, tui_type], self.add_created_record)
        rc = tui_inputs.request_inputs()

        if rc == UserInput.SUCCESS and tui_type.get_answer() == "Petrol":
            self.add_petrol_record()

    def add_petrol_record(self):
        # This is extra functionallity when recording petrol expenditure, which
        # asks additional questions and saves that information in the petrol
        # log.
        tui_litres = TextInput("How many litres did you buy?")
        tui_miles = TextInput("What is the mileage on the car?")
        tui = MultipleInput([tui_litres, tui_miles], self._record_petrol)
        tui.request_inputs()

    def _record_petrol(self, litres, miles):
        most_recent_record = self.read()[-1]
        self.petrol_store.write_new_record(most_recent_record.date, most_recent_record.amount, litres, miles)

    def add_created_record(self, *args):
        self.write_new_record(*args)

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
            if isinstance(types, str):
                types = [types]
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
                if start_date and (record_date < start_date):
                    self.logger.debug("Record before date range")
                    record_counted = False
                if end_date and (record_date > end_date):
                    self.logger.debug("Record after date range")
                    record_counted = False

            if record_counted:
                self.logger.debug("Record counted")
                total += round(float(record.amount), 2)
            else:
                self.logger.debug("Record ignored")
        return round(total, 2)

    def print_records(self):
        self.date_and_types_input(self._print_records)

    def _print_records(self, start_date, end_date, types=[]):
        self.logger.info(f"Printing records from {start_date} to {end_date}, in {types}")
        self.logger.info(f"Filtering by type? {types}")

        filtered_records = self.filter_records([{'start-date': start_date,
                                                'end-date': end_date,
                                                'type': types}])

        ExpenditureFile._print_out_records(filtered_records)

    @staticmethod
    def _print_out_records(records):
        records.sort(key=lambda record: string_to_date(record.date))
        for record in records:
            print(record.to_string())

    def print_current_month(self):
        today = datetime.datetime.today()
        start_date = datetime.date(today.year, today.month, 1)
        filtered_records = self.filter_records([{'start-date' : start_date.strftime('%d/%m/%Y'),
                                                 'end-date' : today.strftime('%d/%m/%Y')}])
        ExpenditureFile._print_out_records(filtered_records)

    def filter_records(self, conditions):
        # [{'start-date': '01/01/2020', 'end-date': '31/01/2020', 'types': [x, y, z]},
        #  {'start-date': '01/03/2020', 'end-date': '02/03/2020', 'types': [all]}]
        filtered_records = []
        for record in self.records:
            append = False
            for condition in conditions:
                if record.compare_to(condition):
                    append = True
            if append:
                filtered_records.append(record)
        return filtered_records

    def print_last_record(self, num_records=1):
        ExpenditureFile._print_out_records(self.records[-int(num_records):])

    def open_csv(self):
        if platform == "linux":
            subprocess.call(['vim', '+', self.file])
        elif platform == "win32" or platform == "win64":
            subprocess.call('notepad ' + self.file)

    def date_and_types_input(self, callback_function):
        questions = []

        tui_start_date = DateInput(text="From which date?")
        tui_end_date = DateInput(text="To which date?", default=datetime.date.today().strftime('%d/%m/%Y'))
        questions.append(tui_start_date)
        questions.append(tui_end_date)

        tui_type = OptionInput("Which type are you interested in?", self.type_store.read())
        tui_type_list = ListInput(tui_type, ListInput.REPEAT_TILL_TERMINATED)
        questions.append(tui_type_list)

        tui = MultipleInput(questions, callback_function)
        tui.request_inputs()

    def selective_summary(self):
        self.date_and_types_input(self._selective_summary)

    def _selective_summary(self, start_date, end_date, types):
        value = self.summary(types=types, dates=[start_date, end_date])
        print("The total value is: %s" % value)

    def create_budgeting_periods(self, start_date, end_date):
        budget_data = json.load(open("expenditure_config.json"))
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
        today = datetime.datetime.today()
        start_date = (today - datetime.timedelta(days=100))
        self.budget_report(start_date.strftime('%d/%m/%Y'), today.strftime('%d/%m/%Y'))

    def budget_report(self, start_date, end_date):
        self.logger.info(f"Creating budget report from {start_date} to {end_date}")
        with open("expenditure_config.json") as budget_json:
            budget_data = json.load(budget_json, object_pairs_hook=OrderedDict)

        budget_map = budget_data["mapping"]
        budgeting_periods = self.create_budgeting_periods(start_date, end_date)
        total_budget = {}

        for period_id, period_start_date in list(enumerate(budgeting_periods))[:-1]:
            spend_totals = {}
            print(period_start_date)
            period_end_date = budgeting_periods[period_id + 1] - datetime.timedelta(days=1)
            for key in budget_map.keys():
                value = self.summary(types=budget_map[key], dates=[period_start_date.strftime('%d/%m/%Y'),
                                                                   period_end_date.strftime('%d/%m/%Y')])
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

        with open("output.csv", "w") as output_handler:
            output_handler.write(output_string)

    def read_email(self):
        email = EmailInfo(10, 10)
        settings = json.load(open("expenditure_config.json"))
        msgs = email.get_messages(10, 'to:' + settings['expenditure_email'])
        if msgs['resultSizeEstimate'] > 0:
            msg_list = msgs['messages']
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

        options = [Option("read email", "email", "Reads supplied email for any expenditure additions", self.read_email),
                   Option("add", "a", "Add an item of expenditure", self.add_record),
                   Option("quit", "q", "Quits the program"),
                   Option("print", "p", "Prints all recorded expenditure between two dates", self.print_records),
                   Option("print current month", "pm", "Prints current month expenditure", self.print_current_month),
                   Option("last", "l", "Prints the last record", self.print_last_record),
                   Option("edit", "e", "Opens the records in notepad for manual editing", self.open_csv),
                   Option("total", "t", "Prints the total expenditure", self.selective_summary),
                   Option("add type", "at", "Adds another valid type", self.add_type),
                   Option("budget", "b", "Produces budget report for approx last 3 months", self.recent_budget_report),
                   Option("full budget", "fb", "Produces budget report for entire history", self.complete_budget_report)]

        tui = OptionInput(text="What would you like to do?", options=options, default="a")
        while tui.chosen_option != "quit":
            self.logger.info("Asking user question")
            tui.request_input()
