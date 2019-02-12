#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# This program is made of two main sections. Section 1 which gives us an excel table of information for each tweet in the dataset. And Section2 which gives us general Information about the dataset in excels files and charts and wordclouds.
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# - - - - - - - - - - - - - - - - - - - - - - - - -
#  S...E...C...T...I...O...N......................1
# - - - - - - - - - - - - - - - - - - - - - - - - -

# --- I.M.P.O.R.T.I.N.G --- M.O.D.U.L.E.S ---------
# ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! !
import sys
from collections import Counter
import json
import xlsxwriter
from nltk import word_tokenize
# ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! !


#--- F.U.N.C.T.I.O.N --- F.O.R --- G.E.T.T.I.N.G --- U.S.E.R --- I.N.F.O.R.M.A.T.I.O.N ----
#@ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ 
def get_user_information(tweet):
    user = tweet.get('user',{})
    user_id = user.get('id',[])
    user_location = user.get('location',[])
    screen_name  = user.get('screen_name',[])
    followers_count = user.get('followers_count',[])
    friends_count = user.get('friends_count',[])
    statuses_count = user.get('statuses_count')
    description = user.get('description',[])
    timezone = user.get('time_zone',[])
    lang = user.get('lang',[])
    # date and time of creation of the account
    date_time_creation_account_raw = user.get('created_at',[])
    words = word_tokenize(date_time_creation_account_raw)
    date_time_creation_account = []
    date_time_creation_account.append (words[5])
    date_time_creation_account.append (words[1])
    date_time_creation_account.append (words[2])
    date_time_creation_account.append (words[3])
    #-----
    return user_id,screen_name,user_location,followers_count,friends_count,statuses_count,description,timezone,lang,date_time_creation_account
#@ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @


#--- F.U.N.C.T.I.O.N --- F.O.R --- G.E.T.T.I.N.G --- M.E.T.A --- D.A.T.A ---------------
#$ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ 
def get_meta_data (tweet):
    #--- S.E.T --- P.R.I.M.E ---- V.A.L.U.E.S ---- F.O.R ----- P.A.R.A.M.E.T.E.R.S -----
    favorite_count_sum = 0
    retweeted_number = 0
    tweet_with_another_tweet_inside = 0
    name_quoter = []
    date_time = []
    hashtags = []
    retweeted_screen_name = []
    in_reply_to_screen_name = []
    source = []
    user_mentions_screen_name = []
    retweet_count = 0
    #------------------------------------------------------------------------------------

    #favorite count analysis, means the number that the tweet of the user has published is liked by others (followers)
    favorite_count_sum += tweet['favorite_count']


    #retweet screen name, full text
    ss = get_retweeted_status(tweet)
    if ss :
        retweeted_screen_name.append(ss)


    # calculating number of tweet_quote
    if tweet['is_quote_status'] == True : 
        tweet_with_another_tweet_inside += 1


    # name of users who the user quoted their tweets
    quoted_user_name = get_quoted_user_id (tweet)
    if quoted_user_name != [] :
        name_quoter.append(quoted_user_name)
    
    #retweet_count says how many times tweets of the user were retweeted by other users
    retweet_count += tweet['retweet_count']

    #date and time of publish for each tweet
    dt = tweet['created_at']  
    date_time.append(dt)
    date_time_processed = date_time_process (date_time)

    #get hashtags
    hashtags.append (get_hashtags(tweet))
    all_hashtags_seperatly = get_hashtags_seperatly (hashtags)

    #get screen name of users who the user is replying to them
    tt = get_in_reply_to_screen_name(tweet) 
    if tt:
        in_reply_to_screen_name.append(tt)

    #geting the source of tweet
    source.append(get_source(tweet))

    
    #getting all users (their screen name) who were mentioned (by @) in the user tweets
    ff = get_user_mentions(tweet) 
    if ff:
        for user in ff:
            user_mentions_screen_name.append(user)


    return date_time_processed, favorite_count_sum, retweeted_screen_name, retweet_count, tweet_with_another_tweet_inside, name_quoter,  in_reply_to_screen_name, source, all_hashtags_seperatly, user_mentions_screen_name  

# $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $
    
#-----F.U.N.C.T.I.O.N.S --- F.O.R --- U.S.E --- I.N --- M.E.T.A --- D.A.T.A --- F.U.N.C.T.I.O.N -----
           # All The Following Functions Get Used In The "get_meta_data()" Function #
# % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 

def get_hashtags(tweet):
    entities = tweet.get('entities',{})
    hashtags = entities.get('hashtags',[])
    return [tag['text'].lower() for tag in hashtags]

 
def get_quoted_user_id (tweet):
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    quoted_user_status = tweet.get('quoted_status',{})
    quoted_user_id = quoted_user_status.get('user',{})
    quoted_user_name = quoted_user_id.get('name',[])
    if quoted_user_name != [] :
        quoted_user_name_safe = quoted_user_name.translate(non_bmp_map)
        return quoted_user_name_safe
    return quoted_user_name
 
def get_retweeted_status(tweet):
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    retweeted_status = tweet.get('retweeted_status',{})
    user_mentions = retweeted_status.get('user',{})
    screen_name = user_mentions.get('screen_name',[])
    string_screen_name = ''.join(screen_name)
    screen_name_safe = string_screen_name.translate(non_bmp_map)
 
    if screen_name_safe != []:
        return screen_name_safe
    
def get_in_reply_to_screen_name(tweet):
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    in_reply_to_screen_name = tweet['in_reply_to_screen_name']
    if in_reply_to_screen_name :
        string_in_reply_to_screen_name = ''.join(in_reply_to_screen_name)
        in_reply_to_screen_name_safe = string_in_reply_to_screen_name.translate(non_bmp_map)
        return in_reply_to_screen_name_safe

def get_source(tweet):
    source = tweet['source']
    if source :
        string_source = ''.join(source)
        words = word_tokenize(string_source)
        length = len(words)
        source_only = words[(length-4)]
        return source_only

def BMP(t): #for use in the following function (get_user_mentions(tweet))
    return "".join((i if ord(i) < 10000 else '\ufffd' for i in t))

def get_user_mentions(tweet):
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    entities = tweet.get('entities',{})
    user_mentions = entities.get('user_mentions',[])
    screen_name_mention_safe = []
    if user_mentions :
        for i in user_mentions :
            d = i.get('screen_name',[])
            dd = BMP(d)
            screen_name_mention_safe.append(dd)
    return screen_name_mention_safe
  
          
def get_hashtags_seperatly (hashtags):
    all_hashtags_seperatly = []
    for hashtag_tweets in hashtags:
        for single_hashtag in hashtag_tweets :
            all_hashtags_seperatly.append (single_hashtag)
    return all_hashtags_seperatly


def date_time_process (date_time):  # this function eliminate unnessesary information of date_time for each tweet such as time of Greenwich and ... , and makes a standard set of date_time including "year , month , day , time(in hour:minute:second)"
    new_set = []
    date_time_processed = []
    for date_time_each in date_time :
        words = word_tokenize(date_time_each)
        new_set.append (words[5])
        new_set.append (words[1])
        new_set.append (words[2])
        new_set.append (words[3])
        date_time_processed.append (new_set)
        new_set = []

    return date_time_processed

# % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
    
#--- F.U.N.C.T.I.O.N --- F.O.R --- G.E.T.T.I.N.G --- M.E.T.A --- D.A.T.A ---------------
#^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^   
def get_text (tweet):
    tweet_text = tweet['full_text']
    tweetid = tweet['id']
    tweet_id = str (tweetid)
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd) #to convert emoji and undefined letters to defined letters and be able to show them
    tweet_text_OK = tweet_text.translate(non_bmp_map)
    return tweet_text_OK , tweet_id
