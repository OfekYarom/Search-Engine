###############################   Import   ##################################################################################################
import string
import math
import urllib
import urllib2
import Tkinter as tk
from Tkinter import *
import wikipedia
###############################    TF - IDF   #################################################################################################
def documents (doc_0):
    
    # get the text from wikipedia according to the user input
    # the function is getting the text for each word and for the all input
    error = 0
    tokenize = lambda doc: doc.lower().split(" ") # organizing the text
    document_0 = doc_0
    all_documents = [document_0]
    check_url = ((('https://en.wikipedia.org/wiki/%s') %(doc_0)))
    check_url = check_url.replace(" ", "_")
    try:# checks if web page is working without getting errors
        urllib.urlopen(check_url)
    except urllib2.HTTPError, e:
        pass
    except urllib2.URLError, e:
        pass
    else: # if no eror acourded the program keep runing the web page
        stat1 = (urllib.urlopen(check_url)).getcode()
        if stat1 == 200:
            # if the web page contians info its keep runing.
            response = (urllib2.urlopen(check_url))
            page_source = response.read()
            if "usually refers to:" not in page_source:
                #gets the info from the web page
                Page = (wikipedia.page(("%s") % (doc_0)))
                doc_one = Page.content
                doc_two = (Page.summary)
                all_documents.append (doc_one)
                all_documents.append (doc_two)
                error = error + 1
    splited = doc_0.split()
    if ((len(splited))>1):
        #if the input is built from more than one word
        # the program gets the info for each word separately
        count = 1
        while (((len(splited))>= count)):
            word = splited[count-1]
            try:# checks if web page is working without getting errors
                (urllib.urlopen((('https://en.wikipedia.org/wiki/%s') %(word))))
            except urllib2.HTTPError, e:
                pass
            except urllib2.URLError, e:
                pass
            else: # if no eror acourding its keep runing the web page
                stat = (urllib.urlopen((('https://en.wikipedia.org/wiki/%s') %(word)))).getcode()
                # if the web page contians info its keep runing.
                if stat == 200:
                    amount_results = (wikipedia.search(("%s") % (word)))
                    last = 0
                    for i in amount_results:
                        if last == 0:
                            try:# checks if web page is working without getting errors
                                (urllib.urlopen((('https://en.wikipedia.org/wiki/%s') %(i))))
                            except urllib2.HTTPError, e:
                                pass
                            except urllib2.URLError, e:
                                pass
                            else: # if no eror acourding its keep runing the web page
                                stat1 = (urllib.urlopen((('https://en.wikipedia.org/wiki/%s') %(i)))).getcode()
                                # if the web page contian info its keep runing.
                                if stat1 == 200:
                                    response = (urllib2.urlopen((('https://en.wikipedia.org/wiki/%s') %(i))))
                                    page_source = response.read()
                                    if "usually refers to:" not in page_source:
                                        #gets the info from the web page
                                        Page = (wikipedia.page(("%s") % (i)))
                                        doc_one = Page.content
                                        doc_two = (Page.summary)
                                        all_documents.append (doc_one)
                                        all_documents.append (doc_two)
                                        error = error + 1
                                        last = last + 1
            count = count + 1
            if (((len(splited)) < count)):
                out_put_fun =[all_documents, error, tokenize]
                return out_put_fun
    else:
        out_put_fun =[all_documents, error, tokenize]
        return out_put_fun

def sublinear_term_frequency(term, tokenized_document): # getting the term and the docs # calling the function (getting it all togheter)
   count = tokenized_document.count(term) # counting how many times the term is shown in the doucement
   if count == 0:
       return 0 # if doesnt shown once returning 0
   else:
      return 1 + math.log(count) 
# if shown retrning the number of times after normalization (log)

def inverse_document_frequencies(tokenized_documents): # getting a document
    idf_values = {}
    all_tokens_set = set([item for sublist in tokenized_documents for item in sublist]) # creatung a set of all the terms in all the documents
    for tkn in all_tokens_set: # for every word
        contains_token = map(lambda doc: tkn in doc, tokenized_documents) #  moving the terms into a map
        idf_values[tkn] = 1 + math.log(len(tokenized_documents)/(sum(contains_token))) # puts in dictionary the value of each word by dividing the number of times the word appears by the total words
    return idf_values

# returning this value

def tfidf(documents, tokenize):
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

def orgnize_info(our_tfidf_comparisons, all_documents):
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
def algo (all_documents,tokenize):# combining all the functions to get the formula and the result
   tfidf_representation = tfidf(all_documents, tokenize)
   our_tfidf_comparisons = []
   for count_0, doc_0 in enumerate(tfidf_representation):
       for count_1, doc_1 in enumerate(tfidf_representation):
           our_tfidf_comparisons.append((cosine_similarity(doc_0, doc_1), count_0, count_1))
   return orgnize_info(our_tfidf_comparisons, all_documents)
# doing this process for each doc
###############################   Nurmlzition for text   #############################################################################################
def text_normal(the_out, the_size):
    # orgnaizing the text for containing not too much words a line
    # depends on the amount of text is changing the length of a line and the size of the text.
    i = 0
    full =[]
    for word in (the_out.split()):
        full.append(word)
        i+= 1
        if i == int(the_size):
            i = 0
            full.append ("\n")
    complite = (' '.join(full))
    return complite

###############################   UI   #############################################################################################
def raise_frame(frame): # function for raising pages
    frame.tkraise()
