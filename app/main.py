import streamlit as st
import json
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq 
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from utils import clean_text  # Ensure this is correctly implemented
# Initialize LLM
llm = ChatGroq(temperature=0,model_name="deepseek-r1-distill-qwen-32b", groq_api_key="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")

# Function to process news article
def parse_and_classify_news(url):
    try:
        # Load webpage content
        loader = WebBaseLoader(url)
        page_data = loader.load().pop().page_content
        cleaned_data = clean_text(page_data)  # Ensure this function is implemented correctly
        
        # LLM Prompt
        prompt_extract = PromptTemplate.from_template("""
        ### SCRAPED TEXT WEBSITE:
        {page_data}
        ### INSTRUCTION:
        The scraped text is from an official news website.
        First, read and understand the content and classify them under the following types and subtypes.
        Here is the list to help you. Make sure to classify news among them.

        Type: Hard News
        Subtypes:
        - Breaking News
        - Political News
        - Business News
        - Crime News
        - International News
        - Health News
        - Environmental News
        - Sports News

        Type: Soft News
        Subtypes:
        - Human Interest Stories
        - Entertainment News
        - Lifestyle News
        - Technology News
        - Science News
        - Cultural News
        - Food News
        - Education News
        - Feature News

        Type: Analysis
        Subtypes:
        - Interviews
        - Investigative Journalism
        - Opinion Pieces/Editorials
        - Reviews
        - Business & Financial News

        Type: Stock Market News
        Subtypes:
        - Economy News
        - Startups and Entrepreneurship News
        - Technology & Digital News

        Type: Technical Aspects
        Subtypes:
        - Cybersecurity News
        - Social Media News
        - Launch News 

        Type: Local News
        Subtypes:
        - Regional/Local Events
        - Local Politics
        - Local Crime

        Type: Disaster and Crisis News
        Subtypes:
        - Natural Disasters
        - Humanitarian Crises
        - Pandemics/Health Crises

        Type: Weather News
        Subtypes:
        - Forecasting
        - Severe Weather Alerts

        Type: Political Opinion & Commentary
        Subtypes:
        - Political Analysis
        - Political Debates

        Type: Celebrity & Gossip News
        Subtypes:
        - Celebrity Gossip
        - Red Carpet Events

        Type: Social & Public Issues News
        Subtypes:
        - Social Justice
        - Human Rights
        - Immigration
        - Opinion & Editorials
        - Columnists
        - Letters to the Editor

        Your job is to:
        1. Extract the **headline of the news**.
        2. Identify the **Type and Subtype** of news among the mentioned categories.
        3. Find the **State** and **Country** where the news is relevant.
        4. Summarize it into a **short blog-friendly description**.

        Return the result in **valid JSON format** with the following keys:
        - 'Type'
        - 'Subtype'
        - 'News Headline'
        - 'State'
        - 'Country'
        - 'Description'

        Ensure that only a **valid JSON** response is returned without any extra text.
        """)

        # Invoke LLM
        chain_extract = prompt_extract | llm
        response = chain_extract.invoke(input={'page_data': cleaned_data})
        json_parser = JsonOutputParser()
        jres = json_parser.parse(response.content)
        # Parse JSON response safely
        try:
            return jres
        except json.JSONDecodeError:
            return {"error": "Invalid JSON received from LLM"}
    except Exception as e:
        return {"error": str(e)}

# Streamlit UI
def create_streamlit_app():
    st.set_page_config(layout="wide", page_title="News Output Generator")
    st.title("News Output Generator")

    url_input = st.text_input("Enter a News Article URL:")
    submit_button = st.button("Submit")

    if submit_button and url_input:
        with st.spinner("Processing..."):
            output = parse_and_classify_news(url_input)
            st.json(output)  # Display structured JSON output in Streamlit UI

# Run Streamlit app
if __name__ == "__main__":
    create_streamlit_app()
