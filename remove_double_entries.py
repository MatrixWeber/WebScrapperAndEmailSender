from os import path


def remove_doubles_of_2_files(filename_src, filename_dst):
    if path.exists(filename_src):
        with open(filename_src, 'r+') as f:
            emails_src = set()
            for email in f.readlines():
                split_emails = str(email).split('\n')
                if split_emails[0]:
                    emails_src.add(split_emails[0])
    if path.exists(filename_dst):
        with open(filename_dst, 'r+') as f:
            emails = set()
            for email in f.readlines():
                split_emails = str(email).split('\n')
                if split_emails[0]:
                    emails.add(split_emails[0])
            email_set = emails.union(emails_src)
            for email in email_set:
                if email:
                    f.write(email + '\n')


def remove_doubles(filename_dst):
    if path.exists(filename_dst):
        with open(filename_dst, 'r') as f:
            emails = set()
            for email in f.readlines():
                split_emails = str(email).split('\n')
                if split_emails[0]:
                    emails.add(split_emails[0])
        with open(filename_dst, 'w') as f:
            for email in emails:
                if email:
                    f.write(email + '\n')

filename_dst = 'email_list.txt'
remove_doubles(filename_dst)