def Search(): # set up and start the procses of the TF IDF
    textInput=txt.get() # get the word from the user
    in_put_fun = documents(textInput)# get it inside the tfidf
    all_documents = in_put_fun[0]
    error = in_put_fun[1]
    tokenize = in_put_fun[2]
    textOutPut= algo(all_documents, tokenize) # starts the tf idf
    if (len(textOutPut.split())) < 330:
        i=0
        textOutPut = text_normal (textOutPut, 15)
    else:
        i=1
        textOutPut = text_normal (textOutPut, 43)
    lbl_10["text"] = textOutPut # bring the output to the user
    if error > 0:
        if i==0:
            raise_frame(f2)# opens the next page to show the output
        else:
            raise_frame(f2)# opens the next page to show the output
            lbl_10.config(font=("Arial Bold", alot_of_txt))
            # depends on the amount of text is changing the length of a line and the size of the text.
    else:
        txt.delete(0, 'end')
        raise_frame(f4)# if no output have found
    # what to do when Search button clicked
    
def Send(): # the algorithem for the radio buttons
    X = var.get()
    if (X == 1 or X == 3):
        raise_frame(f3)
    if (X == 2):
        raise_frame(f3)
    if (X == 4):
        txt.delete(0, 'end')
        raise_frame(f1)
    # what to do when review button clicked

root = Tk() # creating tk window
#creats the components of the pages & the pages
f1 = Frame(root)
f2 = Frame(root)
f3 = Frame(root)
f4 = Frame(root)
# setting the pages size acording to the screen size
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
size_labels = (screenwidth*screenheight)/26200
size_smalllabels = size_labels/2
size_of_txt = size_labels/5
alot_of_txt = size_labels/10
size_of_entry = size_labels*1.5
x_cordnite = ((screenwidth/2)-(screenwidth/2.6))
y_cordnite = ((screenheight/2)-screenheight/2.6)
root.geometry(("%dx%d+%d+%d") %((screenwidth/1.3),(screenheight/1.3),x_cordnite,y_cordnite))
root.resizable(0, 0)
root.title("Search Engine") # giving the window a name

for frame in (f1, f2, f3, f4):
    frame.grid(row=0, column=0, sticky='news')

#page one - get Search Word
lbl_0 = Label(f1, text = "Search Engine", font = ("Arial Bold",size_labels))
lbl_0.grid(column=1, row = 1, sticky=(W, E))
lbl_1 = Label(f1, text = "Looking for info? Type it here and we will find it for you!", font = ("Arial Bold",size_smalllabels))
lbl_1.grid(column=1, row = 2, sticky=(W, E))
txt = Entry(f1, width=int((size_of_entry)))
txt.grid(column = 1, row = 3, pady = size_smalllabels)
txt.focus()
btn = Button(f1, text="Search", command=Search)
btn.grid(column=1, row=4)

#page two - get Feedback
var = IntVar()
lbl_4 = Label(f2, text = "Search Engine", font = ("Arial Bold",size_labels))
lbl_4.grid(column=1, row = 1, sticky=(W, E))
lbl_10 = Label(f2, text = "txt", font = ("Arial Bold",size_of_txt))
lbl_10.grid(column=1, row = 2, sticky=(W, E))
lbl_2 = Label(f2, text = "Is this was helpful? Do you want something better?", font = ("Arial Bold",int(size_smalllabels*1.127)))
lbl_2.grid(column=1, row = 5, sticky=(W, E))
rad1 = Radiobutton(f2,text='Helpful',  variable=var, value=1)
rad2 = Radiobutton(f2,text='Not Helpful',  variable=var, value=2)
rad3 = Radiobutton(f2,text='I Dont Know',  variable=var, value=3)
rad4 = Radiobutton(f2,text='I Want to Search Agin',  variable=var, value=4)
rad1.grid(column=1, row=6)
rad2.grid(column=1, row=7)
rad3.grid(column=1, row=8)
rad4.grid(column=1, row=9)
btn = Button(f2, text="Send", command=Send)
btn.grid(column=1, row=10)

#page three - Last Messege
lbl_5 = Label(f3, text = "Search Engine", font = ("Arial Bold",size_labels))
lbl_5.grid(column=1, row = 1, sticky=(W, E))
lbl_6 = Label(f3, text = "Thank You For Helping Us Improve!", font = ("Arial Bold",int(size_labels/1.26)))
lbl_6.grid(column=1, row = 2, sticky=(W, E))
lbl_7 = Label(f3, text = "Please Come Back Agin For Better Answer", font = ("Arial Bold",int(size_smalllabels*1.2)))
lbl_7.grid(column=1, row = 3, sticky=(W, E))
btn_11 = Button(f3, text="Try Agin", command=(lambda:raise_frame(f1)))
btn_11.grid(column=1, row=10)

#page Four - Last Messege
lbl_12 = Label(f4, text = "Search Engine", font = ("Arial Bold",size_labels))
lbl_12.grid(column=1, row = 1, sticky=(W, E))
lbl_13 = Label(f4, text = "Error Occurred", font = ("Arial Bold",size_labels))
lbl_13.grid(column=1, row = 2, sticky=(W, E))
lbl_14 = Label(f4, text = "Please Check Your Spelling Or Be More Specific And Try Agin", font = ("Arial Bold",int(size_smalllabels/1.07)))
lbl_14.grid(column=1, row = 3, sticky=(W, E))
btn_15 = Button(f4, text="Try Agin", command=(lambda:raise_frame(f1)))
btn_15.grid(column=1, row=10)




raise_frame(f1)# opening the first page - starts UI

root.mainloop() # making it to run until closed by user