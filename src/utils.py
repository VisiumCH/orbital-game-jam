#import helper libraries
import numpy as np
import pickle

#import BERT as a service API
from bert_serving.client import BertClient


def check_user_input_similarity(request_input):

    #check that the input is a dictionary

    if type(request_input) is dict:

        #check that the keys are correct
        if list(request_input.keys())[0]=='word':

            #check the input is a string

            if type(request_input['word']) is str:
                return True
            
            else:
                return False
            
        else:
            return False

    else:
        return False


def check_user_input_sum(request_input):

    #check that the input is a dictionary

    if type(request_input) is dict:

        #check that the keys are correct
        if list(request_input.keys())==['positive_word_1', 'positive_word_2', 'negative_word']:

            #check the input is a string
            if type(request_input['positive_word_1']) is str and type(request_input['positive_word_2']) is str and type(request_input['negative_word']) is str:
                return True
            
            else:
                return False
            
        else:
            return False

    else:
        return False

def check_user_input_prediction(request_input):

    #check that the input is a dictionary

    if type(request_input) is dict:

        #check that the keys are correct
        if list(request_input.keys())[0]=='sentence':

            #check the input is a string
            if type(request_input['sentence']) is str:
                return True
            
            else:
                return False
            
        else:
            return False

    else:
        return False


def check_user_input_information(request_input):

    #check that the input is a dictionary

    if type(request_input) is dict:

        #check that the keys are correct
        if list(request_input.keys())==['request', 'book']:

            #check the input is a string
            if type(request_input['request']) is str and type(request_input['book']) is str:
                return True
            
            else:
                return False
            
        else:
            return False

    else:
        return False

#function to predict the sentiment of a sentence given its embedding
def predict_sentiment(sentence_embedding, clf):

    #convert to list object
    emb_model = sentence_embedding.tolist()

    #predict the class of the sentence embedding
    pred = clf.predict(emb_model)

    # declare the sentiment classes dictionary
    classes_dict = {0: 'strongly negative',
                    1: 'negative',
                    2 : 'neutral',
                    3 : 'positive',
                    4 : 'strongly positive'}

    #retrieve the class string based on the integer prediction
    response = classes_dict[pred[0]]

    return response 

#function to predict the toxicity of a sentence given its embeddings
def predict_toxicity(sentence_embedding, clf):

    #convert to list object
    emb_model = sentence_embedding.tolist()

    #predict the class of the sentence embedding
    pred = clf.predict(emb_model)

    # obtain the indices of the multilabel classification task
    keys = np.where(pred[0]==1)[0]

    # declare the toxicity classes dictionary
    classes_dict = {0: 'toxic',
                    1: 'obscene',
                    2 : 'insult',
                    3 : 'identity hate'}

    # classify non-toxic sentence
    if len(keys)==0:

        response = 'non-toxic'
    
    # classify toxicity
    else:
        response = [classes_dict[toxicity_id] for toxicity_id in keys]

    return response

#function to obtain te embeddings of a sentence
def get_embedding(sentences_list):

    #initialize the bert client
    bc = BertClient()

    #compute the embeddings
    embeddings = bc.encode(sentences_list)

    return embeddings

#load the book embeddings and sentences
def load_books():

    paths=['../books/1984', '../books/dune', '../books/the_hobbit', '../books/mobydick', '../books/the_great_gatsby']
    names=['1984', 'dune', 'the_hobbit', 'moby_dick', 'the_great_gatsby']

    books_dict={}

    for path, name in zip(paths, names):

        #load the embeddings and sentences of the books
        book_emb = pickle.load(open(path+'_embeddings.pkl', 'rb'))
        book_sent = pickle.load(open(path+'_sentences.pkl', 'rb'))

        books_dict[name]=[book_emb, book_sent]
    
    return books_dict

#get the information of within a book
def get_information(sentence_embedding, book_name, books_dict):

    #handle input errors
    try:
        book_source = books_dict[book_name]
    except:
        return 'You have entered the wrong book name'
    
    #convert to list object
    emb_model = sentence_embedding.tolist()

    # compute normalized dot product as score
    score = np.sum(emb_model * book_source[0], axis=1) / np.linalg.norm(book_source[0], axis=1)

    #get the indices of the top 5 answers
    topk_idx = np.argsort(score)[::-1][0]

    #get the list of the most appropriate information retrieved from the book
    response = book_source[1][topk_idx]

    return response

#get the n most similar words to the one given
def get_most_similar_words(word, vectors):

    #get the most similar words to the one given
    sims=vectors.most_similar(word, topn = 5) 

    #obtain the words and discard the similarity score
    response=[s[0] for s in sims]

    return response

#get words arithmentic result
def get_words_sum(positive_word_1, positive_word_2, negative_word, vectors):

    #get the options of the word sum
    words_sum = vectors.most_similar(positive = [positive_word_1, positive_word_2], negative=[negative_word], topn = 1)

    #obtain the words and discard the similarity score
    response=words_sum[0][0]

    return response


    


