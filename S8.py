#---------------------------------------------------------------------------------------
# In this program all features which are unigrams and bigrams (other features such as hashtags, url , user mentions and ... all are included in unigrams) are extracted and then for each tweet we clarify if they posess those features or don't by setting 1 and 0 respectivly for them in an excell file
#---------------------------------------------------------------------------------------
def get_uni_bi_grams_and_states (worksheet1):

    import nltk
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords 
    from nltk.stem import WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()
    from nltk import pos_tag
    import string

    # getting uni bi grams ----------------------------------------
    row_n = 1 #because row = 0 is for titles
    Tweet_ID = worksheet1.col_values(0)
    Retweet_ID = worksheet1.col_values(2)
    Tweet_State = worksheet1.col_values(6)
    del Tweet_State[0]
    number_tweets = len (Tweet_ID) - 1

    tweet_words = []
    list_tweet_uniwords = [] #unigrams per each tweet
    token_lem = [] #lemmatization is much more better than stemming, because at the end, lemm gives us a meaningful word and also for irregular verbs it still works (go, goes,went ==> go) , the only problem with lemm is that it has more computational cost  
    unigrams_list_with_repetition = [] #unigrams of all tweets (without repeated elements)
    additional = ["'s","?","n't","'i",'’','«','could',"'m",'”','would',"'you","...",'–','‘',"'ll","'re","'no","'re",'--',"'yes","'ve","'it",'``',"''",'http',"'that","'it","'the","'they","'he","'d","mrs","mr","'we"]    
    while row_n < len (Tweet_ID) :
        if worksheet1.cell(row_n, 2).value != 'Not a Retweet Only' :
            text = worksheet1.cell(row_n, 4).value
        else :
            text = worksheet1.cell(row_n, 3).value
            
        for i,j in pos_tag(word_tokenize(text)):
            if j[0].lower() in ['a','n','v'] : #(a = adjective , n = noun , v = verb)
                token_lem.append(lemmatizer.lemmatize(i,j[0].lower()))
            else :
                token_lem.append(lemmatizer.lemmatize(i))



        stoplist = set(stopwords.words()) #not defining "english" so it can be able to delete all stopwords from all languages ...
        for word in token_lem :
            if (word.lower() not in stoplist ) and (word not in string.punctuation) and (word.lower() not in additional)  :
                unigrams_list_with_repetition.append(word)
                tweet_words.append (word) # this is for function of enter_data_into_dataset
            
        
        token_lem = []
        list_tweet_uniwords.append(tweet_words)
        tweet_words = []
        row_n += 1
        

        
    unigrams_list = set(unigrams_list_with_repetition)

    

    tweet_biwords = []
    list_tweet_biwords = [] #bigrams per each tweet
    bigrams_list_with_repetition = []#bigrams of all tweets

    for bigram in nltk.bigrams(unigrams_list_with_repetition): #we make bigrams from the unigrams because they are already processed but the importan point is to make them from unigrams_list_with_repetition not unigrams !!! because in unigrams many words are deleted and the sentence of tweets are not in origin order
        bigrams_list_with_repetition.append (bigram)

    bigrams_list = set(bigrams_list_with_repetition)
    for tweet_list in list_tweet_uniwords :
        for bigram in nltk.bigrams(tweet_list) :
            tweet_biwords.append (bigram)
        list_tweet_biwords.append(tweet_biwords)
        tweet_biwords = []

    
    return unigrams_list,bigrams_list,list_tweet_uniwords,list_tweet_biwords,number_tweets,Tweet_ID,Retweet_ID,Tweet_State


#------------------------------------------------------------------------------------
def make_learning_dataset_labels (unigrams_list,bigrams_list,worksheet1_w) :

    number_features = len(unigrams_list) + len(bigrams_list)
    print ("number_features : ",number_features)
    worksheet1_w.set_column (0, (number_features + 1), 30) # to make cells extended so the excel file becomes more beautiful 
    worksheet1_w.write(0, 0, 'Tweet or Retweet ID')
    col_n = 1
    for feature in unigrams_list :
        worksheet1_w.write(0, col_n, feature)
        col_n += 1
    for feature in bigrams_list :
        worksheet1_w.write(0, col_n, str(feature))
        col_n += 1
    worksheet1_w.write(0, col_n, 'Tweet State')
    
    return worksheet1_w,number_features 
