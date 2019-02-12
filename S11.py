#-------------------------------------------
#This program calculates influence and engagement for pure users of each of six category introduced by the previous program
#-------------------------------------------
def main ():
    import xlrd
    import xlsxwriter
    import numpy as np
    import tweepy
    import time
    import math
    import random
    from tweepy import API
    from tweepy import Cursor
    from tweepy import OAuthHandler

    
    #Reading ------------------
    my_path_R = 'D:\\Papers\\Social Network Mining\\Analysis_of_Rumor_Dataset\\Step 11\\Rumor_25\\Input\\'
    workbook_input = xlrd.open_workbook(my_path_R + 'Results_Step_10.xlsx')
    worksheet4_input = workbook_input.sheet_by_name('Sheet4')
    #---
    Pure_Origin_Rumor_Screen_Name = worksheet4_input.col_values(0) #cat = 1
    while '' in Pure_Origin_Rumor_Screen_Name:
        Pure_Origin_Rumor_Screen_Name.remove('')
    Pure_Origin_AntiRumor_Screen_Name = worksheet4_input.col_values(1) #cat = 2
    while '' in Pure_Origin_AntiRumor_Screen_Name:
        Pure_Origin_AntiRumor_Screen_Name.remove('')
    Pure_Retwitter_Rumor_Screen_Name = worksheet4_input.col_values(2) #cat = 3
    while '' in Pure_Retwitter_Rumor_Screen_Name:
        Pure_Retwitter_Rumor_Screen_Name.remove('')
    Pure_Retwitter_AntiRumor_Screen_Name = worksheet4_input.col_values(3) #cat = 4
    while '' in Pure_Retwitter_AntiRumor_Screen_Name:
        Pure_Retwitter_AntiRumor_Screen_Name.remove('')
    Pure_Origin_RumorRelated_Screen_Name = worksheet4_input.col_values(4) #cat = 5
    while '' in Pure_Origin_RumorRelated_Screen_Name:
        Pure_Origin_RumorRelated_Screen_Name.remove('')
    Pure_Retwitter_RumorRelated_Screen_Name = worksheet4_input.col_values(5) #cat = 6
    while '' in Pure_Retwitter_RumorRelated_Screen_Name:
        Pure_Retwitter_RumorRelated_Screen_Name.remove('')
        
    del Pure_Origin_Rumor_Screen_Name[0] #the first element is the label of the column, so we delete it
    del Pure_Origin_AntiRumor_Screen_Name[0] #the first element is the label of the column, so we delete it
    del Pure_Retwitter_Rumor_Screen_Name[0] #the first element is the label of the column, so we delete it
    del Pure_Retwitter_AntiRumor_Screen_Name[0] #the first element is the label of the column, so we delete it
    del Pure_Origin_RumorRelated_Screen_Name[0] #the first element is the label of the column, so we delete it
    del Pure_Retwitter_RumorRelated_Screen_Name[0] #the first element is the label of the column, so we delete it
    #---
    
    if len (Pure_Origin_Rumor_Screen_Name) > 128 :
        Pure_Origin_Rumor_Screen_Name_Final = random.sample (Pure_Origin_Rumor_Screen_Name,128) 
    else :
        Pure_Origin_Rumor_Screen_Name_Final = Pure_Origin_Rumor_Screen_Name

    if len (Pure_Origin_AntiRumor_Screen_Name) > 128 :
        Pure_Origin_AntiRumor_Screen_Name_Final = random.sample (Pure_Origin_AntiRumor_Screen_Name,128) 
    else :
        Pure_Origin_AntiRumor_Screen_Name_Final = Pure_Origin_AntiRumor_Screen_Name

    if len (Pure_Retwitter_Rumor_Screen_Name) > 256 :
        Pure_Retwitter_Rumor_Screen_Name_Final = random.sample (Pure_Retwitter_Rumor_Screen_Name,256)
    else :
        Pure_Retwitter_Rumor_Screen_Name_Final = Pure_Retwitter_Rumor_Screen_Name

    if len (Pure_Retwitter_AntiRumor_Screen_Name) > 256 :
        Pure_Retwitter_AntiRumor_Screen_Name_Final = random.sample (Pure_Retwitter_AntiRumor_Screen_Name,256)
    else :
        Pure_Retwitter_AntiRumor_Screen_Name_Final = Pure_Retwitter_AntiRumor_Screen_Name


    if len (Pure_Origin_RumorRelated_Screen_Name) > 32 :
        Pure_Origin_RumorRelated_Screen_Name_Final = random.sample (Pure_Origin_RumorRelated_Screen_Name,32)
    else :
        Pure_Origin_RumorRelated_Screen_Name_Final = Pure_Origin_RumorRelated_Screen_Name


    if len (Pure_Retwitter_RumorRelated_Screen_Name) > 32 :
        Pure_Retwitter_RumorRelated_Screen_Name_Final = random.sample (Pure_Retwitter_RumorRelated_Screen_Name,32)
    else :
        Pure_Retwitter_RumorRelated_Screen_Name_Final = Pure_Retwitter_RumorRelated_Screen_Name

    
    ALL_Screen_Name = Pure_Origin_Rumor_Screen_Name_Final + Pure_Origin_AntiRumor_Screen_Name_Final + Pure_Retwitter_Rumor_Screen_Name_Final + Pure_Retwitter_AntiRumor_Screen_Name_Final + Pure_Origin_RumorRelated_Screen_Name_Final + Pure_Retwitter_RumorRelated_Screen_Name_Final
    number_users = len (ALL_Screen_Name)
    print ("number_of_selected_users_to_crawl :", number_users)
    #--------------------------    
    #Writing ------------------
    my_path_W = 'D:\\Papers\\Social Network Mining\\Analysis_of_Rumor_Dataset\\Step 11\\Rumor_25\\Output\\'  #address for saving result files (this line need to be re write for new datasets according to the desired address we want to put the results in them)
    workbook_output = xlsxwriter.Workbook(my_path_W + 'Results_Step_11.xlsx')
    #------------------------
    worksheet1_output = workbook_output.add_worksheet() #Sheet 1 (Users with their data)
    worksheet1_output.set_column (0,7,45) #extend the width of columns 
    worksheet1_output.write(0, 0, "Screen Name")
    worksheet1_output.write(0, 1, "User Existence")
    worksheet1_output.write(0, 2, "Percentage of Pure Tweets")
    worksheet1_output.write(0, 3, "Favorited per Tweet")    
    worksheet1_output.write(0, 4, "Favorited per Follower")
    worksheet1_output.write(0, 5, "Retweeted per Tweet")
    worksheet1_output.write(0, 6, "Retweeted per Follower")
    worksheet1_output.write(0, 7, "User Category") 
    #--------------------------
    worksheet2_output = workbook_output.add_worksheet() #Sheet 2 (Users with their data)
    worksheet2_output.set_column (0,5,45) #extend the width of columns 
    worksheet2_output.write(0, 1, "Mean Percentage of Pure Tweets")
    worksheet2_output.write(0, 2, "Mean of Favorited per Tweet")    
    worksheet2_output.write(0, 3, "Mean of Favorited per Follower")
    worksheet2_output.write(0, 4, "Mean of Retweeted per Tweet")
    worksheet2_output.write(0, 5, "Mean of Retweeted per Follower")

    worksheet2_output.write(1, 0, "Pure_Origin_Rumor (Users of Cat1)")
    worksheet2_output.write(2, 0, "Pure_Origin_AntiRumor (Users of Cat2)")
    worksheet2_output.write(3, 0, "Pure_Retwitter_Rumor (Users of Cat3)")
    worksheet2_output.write(4, 0, "Pure_Retwitter_AntiRumor (Users of Cat4)")
    worksheet2_output.write(5, 0, "Pure_Origin_RumorRelated (Users of Cat5)")
    worksheet2_output.write(6, 0, "Pure_Retwitter_RumorRelated (Users of Cat6)")
    #--------------------------
    #Use your keys
    consumer_key = 'EVqx22v0Yb70v7zxY2szQkbmD'
    consumer_secret = 'zltJQ5ZtUfnoNIPAVzruV4E0y4N8JKwap7H5W1fGjw2WKoHjcP' 
    access_token = '771997625105219584-80jgMmbpd1t7SEEluUk2tTR1OmSL9mS'
    access_secret = 'v80pt8bYgbOhKOG6vkz4uHvlMbV188Uc20olxpbBwmacm'

    # OAuth process, using the keys and tokens
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    # Creation of the actual interface, using authentication
    api = tweepy.API(auth) 
    u = 0
    favorite_count_all = []
    retweet_count_all = []
    followers_count_all = []
    not_existed_users = []
    tweet_count_all = []
    NT = 200 # Numner of Tweets we crawl from each user (however part of these tweets are retweets or replys which we ignore them)
    print ("-------")
    while u < number_users :
        user_name = ALL_Screen_Name[u]
        print (u)
        print ("Screen_Name:",user_name)
        favorite_count = []
        retweet_count = []
        c = tweepy.Cursor(api.user_timeline, screen_name= user_name).items(NT)
        while True:
            try :
                tweet = c.next ()
                followers_count = tweet.user._json['followers_count']
                tweet_count = tweet.user._json['statuses_count']
                if (not tweet.in_reply_to_status_id) and (tweet._json['favorite_count'] != 0) : #this line eliminate all retweets and replies , and bring us just pure tweets :)
                    favorite_count.append(tweet._json['favorite_count'])
                    retweet_count.append(tweet._json['retweet_count'])
                                            
            except tweepy.TweepError as e:
                print (e) #this shows the error, if error is caused by the following three cases then we capture it and the program continues OTHERWISE the error stops the program however we can see what type of error it was and we can bring it here as the 4th case to capture in the program
                if 'Rate limit exceeded' in e.reason: #This line captures error resulted when rate limit is reached. it waits in durations of 100 sec till the rate limit is over.
                    print ('Rate limit reached, Do not worry :) just wait 15 min ...')
                    time.sleep(60*15)
                    continue
                    
                if 'Failed to send request:' in e.reason: #This line captures error resulted when the connection or VPN is lost.
                    print ('timeout error caught. machine goes to sleep for 100 seconds, Do not worry :) just make the Connection right...')
                    time.sleep(100)
                    continue
                
                if 'Sorry, that page does not exist.' or 'Not authorized.' in e.reason : #This line captures error resulted when the user is not existed anymore or his/her page is not authorized to access to 
                    print ("User Does not exist anymore ! ")
                    not_existed_users.append (user_name)
                    break
            
            except StopIteration:
                print("StopIteration : No more Tweets!")
                break

        favorite_count_all.append (favorite_count)
        retweet_count_all.append (retweet_count)
        followers_count_all.append (followers_count)
        if tweet_count < NT : #For when the number of published tweets (including tweet/retweet/reply/ ...) for the user is less than NT
            tweet_count_all.append (tweet_count)
        else :
            tweet_count_all.append (NT)
        
        print ("tweet_count :", tweet_count)
        print ("favorite_count :", favorite_count)
        print ("retweet_count :", retweet_count)        
        print ("followers_count :", followers_count)
        print ("-------")

        u += 1
    
    # W.R.I.T.I.N.G   T.H.E  R.E.S.U.L.T.S
    d = 0
    number_pure_tweet_all = []
    while d < number_users :
        number_pure_tweet_all.append(len(favorite_count_all[d]))
        d += 1
    d = 0
    Favorited_per_Tweet_all = []
    while d < number_users :
        Favorited_per_Tweet_all.append(np.mean(favorite_count_all[d]))
        d += 1
    d = 0
    Favorited_per_Follower_all = []
    while d < number_users :
        Favorited_per_Follower_all.append((np.mean(favorite_count_all[d]))/followers_count_all[d])
        d += 1
    d = 0
    Retweeted_per_Tweet_all = []
    while d < number_users :
        Retweeted_per_Tweet_all.append(np.mean(retweet_count_all[d]))
        d += 1
    d = 0
    Retweeted_per_Follower_all = []
    while d < number_users :
        Retweeted_per_Follower_all.append((np.mean(retweet_count_all[d]))/followers_count_all[d])
        d += 1
    d = 0
    #-------
    cat_perc_1 = []
    cat_perc_2 = []
    cat_perc_3 = []
    cat_perc_4 = []
    cat_perc_5 = []
    cat_perc_6 = []

    cat_fatw_1 = []
    cat_fatw_2 = []
    cat_fatw_3 = []
    cat_fatw_4 = []
    cat_fatw_5 = []
    cat_fatw_6 = []

    cat_fafo_1 = []
    cat_fafo_2 = []
    cat_fafo_3 = []
    cat_fafo_4 = []
    cat_fafo_5 = []
    cat_fafo_6 = []

    cat_rttw_1 = []
    cat_rttw_2 = []
    cat_rttw_3 = []
    cat_rttw_4 = []
    cat_rttw_5 = []
    cat_rttw_6 = []

    cat_rtfo_1 = []
    cat_rtfo_2 = []
    cat_rtfo_3 = []
    cat_rtfo_4 = []
    cat_rtfo_5 = []
    cat_rtfo_6 = []
    
    while d < number_users :
        worksheet1_output.write(d + 1, 0, ALL_Screen_Name [d])
        cat = 0
        if ALL_Screen_Name [d] in Pure_Origin_Rumor_Screen_Name :
            cat = 1
        elif ALL_Screen_Name [d] in Pure_Origin_AntiRumor_Screen_Name :
            cat = 2
        elif ALL_Screen_Name [d] in Pure_Retwitter_Rumor_Screen_Name :
            cat = 3
        elif ALL_Screen_Name [d] in Pure_Retwitter_AntiRumor_Screen_Name :
            cat = 4
        elif ALL_Screen_Name [d] in Pure_Origin_RumorRelated_Screen_Name :
            cat = 5
        elif ALL_Screen_Name [d] in Pure_Retwitter_RumorRelated_Screen_Name :
            cat = 6
            
        if ALL_Screen_Name [d] in not_existed_users :
            worksheet1_output.write(d + 1, 1, "NO")
            worksheet1_output.write(d + 1, 2, "NO")
            worksheet1_output.write(d + 1, 3, "NO")
            worksheet1_output.write(d + 1, 4, "NO")
            worksheet1_output.write(d + 1, 5, "NO")
            worksheet1_output.write(d + 1, 6, "NO")
            worksheet1_output.write(d + 1, 7, "NO")
        else :
            worksheet1_output.write(d + 1, 1, "YES")
            if not math.isnan(number_pure_tweet_all[d]/tweet_count_all[d]) and not math.isinf(number_pure_tweet_all[d]/tweet_count_all[d])  :
                worksheet1_output.write(d + 1, 2, (number_pure_tweet_all[d]/tweet_count_all[d]))
                if cat == 1 :
                    cat_perc_1.append (number_pure_tweet_all[d]/tweet_count_all[d])
                elif cat == 2 :
                    cat_perc_2.append (number_pure_tweet_all[d]/tweet_count_all[d])
                elif cat == 3 :
                    cat_perc_3.append (number_pure_tweet_all[d]/tweet_count_all[d])
                elif cat == 4 :
                    cat_perc_4.append (number_pure_tweet_all[d]/tweet_count_all[d])
                elif cat == 5 :
                    cat_perc_5.append (number_pure_tweet_all[d]/tweet_count_all[d])
                elif cat == 6 :
                    cat_perc_6.append (number_pure_tweet_all[d]/tweet_count_all[d])
                    
            else :
                worksheet1_output.write(d + 1, 2, "NAN/INF")
            
            if not math.isnan(Favorited_per_Tweet_all[d]) and not math.isinf(Favorited_per_Tweet_all[d])  :
                worksheet1_output.write(d + 1, 3, Favorited_per_Tweet_all[d])
                if cat == 1 :
                    cat_fatw_1.append (Favorited_per_Tweet_all[d])
                elif cat == 2 :
                    cat_fatw_2.append (Favorited_per_Tweet_all[d])
                elif cat == 3 :
                    cat_fatw_3.append (Favorited_per_Tweet_all[d])
                elif cat == 4 :
                    cat_fatw_4.append (Favorited_per_Tweet_all[d])
                elif cat == 5 :
                    cat_fatw_5.append (Favorited_per_Tweet_all[d])
                elif cat == 6 :
                    cat_fatw_6.append (Favorited_per_Tweet_all[d])
            else :
                worksheet1_output.write(d + 1, 3, "NAN/INF")
                
            if not math.isnan (Favorited_per_Follower_all[d]) and not math.isinf(Favorited_per_Follower_all[d])  : # this measure is good for comparing users
                worksheet1_output.write(d + 1, 4, Favorited_per_Follower_all[d])
                if cat == 1 :
                    cat_fafo_1.append (Favorited_per_Follower_all[d])
                elif cat == 2 :
                    cat_fafo_2.append (Favorited_per_Follower_all[d])
                elif cat == 3 :
                    cat_fafo_3.append (Favorited_per_Follower_all[d])
                elif cat == 4 :
                    cat_fafo_4.append (Favorited_per_Follower_all[d])
                elif cat == 5 :
                    cat_fafo_5.append (Favorited_per_Follower_all[d])
                elif cat == 6 :
                    cat_fafo_6.append (Favorited_per_Follower_all[d])
            else :
                worksheet1_output.write(d + 1, 4, "NAN/INF")

            if not math.isnan (Retweeted_per_Tweet_all[d]) and not math.isinf (Retweeted_per_Tweet_all[d]) : 
                worksheet1_output.write(d + 1, 5, Retweeted_per_Tweet_all[d])
                if cat == 1 :
                    cat_rttw_1.append (Retweeted_per_Tweet_all[d])
                elif cat == 2 :
                    cat_rttw_2.append (Retweeted_per_Tweet_all[d])
                elif cat == 3 :
                    cat_rttw_3.append (Retweeted_per_Tweet_all[d])
                elif cat == 4 :
                    cat_rttw_4.append (Retweeted_per_Tweet_all[d])
                elif cat == 5 :
                    cat_rttw_5.append (Retweeted_per_Tweet_all[d])
                elif cat == 6 :
                    cat_rttw_6.append (Retweeted_per_Tweet_all[d])
            else :
                worksheet1_output.write(d + 1, 5, "NAN/INF")

            if not math.isnan (Retweeted_per_Follower_all[d]) and not math.isinf (Retweeted_per_Follower_all[d])  : # this measure is good for comparing users
                worksheet1_output.write(d + 1, 6, Retweeted_per_Follower_all[d])
                if cat == 1 :
                    cat_rtfo_1.append (Retweeted_per_Follower_all[d])
                elif cat == 2 :
                    cat_rtfo_2.append (Retweeted_per_Follower_all[d])
                elif cat == 3 :
                    cat_rtfo_3.append (Retweeted_per_Follower_all[d])
                elif cat == 4 :
                    cat_rtfo_4.append (Retweeted_per_Follower_all[d])
                elif cat == 5 :
                    cat_rtfo_5.append (Retweeted_per_Follower_all[d])
                elif cat == 6 :
                    cat_rtfo_6.append (Retweeted_per_Follower_all[d])
            else :
                worksheet1_output.write(d + 1, 6, "NAN/INF")


            worksheet1_output.write(d + 1, 7, cat)
                
                
        d += 1

    if cat_perc_1 :
        worksheet2_output.write(1, 1, np.mean(cat_perc_1))
    else :
        worksheet2_output.write(1, 1, "NAN")
    if cat_perc_2 :
        worksheet2_output.write(2, 1, np.mean(cat_perc_2))
    else :
        worksheet2_output.write(2, 1, "NAN")
    if cat_perc_3 :
        worksheet2_output.write(3, 1, np.mean(cat_perc_3))
    else :
        worksheet2_output.write(3, 1, "NAN")
    if cat_perc_4 :
        worksheet2_output.write(4, 1, np.mean(cat_perc_4))
    else :
        worksheet2_output.write(4, 1, "NAN")
    if cat_perc_5 :
        worksheet2_output.write(5, 1, np.mean(cat_perc_5))
    else :
        worksheet2_output.write(5, 1, "NAN")
    if cat_perc_6 :
        worksheet2_output.write(6, 1, np.mean(cat_perc_6))
    else :
        worksheet2_output.write(6, 1, "NAN")



    if cat_fatw_1 :
        worksheet2_output.write(1, 2, np.mean(cat_fatw_1))
    else :
        worksheet2_output.write(1, 2, "NAN")
    if cat_fatw_2 :
        worksheet2_output.write(2, 2, np.mean(cat_fatw_2))
    else :
        worksheet2_output.write(2, 2, "NAN")
    if cat_fatw_3 :
        worksheet2_output.write(3, 2, np.mean(cat_fatw_3))
    else :
        worksheet2_output.write(3, 2, "NAN")
    if cat_fatw_4 :
        worksheet2_output.write(4, 2, np.mean(cat_fatw_4))
    else :
        worksheet2_output.write(4, 2, "NAN")
    if cat_fatw_5 :
        worksheet2_output.write(5, 2, np.mean(cat_fatw_5))
    else :
        worksheet2_output.write(5, 2, "NAN")
    if cat_fatw_6 :
        worksheet2_output.write(6, 2, np.mean(cat_fatw_6))
    else :
        worksheet2_output.write(6, 2, "NAN")


    if cat_fafo_1 :
        worksheet2_output.write(1, 3, np.mean(cat_fafo_1))
    else :
        worksheet2_output.write(1, 3, "NAN")
    if cat_fafo_2 :
        worksheet2_output.write(2, 3, np.mean(cat_fafo_2))
    else :
        worksheet2_output.write(2, 3, "NAN")
    if cat_fafo_3 :
        worksheet2_output.write(3, 3, np.mean(cat_fafo_3))
    else :
        worksheet2_output.write(3, 3, "NAN")
    if cat_fafo_4 :
        worksheet2_output.write(4, 3, np.mean(cat_fafo_4))
    else :
        worksheet2_output.write(4, 3, "NAN")
    if cat_fafo_5 :
        worksheet2_output.write(5, 3, np.mean(cat_fafo_5))
    else :
        worksheet2_output.write(5, 3, "NAN")
    if cat_fafo_6 :
        worksheet2_output.write(6, 3, np.mean(cat_fafo_6))
    else :
        worksheet2_output.write(6, 3, "NAN")


    if cat_rttw_1 :
        worksheet2_output.write(1, 4, np.mean(cat_rttw_1))
    else :
        worksheet2_output.write(1, 4, "NAN")
    if cat_rttw_2 :
        worksheet2_output.write(2, 4, np.mean(cat_rttw_2))
    else :
        worksheet2_output.write(2, 4, "NAN")
    if cat_rttw_3 :
        worksheet2_output.write(3, 4, np.mean(cat_rttw_3))
    else :
        worksheet2_output.write(3, 4, "NAN")
    if cat_rttw_4 :
        worksheet2_output.write(4, 4, np.mean(cat_rttw_4))
    else :
        worksheet2_output.write(4, 4, "NAN")
    if cat_rttw_5 :
        worksheet2_output.write(5, 4, np.mean(cat_rttw_5))
    else :
        worksheet2_output.write(5, 4, "NAN")
    if cat_rttw_6 :
        worksheet2_output.write(6, 4, np.mean(cat_rttw_6))
    else :
        worksheet2_output.write(6, 4, "NAN")
    

    if cat_rtfo_1 :
        worksheet2_output.write(1, 5, np.mean(cat_rtfo_1))
    else :
        worksheet2_output.write(1, 5, "NAN")
    if cat_rtfo_2 :
        worksheet2_output.write(2, 5, np.mean(cat_rtfo_2))
    else :
        worksheet2_output.write(2, 5, "NAN")
    if cat_rtfo_3 :
        worksheet2_output.write(3, 5, np.mean(cat_rtfo_3))
    else :
        worksheet2_output.write(3, 5, "NAN")
    if cat_rtfo_4 :
        worksheet2_output.write(4, 5, np.mean(cat_rtfo_4))
    else :
        worksheet2_output.write(4, 5, "NAN")
    if cat_rtfo_5 :
        worksheet2_output.write(5, 5, np.mean(cat_rtfo_5))
    else :
        worksheet2_output.write(5, 5, "NAN")
    if cat_rtfo_6 :
        worksheet2_output.write(6, 5, np.mean(cat_rtfo_6))
    else :
        worksheet2_output.write(6, 5, "NAN")
    

    workbook_output.close()
    
#-----------------------    
main ()
input ("press enter key to exit ...")

