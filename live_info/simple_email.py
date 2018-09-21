class Email:
    MAX_SUBJECT_LENGTH = 50
    def __init__(self, from_address, to, subject, date):
        self.from_address = from_address
        self.to = to
        self.subject = subject
        self.date = date
        self.short_subject = subject[0:Email.MAX_SUBJECT_LENGTH]