#^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^
def get_retweeted_text (tweet):
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    retweeted_status = tweet.get('retweeted_status',{})
    
    if retweeted_status:
        retweeted_full_text = retweeted_status['full_text']
        retweeted_full_text_OK = retweeted_full_text.translate(non_bmp_map)
        retweetid = retweeted_status['id']
        retweet_id = str (retweetid)
        
    else :
        retweeted_full_text_OK = 'Not a Retweet'
        retweet_id = 'Not a Retweet'

    return retweeted_full_text_OK, retweet_id
#^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^
def get_quoted_text (tweet):
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    quoted_status = tweet.get('quoted_status',{})
    
    if quoted_status:
        quoted_full_text = quoted_status['full_text']
        quoted_full_text_OK = quoted_full_text.translate(non_bmp_map)
        quoteid = quoted_status['id']
        quote_id = str (quoteid)
        
    else :
        quoted_full_text_OK = 'Not a quote'
        quote_id = 'Not a quote'

    return quoted_full_text_OK, quote_id
#^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^
def get_reply_text_id (tweet): #unfortunately twitter just gives us the id of replyed tweet (the tweet that is replyed by the current tweet) not the text 
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    in_reply_to_tweetid = tweet['in_reply_to_status_id']
    reply_id = str (in_reply_to_tweetid)

    return reply_id 
#^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^

# ^^^^^O^^^^^   ^^^^^O^^^^^    ^^^^^O^^^^^    ^^^^^O^^^^^   ^^^^^O^^^^^   ^^^^^O^^^^^  
# ^^^^^O^^^^^   ^^^^^O^^^^^    ^^^^^O^^^^^    ^^^^^O^^^^^   ^^^^^O^^^^^   ^^^^^O^^^^^
# ^^^^^O^^^^^   ^^^^^O^^^^^    ^^^^^O^^^^^    ^^^^^O^^^^^   ^^^^^O^^^^^   ^^^^^O^^^^^



# SECTION 2 --------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------------------------------------------
# finding the 5 users that Have more tweets than other users in dataset, in other word 5 users that have been more activated than other users in the dataset
# ----------------------------------------------------------------------------------------------------------------------------------------------------------
def most_active_user_spreader (worksheet2, U_I_L, S_N_L, Ret_N_L, U_L_L, Fo_C_L, Fr_C_L, So_N_L, my_path):
    worksheet2.write(0, 0, 'Screen Name') 
    worksheet2.write(0, 1, 'ID') 
    worksheet2.write(0, 2, '#Count')
    worksheet2.write(0, 3, 'Location') 
    worksheet2.write(0, 4, '#Followers') 
    worksheet2.write(0, 5, '#Friends') 
    worksheet2.write(0, 6, '#Source')

    
    most_spreader_in_dataset = Counter(S_N_L).most_common(5)
    row  = 1 #because row = 0 was used for labels
    for sp in most_spreader_in_dataset :       
        index = S_N_L.index(sp[0])
        worksheet2.write(row, 0, sp[0])
        worksheet2.write(row, 1, U_I_L[index])
        worksheet2.write(row, 2, sp[1])
        worksheet2.write(row, 3, U_L_L[index]) #sure the user might have used different locations for his/her differernt tweets, but this location is for his/her first tweet in dataset
        worksheet2.write(row, 4, Fo_C_L[index])
        worksheet2.write(row, 5, Fr_C_L[index])
        worksheet2.write(row, 6, So_N_L[index]) #sure the user might have used different sources (devices) for his/her differernt tweets, but this source is for his/her first tweet in dataset            
        row += 1

    # WordCloud of User Spreaders 
    import matplotlib.pyplot as plt
    from wordcloud import WordCloud, STOPWORDS
    import gc
    import time

    wordcloud_oho = WordCloud(width = 1000, height = 500, background_color = 'white').generate(' '.join(S_N_L))
    fig = plt.figure(figsize=(12,12),dpi=100) #here its not required to give high dpi
    plt.imshow(wordcloud_oho)
    plt.axis("off")
    plt.savefig (my_path + 'User_Spreader.png',dpi=1000) # here we give high dpi to save figures with great quality
    plt.show() 
# ----------------------------------------------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------------------------------------------
# finding the 5 TimeZones that users published their tweets from them most (kind of location of users when they sent tweets)
# ----------------------------------------------------------------------------------------------------------------------------------------------------------
def most_timezone_used (worksheet3, T_Z, my_path):
    T_Z_L = []
    worksheet3.write(0, 0, 'Time Zone') 
    worksheet3.write(0, 1, '#Count')
    for i in T_Z :
        if i != 'None' :
            T_Z_L.append (str(i))
    most_TimeZone_in_dataset = Counter(T_Z_L).most_common(10)
    row = 1
    for TimeZone_most in most_TimeZone_in_dataset :
        worksheet3.write(row, 0, TimeZone_most[0])
        worksheet3.write(row, 1, TimeZone_most[1])        
        row += 1

    # WordCloud of TimeZone mentioned  
    import matplotlib.pyplot as plt
    from wordcloud import WordCloud, STOPWORDS

    #--- this part is for getting the words of timezone sticked togather because when they are apart from each other are detected as seperate words by wordcloud module
    from nltk import word_tokenize
    T_Z_L_L = []
    for k in  T_Z_L:
        words = word_tokenize(k)
        parentheses = {'(',')'}
        words_ok = []
        for j in words :
            if j not in parentheses :
                if j != '&' :
                    words_ok.append (j)

     
        t = 0
        hh = ''
        lenwords = len (words_ok)
        while t < lenwords :
            if t < (lenwords - 1) :
                ss = words_ok[t] + ''
                hh += ss                  
            else :
                ss = words_ok[t]
                hh += ss

            t += 1
        T_Z_L_L.append (hh)
   #---------------------------- 
    if T_Z_L_L :
        wordcloud_oho = WordCloud(width = 1000, height = 500, background_color = 'white',stopwords = {'Time'}).generate(" ".join(T_Z_L_L))
        fig = plt.figure(figsize=(12,12),dpi=100) #here its not required to give high dpi
        plt.imshow(wordcloud_oho)
        plt.axis("off")
        plt.savefig (my_path + 'TimeZone.png',dpi=1000) # here we give high dpi to save figures with great quality
        plt.show()
# ----------------------------------------------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------------------------------------------
# finding the 5 Official Language that tweets are written by them
# ----------------------------------------------------------------------------------------------------------------------------------------------------------
def most_official_language_used (worksheet4, L_A_O, my_path):
    L_A_O_L = []
    worksheet4.write(0, 0, 'Official Language') 
    worksheet4.write(0, 1, '#Count')
    for i in L_A_O :
        if i != 'None' :
            L_A_O_L.append (i)
    most_OfficialLanguage_in_dataset = Counter(L_A_O_L).most_common(10)
    row = 1
    for OfficialLanguage_most in most_OfficialLanguage_in_dataset :
        worksheet4.write(row, 0, OfficialLanguage_most[0])
        worksheet4.write(row, 1, OfficialLanguage_most[1])        
        row += 1

    # WordCloud of Official language tweets are written by them 
    import matplotlib.pyplot as plt
    from wordcloud import WordCloud, STOPWORDS

    wordcloud_oho = WordCloud(width = 1000, height = 500, background_color = 'white').generate(' '.join(L_A_O_L))
    fig = plt.figure(figsize=(12,12),dpi=100) #here its not required to give high dpi
    plt.imshow(wordcloud_oho)
    plt.axis("off")
    plt.savefig (my_path + 'OfficialLanguage.png',dpi=1000) # here we give high dpi to save figures with great quality
    plt.show()
