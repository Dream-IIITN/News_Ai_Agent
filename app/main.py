import streamlit as st
import json
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from datetime import datetime
import re
import sqlite3
import pandas as pd

# Initialize the SQLite database
conn = sqlite3.connect('blog.db')
c = conn.cursor()

# Create the posts table if it doesn't exist
c.execute('CREATE TABLE IF NOT EXISTS posts (author TEXT, title TEXT, content TEXT, date DATE)')

# Define some functions for interacting with the database
def add_post(author, title, content, date):
    c.execute('INSERT INTO posts (author, title, content, date) VALUES (?,?,?,?)', (author, title, content, date))
    conn.commit()

def get_all_posts():
    c.execute('SELECT * FROM posts')
    data = c.fetchall()
    return data

def get_post_by_title(title):
    c.execute('SELECT * FROM posts WHERE title=?', (title,))
    data = c.fetchone()
    return data

def delete_post(title):
    c.execute('DELETE FROM posts WHERE title=?', (title,))
    conn.commit()

# Define some HTML templates for displaying the posts
title_temp = """
<div style="background-color:#464e5f;padding:10px;border-radius:10px;margin:10px;">
<h4 style="color:white;text-align:center;">{}</h4>
<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;">
<h6>Author: {}</h6>
<br/>
<br/>
<p style="text-align:justify"> {}</p>
</div>
"""

post_temp = """
<div style="background-color:#464e5f;padding:10px;border-radius:5px;margin:10px;">
<h4 style="color:white;text-align:center;">{}</h4>
<h6>Author: {}</h6>
<h6>Date: {}</h6>
<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;width: 50px;height: 50px;border-radius: 50%;">
<br/>
<br/>
<p style="text-align:justify"> {}</p>
</div>
"""

