def writetoFile(emailSet):
    with open('emails.txt', 'r+') as f:
        emails = set()
        for email in f.readlines():
            split_emails = str(email).split('\n')
            if not split_emails[0].empty():
                emails.add(split_emails[0])
        emailList = emails.union(emailSet)
        for email in emailList:
            with open('emails.txt', 'a') as f:
                f.write(email + '\n')
