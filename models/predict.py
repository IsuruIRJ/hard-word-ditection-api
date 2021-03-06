import nltk
from nltk.stem.lancaster import LancasterStemmer
import os
import json
import datetime
from flask_restful import Api, Resource
from flask import request
# from sklearn import datasets
# from sklearn import svm
# import json
# use natural language toolkit

class Predict(Resource):
    def post(self,data,feed):    
 
        stemmer = LancasterStemmer()

        # 2 classes of training data
        training_data = []
        training_data.append({"class":"easy", "sentence":"this"})
        training_data.append({"class":"easy", "sentence":"is"})        

        for val in data:
            training_data.append({"class":"hard", "sentence":val})
            print(val)


        # print ("%s sentences in training data" % len(training_data))


        # organize data structure for documents, classes and words

        words = []
        classes = []
        documents = []
        ignore_words = ['?']
        # loop through each sentence in our training data
        for pattern in training_data:
            # tokenize each word in the sentence
            w = nltk.word_tokenize(pattern['sentence'])
            # add to our words list
            words.extend(w)
            # add to documents in our corpus
            documents.append((w, pattern['class']))
            # add to our classes list
            if pattern['class'] not in classes:
                classes.append(pattern['class'])

        # stem and lower each word and remove duplicates
        words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
        words = list(set(words))


        # matrix multiplication and sigmoid function to normalize values

        import numpy as np
        import time

        # compute sigmoid nonlinearity
        def sigmoid(x):
            output = 1/(1+np.exp(-x))
            return output

        # convert output of sigmoid function to its derivative
        def sigmoid_output_to_derivative(output):
            return output*(1-output)
        
        def clean_up_sentence(sentence):
            # tokenize the pattern
            sentence_words = nltk.word_tokenize(sentence)
            # stem each word
            sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
            return sentence_words

        # return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
        def bow(sentence, words, show_details=False):
            # tokenize the pattern
            sentence_words = clean_up_sentence(sentence)
            # bag of words
            bag = [0]*len(words)  
            for s in sentence_words:
                for i,w in enumerate(words):
                    if w == s: 
                        bag[i] = 1
                        if show_details:
                            print ("found in bag: %s" % w)

            return(np.array(bag))

        def think(sentence, show_details=False):
            x = bow(sentence.lower(), words, show_details)
            if show_details:
                print ("sentence:", sentence, "\n bow:", x)
            # input layer is our bag of words
            l0 = x
            # matrix multiplication of input and hidden layer
            l1 = sigmoid(np.dot(l0, synapse_0))
            # output layer
            l2 = sigmoid(np.dot(l1, synapse_1))
            return l2



        # probability threshold
        ERROR_THRESHOLD = 0.2
        # load our calculated synapse values
        synapse_file = 'synapses.json' 
        with open(synapse_file) as data_file: 
            synapse = json.load(data_file) 
            synapse_0 = np.asarray(synapse['synapse0']) 
            synapse_1 = np.asarray(synapse['synapse1'])

        def classify(sentence, show_details=False):
            results = think(sentence, show_details)

            results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD ] 
            results.sort(key=lambda x: x[1], reverse=True) 
            return_results =[[classes[r[0]],r[1]] for r in results]
            print ("%s \n classification: %s" % (sentence, return_results))
            return return_results

        classify("this")
        hard_words = []
        for val in feed:
            prediction = classify(val, show_details=True)
            if(prediction[0][0] == "hard"):
                hard_words.append(val)

        print(hard_words, "identified hard words")

        return hard_words