# Set user agent for scraping
os.environ["USER_AGENT"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"

# Load environment variables (Optional)
load_dotenv()

# Initialize LLM (Replace API key with your own)
llm = ChatGroq(
    temperature=0,
    model_name="deepseek-r1-distill-qwen-32b",
    groq_api_key="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"
)

def clean_text(text):
    """ Clean and preprocess the scraped text """
    soup = BeautifulSoup(text, 'html.parser')
    text = soup.get_text()
    text = ' '.join(text.split())
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def parse_and_classify_news(url):
    """ Scrape, classify, and summarize news from a given URL """
    try:
        # Load and clean content
        loader = WebBaseLoader(url)
        page_data = loader.load().pop().page_content
        cleaned_data = clean_text(page_data)

        # Define prompt for AI processing
        prompt_extract = PromptTemplate.from_template("""
        ### SCRAPED TEXT FROM WEBSITE:
        {page_data}

        ### INSTRUCTION:
        Classify the news into these categories and subtypes:
        - Hard News: Breaking News, Politics, Business, Crime, International, Health, Environment, Sports
        - Soft News: Human Interest, Entertainment, Lifestyle, Tech, Science, Food, Education
        - Analysis: Interviews, Investigations, Opinion, Reviews
        - Market News: Economy, Startups, Digital Tech
        - Technical: Cybersecurity, Social Media, Product Launch
        - Local: Regional Events, Local Politics, Crime
        - Disaster News: Natural Disasters, Humanitarian Crises, Pandemics
        - Weather: Forecasts, Alerts
        - Political Opinion: Analysis, Debates
        - Celebrity & Gossip: Gossip, Red Carpet Events
        - Social Issues: Human Rights, Immigration, Editorials

        ### TASK:
        1. Extract **headline** of the news.
        2. Identify **Type and Subtype**.
        3. Detect relevant **State** and **Country**.
        4. Summarize in a **blog-friendly format**.

        Return only valid JSON with:
        - 'Type'
        - 'Subtype'
        - 'News Headline'
        - 'State'
        - 'Country'
        - 'Description'
        """)

        # Process with AI
        chain_extract = prompt_extract | llm
        response = chain_extract.invoke(input={'page_data': cleaned_data})
        json_parser = JsonOutputParser()
        return json_parser.parse(response.content)
    except Exception as e:
        return {"error": str(e)}

def create_streamlit_app():
    """ Streamlit app layout and functionality """
    st.set_page_config(
        layout="wide",
        page_title="NewsGenius | AI-Powered News Summarizer",
        page_icon="📰",
        initial_sidebar_state="expanded"
    )

    # Modern Blue & Black Styling
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] { 
            font-family: 'Poppins', sans-serif;
            background-color: #0a192f;
            color: #e0e7ff;
        }

        .stApp { 
            background: linear-gradient(135deg, #0a192f 0%, #112240 100%);
            padding: 2rem;
        }

        .header-section {
            text-align: center;
            padding: 2rem;
            background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
            color: white;
            border-radius: 12px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
            margin-bottom: 3rem;
        }

        .news-card {
            background-color: #112240;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            border: 1px solid #233554;
        }

        .headline {
            font-size: 2rem;
            font-weight: 700;
            color: #64ffda;
            margin-bottom: 1rem;
        }

        .description {
            font-size: 1.1rem;
            line-height: 1.8;
            color: #ccd6f6;
            margin-top: 1rem;
        }

        .stButton > button {
            width: 100%;
            padding: 0.8rem 1.5rem;
            font-size: 1.1rem;
            font-weight: 600;
            background:rgb(37, 66, 128);
            color: white;
            border-radius: 8px;
            transition: all 0.3s ease;
        }

        .stButton > button:hover {
            background:rgb(18, 36, 96);
            transform: scale(1.05);
        }

        .metadata {
            font-size: 1rem;
            color: #8892b0;
            margin-top: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header Section
    st.markdown("""
        <div class="header-section">
            <h1>📰 NewsGenius</h1>
            <p>Transform any news article into a structured, AI-generated blog post.</p>
        </div>
    """, unsafe_allow_html=True)

    # Input Section
    url_input = st.text_input("Enter News URL:", placeholder="Paste the link here...")

    col1, col2, col3 = st.columns([3, 4, 3])
    with col2:
        submit_button = st.button("✨ Generate Blog Post")

    # Process and Display Results
    if submit_button and url_input:
        with st.spinner("🔮 Analyzing article and generating blog post..."):
            result = parse_and_classify_news(url_input)

            if "error" in result:
                st.error(f"⚠️ Error processing article: {result['error']}")
            else:
                st.markdown(f"""
                    <div class="news-card">
                        <p><strong>{result['Type']}</strong> | <em>{result['Subtype']}</em></p>
                        <h1 class="headline">{result['News Headline']}</h1>
                        <p class="metadata">📍 {result['State']}, {result['Country']} | 📅 {datetime.now().strftime('%B %d, %Y')}</p>
                        <div class="description">{result['Description']}</div>
                    </div>
                """, unsafe_allow_html=True)

                with st.expander("📊 View Metadata"):
                    st.info(f"**Type:** {result['Type']}")
                    st.info(f"**Subtype:** {result['Subtype']}")
                    st.info(f"**Location:** {result['State']}, {result['Country']}")

                # Add a button to save the generated post to the database
                if st.button("💾 Save Post to Blog"):
                    add_post("AI Author", result['News Headline'], result['Description'], datetime.now().strftime('%Y-%m-%d'))
                    st.success("Post saved to blog successfully!")

    # Create a sidebar menu with different options
    menu = ["Home", "View Posts", "Add Post", "Search", "Manage"]
    choice = st.sidebar.selectbox("Menu", menu)

    # Display the selected option
    if choice == "Home":
        st.title("Welcome to my blog")
        st.write("This is a simple blog app built with streamlit and python.")
        st.write("You can view, add, search, and manage posts using the sidebar menu.")
        st.write("Enjoy!")

    elif choice == "View Posts":
        st.title("View Posts")
        st.write("Here you can see all the posts in the blog.")
        # Get all the posts from the database
        posts = get_all_posts()
        # Display each post as a card
        for post in posts:
            st.markdown(title_temp.format(post[1], post[0], post[2][:50] + "..."), unsafe_allow_html=True)
            # Add a button to view the full post
            if st.button("Read More", key=post[1]):
                st.markdown(post_temp.format(post[1], post[0], post[3], post[2]), unsafe_allow_html=True)

    elif choice == "Add Post":
        st.title("Add Post")
        st.write("Here you can add a new post to the blog.")
        # Create a form to get the post details
        with st.form(key="add_form"):
            author = st.text_input("Author")
            title = st.text_input("Title")
            content = st.text_area("Content")
            date = st.date_input("Date")
            submit = st.form_submit_button("Submit")
        # If the form is submitted, add the post to the database
        if submit:
            add_post(author, title, content, date)
            st.success("Post added successfully")

    elif choice == "Search":
        st.title("Search")
        st.write("Here you can search for a post by title or author.")
        # Create a text input to get the search query
        query = st.text_input("Enter your query")
        # If the query is not empty, search for the matching posts
        if query:
            # Get all the posts from the database
            posts = get_all_posts()
            # Filter the posts by the query
            results = [post for post in posts if query.lower() in post[0].lower() or query.lower() in post[1].lower()]
            # Display the results
            if results:
                st.write(f"Found {len(results)} matching posts:")
                for result in results:
                    st.markdown(title_temp.format(result[1], result[0], result[2][:50] + "..."), unsafe_allow_html=True)
                    # Add a button to view the full post
                    if st.button("Read More", key=result[1]):
                        st.markdown(post_temp.format(result[1], result[0], result[3], result[2]), unsafe_allow_html=True)
            else:
                st.write("No matching posts found")

    elif choice == "Manage":
        st.title("Manage")
        st.write("Here you can delete posts or view some statistics.")
        # Create a selectbox to choose a post to delete
        titles = [post[1] for post in get_all_posts()]
        title = st.selectbox("Select a post to delete", titles)
        # Add a button to confirm the deletion
        if st.button("Delete"):
            delete_post(title)
            st.success("Post deleted successfully")
        # Create a checkbox to show some statistics
        if st.checkbox("Show statistics"):
            # Get all the posts from the database
            posts = get_all_posts()
            # Convert the posts to a dataframe
            df = pd.DataFrame(posts, columns=["author", "title", "content", "date"])
            # Display some basic statistics
            st.write("Number of posts:", len(posts))
            st.write("Number of authors:", len(df["author"].unique()))
            st.write("Most recent post:", df["date"].max())
            st.write("Oldest post:", df["date"].min())
            # Display a bar chart of posts by author
            st.write("Posts by author:")
            author_count = df["author"].value_counts()
            st.bar_chart(author_count)

if __name__ == "__main__":
    create_streamlit_app()