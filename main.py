#Import pandas for dataframes
#Import datetime to check day
import numpy as np
import pandas as pd
import datetime
import requests
from twilio.rest import Client

#datetime_object = datetime.datetime.now() #Get current time
today = datetime.date.today() #Get current day
today = pd.Timestamp(today) #Convert current day into usable formate
interviewees = pd.ExcelFile('[File path to the interview information]') #Load in list of interview candidates
interviews_df = interviewees.parse() #Parse interview candidates into dataframe
Reminders = (interviews_df['Date'] - datetime.timedelta(days=1)) #Take their interview day and subtract one to send out reminder
Reminders_df = interviews_df[Reminders == today] #Checking which candidates have reminders today
Reminder_phones = pd.Series.tolist(Reminders_df['Phone'])
Reminder_emails = pd.Series.tolist(Reminders_df['Email'])
account_sid = '[Insert account_sid here]'
auth_token = '[Insert auth_token here]'
client = Client(account_sid, auth_token)
for i in range(Reminders_df.shape[0]):
    Name, Day,Time, Address = (Reminders_df.iloc[i,0],Reminders_df.iloc[i,1],Reminders_df.iloc[i,2],Reminders_df.iloc[i,5])
    Interview_dayOfWeek = Day.day_name()
    Interview_date = Day.date()
    Interview_time = Time
    Text = '''Hello, {}.

This email is a friendly reminder that you have an upcoming interview this {} on {} at {} UTC.
The address of your interview is {}.
We look forward to discussing your qualifications for the position.
Please do not respond to this automated message, email HR for further communication.

Warm Regards,
Precision Headhunters Recruiters.
    '''.format(Name,Interview_dayOfWeek,Interview_date,Interview_time,Address)

    message = client.messages.create(
                              body=Text,
                              from_='[Your twilio number here]',
                              to= '+1' + str(Reminders_df.iloc[0,4])
                          )
    print(message.sid)

    def send_simple_message():
        return requests.post(
            "[Your mailgun url]",
            auth=("api", "[Your api key]"),
            data={"from": "Precision Headhunters Recruiters <[Your mailgun email]",
                "to": str(Reminders_df.iloc[i,3]),
                "subject": "Friendly Interview Reminder",
                "text": Text})
    send_simple_message()

