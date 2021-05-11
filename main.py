from Google import Create_Service
from gmail_stuff import *
from calendar_stuff import *

services = ['google.com', 'teams.microsoft.com', 'zoom.us']

gmailService = gmailAuthenticate()
calService = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

# for some reason if u don't specify a max length, it defaults to 128 so u don't get everything
# events = calService.events().list(calendarId='primary', maxResults=9999).execute()
events = calService.events().list(calendarId=CALENDAR_ID, maxResults=9999).execute()


tomorrowDate = getTomorrowDate()
tomorrowEvents = getEvents(tomorrowDate, events)

message = ""
subject = "About your upcoming CreationCamp session"

with open('message.txt', 'r') as f:
    # without stripping the newline characters, it shows '\n' in the message if it has multiple lines
    # gmail will automatically format it to have multiple lines tho so dont worry
    message = f.read().replace('\n', ' ')
    f.close()

for event in tomorrowEvents:
    link = False
    for s in services:
        try:
            if (s in event['description']):
                link = True
        except:
            # all of CreationCamp's calendar meetings have some description
            # so if you have something without a description,
            # the program won't like it but we don't really need to worry about it
            # cuz it's not a creationcamp meeting
            pass

    #teacher didn't include a link
    if (not link):
        attendees = event['attendees']
        for i in attendees:
            if (i['email'] != myEmail):
                sendMessage(gmailService, i['email'], subject, message)
