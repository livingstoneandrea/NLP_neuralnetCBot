# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 08:36:39 2021

@author: livin
"""
import nltk
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
import json
import pickle
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
#from keras.layers import Sequential
from keras.layers import Dense, Activation,Dropout
from keras.optimizers import SGD
import random


words = []
classes = []
documents = []
ignore_words = ['?', '!',',']

data_file = open('intents.json').read()
print("data file loaded\n %s" %data_file)
intents = json.loads(data_file)

print("intent: {}\n".format(intents))

for intent in intents['intents']:
    for pattern in intent['pattern']:
        print("pattern: {}\n".format(pattern))

        #tokenize each word
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        #add document in the corpus
        documents.append((w, intent['tag']))
    #add to our classes list
    if intent['tag'] not in classes:
        classes.append(intent['tag'])
            
#lemmatize, lower each word and remove duplicates
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))

#sorted classes
classes = sorted(list(set(classes)))

print(len(documents))

print(len(classes), "classes", classes)

print(len(words), "unique lemmatized words", words)
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

#create trining data
training = []

output_empty = [0] * len(classes)

#training bag of words for each sentences
for doc in documents:
    bag = []
    pattern_words = doc[0]
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)
        output_row = list(output_empty)
        output_row[classes.index(doc[1])] = 1
        training.append([bag, output_row])
#shuffle our features and turn into numpy array
random.shuffle(training)
training = np.array(training)

#create trainig and test lists.X - pattern, Y- intents

train_x = list(training[:,0])
train_y = list(training[:,1])

print("Training data created")

#print("train x ", train_x)
#print("triain y", train_y)
#build the model

model = keras.Sequential()
model.add(Dense(128, input_shape=[len(train_x[0])], activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

#compile the model Stochastic Gradient Descent with Nesterov
sgd = SGD(lr=0.01, decay=1e-6, momentum= 0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

#fitting and saving the model
hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=True)
model.save('chatbot_model.h5', hist)
print("model created")


        
        



            