from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
extract = URLExtract()
def fetch_stats(selected_user , df):

    if selected_user != 'ALL':
        df = df[df['user']==selected_user]

    # 1. number of messages
    num_messages = df.shape[0]

    #2. number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    #3. number of media
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    #4. number of links
    links=[]
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)

def most_active_user(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'count': 'precentage', 'user': 'name'})
    return x , df

def create_word_cloud(selected_user , df):
    df = df[df['message'] != '<Media omitted>\n']

    if selected_user != 'ALL':
        df = df[df['user']==selected_user]

    wc = WordCloud(width=500 , height=500 , min_font_size=10 ,background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep = " "))
    return df_wc


def most_common_words(selected_user, df):
    if selected_user != 'ALL':
        df = df[df['user']==selected_user]

    temp = df[df['user'] != "notification"]
    temp = temp[temp['message'] != '<Media omitted>\n']

    # f.open('stop_hinglish.txt' , 'r')
    # stop_words = f.read()

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            # if word not in stop_words
            words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user , df):
    if selected_user != 'ALL':
        df = df[df['user']==selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user , df):
    if selected_user != 'ALL':
        df = df[df['user']==selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user , df):
    if selected_user != 'ALL':
        df = df[df['user']==selected_user]

    timeline = df.groupby(['only_date']).count()['message'].reset_index()

    return timeline

def week_activity_map(selected_user , df):
    if selected_user != 'ALL':
        df = df[df['user']==selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user , df):
    if selected_user != 'ALL':
        df = df[df['user']==selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user , df):
    if selected_user != 'ALL':
        df = df[df['user']==selected_user]

    user_heatmap = df.pivot_table(index='day_name' , columns='period' , values='message' , aggfunc='count').fillna(0)
    return user_heatmap