so pretty much, this scans your google calendar and looks at all events
that weren't made by you starting whenever tomorrow is.

when it finds an event, it'll check the description for either an ms teams,
zoom, or google meets link.

if it doesn't find one, it'll send an email to all attendees who aren't you.

NOTE: ONLY WORKS IF YOU USE A GMAIL ADDRESS

TO MAKE IT WORK:
1) pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
    if you don't know how to use pip/don't have pip, google that one
    if you get really stuck, send me a message on slack and i can help

2) fill out message.txt with whatever you want your message to be
3) in gmail_stuff.py, on line 18, replace my email with your email
4) in calendar_stuff.py, on line 10, replace my calendar id with yours.
    you can find this by going into google calendar, click the 3 dots
    to the right of your specific calendar (on the left hand side of the screen,
    right underneath the month view and 'search for people'), click 'settings and
    sharing' and scroll down to 'integrate calendar', your calendar id is the first
    thing at the top of that section.
5) when u first run the script, it's going to redirect to Google's OAuth 2 service,
    so u know it's secure. if you use a mac, for some reason i couldn't get this to
    work with safari, so just copy the link that the console spits out into chrome.
    you only need to do this the first time you run it.
6) figure out how to make it run at whatever interval u want with either PowerShell or Automator