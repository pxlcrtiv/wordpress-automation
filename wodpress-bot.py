import requests
from langchain.llms import Gemini
import click

# Function to generate blog content
def generate_blog_content(sentence, llm):
    """
    Generates blog content using a given sentence and LLM.

    Args:
        sentence (str): The input sentence for the blog post.
        llm: The LLM model used for generating content.

    Returns:
        str: The generated blog content.
    """
    response = llm(sentence)
    return response

# Function to create a WordPress post
def create_post(wp_url, headers, title, content):
    """
    Creates a WordPress post using the provided information.

    Args:
        wp_url (str): The WordPress API URL for creating posts.
        headers (dict): Headers for the API request, including authorization.
        title (str): The title of the blog post.
        content (str): The content of the blog post.

    Returns:
        requests.Response: The response from the WordPress API.
    """
    data = {
        'title': title,
        'content': content,
        'status': 'draft',  # Set to 'publish' to publish immediately
        'categories': [1],  # Replace with your category IDs
        'tags': [2, 3]      # Replace with your tag IDs
    }
    response = requests.post(wp_url + '/wp-json/wp/v2/posts', headers=headers, json=data)
    return response

@click.command()
@click.option('--gemini-api-key', prompt="Enter your Gemini API key", hide_input=True, confirmation_prompt=True)
@click.option('--wordpress-api-key', prompt="Enter your WordPress API key", hide_input=True, confirmation_prompt=True)
@click.option('--wordpress-url', prompt="Enter your WordPress URL")
def main(gemini_api_key, wordpress_api_key, wordpress_url):
    """
    Creates a WordPress blog post using Gemini.

    This script prompts the user for their Gemini and WordPress API keys, 
    WordPress URL, blog post title, and a sentence to generate content from.
    It then uses Gemini to generate blog content based on the provided sentence
    and creates a draft post on the specified WordPress site.
    """

    # Set up Gemini LLM
    llm = Gemini(api_key=gemini_api_key)

    # Set up WordPress headers
    headers = {
        'Authorization': f'Bearer {wordpress_api_key}',
        'Content-Type': 'application/json',
    }

    title = click.prompt("Enter your desired blog post title")
    sentence = click.prompt("Enter a sentence for the blog post")

    content = generate_blog_content(sentence, llm)

    response = create_post(wordpress_url, headers, title, content)

    if response.status_code == 201:
        click.echo("Blog post created successfully!")
    elif response.status_code == 401:
        click.echo("Unauthorized: Invalid API Key")
    elif response.status_code == 400:
        click.echo("Bad Request:", response.json())
    else:
        click.echo("Failed to create post:", response.status_code, response.json())

if __name__ == '__main__':
    main()
