###############################   Import   ##################################################################################################
from __future__ import division
import string
import math
import urllib2
###############################   Web Download   #############################################################################################
get_html = urllib2.urlopen("http://google.de")
page_source = get_html.read()

###############################   Strip Html Tags   ###########################################################################################
def strip_html_tags(html_and_txt):
   
   converted_list = list(html_and_txt)#���� ��� ������
   i,j = 0,0
	
   while i < len(converted_list):
      if converted_list[i] == '<':# ����� ����
         while converted_list[i] != '>':#���� ��� �� ���� ����
            converted_list.pop(i)
         converted_list.pop(i)# ���� �� �� ��� ����
      else:
         i=i+1 # �� �� ���� ��� ����� ����
		
   spaces='' 
   return spaces.join(converted_list) # ����� ������
print strip_html_tags (page_source)
###############################    TF - IDF   #################################################################################################
tokenize = lambda doc: doc.lower().split(" ") # ���� �� ������� ������

document_0 = "the create pillow."
document_1 = "the the the."
document_2 = "the pillow."
document_3 = "create pillow."
document_4 = "the create"
document_5 = "soft pillow."
document_6 = "the create"

all_documents = [document_0, document_1, document_2, document_3, document_4, document_5, document_6]

def sublinear_term_frequency(term, tokenized_document): # ���� ���� �����
   count = tokenized_document.count(term) # ���� ��� ����� ����� ����� �����
   if count == 0:
       return 0 # �� �� ���� - ����� 0
   else:
      return 1 + math.log(count) # �� ���� ����� �� ���� ������ ���� ���
#  ����� �� ���� ������ ����� ����� ����� ���� ���������� (���)

def inverse_document_frequencies(tokenized_documents): # ���� ����
    idf_values = {}
    all_tokens_set = set([item for sublist in tokenized_documents for item in sublist]) # ���� �� �� �� ������� �������� ��� �������
    for tkn in all_tokens_set: # ��� ���� ������
        contains_token = map(lambda doc: tkn in doc, tokenized_documents) #  ����� �� �� ������� ������ ������ ���� ������ ���
        idf_values[tkn] = 1 + math.log(len(tokenized_documents)/(sum(contains_token))) # �� ������ �� ����� �� �� ���� ��� ����� �� ���� ������ ������� ����� ���� ������
    return idf_values

# ����� �� ���� �� �� ���� �� �� ���� ������ ���� ����� ������� ������

def tfidf(documents):
    tokenized_documents = [tokenize(d) for d in documents]# ���� �� ������� ������ ��������
    idf = inverse_document_frequencies(tokenized_documents) #����� �� ���� �� �� ���� �� �� ����� ������
    tfidf_documents = []
    for document in tokenized_documents: #��� ����
        doc_tfidf = []
        for term in idf.keys(): #����  - ��� ���� ���� ������� ������
            tf = sublinear_term_frequency(term, document)#  ���� ��� ��
            doc_tfidf.append(tf * idf[term])#  ���� �� ����� �� �� ������� ���� ���� ���� ����� �� �����
        tfidf_documents.append(doc_tfidf)
    return tfidf_documents
# ����� �� ������ - ���� �� ���� �� �� ���� ���� ����� �����




def cosine_similarity(vector1, vector2):
    dot_product = sum(p*q for p,q in zip(vector1, vector2))# ���� �� ����� �� ����� ������ �� TF � IDF
    magnitude = math.sqrt(sum([val**2 for val in vector1])) * math.sqrt(sum([val**2 for val in vector2])) # ���� �� �������� ������
    if not magnitude:
        return 0
    return dot_product/magnitude
#����� �� �������
   
tfidf_representation = tfidf(all_documents)
our_tfidf_comparisons = []
for count_0, doc_0 in enumerate(tfidf_representation):
   for count_1, doc_1 in enumerate(tfidf_representation):
      our_tfidf_comparisons.append((cosine_similarity(doc_0, doc_1), count_0, count_1))
      
# ���� �� ������ ���� �� ���� ���� �� ���� ���
def orgnize_info():
   final_match = " "
   best_match = 0
   second_match = 0
   for z in zip(sorted(our_tfidf_comparisons, reverse = True)):
      
      for one_result in z: # ���� �� ���� �� �� ����� ��� ������� ��������� ������
         
         if one_result [2] == 0 or one_result[1] == 0: # ���� �� ������� ��� ��������
            
            for solo in one_result: # ���� �� �� ������ ������ �����
               
               if (solo < 0.999999 and solo != 0): # ���� �� �� �� ���� �� ��� ������
                  
                  if solo > best_match: # ���� �� ������ ����� ����� ������ ���� 
                     best_match = solo
         if best_match == one_result [0]: # ���� ����� ���� ���� �� ��� ������ �������� ������ �� ������ � ����� ����
            
            if one_result[1] != 0:
               
               final_match = all_documents[one_result[1]]
            if one_result[2] != 0:
               
               final_match =  all_documents[one_result[2]]
   return final_match
   
#����� �� ����� ��� ������ ������ ����� ���� ����� 0 ������ ����
print orgnize_info()





