# ----------------------------------------------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------------------------------------------
# finding the 5 users that were retweeted most
# ----------------------------------------------------------------------------------------------------------------------------------------------------------
def most_retweeted_user (worksheet5, U_I_L, S_N_L, Ret_N_L, U_L_L, Fo_C_L, Fr_C_L, So_N_L, my_path):
    Ret_name = []
    worksheet5.write(0, 0, 'Screen Name') 
    worksheet5.write(0, 1, 'ID') 
    worksheet5.write(0, 2, '#Count')
    worksheet5.write(0, 3, 'Location') 
    worksheet5.write(0, 4, '#Followers') 
    worksheet5.write(0, 5, '#Friends') 
    worksheet5.write(0, 6, '#Source')
    

    for i in Ret_N_L :
        if i != 'None' :
            Ret_name.append (i)        
    most_retweeted_in_dataset = Counter(Ret_name).most_common(10)
    row  = 1 #because row = 0 was used for labels
    for ru in most_retweeted_in_dataset :       
        if ru[0] in S_N_L:
            index = S_N_L.index(ru[0])
            worksheet5.write(row, 0, ru[0])
            worksheet5.write(row, 1, U_I_L[index])
            worksheet5.write(row, 2, ru[1])
            worksheet5.write(row, 3, U_L_L[index]) #sure the user might have used different locations for his/her differernt tweets, but this location is for his/her first tweet in dataset
            worksheet5.write(row, 4, Fo_C_L[index])
            worksheet5.write(row, 5, Fr_C_L[index])
            worksheet5.write(row, 6, So_N_L[index]) #sure the user might have used different sources (devices) for his/her differernt tweets, but this source is for his/her first tweet in dataset
            
        else : #since the user who is retweeted  most might not have a tweet in dataset so in this case we put 'out of dataset' for the required information of this user
            worksheet5.write(row, 0, ru[0])
            worksheet5.write(row, 1, 'out of dataset') #since the user who is retweeted  most might not have a tweet in dataset so in this case we put 'out of dataset' for the required information of this user
            worksheet5.write(row, 2, ru[1])
            worksheet5.write(row, 3, 'out of dataset') #since the user who is retweeted  most might not have a tweet in dataset so in this case we put 'out of dataset' for the required information of this user
            worksheet5.write(row, 4, 'out of dataset') #since the user who is retweeted  most might not have a tweet in dataset so in this case we put 'out of dataset' for the required information of this user
            worksheet5.write(row, 5, 'out of dataset') #since the user who is retweeted  most might not have a tweet in dataset so in this case we put 'out of dataset' for the required information of this user
            worksheet5.write(row, 6, 'out of dataset') #since the user who is retweeted  most might not have a tweet in dataset so in this case we put 'out of dataset' for the required information of this user


        row += 1

    # WordCloud of Retweeted User  
    import matplotlib.pyplot as plt
    from wordcloud import WordCloud, STOPWORDS

    wordcloud_oho = WordCloud(width = 1000, height = 500, background_color = 'white').generate(' '.join(Ret_name))
    fig = plt.figure(figsize=(12,12),dpi=100) #here its not required to give high dpi
    plt.imshow(wordcloud_oho)
    plt.axis("off")
    plt.savefig (my_path + 'Retweeted_Users.png',dpi=1000) # here we give high dpi to save figures with great quality
    plt.show()
# ----------------------------------------------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------------------------------------------
# finding the 5 source (kind of device's OS) that are used most in the dataset for publishing tweets
# ----------------------------------------------------------------------------------------------------------------------------------------------------------
def most_source_mentioned (worksheet6, So_N_L, my_path):
    worksheet6.write(0, 0, 'Source Name') 
    worksheet6.write(0, 1, '#Count')      
    most_source_in_dataset = Counter(So_N_L).most_common(10)
    row = 1
    for source_most in most_source_in_dataset :
        worksheet6.write(row, 0, source_most[0])
        worksheet6.write(row, 1, source_most[1])        
        row += 1

    # WordCloud of Source mentioned  
    import matplotlib.pyplot as plt
    from wordcloud import WordCloud, STOPWORDS

    wordcloud_oho = WordCloud(width = 1000, height = 500, background_color = 'white').generate(' '.join(So_N_L))
    fig = plt.figure(figsize=(12,12),dpi=100) #here its not required to give high dpi
    plt.imshow(wordcloud_oho)
    plt.axis("off")
    plt.savefig (my_path + 'Sources.png',dpi=1000) # here we give high dpi to save figures with great quality
    plt.show()
# ----------------------------------------------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------------------------------------------
# finding the 5 users that are menitiond most in the dataset
# ----------------------------------------------------------------------------------------------------------------------------------------------------------
def most_user_mentioned (worksheet7, U_I_L, S_N_L, Ret_N_L, U_L_L, Fo_C_L, Fr_C_L, So_N_L, U_M_N_L, my_path):
    user_list = []
    worksheet7.write(0, 0, 'Screen Name') 
    worksheet7.write(0, 1, 'ID') 
    worksheet7.write(0, 2, '#Count')
    worksheet7.write(0, 3, 'Location') #sure the user might have used different locations for his/her differernt tweets, but this location is for his/her first tweet in dataset
    worksheet7.write(0, 4, '#Followers') 
    worksheet7.write(0, 5, '#Friends') 
    worksheet7.write(0, 6, '#Source') #sure the user might have used different sources (devices) for his/her differernt tweets, but this source is for his/her first tweet in dataset
    for i in U_M_N_L :
        if i != 'None' :
            for j in i :
                user_list.append(j)
    most_user_mentioned_in_dataset = Counter(user_list).most_common(10)
    row  = 1 #because row = 0 was used for labels
    for um in most_user_mentioned_in_dataset :       
        if um[0] in S_N_L:
            index = S_N_L.index(um[0])
            worksheet7.write(row, 0, um[0])
            worksheet7.write(row, 1, U_I_L[index])
            worksheet7.write(row, 2, um[1])
            worksheet7.write(row, 3, U_L_L[index])
            worksheet7.write(row, 4, Fo_C_L[index])
            worksheet7.write(row, 5, Fr_C_L[index])
            worksheet7.write(row, 6, So_N_L[index])
            
        else : #since the user who is retweeted  most might not have a tweet in dataset so in this case we put 'out of dataset' for the required information of this user
            worksheet7.write(row, 0, um[0])
            worksheet7.write(row, 1, 'out of dataset') #since the user who is retweeted  most might not have a tweet in dataset so in this case we put 'out of dataset' for the required information of this user
            worksheet7.write(row, 2, um[1])
            worksheet7.write(row, 3, 'out of dataset') #since the user who is retweeted  most might not have a tweet in dataset so in this case we put 'out of dataset' for the required information of this user
            worksheet7.write(row, 4, 'out of dataset') #since the user who is retweeted  most might not have a tweet in dataset so in this case we put 'out of dataset' for the required information of this user
            worksheet7.write(row, 5, 'out of dataset') #since the user who is retweeted  most might not have a tweet in dataset so in this case we put 'out of dataset' for the required information of this user
            worksheet7.write(row, 6, 'out of dataset') #since the user who is retweeted  most might not have a tweet in dataset so in this case we put 'out of dataset' for the required information of this user


        row += 1

    # WordCloud of User mentioned  
    import matplotlib.pyplot as plt
    from wordcloud import WordCloud, STOPWORDS

    wordcloud_oho = WordCloud(width = 1000, height = 500, background_color = 'white').generate(' '.join(user_list))
    fig = plt.figure(figsize=(12,12),dpi=100) #here its not required to give high dpi
    plt.imshow(wordcloud_oho)
    plt.axis("off")
    plt.savefig (my_path + 'User_Mentioned.png',dpi=1000) # here we give high dpi to save figures with great quality
    plt.show()
