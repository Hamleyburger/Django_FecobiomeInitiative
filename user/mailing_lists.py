import csv
import uuid


# newsletter variable can be set to a different mailing list file if necessary
newsletter = "user/mailing_lists/general_newsletter_emails.csv"

def subscribe(email):
    """ adds any string to mailing list so make sure to validate first?\n
    Also adds an unsubscribe key that can be used in an unsubscribe link """
    email = email.lower()
    with open(newsletter, "r") as mylist:
        reader = csv.DictReader(mylist)
        for row in reader:
            if email == row["email"].lower():
                return
    with open(newsletter, "a") as mylist:
        writer = csv.DictWriter(mylist, fieldnames=["email", "unsubscribe_key"])
        key = uuid.uuid4()
        writer.writerow({"email": email, "unsubscribe_key": key})


def unsubscribe(unsubscribe_key="", unsubscribe_email=""):
    """ for removing subscriber with an unsubscribe link providing an unsubscribe key """
    print("Unsubscribe called")
    rows = []
    unsubscribed = False
    changed = False

    with open(newsletter, "r") as mylist:
        reader = csv.DictReader(mylist)
        for row in reader:
            if (str(unsubscribe_key) != row["unsubscribe_key"]) and (unsubscribe_email.lower() != row["email"].lower()):
                rows.append(row)
            else:
                changed = True
                unsubscribed = True
    if changed:
        with open(newsletter, 'w') as writeFile:
            writer = csv.DictWriter(writeFile, fieldnames=["email", "unsubscribe_key"])
            writer.writeheader()
            writer.writerows(rows)
    return unsubscribed


def get_subscribers_emails():
    subscribers = []
    with open(newsletter, "r") as mylist:
        reader = csv.DictReader(mylist)
        try:
            for row in reader:
                subscribers.append(row["email"])
        except Exception as e:
            pass

    return subscribers

def get_unsubscribe_key(email):
    key = []
    with open(newsletter, "r") as mylist:
        reader = csv.DictReader(mylist)
        try:
            for row in reader:
                if row["email"] == email:
                    key = row["unsubscribe_key"]
        except Exception as e:
            pass

    return key



# get_subscribers_emails()
# subscribe("fdfdfs@fdfs.dk")
# remove_subscriber("lLfeItVfU3TnyTSRuqycaQQWBM98X41JIe4boH6zY75kWan47HQ2yrf9SwQvZcLw")
