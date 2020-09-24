from os import path


def writetoFile(filename, emailSet):
    if path.exists(filename):
        with open(filename, 'r+') as f:
            emails = set()
            for email in f.readlines():
                split_emails = str(email).split('\n')
                if split_emails[0]:
                    emails.add(split_emails[0])
            emailSet = emails.union(emailSet)
    with open(filename, 'w') as f:
        for email in emailSet:
            if email:
                f.write(email + '\n')
