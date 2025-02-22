from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient

# OAuth 2.0 credentials
client_id = "client_id"
client_secret = "client_secret"
token_url = "https://wordpress-site.com/oauth/token"

# Create an OAuth 2.0 session
client = BackendApplicationClient(client_id=client_id)
oauth = OAuth2Session(client=client)
token = oauth.fetch_token(token_url=token_url, client_id=client_id, client_secret=client_secret)

# Use the access token in the header
wordpress_header = {'Authorization': f'Bearer {token["access_token"]}'}

# Function to create a WordPress post
def create_wordpress_post(news_data):
    api_url = 'https://wordpress.com/wp-json/wp/v2/posts'  # Replace with your WordPress site URL
    
    # Prepare article data
    article_data = {
        "title": news_data.get("News Headline", "Untitled Post"),  # Use the news headline as the title
        "content": news_data.get("Description", "No content available."),  # Use the description as the content
        "excerpt": news_data.get("Description", "No excerpt available."),  # Use the description as the excerpt
        "status": "publish",  # Publish the post immediately
        "slug": news_data.get("News Headline", "").lower().replace(" ", "-"),  # Generate slug from the headline
        "meta": {  # Yoast SEO fields
            "_yoast_wpseo_title": news_data.get("News Headline", "Untitled Post"),
            "_yoast_wpseo_metadesc": news_data.get("Description", "No description available."),
            "_yoast_wpseo_focuskw": news_data.get("Type", "News"),
            "_yoast_wpseo_canonical": f"https://ainews67.wordpress.com/{news_data.get('News Headline', '').lower().replace(' ', '-')}",
            "_yoast_wpseo_meta-robots-noindex": "0",
            "_yoast_wpseo_meta-robots-nofollow": "0",
        },
        "comment_status": "closed",  # Disable comments
        "ping_status": "closed",  # Disable pingbacks
        "sticky": False,  # Not a sticky post
    }

    # Send POST request to create the post
    response = requests.post(api_url, headers=wordpress_header, json=article_data)
    
    # Check the response
    if response.status_code == 201:
        return response.json().get("link")  # Return the URL of the created post
    else:
        return None

# Streamlit UI
def create_streamlit_app():
    st.set_page_config(layout="wide", page_title="News Output Generator")
    st.title("News Output Generator")

    url_input = st.text_input("Enter a News Article URL:")
    submit_button = st.button("Submit")

    if submit_button and url_input:
        with st.spinner("Processing..."):
            # Parse and classify the news
            news_data = parse_and_classify_news(url_input)
            
            # Display the parsed news data
            st.subheader("Parsed News Data")
            st.json(news_data)

            # Publish the news to WordPress
            if "error" not in news_data:
                post_url = create_wordpress_post(news_data)
                if post_url:
                    st.success(f"Post created successfully! [View Post]({post_url})")
                else:
                    st.error("Failed to create the post.")
            else:
                st.error(news_data["error"])