# ----------------------------------------------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------------------------------------------
# finding the most 5 hashtags that were used most in the dataset
# ----------------------------------------------------------------------------------------------------------------------------------------------------------
def most_used_hashtags (worksheet8, H_N_L, my_path):
    hashtag_list = []
    worksheet8.write(0, 0, 'Hashtag Name') 
    worksheet8.write(0, 1, '#Count')     
    for i in H_N_L :
        if i != 'None' :
            for j in i :
                hashtag_list.append(j)
    row = 1
    most_hashtags_in_dataset = Counter(hashtag_list).most_common(10)            
    for hashtag_most in most_hashtags_in_dataset :
        worksheet8.write(row, 0, hashtag_most[0])
        worksheet8.write(row, 1, hashtag_most[1])        
        row += 1

    import matplotlib.pyplot as plt
    from wordcloud import WordCloud, STOPWORDS

    wordcloud_oho = WordCloud(width = 1000, height = 500, background_color = 'white').generate(' '.join(hashtag_list))
    fig = plt.figure(figsize=(12,12),dpi=100) #here its not required to give high dpi
    plt.imshow(wordcloud_oho)
    plt.axis("off")
    plt.savefig (my_path + 'hashtags.png',dpi=1000) # here we give high dpi to save figures with great quality
    plt.show()
# ----------------------------------------------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------------------------------------------
# finding the frequencies of use for different kinds of tweets in the dataset
# ----------------------------------------------------------------------------------------------------------------------------------------------------------
def types_of_tweets (worksheet9 ,Ret_N_L, Ret_C_L, Q_N_L, Rep_N_L,  tweet_number, my_path): #save data in excel sheet and also draw a pie plot

    worksheet9.write(0, 0, 'tweet_number')
    worksheet9.write(0, 1, 'PureTweet')
    worksheet9.write(0, 2, 'Retweet') 
    worksheet9.write(0, 3, 'Quote')
    worksheet9.write(0, 4, 'Reply') 
    worksheet9.write(0, 5, 'Retweet+Quote') 
    worksheet9.write(0, 6, 'Retweet+Reply') 
    worksheet9.write(0, 7, 'Retweet+Quote+Reply')
    worksheet9.write(0, 8, 'Quote+Reply')

    worksheet9.write(1, 0, tweet_number)
    worksheet9.write(2, 0, '100%')

    Ret_N_index_list = []
    Q_N_index_list = []
    Rep_N_index_list = []
    Ret_Q_N_index_list = []
    Ret_Rep_N_index_list = []
    Ret_Q_Rep_N_index_list = []
    Q_Rep_N_index_list = []
    
        
    for name in Ret_N_L:
        if name!= 'None' :
            Ret_N_index = Ret_N_L.index (name)
            Ret_N_index_list.append(Ret_N_index)

    for name in Q_N_L:
        if name!= 'None' :
            Q_N_index = Q_N_L.index (name)
            Q_N_index_list.append(Q_N_index)
            
    for name in Rep_N_L:
        if name!= 'None' :
            Rep_N_index = Rep_N_L.index (name)
            Rep_N_index_list.append(Rep_N_index)

    for index in Ret_N_index_list :
        if (index in Q_N_index_list) and (index in Rep_N_index_list) :
            Ret_Q_Rep_N_index_list.append(index)
            Ret_N_index_list.remove(index)
            Q_N_index_list.remove (index)
            Rep_N_index_list.remove (index)
        elif index in Q_N_index_list :
            Ret_Q_N_index_list.append(index)
            Ret_N_index_list.remove (index)
            Q_N_index_list.remove (index)
        elif index in Rep_N_index_list :
            Ret_Rep_N_index_list.append(index)
            Ret_N_index_list.remove (index)
            Rep_N_index_list.remove (index)

    for index in Q_N_index_list:
        if index in Rep_N_index_list:
            Q_Rep_N_index_list.append (index)
            Q_N_index_list.remove (index)
            Rep_N_index_list.remove (index)


    c = len(Ret_N_index_list)
    Ret_N_Percentage = (c/tweet_number)*100
    Ret_N_Percentage_st = str (round (Ret_N_Percentage,2)) + '%'
    worksheet9.write(1, 2, c)
    worksheet9.write(2, 2, Ret_N_Percentage_st)    

    d = len(Q_N_index_list)
    Q_N_Percentage = (d/tweet_number)*100
    Q_N_Percentage_st = str (round (Q_N_Percentage,2)) + '%'
    worksheet9.write(1, 3, d)
    worksheet9.write(2, 3, Q_N_Percentage_st)

    e = len(Rep_N_index_list)
    Rep_N_Percentage = (e/tweet_number)*100
    Rep_N_Percentage_st = str (round (Rep_N_Percentage,2)) + '%'
    worksheet9.write(1, 4, e)
    worksheet9.write(2, 4, Rep_N_Percentage_st)

    
    f = len(Ret_Q_N_index_list)
    Ret_Q_Percentage = (f/tweet_number)*100
    Ret_Q_Percentage_st = str (round (Ret_Q_Percentage,2)) + '%'
    worksheet9.write(1, 5, f)
    worksheet9.write(2, 5, Ret_Q_Percentage_st)


    g = len(Ret_Rep_N_index_list)
    Ret_Rep_Percentage = (g/tweet_number)*100
    Ret_Rep_Percentage_st = str (round (Ret_Rep_Percentage,2)) + '%'
    worksheet9.write(1, 6, g)
    worksheet9.write(2, 6, Ret_Rep_Percentage_st)

    h = len(Ret_Q_Rep_N_index_list)
    Ret_Q_Rep_N_Percentage = (h/tweet_number)*100
    Ret_Q_Rep_N_Percentage_st = str (round (Ret_Q_Rep_N_Percentage,2)) + '%'
    worksheet9.write(1, 7, h)
    worksheet9.write(2, 7, Ret_Q_Rep_N_Percentage_st)
    

    i = len(Q_Rep_N_index_list)
    Q_Rep_N_Percentage = (i/tweet_number)*100
    Q_Rep_N_Percentage_st = str (round (Q_Rep_N_Percentage,2)) + '%'
    worksheet9.write(1, 8, i)
    worksheet9.write(2, 8, Ret_Q_Rep_N_Percentage_st)

    pure_tweets = tweet_number - c - d - e - f - g - h - i
    pure_tweets_percentage = (pure_tweets/tweet_number)*100
    pure_tweets_percentage_st = str (round (pure_tweets_percentage,2)) + '%'
    worksheet9.write(1, 1, pure_tweets)
    worksheet9.write(2, 1, pure_tweets_percentage_st)

    import matplotlib.pyplot as plt

    # for having a pie plot we need two things : labels and values (sizes) which we get by the following codes
    # labels
    labels = []
    if pure_tweets != 0 :
        labels.append ('Pure')
    if c != 0 :
        labels.append ('Retweet')
    if d != 0 :
        labels.append ('Quote')
    if e != 0 :
        labels.append ('Reply')
    if f != 0 :
        labels.append ('Retweet&Quote')
    if g != 0 :
        labels.append ('Retweet&Reply')
    if h != 0 :
        labels.append ('Retweet&Quote&Reply')
    if i != 0 :
        labels.append ('Quote&Reply')

    # sizes
    sizes = []
    if pure_tweets != 0 :
        sizes.append (pure_tweets)
    if c != 0 :
        sizes.append (c)
    if d != 0 :
        sizes.append (d)
    if e != 0 :
        sizes.append (e)
    if f != 0 :
        sizes.append (f)
    if g != 0 :
        sizes.append (g)
    if h != 0 :
        sizes.append (h)
    if i != 0 :
        sizes.append (i)

    fig = plt.figure(figsize = (8,6),dpi=100) #here its not required to give high dpi
    fig = plt.pie(sizes, autopct='%1.1f%%')
    patches, texts = plt.pie(sizes)
    plt.legend(patches, labels, loc="best")
    plt.axis('equal')
    plt.savefig(my_path + 'type_tweets.png', dpi=1000)# here we give high dpi to save figures with great quality
    plt.show()
