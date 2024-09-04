from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Example scraping YouTube (Title and view count of a video)
def scrape_youtube(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('meta', {'name': 'title'})['content']
    views = soup.find('meta', {'itemprop': 'interactionCount'})['content']
    return {"title": title, "views": views}

# Example scraping Amazon (Product title and price)
def scrape_amazon(url):
    headers = {"User-Agent": "Your User Agent"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find(id='productTitle').get_text(strip=True)
    price = soup.find('span', {'class': 'a-offscreen'}).get_text()
    return {"title": title, "price": price}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    youtube_url = request.form.get('youtube_url')
    amazon_url = request.form.get('amazon_url')

    youtube_data = scrape_youtube(youtube_url)
    amazon_data = scrape_amazon(amazon_url)

    return render_template('results.html', youtube=youtube_data, amazon=amazon_data)

if __name__ == '__main__':
    app.run(debug=True)
