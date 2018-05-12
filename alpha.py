###############################   Import   ##################################################################################################
from __future__ import division
import string
import math
import urllib2
###############################   Web Download   #############################################################################################
get_html = urllib2.urlopen("http://google.de")
page_source = get_html.read()
from HTMLParser import HTMLParser
###############################   Strip Html Tags   ###########################################################################################
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset() # cleans the buffer and setting up
        self.fed = []
    def handle_data(self, l): # gets word and uppend it to a list
        self.fed.append(l)
    def handle_entityref(self, name):
        self.fed.append('&%s;' % name)#using regex to clean the html out
    def get_data(self): # getting all to words togheter
        return ''.join(self.fed)

def html_to_text(html): # building an object and activiting the class
    s = MLStripper()
    s.feed(html) # 'feeding' the class each word
    return s.get_data()
###############################    TF - IDF   #################################################################################################
tokenize = lambda doc: doc.lower().split(" ") # organizing the text

document_0 = "the create pillow."
document_1 = "the the the."
document_2 = "the pillow."
document_3 = "create pillow."
document_4 = "the create"
document_5 = "soft pillow."
document_6 = "the create"

all_documents = [document_0, document_1, document_2, document_3, document_4, document_5, document_6]

def sublinear_term_frequency(term, tokenized_document): # getting the term
   count = tokenized_document.count(term) # counting how many times the term is shown in the doucement
   if count == 0:
       return 0 # if doesnt shown once returning 0
   else:
      return 1 + math.log(count) 
# if shown retrning the number of times after normalization (log)

def inverse_document_frequencies(tokenized_documents): # getting a document
    idf_values = {}
    all_tokens_set = set([item for sublist in tokenized_documents for item in sublist]) # creatung a set of all the terms in all the documents
    for tkn in all_tokens_set: # לכל מונח ברשימה
        contains_token = map(lambda doc: tkn in doc, tokenized_documents) #  moving the terms into a map
        idf_values[tkn] = 1 + math.log(len(tokenized_documents)/(sum(contains_token))) # puts in dictionary the value of each word by dividing the number of times the word appears by the total words
    return idf_values

# returning this value

def tfidf(documents):
    tokenized_documents = [tokenize(d) for d in documents]# converting the documents to a different format
    idf = inverse_document_frequencies(tokenized_documents) #putting the value of each word in a varbile by idf
    tfidf_documents = []
    for document in tokenized_documents: # for each doc
        doc_tfidf = []
        for term in idf.keys(): #for each catgory in the dictionary
            tf = sublinear_term_frequency(term, document)
            doc_tfidf.append(tf * idf[term])#  Calculates the product of the idf and tf
        tfidf_documents.append(doc_tfidf)
    return tfidf_documents
# getting all the functions to work togheter




def cosine_similarity(vector1, vector2):
    dot_product = sum(p*q for p,q in zip(vector1, vector2))# Calculates the sum of the idf and tf
    magnitude = math.sqrt(sum([val**2 for val in vector1])) * math.sqrt(sum([val**2 for val in vector2])) # put the results in the formula
    if not magnitude:
        return 0
    return dot_product/magnitude
#normalization
   
tfidf_representation = tfidf(all_documents)
our_tfidf_comparisons = []
for count_0, doc_0 in enumerate(tfidf_representation):
   for count_1, doc_1 in enumerate(tfidf_representation):
      our_tfidf_comparisons.append((cosine_similarity(doc_0, doc_1), count_0, count_1))
      
# doing this process for each doc
def orgnize_info():
   final_match = " "
   best_match = 0
   second_match = 0
   for z in zip(sorted(our_tfidf_comparisons, reverse = True)):
      
      for one_result in z: #Receives the value of each adjustment and the relevant documents for the adjustment
         
         if one_result [2] == 0 or one_result[1] == 0: # Filters the irrelevant documents
            
            for solo in one_result: # Receives all entries in a single configuration
               
               if (solo < 0.999999 and solo != 0): # Filtering everything that is not the matching value
                  
                  if solo > best_match: # Checks what is the best match and stores it
                     best_match = solo
         if best_match == one_result [0]: #Checking which document that is not zero The match is relevant and stores the result
            
            if one_result[1] != 0:
               
               final_match = all_documents[one_result[1]]
            if one_result[2] != 0:
               
               final_match =  all_documents[one_result[2]]
   return final_match
   
print orgnize_info()




























