import re
import pandas as pd

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{1,2}\s[ap]m\s-\s'

    message = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_message': message, 'message_dates': dates})

    # Step 1: Replace narrow no-break space with a regular space
    df['message_dates'] = df['message_dates'].str.replace('\u202f', ' ')

    # Step 2: Strip the trailing ' - '
    df['message_dates'] = df['message_dates'].str.replace(' - $', '', regex=True)

    # Step 3: Convert message_dates datatype
    df['message_dates'] = pd.to_datetime(df['message_dates'], format='%d/%m/%y, %I:%M %p')
    df.rename(columns={'message_dates': 'date'}, inplace=True)

    # seperate user name and message
    users = []
    messages = []
    for m in df['user_message']:
        entry = re.split(r'^(.*?):\s', m, maxsplit=1)
        if len(entry) > 2:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df