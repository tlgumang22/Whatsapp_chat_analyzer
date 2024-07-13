import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Watsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    #fetch unique user
    user_list = df['user'].unique().tolist()
    user_list.remove('notification')
    user_list.sort();
    user_list.insert(0 , "ALL")

    selected_user = st.sidebar.selectbox("Show Analysis W.R.T." , user_list)

    num_messages , words , num_media_messages , num_links = helper.fetch_stats(selected_user , df)

    if st.sidebar.button("Show Analysis"):

        #stats area
        st.title("Statistics")
        col1 , col2 , col3 , col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total Media")
            st.title(num_media_messages)
        with col4:
            st.header("Total Links")
            st.title(num_links)

        #monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user , df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'] , timeline['message'] , color='green')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        #daily timeline
        st.title("Daily Timeline")
        timeline = helper.daily_timeline(selected_user , df)
        fig, ax = plt.subplots()
        ax.plot(timeline['only_date'], timeline['message'], color='purple')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #activity map
        st.title("Activity Bar Graph")
        col1 , col2 = st.columns(2)

        with col1:
            st.header("Most Active Day")
            weekly_timeline = helper.week_activity_map(selected_user, df)
            fig,ax = plt.subplots()
            ax.bar(weekly_timeline.index , weekly_timeline.values , color='lightcoral')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most Active Month")
            monthly_timeline = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(monthly_timeline.index, monthly_timeline.values, color='moccasin')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        #heatmap
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user ,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap((user_heatmap))
        st.pyplot(fig)

        #finding most active user in group
        if selected_user == 'ALL':
            st.title("Most Active User")
            x , new_df = helper.most_active_user(df)
            fig , ax = plt.subplots()

            col1 , col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values , color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        #creating word cloud
        st.title("Word Cloud")
        df_wc = helper.create_word_cloud(selected_user , df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most common words
        st.title("Most Common Words")
        most_common_df = helper.most_common_words(selected_user , df)
        fig,ax = plt.subplots();
        ax.bar(most_common_df[0] , most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #emoji analysis
        emoji_df = helper.emoji_helper(selected_user , df)
        st.title("Emoji Analysis")
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head() , labels=emoji_df[0].head() , autopct="%0.2f")
            st.pyplot(fig)