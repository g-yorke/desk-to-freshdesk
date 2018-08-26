# desk-to-freshdesk

With Desk.com's recent end-of-life announcement, we needed to move about 5,000 resolved Desk tickets to our replacement platform,Freshdesk. This Python 3.7 script uses a CSV file exported from Desk to create stripped down tickets in Freshdesk. There are many possible improvements, but this gave us what we needed, and may help others.

The newly created (but resolved) Freshdesk tickets have the subject "Desk #" and your old Desk ticket number as a prefix before the Desk subject. The original datestamp is at the beginning of the body. Unfortunately, the Freshdesk API doesn't let us set the created date, so in Freshdesk the tickets will show as created when imported.

You should test the script with a subset (5 - 10 records) set of your CSV file. See the note below about editing the test CSV.

The script takes into account Freshdesk's API rate limits. You'll be asked what hourly rate to use -- see below.


LIMITATIONS AND KNOWN ISSUES:

1) The script only sends title, body, and requester email to Freshdesk. It sets the new tickets as resolved, priority 1 (low), and source = email. Notably missing are assigned agent or group, or tags.

2) Rows are skipped if the Desk record is missing requestor email address -- these are reported on screen as errors.

3) The ticket body doesn't have paragraph breaks.

4) IMPORTANT: You have to remember to turn off email notifications before the process, so old Desk requesters don't get new "We received your request" notifications. See below.


Ideas for improvement:

- fix issue where row fails if no Desk.com email address. Could set a Freshdesk unique_external_id instead (Freshdesk requires email, or one of: requester_id, phone, twitter_id, facebook_id, unique_external_id)
- have a test mode that finds a user-entered Desk ticket and loops only x more times. Substitute user-designated email address.
- clean up the body field to break between inbound and outbound messages
- import more fields and values: save using other statuses than 'resolved', set assigned agent(s), set custom fields.
- store Freshdesk domain, CSV path, CSV filename after initial user entry
- log only the errors to a file
- handle case of can't find CSV file


USING THE SCRIPT:

Export your Desk cases: https://support.desk.com/customer/en/portal/articles/1192427-exporting-cases

The script assumes the Desk CSV file is named desk-export.csv and is on your OS X or Windows desktop. It also assumes you're using an English language system where the desktop is named 'desktop.' Change the script if necessary.

Have the following handy since the script will ask for them: 

1) Your Freshdesk API key as described here: https://support.freshdesk.com/support/solutions/articles/215517-how-to-find-your-api-key 

2) Your Freshdesk support site name -- usually the your company's name where "subdomain" is when you go to your help desk at "subdomain.freshdesk.com." When prompted, enter the name without quotes.

3) Your Freshdesk plan name and API rate limit. As of August 2018, hourly rate limits were: Sprout 1,000; Blossom or Garden 2,000; Estate or Forest 5,000


Testing:

You should test this on five or ten records first. Create a version of your CSV file with only that many rows. Edit the test CSV file to replace the requester's email addresses with an internal one -- that way you won't send a notification to the original requester. You can do this in Excel and save the file as a CSV. Be sure to keep the header row. After the test, remember to delete the newly created test tickets. They are imported as status = resolved so you may need to change views or filters to see them.


IMPORTING 'FOR REAL:'

IMPORTANT: if you have automatic requester email notifications enabled in Freshdesk, when importing the entire CSV file, turn those notifications OFF in admin > email notifications > requester notifications > new ticket created.

Remember to turn notifications back on when done.


NOTES AND REFERENCE:

Freshdesk API reference: https://developers.freshdesk.com/api/#quick-reference
how to get API key: https://support.freshdesk.com/support/solutions/articles/215517-how-to-find-your-api-key
sample code: https://github.com/freshdesk/fresh-samples/blob/3dd7277c563bc30d148cb5c8bac5364e7e73a185/Python/create_ticket.py
