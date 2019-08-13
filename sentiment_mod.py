# -*- coding: utf-8 -*-
import nltk
import random
import pickle

from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize


class VoteClassifier(ClassifierI):  # VoteClassifier uses ClassifierI to develop a new classifier

    def __init__(self, *classifiers):  # classifiers used for voting - LinearSVC, Naive Bayes, NuSVC classifiers
        self._classifiers = classifiers
        
    def classify(self, features):  # classifiers are used to classify each text and returns the mode of votes
        votes=[]
        for c in self._classifiers: #iterating over all classifiers to get its vote
            v = c.classify(features)
            votes.append(v)
        return mode(votes)   # returning mode of the votes
    
    def confidence(self,features):  # find the confidence of the vote calculated-
        # if neg with 1.0 confidence text termed as negative
        # elsif pos with 1.0 confidence text termed as positive
        # else text termed as neutral
        votes=[]
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
            
        choice_votes= votes.count(mode(votes))
        # calculating confidence of votes given by each classifier
        conf= choice_votes/len(votes)
        return conf
    
# text files for training classifiers
short_pos = open("short_reviews/positive.txt", "r").read()
short_neg = open("short_reviews/negative.txt", "r").read()

documents= []
all_words = []

#  j is adject, r is adverb, and v is verb
#allowed_word_types = ["J","R","V"]
allowed_word_types = ["J"]  # adjects are most important for sentiment analysis hence choosing them

for p in short_pos.split('\n'):   # spliting positive texts
     documents.append( (p, "pos") )
     words = word_tokenize(p)  # tokenizing reviews and tokenizing words
     pos = nltk.pos_tag(words)  # list of positive words
     for w in pos:
         if w[1][0] in allowed_word_types:
             all_words.append(w[0].lower())  # list of all words - positive and negative adjectives


for p in short_neg.split('\n'):
     documents.append((p, "neg"))
     words = word_tokenize(p)
     pos = nltk.pos_tag(words)
     for w in pos:
         if w[1][0] in allowed_word_types:
             all_words.append(w[0].lower())



for r in short_pos.split('\n'):   # adding positive texts
     documents.append((r, "pos"))


for r in short_neg.split('\n'):  # adding negative texts
     documents.append((r, "neg"))


# tokenizing words for negative and positive reviews

short_pos_words = word_tokenize(short_pos)
short_neg_words = word_tokenize(short_neg)


# for w in short_pos_words:
#      all_words.append(w.lower())
#
# for w in short_neg_words:
#      all_words.append(w.lower())
# all_words= nltk.FreqDist(all_words)

# save_allWords = open("allWords.pickle","wb")    #saving all_words using pickle.#
# pickle.dump(all_words,save_allWords)
# save_allWords.close()

all_words_f=open("Pickled files/allWords.pickle", "rb")   # using pickle to open a previously saved classifier
all_words=pickle.load(all_words_f)
all_words_f.close()



#word_features= list(all_words.keys())[:5000]

# save_word_features = open("word_features.pickle","wb")    #saving word_features using pickle.
# pickle.dump(word_features,save_word_features)
# save_word_features.close()

word_features_f=open("Pickled files/word_features.pickle", "rb")   # using pickle to open a previously saved classifier
word_features=pickle.load(word_features_f)
word_features_f.close()



def find_features(documents):
    '''Finds features of texts from word tokens '''
    words=word_tokenize(documents)
    features={}
    for w in word_features:
       features[w]= (w in words)
    return features


# save_find_features=open("Pickled files/find_features.pickle","wb")
# pickle.dump(find_features,save_find_features)
# save_find_features.close()

# find_features_f= open("find_features.pickle", "rb")
# find_features=pickle.load(find_features_f)
# find_features_f.close()

#featuresets=[(find_features(rev),category) for (rev, category) in documents]

# save_featuresets = open("featuresets.pickle","wb")    #saving featuresets using pickle.
# pickle.dump(featuresets,save_featuresets)
# save_featuresets.close()

featuresets_f=open("Pickled files/featuresets.pickle", "rb")   # using pickle to open a previously saved classifier
featuresets=pickle.load(featuresets_f)
featuresets_f.close()


random.shuffle(featuresets)    # shuffle featuresets for better training and testing
#print(len(featuresets))

training_set=featuresets[:10000]      #training testing split
testing_set=featuresets[10000:]


#classifier=nltk.NaiveBayesClassifier.train(training_set) #nltk Naive Bayes
classifier_f=open("Pickled files/NaiveBayes.pickle", "rb")   # using pickle to open a previously saved classifier
classifier=pickle.load(classifier_f)
classifier_f.close()



#print("Original Naive bayes accuracy is:",(nltk.classify.accuracy(classifier,testing_set))*100)


#classifier.show_most_informative_features(15)



# save_classifier = open("NaiveBayes.pickle","wb")    #saving a classifier using pickle.
# pickle.dump(classifier,save_classifier)
# save_classifier.close()




# LinearSVC_classifier= SklearnClassifier(LinearSVC())
# LinearSVC_classifier.train(training_set)

classifier_f=open("Pickled files/LinearSVC_classifier.pickle", "rb")   # using pickle to open a previously saved classifier
LinearSVC_classifier=pickle.load(classifier_f)
classifier_f.close()

#print("LinearSVC_classifier accuracy is:",(nltk.classify.accuracy(LinearSVC_classifier,testing_set))*100)

# save_LinearSVC = open("LinearSVC_classifier.pickle","wb")
# pickle.dump(LinearSVC_classifier, save_LinearSVC)
# save_LinearSVC.close()

#NuSVC_classifier= SklearnClassifier(NuSVC())
#NuSVC_classifier.train(training_set)

classifier_f=open("Pickled files/NuSVC_classifier.pickle", "rb")   # using pickle to open a previously saved classifier
NuSVC_classifier=pickle.load(classifier_f)
classifier_f.close()


#print("NuSVC_classifier accuracy is:",(nltk.classify.accuracy(NuSVC_classifier,testing_set))*100)

# save_NuSVC = open("NuSVC_classifier.pickle","wb")
# pickle.dump(NuSVC_classifier, save_NuSVC)
# save_NuSVC.close()


# VoteClassifier class instance uses Naive Bayes, NuSVC and Linear SVC classifier (SVC -State Vector Classification)
voted_classifier = VoteClassifier(classifier,
                                  NuSVC_classifier,
                                  LinearSVC_classifier
                                 )


def sentiment(text):
    """
    method used to find the sentiment of a string
    :param text: string as an input whose sentiment has to be computed
    :return: pos , neg or neutral is returned
    """
    feats = find_features(text)   # using find_features method to find features in text
    vote = voted_classifier.classify(feats)  # calculating vote
    conf = voted_classifier.confidence(feats)  # calculating confidence for vote given
    if conf != 1.0:  # using confidence to classify neutral texts
        vote = "neutral"

    return vote