# ----------------------------------------------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------------------------------------------
# finding information about date and time of the dataset
# ----------------------------------------------------------------------------------------------------------------------------------------------------------    
def seperate_tweets_by_day (D_T_P_L): #this function seperate tweets by day, in other word all tweets that published in a same day get togather as a list, so each list include all tweets published in a specific day, and seperate_days (the result of this function) will be a list (list of lists) which includes all the mentioned lists  

    seperate_days = []
    today = []
    current = []
    current.append(D_T_P_L[0][0])
    current.append(D_T_P_L[0][1])
    current.append(D_T_P_L[0][2])

    


    for date_time_processed_each in D_T_P_L :

        if (date_time_processed_each[0] == current[0] and date_time_processed_each[1] == current[1] and date_time_processed_each[2] == current[2]):
            today.append (date_time_processed_each)
 
        else :
            seperate_days.append(today)
            today = []
            today.append (date_time_processed_each)
            current = []
            current.append (date_time_processed_each[0])
            current.append (date_time_processed_each[1])
            current.append (date_time_processed_each[2])


    seperate_days.append(today)


    return seperate_days

#-------
def month_name_to_integer (month_name): #no need to explain (we use this function in the function of "calculating_period_of_dataset") :)
    if month_name == 'Jan' :
        month_integer = 1
    if month_name == 'Feb' :
        month_integer = 2
    if month_name == 'Mar' :
        month_integer = 3
    if month_name == 'Apr' :
        month_integer = 4
    if month_name == 'May' :
        month_integer = 5
    if month_name == 'Jun' :
        month_integer = 6
    if month_name == 'Jul' :
        month_integer = 7
    if month_name == 'Aug' :
        month_integer = 8
    if month_name == 'Sep' :
        month_integer = 9
    if month_name == 'Oct' :
        month_integer = 10
    if month_name == 'Nov' :
        month_integer = 11
    if month_name == 'Dec' :
        month_integer = 12

    return month_integer

#-------
def Date_Time_Analysis (worksheet10, D_T_P_L, tweet_number, my_path, worksheet11, worksheet12): #this function calculates the total number of days it last from the first tweet of dataset to the last tweet of dataset (in other word the difference between the date of first tweet of dataset and the date of the last tweet of the dataset in terms of day)
    worksheet10.write(0, 0, 'First Date')
    worksheet10.write(0, 1, 'Last Date') 
    worksheet10.write(0, 2, 'Duration of Dataset (Days)')
    worksheet10.write(0, 3, '#Inactive Days')
    worksheet10.write(0, 4, 'mean tweet/activeday')
    worksheet10.write(0, 5, 'Duration of Dataset (Hours)')
    worksheet10.write(0, 6, '#Inactive Hours')
    worksheet10.write(0, 7, 'mean tweet/activehour')

    # day analysis ---
    total_period_of_dataset_in_hours = day_analysis (worksheet10 ,D_T_P_L, tweet_number, my_path, worksheet11)
    #-----------------
    # hour analysis --
    hour_analysis (worksheet10, D_T_P_L, tweet_number, total_period_of_dataset_in_hours, my_path, worksheet12) 
    # ----------------
    
##    return total_period_of_dataset, first_date, last_date, active_days_number, mean_tweet_per_day
#------
def day_analysis (worksheet10, D_T_P_L, tweet_number, my_path, worksheet11):
    import matplotlib.pyplot as plt
    from datetime import datetime
    from dateutil import relativedelta
    
    
    first_date = [] #date and time of the first tweet of dataset (begining of tweets related to the dataset), the format is  [year,month,day,hour,minute]
    end_data = len(D_T_P_L) - 1
    year_integer = int(D_T_P_L[end_data][0])
    first_date.append(year_integer)
    month_integer = month_name_to_integer (D_T_P_L[end_data][1])
    first_date.append(month_integer)
    day_integer = int(D_T_P_L[end_data][2])
    first_date.append(day_integer)
    hour_str = D_T_P_L[end_data][3][0] + D_T_P_L[end_data][3][1]
    hour_integer_first = int (hour_str)
    first_date.append(hour_integer_first)
    min_str = D_T_P_L[end_data][3][3] + D_T_P_L[end_data][3][4]
    min_integer_first = int (min_str)
    first_date.append(min_integer_first)

    
    last_date = [] #date and time of the last tweet of dataset which is very close to the date and time of capturing dataset, the format is  [year,month,day,hour,minute]
    year_integer = int(D_T_P_L[0][0])
    last_date.append(year_integer)
    month_integer = month_name_to_integer (D_T_P_L[0][1])
    last_date.append(month_integer)
    day_integer = int(D_T_P_L[0][2])
    last_date.append(day_integer)
    hour_str = D_T_P_L[0][3][0] + D_T_P_L[0][3][1]
    hour_integer_last = int (hour_str)
    last_date.append(hour_integer_last)
    min_str = D_T_P_L[0][3][3] + D_T_P_L[0][3][4]
    min_integer_last = int (min_str)
    last_date.append(min_integer_last)
    day_info = []
    day_info_1 = []
    day_info_2 = []
    y = []
    x = []
    x_str = []


    d_first = datetime(first_date[0], first_date[1], first_date[2], first_date[3], first_date[4])
    d_last = datetime(last_date[0], last_date[1], last_date[2], last_date[3], last_date[4])
    delta = relativedelta.relativedelta(d_last,d_first)

    #to know how many days the dataset covers (notice that delta.days gives us the number of days in term of 24 hours, for example if the first tweet of dataset is for [2017,12,13,18,33] and the last tweet is for [2017,12,15,6,24] then delta.days gives us 1 (because the difference between them is 36 hours which gives (1(24) + 12) means 1 day and some hours, but as we see it covers three days (13 dec, 14 dec, 15 dec) and we want to show 3 days (as total period of dataset in days) not 1 day! so we use the following codes the get that) 
    if (hour_integer_first + delta.hours) < 24 :
        total_period_of_dataset_in_days = delta.days + 1
    else :
        total_period_of_dataset_in_days = delta.days + 2
    #------------------------------------------------------------

    #to know how many days the dataset covers (notice that delta.days gives us the number of hours in term of 60 minutes, for example if the first tweet of dataset is for [2017,12,15,19,50] and the last tweet is for [2017,12,15,21,20] then delta.hours gives us 1 (because the difference between them is 90 minutes which gives (1(60) + 30) means 1 hour and some minutes, but as we see it covers three hours (19, 20, 21) and we want to show 3 hours (as total period of dataset in hours) not 1 hour! so we use the following codes the get that) 
    if (min_integer_first + delta.minutes) < 60 :
        total_period_of_dataset_in_hours = delta.days*24 + delta.hours + 1
    else :
        total_period_of_dataset_in_hours = delta.days*24 + delta.hours + 2
    #------------------------------------------------------------
        
 
    
    seperate_days = seperate_tweets_by_day (D_T_P_L)
    active_days_number = len(seperate_days)
    inactive_days_number = total_period_of_dataset_in_days - active_days_number 
    mean_tweet_per_day = round(tweet_number/active_days_number,2)


    for d in seperate_days :
        d_i = []
        d_i_2 = [] 
        number_tweet_in_day = len (d)
        the_date = d[0][0] + "_" + d[0][1] + "_" + d[0][2]
        month_num = month_name_to_integer (d[0][1]) 
        the_date_2 = d[0][0] + "/" + str (month_num) + "/" + d[0][2] 
        d_i.append (the_date)
        d_i_2.append (the_date_2) 
        d_i.append (number_tweet_in_day)
        d_i_2.append (number_tweet_in_day) 
        day_info_1.append (d_i)  #day_info_1 = [[day(date), number of tweets in the day], [previous day, number of tweets in the day] , ...]]
        day_info_2.append (d_i_2) 
            

    list.reverse (day_info_2) #because we started to capture tweets from the last tweet in our time and went back through the time, now for ploting we need to start from the begining time so we inverse the list

