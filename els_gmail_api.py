import ezgmail
import os
from threading import Thread


def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        file_content = f.read()
    return file_content


def get_contacts(filename):
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            emails.append(a_contact.replace('\n', ''))
    return emails


os.chdir(r'/Users/alexanderweber/Documents/GitHub/python_projects/WebScrapperAndEmailSender/')
ezgmail.init()

message = read_file('email_message.txt')
emails = get_contacts('email_list.txt')
emails_already_sent = get_contacts('email_list_already_sent.txt')
for email in emails_already_sent:
    try:
        emails.remove(email)
    except:
        pass
# ezgmail.send(email, 'Automatisierung Ihres Computers', message,
#              ['Automatisierung Ihres Computers.eml'])
threads = []
for email in emails:
    t = Thread(target=ezgmail.send, args=(email, 'Automatisierung Ihres Computers', message,
                                          ['Automatisierung Ihres Computers.eml']))
    threads.append(t)
    t.start()
for x in threads:
    x.join()

print('Succeessfully sent emails: ' + str(emails))

with open('email_list_already_sent.txt', 'a') as f:
    f.write(emails)
# unreadThreads = ezgmail.unread()  # List of GmailThread objects.
# ezgmail.summary(unreadThreads)

# recentThreads = ezgmail.recent()

# resultThreads = ezgmail.search('subject:Automatisierung')
# print(len(resultThreads))
# ezgmail.summary(resultThreads)
