from datetime import datetime, timezone

CLIENT_SECRET_FILE = 'client_secret_file.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']

#gonna need to change this to whatever ur calendar id is, u can google how to get that
#i don't think it'll necessairly be ur email, so make sure to check
CALENDAR_ID = 'petergelgor7@gmail.com'


#gets tomorrows date in the form 'yyyy-mm-dd'
def getTomorrowDate():
    local_time = datetime.now(timezone.utc).astimezone()
    current_date = local_time.isoformat()[0:10]


    thirtyMonths = ['09', '04', '06', '11']
    thirtyOneMonths = ['01', '03', '05', '07', '08', '10', '12']


    currentYear = current_date[0:4]
    currentMonth = current_date[5:7]
    currentDay = current_date[8:10]

    #just kinda forcing these variables into existence before i use em
    tomorrowYear = None
    tomorrowMonth = None
    tomorrowDay = None

    #month shifting
    if (currentMonth in thirtyMonths and currentDay == "30"):
            # year can't switch on 30 day months
            tomorrowYear = currentYear
            tomorrowMonth = str(int(currentMonth) + 1)
            if (len(tomorrowMonth) == 1):
                #all date values need 2 numbers
                tomorrowMonth = '0' + tomorrowMonth
            tomorrowDay = '01'

    elif (currentMonth in thirtyOneMonths and currentDay == "31"):
        # year might switch if it's december
        if (currentMonth == '12'):
            tomorrowYear = str(int(currentYear) + 1)
            tomorrowMonth = '01'
            tomorrowDay = '01'
        else:
            tomorrowYear = currentYear
            tomorrowMonth = str(int(currentMonth) + 1)
            if (len(tomorrowMonth) == 1):
                tomorrowMonth = '0' + tomorrowMonth
            tomorrowDay = '01'

    #gotta deal with february
    elif (currentMonth == "02" and currentDay == "28"):
        tomorrowYear = currentYear
        tomorrowMonth = '03'
        tomorrowDay = '01'

    #not a month switch
    else:
        tomorrowYear = currentYear
        tomorrowMonth = currentMonth
        tomorrowDay = str(int(currentDay) + 1)

        if (len(tomorrowDay) == 1):
            tomorrowDay = '0' + tomorrowDay

    #compiling it all together
    tomorrowDate = tomorrowYear + '-' + tomorrowMonth + '-' + tomorrowDay
    return tomorrowDate

#gets events on a certain date
def getEvents(date, events):
    eventsOnDate = []

    for event in events['items']:
        # idk why but some of the events use date format, and some use datetime. janky but functional workaround incoming:
        try:
            if (str(event['start']['date']) == date):
                eventsOnDate.append(event)
        except:
            try:
                # only give a shit about the first 10 things (the date as yyyy-mm-dd) with the datetime
                if (str(event['start']['dateTime'])[0:10] == date):
                    eventsOnDate.append(event)
            except:
                # lmao error handling at its finest
                # real shit if it doesn't have a date or a datetime, we don't really care about it, and i don't want the
                # program to crash cuz of a stupid unspecified event
                pass

    return eventsOnDate
