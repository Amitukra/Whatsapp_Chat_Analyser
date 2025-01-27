# from app import num_messages
from collections import Counter

import matplotlib.pyplot as plt
from numpy.ma.core import shape
from pygments.lexer import words
# from pygments.styles.dracula import background
from streamlit import columns
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji


extract = URLExtract()


def fetch_stats(selected_user, df):

    if selected_user == 'Overall':

        # fetch number of massage
        num_messages = df.shape[0]

        # fetch number of words

        words = []
        for message in df['message']:
            words.extend(str(message).split())

        #  fetch the number of media
        num_media = df[df['message'] == ': <Media omitted>'].shape[0]

        #  fetch the number of link
        links=[]
        for message in df['message']:
            links.extend(extract.find_urls(message))

        return num_messages, len(words), num_media, len(links)

    else:

        # fetch number of massages
        new_df = df[df['user_name'] == selected_user]
        num_messages = new_df.shape[0]

        # fetch number of media
        num_media= new_df[new_df['message'] == ': <Media omitted>'].shape[0]

        # fetch number of words

        words = []
        for message in new_df['message']:
            words.extend(str(message).split())

        # fetch number of links
        links=[]
        for message in new_df['message']:
            links.extend(extract.find_urls(message))

        return num_messages, len(words), num_media, len(links)

# def fetch_link_stats(selected_user, df1):
#
#     if selected_user == 'Overall':
#
#         #  fetch the number of link
#         links = []
#         for message in df1['message']:
#             links.extend(extract.find_urls(message))
#
#         return len(links)
#
#     else:
#
#         # fetch number of links
#         new_df = df1[df1['user_name'] == selected_user]
#
#         links = []
#         for message in new_df['message']:
#             links.extend(extract.find_urls(message))
#
#         return len(links)


def fetch_most_busiest_user(df):
    x = df['user_name'].value_counts().head(5)

    df = round((df['user_name'].value_counts()/df.shape[0]) * 100,2).reset_index().rename(columns ={"count":"percentage"})

    return x, df

def create_wordcloud(selected_user, df):
    # Extract rows where 'user_message' does NOT contain '<Media omitted>'
    df = df[~df['message'].str.contains('<Media omitted>', na=False)]
    df['message'] = df['message'].str.replace('\n', '', regex=False)
    df = df[~df['message'].str.contains('This message was deleted', na=False)]
    df = df[~df['message'].str.contains('You deleted this message', na=False)]

    if selected_user != 'Overall':
        df = df[df['user_name'] == selected_user]
    wc = WordCloud(width=500, height = 500,min_font_size=10,background_color='white')
    # wc = WordCloud()
    df_wc =wc.generate(df['message'].str.cat(sep=" "))

    return df_wc

def most_common_words(selected_user, df):

    f =open('stop_hinglish.txt','r')
    stop_word = f.read()

    if selected_user != 'Overall':
        df = df[df['user_name'] == selected_user]

    # Extract rows where 'user_message' does NOT contain '<Media omitted>'
    temp = df[~df['message'].str.contains('<Media omitted>', na=False)]
    temp['message'] = temp['message'].str.replace('\n', '', regex=False)
    temp = temp[~temp['message'].str.contains('This message was deleted', na=False)]
    temp = temp[~temp['message'].str.contains('You deleted this message', na=False)]

    words = []

    for massage in temp['message']:
        for word in massage.lower().split():
            if word not in stop_word:
                words.append(word)

    most_common_df= pd.DataFrame(Counter(words).most_common(20))

    return most_common_df


def emoji_helper(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user_name'] == selected_user]

    emojis = []
    for massage in df["message"]:
        emojis.extend(emoji.distinct_emoji_list(massage))

    emoji_df =pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def montly_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user_name'] == selected_user]

    timeline = df.groupby(['year', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time
    timeline.rename(columns={'message': 'num_message'}, inplace=True)

    return timeline

def daily_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user_name'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def activity_map(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user_name'] == selected_user]

    day_name = df['day_name'].value_counts().reset_index()
    month_name = df['month'].value_counts().reset_index()
    return month_name,day_name

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user_name'] == selected_user]

    user_heatmap =df.pivot_table(index='day_name', columns="period", values='message', aggfunc='count').fillna(0)

    return user_heatmap






