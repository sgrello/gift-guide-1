




from flask import render_template, request, url_for
from app import app
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_search_phrases(details):
    prompt = (
        f"Based on the following details: {details}, suggest 5 highly relevant and specific search phrases "
        f"to find gift items on Amazon. Consider the recipient's interests and preferences. "
        f"Each search phrase/gift idea should be a specific product that someone would search for on Amazon but avoid using too specific brand names or things of that sort. "
        f"Avoid too many similar suggestions and focus on things that relate to the details as well as broader things that that type of person would also be interested in. The final output should just be simple search terms for the items and nothing more."
    )
    
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful gift idea assistant specializing in finding gifts on Amazon."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150 * 10,  # Adjust max_tokens based on the number of ideas requested
        temperature=0.7
    )

    # Split the content into lines and strip any leading/trailing whitespace
    search_phrases = [line.strip() for line in response.choices[0].message.content.strip().split('\n') if line.strip()]
    
    return search_phrases




@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['GET'])
def recommend():
    details = request.args.get('details', '')
    search_phrases = generate_search_phrases(details)
    products = [{'title': phrase} for phrase in search_phrases]
    return render_template('recommendations.html', products=products)


@app.route('/gift_guide_collection')
def gift_guide_collection():
    return render_template('gift_guide_collection.html')


@app.route('/guide_for_him')
def guide_for_him():
    return render_template('guide_for_him.html')

@app.route('/guide_for_her')
def guide_for_her():
    return render_template('guide_for_her.html')