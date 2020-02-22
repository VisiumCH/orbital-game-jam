# API imports
from flask import Flask, request, abort
import flask_monitoringdashboard as dashboard
from config import Config
from config import DevelopmentConfig, ProductionConfig


# helpers
import sys
import joblib


sys.path.append('..')

#external scripts imports for prediction purposes
from src.utils import load_books, predict_sentiment, predict_toxicity, get_embedding, get_information, check_user_input_information, check_user_input_prediction


#here the configurations of the Flask API are set
app = Flask(__name__)

#bind the API to a dashboard
dashboard.bind(app)

#set configurations
productionconfigurations=ProductionConfig()
app.config['DEBUG']=productionconfigurations.DEBUG

#load the prediction models
clf_toxicity = joblib.load('../src/models/toxicity.joblib')
clf_sentiment = joblib.load('../src/models/sentiment.joblib')

#load the embedding and sentences of the books
books_dict = load_books()


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

        abort(400)


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

        abort(400)


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

        abort(400)


if __name__ == '__main__':

    #set threaded to True to handle multiple queries
    app.run(threaded=True, host='0.0.0.0', port=3000)
