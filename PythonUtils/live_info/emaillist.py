from PythonUtils.live_info.simple_email import Email

class EmailList:
    def __init__(self):
        self.emails = []

    def add_email(self, from_address, to, subject, date):
        self.emails.append(Email(from_address, to,subject,date))

    def to_string(self):
        if self.emails == []:
            return_string = "Email list is empty"
        else:
            max_lengths = {'From':0,'Delivered-To':0,'Subject':0,'Date':0}
            return_string = ""
            for email in self.emails:
                 if len(email.from_address) > max_lengths['From']:
                     max_lengths['From'] = len(email.from_address)
                 if len(email.to) > max_lengths['Delivered-To']:
                     max_lengths['Delivered-To'] = len(email.to)
                 if len(email.short_subject) > max_lengths['Subject']:
                     max_lengths['Subject'] = len(email.short_subject)
            for email in self.emails:
                return_string += email.from_address.ljust(max_lengths['From']) + " | "
                return_string += email.to.ljust(max_lengths['Delivered-To']) + " | "
                return_string += email.date + " | "
                return_string += email.short_subject.ljust(max_lengths['Subject'])
                return_string += "\n"
        return return_string
