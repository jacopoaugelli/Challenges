def passlist():
    with open("passwords.lst", "r") as p:
        for i in p:
            yield i.replace('\n', '')

def userlist():
    with open("users.lst", "r") as u:
        for i in u:
            yield i.replace('\n', '')
