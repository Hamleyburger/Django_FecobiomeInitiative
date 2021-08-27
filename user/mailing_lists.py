import os
import csv
from django.utils.crypto import get_random_string


# newsletter variable can be set to a different mailing list file if necessary
newsletter = "user/mailing_lists/general_newsletter_emails.csv"

def add_subscriber(email):
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
        key = get_random_string(64).replace(',', '') # remove delimiter from key
        writer.writerow({"email": email, "unsubscribe_key": key})


def remove_subscriber(unsubscribe_key):
    """ for removing subscriber with an unsubscribe link providing unsubscribe key """
    rows = []
    changed = False
    with open(newsletter, "r") as mylist:
        reader = csv.DictReader(mylist)
        for row in reader:
            if unsubscribe_key != row["unsubscribe_key"]:
                rows.append(row)
            else:
                changed = True
    if changed:
        with open(newsletter, 'w') as writeFile:
            writer = csv.DictWriter(writeFile, fieldnames=["email", "unsubscribe_key"])
            writer.writeheader()
            writer.writerows(rows)




#add_subscriber("fdfdfs@fdfs.dk")
# remove_subscriber("lLfeItVfU3TnyTSRuqycaQQWBM98X41JIe4boH6zY75kWan47HQ2yrf9SwQvZcLw")
