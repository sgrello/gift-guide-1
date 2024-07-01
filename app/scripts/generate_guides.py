import openai
import requests
from bs4 import BeautifulSoup
import os

# Set up OpenAI API key
openai.api_key = 'your_openai_api_key'

# Amazon API credentials
amazon_api_key = 'your_amazon_api_key'
amazon_associate_tag = 'your_amazon_associate_tag'

# List of gift guides
gift_guides = [
    "best gifts for mothers",
    "best gifts for fathers",
    # Add more guides here
]

# Directory to save HTML files
output_directory = "../templates/gift_guides"  # Relative path to the app folder

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

def generate_gift_ideas(guide):
    prompt = f"Generate 50 popular gift ideas for {guide}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1500
    )
    gift_ideas = response.choices[0].text.strip().split("\n")
    return gift_ideas

def generate_meta_description(guide):
    prompt = f"Generate a meta description for a gift guide titled '{guide}'"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50
    )
    meta_description = response.choices[0].text.strip()
    return meta_description

def generate_meta_keywords(guide):
    prompt = f"Generate meta keywords for a gift guide titled '{guide}'"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50
    )
    meta_keywords = response.choices[0].text.strip().split(", ")
    return meta_keywords

def generate_on_screen_description(guide):
    prompt = f"Generate an on-screen description in a playful tone for a gift guide titled '{guide}'"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    on_screen_description = response.choices[0].text.strip()
    return on_screen_description

def fetch_product_info(product_name):
    search_url = f"https://api.amazon.com/products?search={product_name}&apikey={amazon_api_key}&associate_tag={amazon_associate_tag}"
    response = requests.get(search_url)
    product_info = response.json()
    return product_info

def generate_html(guide, gift_ideas, meta_description, meta_keywords, on_screen_description, products):
    # Template HTML structure
    html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{meta_description}">
    <meta name="keywords" content="{meta_keywords}">
    <style>
        /* Include your CSS styles here */
        body {{
            font-family: 'Roboto', sans-serif;
            margin: 0;
            background-color: #f4f4f9;
            color: #333;
            line-height: 1.6;
        }}
        .nav {{
            width: 100%;
            background-color: #007bff;
            padding: 10px 20px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            box-sizing: border-box;
        }}
        .nav .logo {{
            font-size: 24px;
            font-weight: bold;
            color: white;
            text-decoration: none;
        }}
        .nav .nav-links {{
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        .nav a {{
            color: white;
            padding: 10px 15px;
            text-decoration: none;
        }}
        .nav a:hover {{
            background-color: #0056b3;
            border-radius: 5px;
        }}
        .header {{
            background-color: #007bff;
            color: white;
            padding: 60px 20px;
            text-align: center;
            box-sizing: border-box;
        }}
        .header h1 {{
            font-size: 36px;
            margin: 0;
        }}
        .header p {{
            font-size: 18px;
            margin: 10px 0 0;
        }}
        .container {{
            max-width: 1200px;
            margin: 20px auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            box-sizing: border-box;
        }}
        .product-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }}
        .product {{
            background-color: #fff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            text-align: center;
        }}
        .product img {{
            max-width: 100%;
            height: auto;
            margin-bottom: 10px;
        }}
    </style>
</head>
<body>
    <div class="nav">
        <a href="index.html" class="logo">GiftScout</a>
        <div class="nav-links">
            <a href="index.html">Home</a>
            <a href="gift_guides.html">Gift Guides</a>
            <a href="about.html">About</a>
            <a href="contact.html">Contact</a>
        </div>
    </div>
    <div class="header">
        <h1>{title}</h1>
        <p>{on_screen_description}</p>
    </div>
    <div class="container">
        <div class="product-grid">
            {products_html}
        </div>
    </div>
</body>
</html>
    """

    # Generate HTML for each product
    products_html = ""
    for product in products:
        product_html = f"""
        <div class="product">
            <h2>{product['name']}</h2>
            <img src="{product['image']}" alt="{product['name']}">
            <a href="{product['url']}">View on Amazon</a>
        </div>
        """
        products_html += product_html

    # Fill in the template with the actual content
    html_content = html_template.format(
        title=guide,
        meta_description=meta_description,
        meta_keywords=", ".join(meta_keywords),
        on_screen_description=on_screen_description,
        products_html=products_html
    )
    return html_content

# Main loop to create webpages
for guide in gift_guides:
    gift_ideas = generate_gift_ideas(guide)
    meta_description = generate_meta_description(guide)
    meta_keywords = generate_meta_keywords(guide)
    on_screen_description = generate_on_screen_description(guide)
    products = [fetch_product_info(idea) for idea in gift_ideas]
    html_content = generate_html(guide, gift_ideas, meta_description, meta_keywords, on_screen_description, products)
    
    file_name = f"{guide.replace(' ', '_')}.html"
    file_path = os.path.join(output_directory, file_name)
    
    with open(file_path, "w") as file:
        file.write(html_content)
