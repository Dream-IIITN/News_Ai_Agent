from langchain.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate
from langchain.chat_models import ChatGroq
import json

# Initialize LLM
llm = ChatGroq(model="deepseek-r1-distill-qwen-32b", api_key="YOUR_GROQ_API_KEY")

# Function to process news article
def parse_and_classify_news(url):
    # Load webpage content
    loader = WebBaseLoader(url)
    page_data = loader.load()[0].page_content  

    # LLM Prompt
    prompt_extract = PromptTemplate.from_template("""
        ###SCRAPED TEXT WEBSITE:
        {page_data}
        ###INSTRUCTION:
        Classify the news under the given categories, extract headline, type, subtype, location (Region, State, Country), and generate a short blog-style summary. Return valid JSON:
        ###VALID JSON (NO PREAMBLE):
    """)
    
    chain_extract = prompt_extract | llm
    res = chain_extract.invoke(input={'page_data': page_data})
    
    # Parse and return JSON response
    return json.loads(res.content)

# Example usage
news_json = parse_and_classify_news("https://example.com/news-article")
print(news_json)
