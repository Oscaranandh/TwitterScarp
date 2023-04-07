import snscrape.modules.twitter as sntwit
import pymongo as pm
import pandas as pd
from pymongo import MongoClient
import streamlit as st
# tweeter data scrapping as per keyword or hashtag
st.session_state.data=[]
st.session_state.df=None
st.markdown("""
    <h1 style='text-align: center;color: #1DA1F2;'>Twitter Scarping </h1>
""", unsafe_allow_html=True)
image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRZnp8CTWyCR9SAsEQlhDOAj3kIUawmnH_TLg&usqp=CAU"
caption_s={"color":"#1DA1F2"}
st.image(image_url,width=700)
st.write("""Twitter is a popular social media platform where users can post their thoughts, opinions, and updates on a variety of topics. As a result, it is an excellent source of data for research and analysis purposes. However, extracting data from Twitter manually can be a time-consuming task. That's where a Twitter scraping tool comes in handy.

In this user interface website for Twitter scraping, you can enter a keyword or hashtag related to the data you want to extract. You can also choose the number of tweets you want to extract. Once you submit the form, the website will use the snscrape Python package to extract the relevant data from Twitter.

The extracted data will then be displayed on the website, and you will also have the option to download it in either CSV or JSON format. Additionally, you can choose to upload the data to a MongoDB database by clicking on the "Upload Data" checkbox. If you decide to upload the data, you can see a list of collection names in the database.

Overall, this user interface website makes it easy to extract and analyze Twitter data quickly and efficiently.""",style="color: blue")
def Scrape_twitter_data(search, num_tweet):
    data1 = []
    for i, tweet in enumerate(sntwit.TwitterSearchScraper(search).get_items()):
        if i>num_tweet:
            break
        data1.append([tweet.date,tweet.id,tweet.url,tweet.content,tweet.user.username,tweet.replyCount,tweet.retweetCount,tweet.lang,tweet.likeCount,tweet.source])
    df=pd.DataFrame(data1,columns=["Date","ID","URL","Content","User_name","Reply_count","Retweet_count","Language","Likes_count","Source"])
    st.session_state.df=df
    st.session_state.data = df.to_dict("records")

with st.form("my-form"):
    st.markdown("<h3 style='color:#1DA1F2;'>Search Box</h3>", unsafe_allow_html=True)
    search= st.text_input("Enter a keyword or hashtag based on that data should be scrapped: ")
    number_tweets=st.slider('Enter the count of tweets to be scrapped:', 0,1000,100)
    submit=st.form_submit_button("Submit")

if submit:
    Scrape_twitter_data(search,number_tweets)

if st.session_state.df is not None:
    st.write("Scraped Twitter data:")
    st.write(st.session_state.df)
st.markdown("<h3 style='color:#1DA1F2;'>Uploading your data here</h3>", unsafe_allow_html=True)
st.write("Press enter upload to upload the data into database:")
upload_button=st.checkbox("Upload Data")
if upload_button is True :
    if st.session_state.data:
        client=MongoClient("mongodb://localhost:27017/")
        db=client["tweeter_database"]
        collection=db[search]
        db.collection.insert_many(st.session_state.data)
        st.success("Data has been uploaded:",icon='✅')
        st.write("list of collection names:")
        mycoll=db.list_collection_names()
        st.write(mycoll)
else:
    st.error("No data to upload.")

if st.session_state.df is not None:
    st.markdown("<h3 style='color:#1DA1F2;'>Download the file </h3>", unsafe_allow_html=True)
    st.write("Download the file in the format you want:")
    st.write("Download in csv format")
    def convert_to_csv(df1):
        return df1.to_csv()
    csv_file=convert_to_csv(st.session_state.df)
    st.download_button(csv_file,f"{search}_tweet.csv","text/csv",key="download-csv")
    st.write("Downalod in json format")
    def convert_to_json(df1):
        return df1.to_json()
    json_file=convert_to_json(st.session_state.df)
    st.download_button(json_file,f"{search}_tweet.json","text/json",key="download-json")

st.markdown("<h3 style='color:#1DA1F2;'>Thanks for visiting our page</h3>", unsafe_allow_html=True)
st.write("""The app is designed to be user-friendly and easy to use, with clear instructions and intuitive controls. Users can easily access and manipulate their scraped data, making it a useful tool for data analysis and research.""")