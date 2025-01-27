import re
import pandas as pd
from datetime import datetime
from calendar import month_name,day_name

def preprocess(data):
    Pattern = '\d{1,2}/\d{2}/\d{2},\s\d{1,2}:\d{2}\s(?:am|pm)\s-\s'

    massages = re.split(Pattern, data)[1:]
    dates = re.findall(Pattern, data)

    def convert_to_24_hour(date_str):
        # Remove the narrow space and AM/PM indicators
        date_str = date_str.replace('\u202fpm', ' PM').replace('\u202fam', ' AM')

        # Extract date and time part (before '-')
        date_time_str = date_str.split(' - ')[0]

        # Convert the string to a datetime object
        date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y, %I:%M %p')

        # Return the 24-hour formatted date and time string
        return date_time_obj.strftime('%d/%m/%y, %H:%M')

    # Apply conversion to each item in the list
    converted_data = [convert_to_24_hour(item) for item in dates]

    df = pd.DataFrame({'user_message': massages, 'message_date': converted_data})


    # convert message_date type
    df['message_date'] = pd.to_datetime(df['message_date'])

    df.rename(columns={'message_date': 'date'}, inplace=True)

    list_of_lists = df.values.tolist()

    # filtered_raw_data = [row for row in list_of_lists if "<Media omitted>" not in row[0]]
    #
    # df = pd.DataFrame(filtered_raw_data)

    df.rename(columns={0: 'user_message', 1: 'date'}, inplace=True)

    def split_message(row):
        # Use regular expressions to split based on the keywords
        match = re.search(r'(added |changed |turned |updated |: |left )', row)
        if match:
            action = match.group(0)
            parts = row.split(action, 1)
            user = parts[0].strip()
            message = action + parts[1].strip()
            return pd.Series([str(user), str(message)])
        return pd.Series([None, str(row)])

    # Apply the function to split user and message
    df[['user_name', 'message']] = df['user_message'].apply(split_message)

    # df[['user_name', 'message']] = df['user_message'].str.split(': ', n=1, expand=True)
    df = df.drop(columns=['user_message'])

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minutes'] = df['date'].dt.minute
    df['only_date'] = df['date'].dt.date
    df["day_name"] = df['date'].dt.day_name()

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))

        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))

        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df["period"] = period

    df =df[2:]
    df = df.reset_index(drop=True)



    return df

