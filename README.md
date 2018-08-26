# desk-to-freshdesk

With Desk.com's recent end-of-life announcement, we needed to move about 5,000 Desk tickets to our replacement platform,
Freshdesk. This Python 3.7 script uses the CSV file exported from Desk to create new tickets in Freshdesk.


LIMITATIONS AND KNOWN ISSUES:

The script only sends title, body, and requester email to Freshdesk. It sets the new tickets as resolved, priority 1 (low),
and source = email. 

The body doesn't have paragraph breaks.

Rows FAIL if Desk record is missing requestor email address -- the row is skipped. Freshdesk requires email, or one of: 
requester_id, phone, twitter_id, facebook_id, unique_external_id

IMPORTANT: You have to remember to turn off email notifications before the process, so old Desk requesters don't get new
"We received your request" notifications. See below.


Ideas for improvement:

- fix issue where row fails if no Desk.com email address. Could set a Freshdesk unique_external_id instead.
- have a test mode that finds a specific Desk ticket and loops only x times. Substitute user-designated email address.
- clean up the body field to break between inbound and outbound messages
- import more fields and values: save using other statuses than 'resolved', set assigned agent(s), custom fields.
- store domain, path, filename after initial user entry
- log only the errors to a file
- handle case of can't find CSV file


USING THE SCRIPT:

Export Desk cases: https://support.desk.com/customer/en/portal/articles/1192427-exporting-cases


Preparation:

You need to get your Freshdesk API key as described here:
https://support.freshdesk.com/support/solutions/articles/215517-how-to-find-your-api-key 

You need to know your Freshdesk support site name -- usually the your company's name where "subdomain" is when you go to 
your help desk at "subdomain.freshdesk.com." When prompted, enter the name without quotes.

The script assumes the Desk CSV file is named desk-export.csv and is on your desktop. It also assumes you're using
an English language system where the desktop is named 'desktop.' Change the script if necessary.


Testing:

You should test this on five or ten records first. Create a version of your CSV file with only that many rows.
Edit the test CSV file to replace the requester's email addresses with an internal one -- that way you won't send a
notification to the original requester. You can do this in Excel and save the file as a CSV. Be sure to keep the header row.
After the test, remember to delete the newly created test tickets. They are imported as status = resolved so you may need to
change views or filters to see them.


IMPORTING 'FOR REAL:'

IMPORTANT: if you have automatic requester email notifications enabled in Freshdesk, when importing the entire CSV file, turn those notifications OFF in admin > email notifications > requester notifications > new ticket created.

Remember to turn notifications back on when done.


NOTES AND REFERENCE:

Freshdesk API reference: https://developers.freshdesk.com/api/#quick-reference
how to get API key: https://support.freshdesk.com/support/solutions/articles/215517-how-to-find-your-api-key
sample code: https://github.com/freshdesk/fresh-samples/blob/3dd7277c563bc30d148cb5c8bac5364e7e73a185/Python/create_ticket.py