#------------------------------------------------------------
    # adding empty days to the day_info ------------------------------
    date_format = "%Y/%m/%d"
    ww = 0
    empty_days = []
    empty_days_t = []
    while ww < len (day_info_2):
        if ww != 0:
            aa = datetime.strptime (day_info_2[ww][0], date_format) - datetime.strptime (day_info_2[ww-1][0], date_format)
            if aa.days > 1 :
                empty_days.append (ww-1)
                empty_days.append (aa.days - 1)
                empty_days_t.append (empty_days) # gives us [x,y] in which x is the (index-1) of a place in day_info that we need to insert y empty days, for example : empty_days_t = [[x,y],[s,u]] means we have two gaps in the dataset one index x for y epmty days and the other in the index of s for u empty days
                empty_days = []
    
        ww += 1
        
    day_info_t = []
    from datetime import timedelta
    nd_n = 1
    new_day_list = []
    case_index = []
    for case in empty_days_t :
        ttt = 0
        d_i_i = []
        new_day = []
        cc = 1
        ttt = 1
        case_index.append (case[0])
        new_case_list = []
        while ttt < (case[1] + 1) :            
            day_info_t_c = day_info_2 [:]
            new_date = datetime.strptime (day_info_2[case[0]][0], date_format) + timedelta(days=ttt)
            new_date_str = new_date.strftime("%Y_%m_%d")
            d_i_i.append (new_date_str)
            d_i_i.append (0)
            
            new_day.append (d_i_i)
            new_case_list.append (new_day)
            d_i_i = []
            new_day = []
            ttt += 1

        new_day_list.append  (new_case_list)

    
    list.reverse (day_info_1)
    uu = 0
    for case_set in new_day_list :
        for nd in case_set:
            day_info_1 = day_info_1[:(case_index[uu] + nd_n)] + nd + day_info_1[(case_index[uu] + nd_n):]
            nd_n += 1
        uu += 1
        
#------------------------------------------------------------
            
    fff = 0
    for di in day_info_1:
        y.append(di[1])
        N = len(y)
        x.append(fff)
        x_str.append(str(fff))
        fff += 1

    fig = plt.figure(figsize=(8,6),dpi=100) #here its not required to give high dpi
    plt.bar(x, y, width=0.5, color="green")
    plt.xticks(x , x_str) # this is for avoiding the show of other numbers on the x axis except the number of exact hours
    plt.xlabel('time (day)')
    plt.ylabel('number of tweets')
    plt.savefig (my_path + 'time_day.png',dpi=1000) # here we give high dpi to save figures with great quality
    plt.show()
    
    

    worksheet10.write(1, 0, ','.join(D_T_P_L[end_data]))
    worksheet10.write(1, 1, ','.join(D_T_P_L[0])) 
    worksheet10.write(1, 2, total_period_of_dataset_in_days)
    worksheet10.write(1, 3, inactive_days_number)
    worksheet10.write(1, 4, mean_tweet_per_day)


    # The output of this big function is hour_info_1 which gives us [['date', #tweet], ... ] (for example like this : [['2018_Jan_05', 301], ...]) (sure with days with 0 tweet inside, for example ['2018_Jan_03', 0]) 
    # Here we write and save this information on sheet 12
    worksheet11.write(0, 0, 'Date')
    worksheet11.write(0, 1, '#tweet')

    hhh = 1
    for datetweet in day_info_1 :
        worksheet11.write(hhh, 0, datetweet[0])
        worksheet11.write(hhh, 1, datetweet[1])
        hhh += 1


    return total_period_of_dataset_in_hours
#------------------------------------------
def hour_analysis (worksheet10, D_T_P_L, tweet_number, total_period_of_dataset_in_hours, my_path, worksheet12): #this function seperate tweets by day, in other word all tweets that published in a same day get togather as a list, so each list include all tweets published in a specific day, and seperate_days (the result of this function) will be a list (list of lists) which includes all the mentioned lists  
    import matplotlib.pyplot as plt
    from datetime import datetime
    from dateutil import relativedelta
    seperate_hours = []
    hour = []
    hour_current = D_T_P_L[0][3][0] + D_T_P_L[0][3][1]
    hour_info_1 = []
    hour_info_2 = []
    y = []
    x = []
    x_str = []

    for date_time_processed_each in D_T_P_L :
        h_c = date_time_processed_each[3][0] + date_time_processed_each[3][1]

        if h_c == hour_current :
            hour.append (date_time_processed_each)
 
        else :
            seperate_hours.append(hour)
            hour = []
            hour.append (date_time_processed_each)
            hour_current = []
            hour_current = date_time_processed_each[3][0] + date_time_processed_each[3][1]


    seperate_hours.append(hour)

#---------------------------------------------------
    for h in seperate_hours :
        h_i = []
        h_i_2 = [] 
        number_tweet_in_hour = len (h)
        the_time = h[0][0] + "_" + h[0][1] + "_" + h[0][2] + " " + h [0][3][0] + h [0][3][1]
        
        month_num = month_name_to_integer (h[0][1]) 
        the_time_2 = h[0][0] + "/" + str (month_num) + "/" + h[0][2] + " " + h [0][3][0] + h [0][3][1] 
        h_i.append (the_time)
        h_i_2.append (the_time_2) 
        h_i.append (number_tweet_in_hour)
        h_i_2.append (number_tweet_in_hour) 
        hour_info_1.append (h_i)  #hour_info_1 = [[hour(time), number of tweets in the hour], [previous hour, number of tweets in the hour] , ...]]
        hour_info_2.append (h_i_2) 
             
    list.reverse (hour_info_2) #because we started to capture tweets from the last tweet in our time and went back through the time, now for ploting we need to start from the begining time so we inverse the list
#--------------------------------------------------

# adding empty hours to the hour_info ------------------------------
    date_format = '%Y/%m/%d %H'
    ww = 0
    empty_hours = []
    empty_hours_t = []
    while ww < len (hour_info_2):
        if ww != 0:
            aa = datetime.strptime (hour_info_2[ww][0], date_format) - datetime.strptime (hour_info_2[ww-1][0], date_format)
            hours_diff = (aa.total_seconds())//3600
            if hours_diff > 1 :
                empty_hours.append (ww-1)
                empty_hours.append (hours_diff - 1)
                empty_hours_t.append (empty_hours) # gives us [x,y] in which x is the (index-1) of a place in hour_info_1 that we need to insert y empty days, for example : empty_days_t = [[x,y],[s,u]] means we have two gaps in the dataset one index x for y epmty days and the other in the index of s for u empty days
                empty_hours = []
    
        ww += 1
         
    hour_info_t = []
    from datetime import timedelta
    nd_n = 1
    new_hour_list = []
    case_index = []
    for case in empty_hours_t :
        ttt = 0
        d_i_i = []
        new_hour = []
        cc = 1
        ttt = 1
        case_index.append (case[0])
        new_case_list = []
        while ttt < (case[1] + 1) :            
            hour_info_t_c = hour_info_2 [:]
            new_date = datetime.strptime (hour_info_2[case[0]][0], date_format) + timedelta(hours=ttt)
            new_date_str = new_date.strftime("%Y_%m_%d %H")
            d_i_i.append (new_date_str)
            d_i_i.append (0)
            
            new_hour.append (d_i_i)
            new_case_list.append (new_hour)
            d_i_i = []
            new_hour = []
            ttt += 1

        new_hour_list.append  (new_case_list)

    list.reverse (hour_info_1)
    uu = 0
    for case_set in new_hour_list :
        for nd in case_set:
            hour_info_1 = hour_info_1[:(case_index[uu] + nd_n)] + nd + hour_info_1[(case_index[uu] + nd_n):]
            nd_n += 1
        uu += 1
    

    