#------------------------------------------------------------------------------------
def enter_data_into_dataset (list_tweet_uniwords,list_tweet_biwords,number_features,worksheet1_w,number_tweets,Tweet_ID,Retweet_ID,unigrams_list,bigrams_list,Tweet_State,worksheet2_w,worksheet1) :

    col_n = 1
    row_n = 1
    all_uni_bi = []
    Frequency = worksheet1.col_values(1)
    
    for uni in unigrams_list :
        all_uni_bi.append (uni)
    for bi in bigrams_list :
        all_uni_bi.append (bi)


    while row_n < (number_tweets + 1) :

        if Retweet_ID[row_n] != "Not a Retweet Only" : #for retweets we enter the retweet id in the first column
            worksheet1_w.write(row_n, 0, Retweet_ID[row_n])
        else :
            worksheet1_w.write(row_n, 0, Tweet_ID[row_n])
            
        while col_n < (number_features + 1) :
            if all_uni_bi [col_n - 1] in list_tweet_uniwords[row_n - 1] :
                worksheet1_w.write(row_n, col_n, '1')
            elif all_uni_bi [col_n - 1] in list_tweet_biwords[row_n - 1] :
                worksheet1_w.write(row_n, col_n, '1')

                
            else :
                worksheet1_w.write(row_n, col_n, '0')
            col_n += 1
        row_n += 1
        col_n = 1



    row_n = 1
    while row_n < (number_tweets + 1) :
        worksheet1_w.write(row_n, (number_features + 1), Tweet_State[row_n - 1])
        row_n += 1
        

    #Sheet 2 ----
    worksheet2_w.set_column (0, 1, 30) # to make cells extended so the excel file becomes more beautiful 
    worksheet2_w.write(0, 0, 'Tweet or Retweet ID')
    worksheet2_w.write(0, 1, '#Frequency')
    
    row_n = 1
    while row_n < (number_tweets + 1) :
        if Retweet_ID[row_n] != "Not a Retweet Only" : #for retweets we enter the retweet id in the first column
            worksheet2_w.write(row_n, 0, Retweet_ID[row_n])
        else :
            worksheet2_w.write(row_n, 0, Tweet_ID[row_n])
        row_n += 1

    row_n = 1
    while row_n < (number_tweets + 1) :
        worksheet2_w.write(row_n, 1, Frequency[row_n])
        row_n += 1
        
    
#------------------------------------------------------------------------------------
def main ():
    
    import xlrd

    #Getting uni bi grams and states of tweets ----
    my_path = 'D:\\Papers\\Social Network Mining\\Creating_Dataset\\Step8\\False Rumors\\False_Rumor_24\\Input\\'
    workbook = xlrd.open_workbook(my_path + 'final_judgment.xlsx')
    worksheet1 = workbook.sheet_by_name('Sheet1')

    import xlsxwriter
    my_path_learning_dataset = 'D:\\Papers\\Social Network Mining\\Creating_Dataset\\Step8\\False Rumors\\False_Rumor_24\\Output\\'
    workbook_w = xlsxwriter.Workbook(my_path_learning_dataset + 'excel_learning_dataset.xlsx')
    worksheet1_w = workbook_w.add_worksheet()
    worksheet2_w = workbook_w.add_worksheet()

    #---- G.E.T -- U.N.I.G.R.A.M.S -- A.N.D -- B.I.G.R.A.M.S ---------------------------
    unigrams_list,bigrams_list,list_tweet_uniwords,list_tweet_biwords,number_tweets,Tweet_ID,Retweet_ID,Tweet_State = get_uni_bi_grams_and_states (worksheet1)

    #---- M.A.K.I.N.G -- L.E.A.R.N.I.N.G -- D.A.T.A.S.E.T -- L.A.B.E.L.S ---------------
    worksheet1_w,number_features = make_learning_dataset_labels (unigrams_list,bigrams_list,worksheet1_w)

    #---- E.N.T.E.R.I.N.G -- D.A.T.A -- I.N.T.O -- D.A.T.A.S.E.T -----------------------
    enter_data_into_dataset (list_tweet_uniwords,list_tweet_biwords,number_features,worksheet1_w,number_tweets,Tweet_ID,Retweet_ID,unigrams_list,bigrams_list,Tweet_State,worksheet2_w,worksheet1)

    

    workbook_w.close()

#------------------------------------------------------------------------------------

main()    
input ("press enter key to exit ... ")
