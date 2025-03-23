import streamlit as st
from pygooglenews import GoogleNews

gn = GoogleNews(lang = 'en', country = 'US')

def fetch_news(category=None, query=None):
    gn = GoogleNews()
    if query:
        news_items = gn.search(query).get('entries', [])
    else:
        news_items = gn.topic(category).get('entries', []) if category else []
    return news_items

st.subheader("📰 Latest News")

if "user_data" in st.session_state:
    # Sidebar options
    st.sidebar.header("Settings")
    categories = ["World", "Nation", "Business", "Technology", "Entertainment", "Sports", "Science", "Health"]
    category = st.sidebar.selectbox("Select news category:", [None] + categories)
    query = st.sidebar.text_input("Or search for specific news:")
    if not query:
        news_items = gn.topic_headlines({category.capitalize}, proxies=None, scraping_bee = None)
        if news_items:
            for news in news_items:  # Display only top 10 results
                st.subheader(news)
                st.write(news['published'])
                st.write(news['summary'])
                st.markdown(f"[Read more]({news['link']})")
                st.write("---")
    elif query:
        s = gn.search()
    else:
        st.write("No news found. Try a different category or search.")
else:
    st.error("You need to authenticate first. Please login or sign up.")