import os
import csv
import time
import requests
import json

# IF YOU HAVE FRESHDESK REQUESTER NOTIFICATIONS ENABLED, TURN THEM OFF BEFORE RUNNING THIS. SEE THE README.

# WARNING: Rows FAIL and are skipped if Desk record is missing email address. Freshdesk requires
# email, or one of: requester_id, phone, twitter_id, facebook_id, unique_external_id

# user-dependent variables for Freshdesk. Change these if needed.
#   Freshdesk_domain is in your company's help desk name, as in yourcompany.freshdesk.com
#   how to find API key: https://support.freshdesk.com/support/solutions/articles/215517-how-to-find-your-api-key
#   the csv_path assumes the file is on the user's desktop. This works only for language systems where the desktop
#   is named "desktop"
#   change the name of the CSV file if needed

freshdesk_domain = input("enter your company's Freshdesk subdomain, like yourcompany in yourcompany.freshdesk.com: ")
api_key = input("enter your Freshdesk API key, like ghrbXmsjcNK6uDjTC0qG: ")
csv_path = os.path.expanduser('~/Desktop/') # works for OS X and Windows where language = English
# if necessary, hard-code the path like the next line
# csv_path = "~/Desktop/"
csv_filename = "desk-export.csv"

# different Freshdesk plans have different rate limits -- see the API reference link above
# as of August 2018, hourly rate limits were: Sprout 1,000; Blossom or Garden 2,000; Estate or Forest 5,000
# calculation is conservative since it ignores processing time
cap = int(input("maximum requests per hour: "))
delay = round((1/(cap/3600)),2)

# set some vars used in the POST request later
freshdesk_url = "https://"+ freshdesk_domain +".freshdesk.com/api/v2/tickets"
password = "x" # not used if using api_key
headers = { 'Content-Type' : 'application/json' }


# open the CSV file
with open(csv_path + csv_filename, newline='', encoding='utf-8') as csvfile:
  
    # create an object that maps the information in each row of the CSV file to an OrderedDict
    # 1st row of the CSV file has the field names. Since fieldnames parameter is not set, the key are the 1st row data
    reader = csv.DictReader(csvfile)

    # iterate through the object one row at a time
    for row in reader:
        time.sleep(delay) # stay under API rate limit
        print('Desk case: ', row['Case #'], ' … ',end = " ")

        # extract the Desk case #, subject, description, and requester email, and structure as JSON
        fd_ticket = {
            'subject' : 'Desk #' + row['Case #'] + ': ' + row['Case Subject'],
            'description' : '[originally created ' + row['Created At'] + '] ' + row['Body'],
            'email' : row['Email Address'], # fails if missing this email address; could backstop w unique_external_id
            'status' : 4,
            'priority' : 1,
            'source' : 1,
            # Freshdesk doesn't allow you to set the created_at' value
        }

        # post to Freshdesk
        r = requests.post(freshdesk_url, auth = (api_key, password), headers = headers, data = json.dumps(fd_ticket))

        # handle the response -- modified from the GitHub code samples
        if r.status_code == 201:
            print ("Ticket created successfully. Location Header : ", r.headers['Location'])
        else:
            print ("Failed to create ticket. Errors are:")
            response = json.loads(r.content)
            errors = response["errors"]
            for error in errors:
                print ("Field : ", error["field"], " |  Message : ", error["message"], " | Code : ", error["code"])
            print (response["errors"])

            print ("x-request-id : ", r.headers['x-request-id'])
            print ("Status Code : ", str(r.status_code))
        print()

    print('done!')
