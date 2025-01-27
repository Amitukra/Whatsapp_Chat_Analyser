from cProfile import label
from calendar import month_name, day_name

import streamlit as st
from PIL.ImageColor import colormap
from matplotlib.pyplot import subplots
from mpl_toolkits.mplot3d.art3d import rotate_axes
from streamlit import header, columns

import preprocesser, helper
import matplotlib.pyplot as plt
import seaborn as sns

from helper import fetch_most_busiest_user, montly_timeline, daily_timeline

st.sidebar.title('whatsapp chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()

    data = bytes_data.decode("utf-8")

    df= preprocesser.preprocess(data)




    # fetch unique user

    user_list =  df['user_name'].dropna().unique().tolist()

    user_list.sort()

    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox('Show analysis wrt', user_list)

    if st.sidebar.button("Show Analysis"):

        num_messages, words,num_link,num_media= helper.fetch_stats(selected_user,df)

        st.title('Top Statistics')

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.write(selected_user +" Total massages ")
            st.title(num_messages)

        with col2:
            st.write(selected_user + " Total word send")
            st.title(words)

        with col3:
            st.write(selected_user + " Total Media send")
            st.title(num_media)

        with col4:
            st.write(selected_user + " Total link send ")
            st.title(num_link)

        # Monthly Timeline

        st.title("Montly Timeline")

        timeline = helper.montly_timeline(selected_user, df)

        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['num_message'],color="red")
        plt.xticks(rotation='vertical')
        plt.ylabel("Number of Messages")
        st.pyplot(fig)

        # Daily timeline
        st.title("Daily timeline")

        daily_timeline = helper.daily_timeline(selected_user, df)

        fig,ax = plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['message'])
        plt.xticks(rotation='vertical')
        plt.ylabel("Number of Messages")
        st.pyplot(fig)

        # weekly and Monthly Activity map

        month_name,day_name =helper.activity_map(selected_user, df)
        st.title("Activity map")
        col1, col2 = columns(2)

        with col1:

            fig,ax = subplots()
            ax.bar(day_name['day_name'],day_name['count'],color = "orange")
            plt.xticks(rotation='vertical')
            plt.ylabel("Number of Messages")
            st.pyplot(fig)

        with col2:
            fig,ax = subplots()
            ax.bar(month_name['month'],month_name['count'])
            plt.xticks(rotation='vertical')
            plt.ylabel("number of messages")
            st.pyplot(fig)

        # weekly activity Heatmap

        user_heatmap =helper.activity_heatmap(selected_user, df)
        st.title("Weekly Activity Heatmap")
        plt.figure(figsize=(15,10))
        fig,ax =plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)




        # finding the busiest user in the group(group level)
        if selected_user =='Overall':
            st.title(selected_user +' Most Busy user')

            x, new_df = helper.fetch_most_busiest_user(df)
            fig, ax =plt.subplots()

            col1, col2 = st.columns(2)

            with col1:

                ax.bar(x.index, x.values,color ='green')
                plt.xticks(rotation ='vertical', color = 'green')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # wordcloud
        st.title("wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words

        most_common_df = helper.most_common_words(selected_user, df)

        st.title('Most Common words used')
        fig,ax= plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical', color='green')
        st.pyplot(fig)

        # most used emoji

        emoji_df =helper.emoji_helper(selected_user, df)

        st.title('Emoji Analysis')

        col1,col2 =st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            plt.rcParams['font.family'] = 'Segoe UI Emoji'
            fig,ax= plt.subplots()
            ax.pie(emoji_df[1].head(10),labels=emoji_df[0].head(10),autopct='%1.1f%%')
            st.pyplot(fig)








