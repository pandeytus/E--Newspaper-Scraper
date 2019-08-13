from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph, PageBreak
from reportlab.lib.styles import ParagraphStyle
import pymongo
import re
import datetime
import pandas as pd
import os
import nltk
import heapq
import sentiment_mod as s
from googletrans import Translator
from langdetect import detect


def summarize():
    """
    summarize method for deducing crisp of the complete article text. Using nltk and heapq libraries
    :return: string -  summary of the article as a string variable
    """
    formatted_news = re.sub(r'\s+', ' ', rows.Article)  # removing extra space
    sentence_list = nltk.sent_tokenize(rows.Article)  # tokenizing paragraphs by sentences, i.e.
    # sentence tokenizing for later adding in the result
    stopwords = nltk.corpus.stopwords.words('english')  # adding english stopwords to a variable

    word_frequencies = {}   # dictionary to store words with their frequency i.e. , the number of times they appear
    for word in nltk.word_tokenize(formatted_news):  # iterating over tokenized words
        if word not in stopwords:   # check for excluding english stopwords
            if word not in word_frequencies.keys():   # if word not already present in word frequency dictionary key
                word_frequencies[word] = 1    # frequency of word set to 1
            else:
                word_frequencies[word] += 1    # if word already present in key increment its frequency by 1
            maximum_frequency = max(word_frequencies.values())
        for words in word_frequencies.keys():
            word_frequencies[words] = (word_frequencies[words]/maximum_frequency)
    sentence_scores = {}      # scores of the sentences present in article greater the score more important it is to the article
    for sent in sentence_list:  # iterating over tokenized sentences
        for word in nltk.word_tokenize(sent.lower()):  # iterating over words
            if word in word_frequencies.keys():    # iterating over word frequency dict keys
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word] # adding frequencies of individual words to
                        # compute the score of the sentence
    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)  # get top sentences based on score
    # number of lines has been set to 7 right now, but can be changed to change the length of summary.

    summary = ' '.join(summary_sentences)  # join the individual top sentences to form the summary of article
    return summary


translator = Translator()   # initializing googletrans Translator instance

pdfmetrics.registerFont(TTFont('gargi','Font/gargi.ttf'))  # register font for printing text present in Font directory


myclient = pymongo.MongoClient("mongodb://localhost:27017/") # connecting to mongodb server
mydb = myclient["NewsDB"]  # specifying our database in the server
mycol = mydb[f"Articles{datetime.date.today()}"]  # specifying the collection

#  collections are named by date to store articles scraped in
#  different dates separately for easier management of scraped data


myquery = {
    'Article': re.compile(r"Himachal")    # query for finding articles having keyword "Himachal" in the article body
}

df = pd.DataFrame(list(mycol.find(myquery)))  # getting the query result as a pandas dataframe
#df.to_csv("news.csv")   # saving in a csv file temporarily

my_doc = SimpleDocTemplate('PDFs/News{}.pdf'.format(datetime.date.today()))   # specifying name of pdf file
# and initializing pdf document as a SimpleDocTemplate
flowables = []   # List flowables for storing text and variables to output to the pdf document
sample_style_sheet = getSampleStyleSheet()   # style sheet for automatic font and other styling in the document
sample_style_sheet.add(ParagraphStyle(name='TestStyle',
                               fontName='gargi',         # adding our own style attribute to the style sheet template
                               fontSize=12,              # adding for writing hindi font to the pdf document
                               leading=12))
#df = pd.read_csv("news.csv", sep =',', encoding='utf-8')  # opening the previously saved temporary csv file having query results
for index, rows in df.iterrows():  # iterating over dataframe of the query result
    if len(str(rows.Article)) > 700:  # ignoring small insignificant articles
        lang = detect(rows.Article)  # detecting language of article
        if lang == 'en':   # language of article is english
            sentiment = s.sentiment(rows.Article)  # computing sentiment of article
        else:     # if language of article is not English
            try:
                translated_article = translator.translate(str(rows.Article))  # translate for sentiment analysis
                sentiment = s. sentiment(translated_article.text)  # computing sentiment of translated document
            except Exception as e:
                pass

        # adding various components of scraped data as a Paragraph instance
        paragraph_1 = Paragraph("Website", sample_style_sheet['Heading2'])
        paragraph_2 = Paragraph(rows.Website, sample_style_sheet['TestStyle'])
        paragraph_3 = Paragraph("URL", sample_style_sheet['Heading2'])
        paragraph_4 = Paragraph(rows.URL, sample_style_sheet['TestStyle'])
        paragraph_5 = Paragraph("Headline", sample_style_sheet['Heading2'])
        paragraph_6 = Paragraph(rows.Headline, sample_style_sheet['TestStyle'])
        paragraph_7 = Paragraph("Time", sample_style_sheet['Heading2'])
        paragraph_8 = Paragraph(str(rows.Time), sample_style_sheet['TestStyle'])
        paragraph_9 = Paragraph("Authors", sample_style_sheet['Heading2'])
        paragraph_10 = Paragraph(str(rows.Author), sample_style_sheet['TestStyle'])
        paragraph_11 = Paragraph("Summary of Article", sample_style_sheet['Heading2'])
        paragraph_12 = Paragraph(summarize(), sample_style_sheet['TestStyle'])
        paragraph_13 = Paragraph("Sentiment", sample_style_sheet['Heading2'])
        paragraph_14 = Paragraph(sentiment, sample_style_sheet['TestStyle'])
        paragraph_15 = Paragraph("Content", sample_style_sheet['Heading2'])
        paragraph_16 = Paragraph(rows.Article, sample_style_sheet['TestStyle'])


        # appending all the paragraphs to the flowables
        flowables.append(paragraph_1)
        flowables.append(paragraph_2)
        flowables.append(paragraph_3)
        flowables.append(paragraph_4)
        flowables.append(paragraph_5)
        flowables.append(paragraph_6)
        flowables.append(paragraph_7)
        flowables.append(paragraph_8)
        flowables.append(paragraph_9)
        flowables.append(paragraph_10)
        flowables.append(paragraph_11)
        flowables.append(paragraph_12)
        flowables.append(paragraph_13)
        flowables.append(paragraph_14)
        flowables.append(paragraph_15)
        flowables.append(paragraph_16)
        flowables.append(PageBreak())  # Next page after one article has been printed on document

my_doc.build(flowables)  # building the pdf document from the flowables list
#os.remove('news.csv')
