from flask import Flask, render_template, request
from src.extensions import es
from src.retrieve_tweet import search_tweets
import os
import logging

# Log transport
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)


@app.route('/')
def main():
    # Render template
    return render_template('index.html')


@app.route('/', methods=['POST'])
def get_tweet_words():
    query = request.form['tweet_words']
    # How to persis same connection through-out the app?
    # https://stackoverflow.com/questions/55523299/best-practices-for-persistent-database-connections-in-python-when-using-flask
    es.init_app(app)
    tweet = search_tweets(query)
    # Send to html
    return render_template('index.html', tweet=tweet)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