###---------------------------------------------------
##  
    fff = 0
    for hi in hour_info_1:
        y.append(hi[1])
        N = len(y)
        x.append(fff)
        if fff%24 == 0 : #because number of hours are huge and showing the label of all of them on the x=axis  is a mess, so we just show 0, 24 , 48 , ... labels on x-axis
            x_str.append(str(fff))
        else :
            x_str.append('')
            
        fff += 1
    fig = plt.figure(figsize=(8,6),dpi=100) #here its not required to give high dpi
    plt.bar(x, y,  width=0.5, color="blue")
    plt.xticks(x , x_str) # this is for avoiding the show of other numbers on the x axis except the number of exact hours
    plt.xlabel('time (hour)')
    plt.ylabel('number of tweets')
    plt.savefig (my_path + 'time_hour.png',dpi=1000) # here we give high dpi to save figures with great quality
    plt.show()

 
    number_active_hours = len (hour_info_1)
    number_inactive_hours = total_period_of_dataset_in_hours - number_active_hours  
    mean_tweet_per_active_hour = round (tweet_number/number_active_hours,2)
    
    worksheet10.write(1, 5, total_period_of_dataset_in_hours)
    worksheet10.write(1, 6, number_inactive_hours)
    worksheet10.write(1, 7, mean_tweet_per_active_hour)
    

    # The output of this big function is hour_info_1 which gives us [['date hour', #tweet], ... ] (for example like this : [['2017_Dec_30 19', 1], ... ,['2018_Jan_08 12', 1]]) 
    # Here we write and save this information on sheet 12
    worksheet12.write(0, 0, 'Date Hour')
    worksheet12.write(0, 1, '#tweet')

    hhh = 1
    for datehourtweet in hour_info_1 :
        worksheet12.write(hhh, 0, datehourtweet[0])
        worksheet12.write(hhh, 1, datehourtweet[1])
        hhh += 1
        
        


