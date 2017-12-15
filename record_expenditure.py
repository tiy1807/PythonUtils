# ------------------------------------------------------------------------------
# Record Expenditure
# 
# Produces records of expenditure in a text file.
# ------------------------------------------------------------------------------

# Used to open notepad to edit the csv file
import subprocess

# Used to find the current day
import datetime

IS_TEST = False
OUTPUT_LOCATION = "C:\\Users\\owner\\OneDrive\\SkyDocuments\\Finances\\ExpenditureRecord\\"
TEST_LOCATION = "C:\\Users\\owner\\OneDrive\\SkyDocuments\\Finances\\ExpenditureRecordTEST\\"

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
    
        if access == 'w': 
            # Asks the user to input the date
            
            today = datetime.date.today().strftime('%d/%m/%Y')
            self.date = input("When did you spend it? (default: " + today + ")\n")
            
            # Default value of todays date.
            if self.date == "":
                self.date = today
        
            # Asks the user to provide the amount in pounds
            self.amount = input("How much have you spent?\n")
            
            # Asks the user to input where the expenditure took place
            self.where = input("Where did you spend it?\n")

            # Asks the user to input the type of expenditure. The type must be a
            # valid, as defined in the configuration file. If the type is not valid
            # the user may add the type to the list of valid types.
            valid_types = data.get("type")
            
            type_is_invalid = True
            while type_is_invalid:
                type = input("What kind of expenditure was it? ('view all' to see valid types)\n")
                if type in valid_types:
                    self.type = type
                    type_is_invalid = False
                elif type == "view all":
                    # Prints all the valid types
                    for valid_type in valid_types:
                        print(valid_type)
                else:
                    add = input("type " + type + " is not valid. Would you like to add it "
                             "as a valid type? (y, n)\n")
                    if add == "y":
                        config_file = open(OUTPUT_LOCATION + "expenditure.config", "a")
                        config_file.write("," + type)
                        config_file.close()
                        type_is_invalid = False
                        self.type = type
        elif access == 'r':
            data = data.rstrip()
            properties = data.split(",")
            self.date = properties[0]
            self.amount = properties[1]
            self.where = properties[2]
            self.type = properties[3]
        else:
            print("Something has gone wrong ...")
                
    def append_to_file(self, file):
        # Opens the file and writes the line
        file_handler = open(file,'a')
        file_handler.write(self.to_string() + "\n")
        print("Added " + self.to_string() + " to " + file)
        file_handler.close()
        
    def to_string(self):
        properties = [self.date, self.amount, self.where, self.type]
        return ",".join(properties)

# ------------------------------------------------------------------------------
# Class ExpenditureFile
#
# Holds the file where the expenditure is written. Has two properties:
# - file    - This is the full file path to the csv where the expenditure data
#             is stored.
# - config  - This is the full file path to the comma separated file where the
#             configuration data is stored.
# - records - This contains a list of expenditure record objects. This reads all
#             of the records.
# ------------------------------------------------------------------------------
class ExpenditureFile:
    def __init__(self, file, config):
        self.file = file
        self.config = config
        
        # Read all the records in the expenditure file
        self.records = []
        file_handler = open(self.file,'r')
        for line in file_handler.readlines():
            record = ExpenditureRecord(line,'r')
            #print(record.to_string())
            self.records.append(record)
        file_handler.close()
    
    # Adds a new record
    def add_record(self):
        new_record = ExpenditureRecord(self.config, 'w')
        new_record.append_to_file(self.file)
        self.records.append(new_record)
   
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
        if "types" in properties.keys():
            types = properties.get("types")
                
        if "dates" in properties.keys():
            dates = properties.get("dates")
            if len(dates) == 2:
                start_date = string_to_date(dates[0])
                end_date = string_to_date(dates[1])
           
        for record in self.records:
            record_counted = False
            if types and record.type in types:
                record_counted = True
            if dates:
                record_date = string_to_date(record.date)
                if start_date and record_date >= start_date and end_date and record_date <= end_date:
                    record_counted = True
            if not properties:
                record_counted = True
                
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
        
        
if __name__ == "__main__":
       
    config_file = open(OUTPUT_LOCATION + "expenditure.config", "r")
    for line in config_file.readlines():
        if line[:5] == "type:":
            valid_types = line[5:].split(",")
    
    config = {"type" : valid_types}
    
    config_file.close()
    
    if IS_TEST:
        print("Running in test mode")
        expenditure_file = ExpenditureFile(TEST_LOCATION + "expenditure.csv", config)
    else:
        expenditure_file = ExpenditureFile(OUTPUT_LOCATION + "expenditure.csv", config)

    keep_going = True
    while keep_going:
        tui = input("What would you like to do? (a, c, p, l, e, total)\n")
        if tui == "a":
            expenditure_file.add_record()
        elif tui == "c":
            keep_going = False
        elif tui == "p":
            expenditure_file.print_all_records()
        elif tui == "l":
            expenditure_file.print_last_record()
        elif tui == "e":
            expenditure_file.open_csv()
        elif tui == "total":
            expenditure_file.summary()
        elif tui[0:5] == "total":
            args = tui.split("-")
            dates = []
            types = []
            for arg in args:
                if arg[0] == "d":
                    dates = arg.split(" ")[1:3]
                elif arg[0] == "t":
                    arg = arg[2:]
                    types = arg.split(",")
                    
            expenditure_file.summary(dates=dates,types=types)
        elif tui == "type total":
            input_types = input("Which types would you like to total?\n").split(",")
            invalid_types = []
            for input_type in input_types:
                if input_type not in valid_types:
                    print("Invalid type " + input_type + " found, ignoring this type")
                    invalid_types.append(input_type)
                    
            for invalid_type in invalid_types:
                input_types.remove(invalid_type)
            
            # If there are still input_types left after the invalid ones have
            # been removed then find the summary of these types.
            if input_types:
                expenditure_file.summary(types=input_types)
        else:
            print("Input '" + tui + "' not recognised, try again")