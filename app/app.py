# API imports
from flask import Flask, request
import flask_monitoringdashboard as dashboard
from config import Config
from config import DevelopmentConfig


# helpers
import sys
import joblib
from pymagnitude import *


sys.path.append('..')

#external scripts imports for prediction purposes
from src.utils import load_books, predict_sentiment, predict_toxicity, get_embedding, get_information, check_user_input_information, check_user_input_prediction, check_user_input_similarity,check_user_input_sum,  get_most_similar_words, get_words_sum


#here the configurations of the Flask API are set
app = Flask(__name__)

#bind the API to a dashboard
dashboard.bind(app)

#set configurations
developmentconfigurations=DevelopmentConfig()
app.config['DEBUG']=developmentconfigurations.DEBUG

#load the prediction models
clf_toxicity = joblib.load('../src/models/toxicity.joblib')
clf_sentiment = joblib.load('../src/models/sentiment.joblib')

#load the embedding and sentences of the books
books_dict = load_books()

#load the word_to_vec space
vectors_word_to_vec = Magnitude("../src/models/GoogleNews-vectors-negative300.magnitude.1")
vectors_fasttest = Magnitude("../src/models/wiki-news-300d-1M-subword.magnitude")


# endpoint to obtain result of words sum
@app.route('/get_words_arithmetic',  methods=["POST"])
def words_sum():

    #get the input from the user
    content=request.get_json()

    #check request correctness
    check = check_user_input_sum(content)


    if check:

        #get the word
        positive_word_1 = content['positive_word_1']
        positive_word_2 = content['positive_word_2']
        negative_word = content['negative_word']

        #get the most similar words
        words = get_words_sum(positive_word_1, positive_word_2, negative_word, vectors_fasttest)

        return {'word':words}
    
    else:

        return {'word': 'Your request is wrong. Check the request format!'}

# endpoint to obtain the similarity between two sentences
@app.route('/get_similar_words',  methods=["POST"])
def similarity_prediction():

    #get the input from the user
    content=request.get_json()

    #check request correctness
    check = check_user_input_similarity(content)


    if check:

        #get the word
        word = content['word']

        #get the most similar words
        words = get_most_similar_words(word, vectors_word_to_vec)

        return {'similar_words':words}
    
    else:

        return {'similar_words': 'Your request is wrong. Check the request format!'}


# endpoint to obtain the sentiment of sentence
@app.route('/get_sentiment',  methods=["POST"])
def sentiment_prediction():

    #get the input from the user
    content=request.get_json()

    #check request correctness
    check = check_user_input_prediction(content)

    if check:

        #get sentence
        sentence = content['sentence']

        #get the vector embedding representation of the sentences
        embeddings = get_embedding([sentence])

        #predict the sentence sentiment by loading the sentiment prediction model
        response = predict_sentiment(embeddings, clf_sentiment)


        return {'sentiment': response}
    
    else:

        return {'sentiment': 'Your request is wrong. Check the request format!'}


# enpoint to obtain the toxicity of a sentence
@app.route('/get_toxicity', methods=["POST"])
def toxicity_prediction():

    #get the input from the user
    content=request.get_json()

    #check request correctness
    check = check_user_input_prediction(content)

    if check:

        #get sentence
        sentence = content['sentence']

        #get the vector embedding representation of the sentences
        embeddings = get_embedding([sentence])

        #predict the sentence sentiment by loading the toxicity prediction model
        response = predict_toxicity(embeddings, clf_toxicity)

        return {'toxicity':response}
    
    else:

        return {'toxicity': 'Your request is wrong. Check the request format!'}


# endpoint to obtain the information from a book
@app.route('/get_information', methods=["POST"])
def information_book():

    #get the input from the user
    content=request.get_json()

    #check request correctness
    check = check_user_input_information(content)

    if check:

        #get sentence and book
        sentence = content['request']
        book_name = content['book']

        #get the vector embedding representation of the sentences
        embeddings = get_embedding([sentence])

        #get the 5 most relevant sentences from the book which contain the information required

        response = get_information(embeddings, book_name, books_dict)

        return {'sentence':response}
    
    else:

        return {'sentence': 'Your request is wrong. Check the request format!'}


if __name__ == '__main__':

    #set threaded to True to handle multiple queries
    app.run(threaded=True)
