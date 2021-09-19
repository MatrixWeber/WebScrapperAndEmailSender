import ezgmail
import os
#from threading import Thread


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


project_dir = os.getcwd()
ezgmail.init()

message = read_file(project_dir + '/email_message.txt')
emails = get_contacts(project_dir + '/email_list.txt')
emails_already_sent = get_contacts(project_dir + '/email_list_already_sent.txt')
for email in emails_already_sent:
    try:
        emails.remove(email)
    except:
        pass

threads = []
for email in emails:
    ezgmail.send(email, 'Automatisierung Ihres Computers', message, [project_dir + '/alexanderWeberLogoHeller.png', project_dir + '/qr-code.png'])
   # t = Thread(target=ezgmail.send, args=(email, 'Automatisierung Ihres Computers', message,
                                          #[project_dir + '/alexanderWeberLogoHeller.png', project_dir + '/qr-code.png']))
#   threads.append(t)
#    t.start()
#for x in threads:
#    x.join()

print('Succeessfully sent emails: ' + str(emails))

with open('email_list_already_sent.txt', 'a') as f:
    for email in emails:
        f.write(email + '\n')

