from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime
from live_info.emaillist import EmailList
from live_info.display_item import DisplayItem

class EmailInfo(DisplayItem):
    def __init__(self, expiry_duration, num_messages):
        DisplayItem.__init__(self, expiry_duration)
        # Setup the Gmail API
        SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
        store = file.Storage('live_info\credentials.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('live_info\client_secret.json', SCOPES)
            creds = tools.run_flow(flow, store)
        self.service = build('gmail', 'v1', http=creds.authorize(Http()))
        self.num_messages = num_messages

    def get_latest_messages(self, num_messages):
        return self.service.users().messages().list(userId='me',maxResults=num_messages).execute()

    def get_messages(self, max_results=10, q=''):
        return self.service.users().messages().list(userId='me',maxResults=max_results, q=q).execute()

    def get_message(self, msg_id):
        return self.service.users().messages().get(userId='me',id=msg_id, format='full').execute()

    def get_info(self):
        resp = self.get_latest_messages(self.num_messages)
        email_list = EmailList()
        for email in resp['messages']:
            email_resp = self.service.users().messages().get(userId='me',id=email['id'],format='metadata').execute()
            headers = email_resp['payload']['headers']
            for header in headers:
                if header['name'] == 'From':
                    if "<" in header['value']:
                        from_address = str(header['value']).split("<")[1][:-1]
                    else:
                        from_address = str(header['value'])
                elif header['name'] == 'Delivered-To':
                    to = str(header['value'])
                elif header['name'] == 'Subject':
                    subject = str(header['value'])
            date = datetime.datetime.fromtimestamp(int(email_resp['internalDate'])/1000).strftime("%d/%m/%Y %H:%M")
            email_list.add_email(from_address,to,subject,date)
        return (email_list.to_string().encode('ascii','ignore')).decode('utf-8','ignore')

if __name__ == "__main__":
    emails = EmailInfo(10)
    print(emails.latest_messages_string())