#---------------------------- M.A.I.N ------------------
#---------------------------- M.A.I.N ------------------
#---------------------------- M.A.I.N ------------------
def main ():
    #---- O.P.E.N ---- A.N.D --- R.E.A.D --- D.A.T.A.S.E.T --------
    fname_dataset = "D:\\Papers\\Social Network Mining\\Creating_Dataset\\Step5\\False Rumors\\False_Rumor_23\\Input\\Pro-ChoiceActivist.jsonl"  #be carefull, put \\ instead of \ between folders of address (as you see I've done it), and remember this line needs to be re_writed again for any new dataset according to the address of the new dataset 
    U_I_L = []
    S_N_L = []
    U_L_L = []
    Fo_C_L = []
    Fr_C_L = []
    D_T_P_L = []
    Fa_C_L = []
    Ret_N_L = []
    Ret_C_L = []
    Q_N_L = []
    Rep_N_L = []
    So_N_L = []
    H_N_L = []
    U_M_N_L = []
    T_Z = []
    L_A_O = []

    with open (fname_dataset,'r') as f :
        tweet_number = 0
        row = 1 #because row=0 is for titles of columns which we set in the following block of code lines (giving titles to columns of tables)
        my_path = 'D:\\Papers\\Social Network Mining\\Creating_Dataset\\Step5\\False Rumors\\False_Rumor_23\\Output\\'  #address for saving result files (this line need to be re write for new datasets according to the desired address we want to put the results in them)
        workbook = xlsxwriter.Workbook(my_path + 'excel_results.xlsx')

        # FOR SECTION 1 --------------------
        worksheet = workbook.add_worksheet()
        # ----------------------------------

        # FOR SECTION 2 --------------------
        worksheet2 = workbook.add_worksheet()
        worksheet3 = workbook.add_worksheet()
        worksheet4 = workbook.add_worksheet()
        worksheet5 = workbook.add_worksheet()
        worksheet6 = workbook.add_worksheet()
        worksheet7 = workbook.add_worksheet()
        worksheet8 = workbook.add_worksheet()
        worksheet9 = workbook.add_worksheet()
        worksheet10 = workbook.add_worksheet()
        worksheet11 = workbook.add_worksheet()
        worksheet12 = workbook.add_worksheet()
        testnumber = 0
        # -----------------------------------

        # FOR SECTION 1 --------------------
        #--- G.I.V.I.N.G -- T.I.T.L.E -- T.O -- C.O.L.U.M.N.S --- O.F --- T.A.B.L.E -----
        #--- D.A.T.A --- F.O.R --- U.S.E.R --- W.H.O -- P.U.B.L.I.S.H.E.D -- T.W.E.E.T --
        worksheet.write(0, 0, 'ID') #ID of the user
        worksheet.write(0, 1, 'Screen Name') #screen name of the user        
        worksheet.write(0, 2, 'Description') #description of the user
        worksheet.write(0, 3, '#Tweets') #number of tweets the user published 
        worksheet.write(0, 4, 'Date_time_creation_account') #date and time of the creation account by the user
        worksheet.write(0, 5, 'Language') #lang of the user
        worksheet.write(0, 6, 'Timezone') #timezone of the user        
        worksheet.write(0, 7, 'Location') #location that is claimed by the user (not nesessary the real location)
        worksheet.write(0, 8, '#Followers') #number of the follower the user has
        worksheet.write(0, 9, '#Friends') #number of users the user followes
        #--- D.A.T.A --- F.O.R ---- M.E.T.A.D.A.T.A --- O.F ---- T.W.E.E.T --------------
        worksheet.write(0, 10, 'Date&Time') #Date and Time in which the tweet was publishe
        worksheet.write(0, 11, '#Favorite') #number of like the tweet had gotten at the time of capturing 
        worksheet.write(0, 12, 'Retweeted Screen Name') #Screen name of the user whose tweet is retwitted by the current tweet
        worksheet.write(0, 13, '#Retweet') #number of times that the origin tweet (what the current tweet is a retweet of it) has been retweeted (till the time of capturing data)
        worksheet.write(0, 14, 'Another Tweet Inside') # value 1 if the current tweet has another tweet inside , value 0 if the current tweet does not have any other tweet inside 
        worksheet.write(0, 15, 'Quote Name') #the name of user whose tweet is quoted by the current tweet
        worksheet.write(0, 16, 'Reply name') #the name of user who published a tweet that the current tweet is a reply to it
        worksheet.write(0, 17, 'Source') #the source device used for publishing the current tweet
        worksheet.write(0, 18, 'Hashtags') #all hashtags used in the current tweet
        worksheet.write(0, 19, 'Mentioned Names') #all user names who have been mentioned in the current tweet (all users who are tagged)
        #--- D.A.T.A --- F.O.R ---- T.E.X.T -- O.F ---- T.W.E.E.T ------------------------
        worksheet.write(0, 20, 'Text')#the text of tweet
        worksheet.write(0, 21, 'Tweet ID')#the ID of tweet
        worksheet.write(0, 22, 'Retweet Text')#the text of Retweet
        worksheet.write(0, 23, 'Retweet ID')#the ID of Retweet
        worksheet.write(0, 24, 'Quote Text')#the text of Quote
        worksheet.write(0, 25, 'Quote ID')#the ID of Quote
        worksheet.write(0, 26, 'Reply ID')#the ID of Reply
        # -----------------------------------


        # --- SECTION 1  --------------------
        #--- R.E.A.D --- E.A.C.H ---- T.W.E.E.T ---- S.E.P.E.R.A.T.E.L.Y -----------------
        test_number = 0
        
        for line in f:
                        
            # --- S   E   C   T   I   O    N      1   ----
            #--- G.E.T --- T.W.E.E.T.S --- F.R.O.M ---- D.A.T.A.S.E.T ----
            tweet_number += 1
            tweet = json.loads(line) #each line of jsonl is a separate tweet
            #-------------------------------------------------------------
                        
            #--- G.E.T --- U.S.E.R --- I.N.F.O --
            user_id,screen_name,user_location,followers_count,friends_count,statuses_count,description,timezone,lang,date_time_creation_account  = get_user_information(tweet)
            #-------------------------------------------------------------

                    
            #--- G.E.T --- M.E.T.A.D.A.T.A ---- T.W.E.E.T ----
            date_time_processed, favorite_count_sum, retweeted_screen_name, retweet_count, tweet_with_another_tweet_inside, name_quoter,  in_reply_to_screen_name, source, all_hashtags_seperatly, user_mentions_screen_name = get_meta_data (tweet)


            #--- G.E.T --- T.E.X.T ----- T.W.E.E.T -----------
            tweet_text_OK, tweet_id = get_text (tweet)
            retweeted_full_text_OK , retweet_id = get_retweeted_text (tweet)
            quoted_full_text_OK, quote_id = get_quoted_text (tweet)
            reply_id = get_reply_text_id (tweet)

                            
            #--- W.R.I.T.H --- D.A.T.A --------
            worksheet.write(row, 0, user_id)
            worksheet.write(row, 1, screen_name)
            worksheet.write(row, 2, description) #description of the user
            worksheet.write(row, 3, statuses_count) #number of tweets the user published 
            worksheet.write(row, 4, ' , '.join(date_time_creation_account)) #date and time of the creation account by the user
            worksheet.write(row, 5, lang) #lang of the user
            worksheet.write(row, 6, timezone) #timezone of the user
            worksheet.write(row, 7, user_location)
            worksheet.write(row, 8, followers_count)
            worksheet.write(row, 9, friends_count)
            worksheet.write(row, 10,  ','.join(map(str, date_time_processed)))#','.join(map(str, x)) is for changing a list with int inside to a string
            worksheet.write(row, 11,  favorite_count_sum)
            worksheet.write(row, 12,  ''.join(retweeted_screen_name)) #''.join(x) if for changing list to string
            worksheet.write(row, 13,  retweet_count)
            worksheet.write(row, 14,  tweet_with_another_tweet_inside)
            worksheet.write(row, 15,  ''.join(name_quoter)) #''.join(x) if for changing list to string
            worksheet.write(row, 16, ''.join(in_reply_to_screen_name)) #''.join(x) if for changing list to string
            worksheet.write(row, 17, ''.join(source)) #''.join(x) if for changing list to string
            worksheet.write(row, 18, ','.join(all_hashtags_seperatly)) #''.join(x) if for changing list to string
            worksheet.write(row, 19, ','.join(user_mentions_screen_name)) #''.join(x) if for changing list to string
            worksheet.write(row, 20, tweet_text_OK)
            worksheet.write(row, 21, tweet_id)
            worksheet.write(row, 22, retweeted_full_text_OK)
            worksheet.write(row, 23, retweet_id)
            worksheet.write(row, 24, quoted_full_text_OK)
            worksheet.write(row, 25, quote_id)
            worksheet.write(row, 26, reply_id)                
            # ----------------------------------

            # --- SECTION 2   --------------
            #--- P.U.T.T.I.N.G -- D.A.T.A -- I.N -- L.I.S.T -- F.O.R -- G.E.N.E.R.A.L -- A.N.A.L.Y.S.I.S
            #-------------------------------------------------------------------
            U_I_L.append (user_id)
            #--------------------------
            S_N_L.append (screen_name)
            #--------------------------
            if timezone :                
                T_Z.append (timezone)
            else :
                T_Z.append ('None')    
            #--------------------------
            from langcodes import Language
            if lang == 'zh-CN' :
                lang_converted = 'ChinaChinese'
            elif lang == 'zh-SG' :
                lang_converted = 'SingaporeChinese'
            elif lang == 'zh-TW' :
                lang_converted = 'TaiwanChinese'
            elif lang == 'zh-HK' :
                lang_converted = 'HongKongChinese'
            else :
                lang_converted = Language.make(language=lang).language_name() #convert for example 'sv' to 'swedish'

            words = word_tokenize(lang_converted)
            words_sticked = ''.join(words)
            L_A_O.append (words_sticked)
            #--------------------------
            if user_location :
                U_L_L.append (user_location)
            else :
                U_L_L.append ('None')
            #--------------------------
            Fo_C_L.append (followers_count)
            #--------------------------
            Fr_C_L.append (friends_count)
            #--------------------------
            if date_time_processed :
                D_T_P_L.append (date_time_processed[0])
            else :
                D_T_P_L.append ('None')

            #--------------------------
            Fa_C_L.append(favorite_count_sum)
            #--------------------------
            Ret_N = ''.join(retweeted_screen_name)
            if Ret_N :
                Ret_N_L.append (Ret_N)
            else :
                Ret_N_L.append ('None')
            #--------------------------
            Ret_C_L.append (retweet_count)
            #--------------------------
            Q_N = ''.join(name_quoter)
            if Q_N :
                Q_N_L.append (Q_N)
            else :
                Q_N_L.append ('None')
            #--------------------------
            Rep_N = ''.join(in_reply_to_screen_name)
            if Rep_N :
                Rep_N_L.append (Rep_N)
            else :
                Rep_N_L.append ('None')
            #--------------------------
            if source :
                So_N_L.append (source[0])
            else :
                So_N_L.append ('None')
            #--------------------------
            if all_hashtags_seperatly :
                H_N_L.append (all_hashtags_seperatly)
            else :
                H_N_L.append ('None')
            #--------------------------    
            if user_mentions_screen_name :
                U_M_N_L.append (user_mentions_screen_name)
            else :
                U_M_N_L.append ('None')
            #--------------------------
                            

            #--- going to next line in excel file ---
            row += 1
            if row%100 == 0 :  # just to know the program is in which state during run of the program (perticularly for huge input files that takes a lot of time)
                print (row)
            test_number += 1


        # --- SECTION 2   --------------
        most_active_user_spreader (worksheet2, U_I_L, S_N_L, Ret_N_L, U_L_L, Fo_C_L, Fr_C_L, So_N_L, my_path)
        most_timezone_used (worksheet3, T_Z, my_path)
        most_official_language_used (worksheet4, L_A_O, my_path)
        most_retweeted_user (worksheet5, U_I_L, S_N_L, Ret_N_L, U_L_L, Fo_C_L, Fr_C_L, So_N_L, my_path)
        most_source_mentioned (worksheet6, So_N_L, my_path)
        most_user_mentioned (worksheet7, U_I_L, S_N_L, Ret_N_L, U_L_L, Fo_C_L, Fr_C_L, So_N_L, U_M_N_L, my_path)
        most_used_hashtags (worksheet8, H_N_L, my_path)
        types_of_tweets (worksheet9 ,Ret_N_L, Ret_C_L, Q_N_L, Rep_N_L,  tweet_number, my_path)
        Date_Time_Analysis (worksheet10, D_T_P_L, tweet_number, my_path,  worksheet11, worksheet12)
        # -------------------------------


        workbook.close()
#----------------------------------------------
#----------------------------------------------
#----------------------------------------------

                
main()
input (" press any key to exit ... ")
