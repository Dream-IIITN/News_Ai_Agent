import requests
import base64

wordpress_user = "bt22cse134"
wordpress_password = "@aiagentflipr"
wordpress_credentials = wordpress_user + ":" + wordpress_password
wordpress_token = base64.b64encode(wordpress_credentials.encode())
wordpress_token_decoded = wordpress_token.decode('utf-8')
wordpress_header = {'Authorization': 'Basic ' + wordpress_token_decoded}
print(wordpress_header)

def create_wordpress_post():
    api_url = 'https://ainews67.wordpress.com/wp-json/wp/v2/posts' 
    article_data = {
    "title": "My New Blog Post",  # Required: Title of the post
    "content": "This is the content of my new blog post. It can include <strong>HTML</strong> and <em>formatting</em>.",  # Required: Main content of the post
    "excerpt": "A short summary of the blog post.",  # Optional: Short summary or excerpt
    "status": "publish",  # Optional: Post status. Default is "draft". Options: "publish", "draft", "pending", "private"
    "slug": "my-new-blog-post",  # Optional: Custom URL slug. If not provided, WordPress generates one from the title
    "date": "2023-10-15T12:00:00",  # Optional: Publication date in ISO 8601 format. Default is the current date and time
    'meta': {  # Optional: Custom fields (metadata) for the post
            # Yoast SEO Fields
            '_yoast_wpseo_title': 'Example WordPress Post | SEO Title',  # SEO title template
            '_yoast_wpseo_metadesc': 'This is a meta description for my new blog post.',  # Meta description
            '_yoast_wpseo_focuskw': 'WordPress Post',  # Focus keyword
            '_yoast_wpseo_canonical': 'https://ainews67.wordpress.com/example-post',  # Canonical URL
            '_yoast_wpseo_meta-robots-noindex': '0',  # Index the post (0 = index, 1 = noindex)
            '_yoast_wpseo_meta-robots-nofollow': '0',  # Follow links (0 = follow, 1 = nofollow)
        },
    "comment_status": "open",  # Optional: Whether comments are allowed. Default is the site's default setting. Options: "open", "closed"
    "ping_status": "open",  # Optional: Whether pingbacks and trackbacks are allowed. Default is the site's default setting. Options: "open", "closed"
    "sticky": False,  # Optional: Whether the post should be sticky (pinned to the top of the blog). Default is False
    "template": "custom-template.php"  # Optional: Custom template for the post (if supported by the theme)
}
    response = requests.post(api_url, headers=wordpress_header, json=article_data)
    if response.status_code == 201:
        print("Post created successfully!")
        print("Post URL:", response.json().get('link'))  
    else:
        print("Failed to create the post.")
        print("Status Code:", response.status_code)
        print("Response:", response.json()) 
create_wordpress_post()
