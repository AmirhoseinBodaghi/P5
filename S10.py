#------------------------------------------------------------------------------------------------
# THIS PROGRAM GETS Divide users into the following categories :
    #1- Origin Spreaders of Rumor Tweet (Category 1)
    #2- Origin Spreaders of Anti-Rumor Tweet (Category 2)
    #3- Rumor Retwitter (Category 3)
    #4- Anti-Rumor Retwitter (Category 4)
    #5- Origin Spreaders of Rumor Related Tweet (Category 5)
    #6- Retwitter of Rumor Related Tweet (Category 6)

# Then for each user it gives us the following data in output sheet 1:
    #1- User ID
    #2- User Screen Name
    #3- Number of published Tweet as Origin Spreaders of Rumor (Category 1)
    #4- Number of published Tweet as Origin Spreaders of Anti-Rumor (Category 2)
    #5- Number of published Tweet as Rumor Retwitter (Category 3)
    #6- Number of published Tweet as Anti-Rumor Retwitter (Category 4)
    #7- Number of published Tweet as Origin Spreaders of Rumor Related Tweet (Category 5)
    #8- Number of published Tweet as Retwitter of Rumor Related Tweet (Category 6)
    #9- The ratio of Following to Follower
    #10- Number of days of membership
    #11- Mean of Published Tweet per Day
    #12- Negative score for The Description sentence
    #13- Positive score for The Description sentence
    #14- Compound score for The Description sentence

# Furthermore we give the following data for each category in output sheet 2:
    #1- Mean of the ratio of Following to Follower for all users in the category
    #2- Mean of number of days of membership for all users in the category
    #3- Mean of published Tweet per Day for all users in the category
    #4- Mean of negative score for The Description sentence for all users in the category
    #5- Mean of positive score for The Description sentence for all users in the category
    #6- Mean of compound score for The Description sentence for all users in the category

# Also we give the following data for Pure users in each category in output sheet 3: (for example "user a" who has 1 tweet in category 1 and 1 retweet in category 3 , will be cncidered in both Category 1 and Category 3 but will not be considered as a pure user in none of them, a pure user is a user who has tweets/retweets only in ONE category, for example user b who has 5 tweets in only category 2 and has no tweet/retweet in any other category is considered as a pure user for Category 2)
    #1- Mean of the ratio of Following to Follower for all PURE users in the category
    #2- Mean of number of days of membership for all PURE users in the category
    #3- Mean of published Tweet per Day for all PURE users in the category
    #4- Mean of negative score for The Description sentence for all PURE users in the category
    #5- Mean of positive score for The Description sentence for all PURE users in the category
    #6- Mean of compound score for The Description sentence for all PURE users in the category

# Finally we give the list of Pure users (list of screen names) in each category in sheet 4:
    #1- Screen names of all PURE users in the category 1
    #2- Screen names of all PURE users in the category 2
    #3- Screen names of all PURE users in the category 3
    #4- Screen names of all PURE users in the category 4
    #5- Screen names of all PURE users in the category 5
    #6- Screen names of all PURE users in the category 6
#------------------------------------------------------------------------------------------------
def tweet_per_day (date1, date2, number_tweets):
    from datetime import date
    from nltk import ngrams
    #making the first date into standard format
    i = 0
    unigrams = ngrams(date1.split(),1)
    for gram in unigrams :
        if i == 0 :
            d1_year = gram[0]
        elif i == 2 :
            month_name = gram[0]
            if month_name == 'Jan' :
                d1_month = 1
            if month_name == 'Feb' :
                d1_month = 2
            if month_name == 'Mar' :
                d1_month = 3
            if month_name == 'Apr' :
                d1_month = 4
            if month_name == 'May' :
                d1_month = 5
            if month_name == 'Jun' :
                d1_month = 6
            if month_name == 'Jul' :
                d1_month = 7
            if month_name == 'Aug' :
                d1_month = 8
            if month_name == 'Sep' :
                d1_month = 9
            if month_name == 'Oct' :
                d1_month = 10
            if month_name == 'Nov' :
                d1_month = 11
            if month_name == 'Dec' :
                d1_month = 12
        elif i == 4 :
            d1_day = gram[0]
        i += 1

    #making the second date into standard format
    d2_year = date2[2] + date2[3] + date2[4] + date2[5]
    month_name = date2[10] + date2[11] + date2[12]
    if month_name == 'Jan' :
        d2_month = 1
    if month_name == 'Feb' :
        d2_month = 2
    if month_name == 'Mar' :
        d2_month = 3
    if month_name == 'Apr' :
        d2_month = 4
    if month_name == 'May' :
        d2_month = 5
    if month_name == 'Jun' :
        d2_month = 6
    if month_name == 'Jul' :
        d2_month = 7
    if month_name == 'Aug' :
        d2_month = 8
    if month_name == 'Sep' :
        d2_month = 9
    if month_name == 'Oct' :
        d2_month = 10
    if month_name == 'Nov' :
        d2_month = 11
    if month_name == 'Dec' :
        d2_month = 12
    d2_day = date2[17] + date2[18]

    
    d1 = date(int(d1_year),int(d1_month),int(d1_day))
    d2 = date (int(d2_year),int(d2_month),int(d2_day))
    number_days_membership = abs(d2-d1).days + 1 #we add 1 because if two dates be on a same day then it means 1 day (for example if the date of membership is 2017/2/23 and date of publishing tweet is 2017/2/23 , we count it as 1 day (even though it is less than one full day) 
    mean_tweet_per_day_full = number_tweets/number_days_membership
    mean_tweet_per_day = round(mean_tweet_per_day_full,3) # round the answer up to three decimal digit   

    return number_days_membership,mean_tweet_per_day

#------------------------------------
#This funstion analyse description sentence in the profile of users in terms of being negative (negative_score) or being positive (positive_score) or how much positive or negative (compound_score) the sentence is 
def Description_Analysis (description) :
    import nltk
    import nltk.sentiment.vader
    from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
    sid = SIA()
    ps = sid.polarity_scores(description)
    negative_score = ps.get ('neg') # shows the proportion of sentence that is negative (close to percentage of negative words in the sentence)
    positive_score = ps.get ('pos') # shows the proportion of sentence that is postive (close to percentage of positive words in the sentence)
    neutral_score = ps.get ('neu') # shows the proportion of sentence that is neutral (note: negative_score + positive_score + neutral_score = 1)
    compound_score = ps.get ('compound') #shows the intensity of positive being or negative being of the sentence, +1 for the most postive sentense and -1 for the most negative sentence (for example "amir is an excellent boy" has compound_score = 0.57 but "amir is a good boy" has compound_score = 0.44 because "excellent" is more intensed than "good") 
    return negative_score, positive_score, compound_score
#------------------------------------    

def main ():
    #Reading
    import xlrd
    import xlsxwriter
    import numpy as np

    
    #Reading ------------------
    my_path_R = 'D:\\Papers\\Social Network Mining\\Analysis_of_Rumor_Dataset\\Step 10\\Rumor_20\\Input\\'
    workbook_input = xlrd.open_workbook(my_path_R + 'DATASET.xlsx')
    worksheet1_input = workbook_input.sheet_by_name('Sheet1')
    worksheet9_input = workbook_input.sheet_by_name('Sheet9') #for reading number of tweets the dataset has
    #--------------------------
    
    #Writing ------------------
    my_path_W = 'D:\\Papers\\Social Network Mining\\Analysis_of_Rumor_Dataset\\Step 10\\Rumor_20\\Output\\'  #address for saving result files (this line need to be re write for new datasets according to the desired address we want to put the results in them)
    workbook_output = xlsxwriter.Workbook(my_path_W + 'Results_Step_10.xlsx')

    #------------------------
    worksheet1_output = workbook_output.add_worksheet() #Sheet 1 (Users with their data)
    worksheet1_output.set_column (0,15,45) #extend the width of columns 
    worksheet1_output.write(0, 0, "ID")
    worksheet1_output.write(0, 1, "Screen Name")
    worksheet1_output.write(0, 2, "Number of being as Origin Spreader of Rumor")
    worksheet1_output.write(0, 3, "Number of being as Origin Spreader of Anti-Rumor")
    worksheet1_output.write(0, 4, "Number of being as Rumor Retwitter")
    worksheet1_output.write(0, 5, "Number of being as Anti-Rumor Retwitter")
    worksheet1_output.write(0, 6, "Number of being as Origin Spreaders of Rumor Related Tweet")
    worksheet1_output.write(0, 7, "Number of being as Retwitter of Rumor Related Tweet")
    worksheet1_output.write(0, 8, "Following to Follower")
    worksheet1_output.write(0, 9, "days of membership")
    worksheet1_output.write(0, 10, "Mean of Published Tweet per Day")
    worksheet1_output.write(0, 11, "Negative score for The Description sentence")
    worksheet1_output.write(0, 12, "Positive score for The Description sentence")
    worksheet1_output.write(0, 13, "Compound score for The Description sentence")
    worksheet1_output.write(0, 14, "Number of Followers")
    worksheet1_output.write(0, 15, "Number of Followings")
    #--------------------------
    worksheet2_output = workbook_output.add_worksheet() #Sheet 2 (The mean results in each Category)
    worksheet2_output.set_column (0,6,45) #extend the width of columns 
    worksheet2_output.write(0, 1, "Following to Follower")
    worksheet2_output.write(0, 2, "days of membership")
    worksheet2_output.write(0, 3, "Mean of Published Tweet per Day")
    worksheet2_output.write(0, 4, "Negative score for The Description sentence")
    worksheet2_output.write(0, 5, "Positive score for The Description sentence")
    worksheet2_output.write(0, 6, "Compound score for The Description sentence")
    worksheet2_output.write(1, 0, "Origin Spreader of Rumor")
    worksheet2_output.write(2, 0, "Origin Spreader of Anti-Rumor")
    worksheet2_output.write(3, 0, "Rumor Retwitter")
    worksheet2_output.write(4, 0, "Anti-Rumor Retwitter")
    worksheet2_output.write(5, 0, "Origin Spreaders of Rumor Related Tweet")
    worksheet2_output.write(6, 0, "Retwitter of Rumor Related Tweet")
    #--------------------------
    worksheet3_output = workbook_output.add_worksheet() #Sheet 3 (The mean results for pure users in each Category)
    worksheet3_output.set_column (0,2,45) #extend the width of columns 
    worksheet3_output.write(0, 1, "Following to Follower")
    worksheet3_output.write(0, 2, "Percentage in the Category")
    worksheet3_output.write(1, 0, "Pure Origin Spreader of Rumor")
    worksheet3_output.write(2, 0, "Pure Origin Spreader of Anti-Rumor")
    worksheet3_output.write(3, 0, "Pure Rumor Retwitter")
    worksheet3_output.write(4, 0, "Pure Anti-Rumor Retwitter")
    worksheet3_output.write(5, 0, "Pure Origin Spreaders of Rumor Related Tweet")
    worksheet3_output.write(6, 0, "Pure Retwitter of Rumor Related Tweet")
    #--------------------------
    worksheet4_output = workbook_output.add_worksheet() #Sheet 4 (The mean results in each Category)
    worksheet4_output.set_column (0,6,45) #extend the width of columns 
    worksheet4_output.write(0, 0, "Screen Name of Pure Origin Spreader of Rumor")
    worksheet4_output.write(0, 1, "Screen Name of Pure Origin Spreader of Anti-Rumor")
    worksheet4_output.write(0, 2, "Screen Name of Pure Rumor Retwitter")
    worksheet4_output.write(0, 3, "Screen Name of Pure Anti-Rumor Retwitter")
    worksheet4_output.write(0, 4, "Screen Name of Pure Origin Spreaders of Rumor Related Tweet")
    worksheet4_output.write(0, 5, "Screen Name of Pure Retwitter of Rumor Related Tweet")
    #--------------------------


    row_input = 1

    
    number_of_tweets_in_dataset = int (worksheet9_input.cell(1, 0).value)

    C1_id_list = []
    C1_screen_name_list = []
    C1_fwing_to_fwer = []
    C1_number_days_membership = []
    C1_mean_tweet_per_day = []
    C1_negative_score = []
    C1_positive_score = []
    C1_compound_score = []
    C1_fwer = []
    C1_fwing = []

    C2_id_list = []
    C2_screen_name_list = []
    C2_fwing_to_fwer = []
    C2_number_days_membership = []
    C2_mean_tweet_per_day = []
    C2_negative_score = []
    C2_positive_score = []
    C2_compound_score = []
    C2_fwer = []
    C2_fwing = []

    C3_id_list = []
    C3_screen_name_list = []
    C3_fwing_to_fwer = []
    C3_number_days_membership = []
    C3_mean_tweet_per_day = []
    C3_negative_score = []
    C3_positive_score = []
    C3_compound_score = []
    C3_fwer = []
    C3_fwing = []
    
    C4_id_list = []
    C4_screen_name_list = []
    C4_fwing_to_fwer = []
    C4_number_days_membership = []
    C4_mean_tweet_per_day = []
    C4_negative_score = []
    C4_positive_score = []
    C4_compound_score = []
    C4_fwer = []
    C4_fwing = []

    C5_id_list = []
    C5_screen_name_list = []
    C5_fwing_to_fwer = []
    C5_number_days_membership = []
    C5_mean_tweet_per_day = []
    C5_negative_score = []
    C5_positive_score = []
    C5_compound_score = []
    C5_fwer = []
    C5_fwing = []

    C6_id_list = []
    C6_screen_name_list = []
    C6_fwing_to_fwer = []
    C6_number_days_membership = []
    C6_mean_tweet_per_day = []
    C6_negative_score = []
    C6_positive_score = []
    C6_compound_score = []
    C6_fwer = []
    C6_fwing = []
    
    while row_input < (number_of_tweets_in_dataset + 1) : #we add 1 to the number_of_tweets_in_dataset because the first row belongs to the labels

        # entering data to the Category 1
        if worksheet1_input.cell(row_input, 28).value == "r" and worksheet1_input.cell(row_input, 27).value[0] == "T" :
            C1_id_list.append (worksheet1_input.cell(row_input, 0).value)
            C1_screen_name_list.append (worksheet1_input.cell(row_input, 1).value)
            fwing = int (worksheet1_input.cell(row_input, 9).value)
            fwer = int (worksheet1_input.cell(row_input, 8).value)
            if fwer == 0 :
                fwer = 1 #to avoid devision by zero error for those users who do not have any follower
            fwing_to_fwer = fwing/fwer #following to follower ratio            
            description = worksheet1_input.cell(row_input, 2).value
            if description :
                negative_score, positive_score, compound_score = Description_Analysis (description)
            else :
                negative_score = 0
                positive_score = 0
                compound_score = 0
            number_tweets = worksheet1_input.cell(row_input, 3).value
            date1 = worksheet1_input.cell(row_input, 4).value
            date2 = worksheet1_input.cell(row_input, 10).value
            number_days_membership, mean_tweet_per_day = tweet_per_day (date1, date2, number_tweets)

            C1_fwing_to_fwer.append (fwing_to_fwer) 
            C1_number_days_membership.append (number_days_membership)
            C1_mean_tweet_per_day.append (mean_tweet_per_day)
            C1_negative_score.append (negative_score)
            C1_positive_score.append (positive_score)
            C1_compound_score.append (compound_score)
            C1_fwer.append (fwer)
            C1_fwing.append (fwing)
            


        # entering data to the Category 2
        elif worksheet1_input.cell(row_input, 28).value == "a" and worksheet1_input.cell(row_input, 27).value[0] == "T" :            
            C2_id_list.append (worksheet1_input.cell(row_input, 0).value)
            C2_screen_name_list.append (worksheet1_input.cell(row_input, 1).value)
            fwing = int (worksheet1_input.cell(row_input, 9).value)
            fwer = int (worksheet1_input.cell(row_input, 8).value)
            if fwer == 0 :
                fwer = 1 #to avoid devision by zero error for those users who do not have any follower
            fwing_to_fwer = fwing/fwer #following to follower ratio
            description = worksheet1_input.cell(row_input, 2).value
            if description :
                negative_score, positive_score, compound_score = Description_Analysis (description)
            else :
                negative_score = 0
                positive_score = 0
                compound_score = 0    
            number_tweets = worksheet1_input.cell(row_input, 3).value
            date1 = worksheet1_input.cell(row_input, 4).value
            date2 = worksheet1_input.cell(row_input, 10).value
            number_days_membership, mean_tweet_per_day = tweet_per_day (date1, date2, number_tweets)

            C2_fwing_to_fwer.append (fwing_to_fwer) 
            C2_number_days_membership.append (number_days_membership)
            C2_mean_tweet_per_day.append (mean_tweet_per_day)
            C2_negative_score.append (negative_score)
            C2_positive_score.append (positive_score)
            C2_compound_score.append (compound_score)
            C2_fwer.append (fwer)
            C2_fwing.append (fwing)
            


        # entering data to the Category 3
        elif worksheet1_input.cell(row_input, 28).value == "r" : 
            C3_id_list.append (worksheet1_input.cell(row_input, 0).value)
            C3_screen_name_list.append (worksheet1_input.cell(row_input, 1).value)
            fwing = int (worksheet1_input.cell(row_input, 9).value)
            fwer = int (worksheet1_input.cell(row_input, 8).value)
            if fwer == 0 :
                fwer = 1 #to avoid devision by zero error for those users who do not have any follower
            fwing_to_fwer = fwing/fwer #following to follower ratio
            description = worksheet1_input.cell(row_input, 2).value
            if description :
                negative_score, positive_score, compound_score = Description_Analysis (description)
            else :
                negative_score = 0
                positive_score = 0
                compound_score = 0
            number_tweets = worksheet1_input.cell(row_input, 3).value
            date1 = worksheet1_input.cell(row_input, 4).value
            date2 = worksheet1_input.cell(row_input, 10).value
            number_days_membership, mean_tweet_per_day = tweet_per_day (date1, date2, number_tweets)

            C3_fwing_to_fwer.append (fwing_to_fwer) 
            C3_number_days_membership.append (number_days_membership)
            C3_mean_tweet_per_day.append (mean_tweet_per_day)
            C3_negative_score.append (negative_score)
            C3_positive_score.append (positive_score)
            C3_compound_score.append (compound_score)
            C3_fwer.append (fwer)
            C3_fwing.append (fwing)



        # entering data to the Category 4
        elif worksheet1_input.cell(row_input, 28).value == "a" :
            C4_id_list.append (worksheet1_input.cell(row_input, 0).value)
            C4_screen_name_list.append (worksheet1_input.cell(row_input, 1).value)
            fwing = int (worksheet1_input.cell(row_input, 9).value)
            fwer = int (worksheet1_input.cell(row_input, 8).value)
            if fwer == 0 :
                fwer = 1 #to avoid devision by zero error for those users who do not have any follower
            fwing_to_fwer = fwing/fwer #following to follower ratio
            description = worksheet1_input.cell(row_input, 2).value
            if description :
                negative_score, positive_score, compound_score = Description_Analysis (description)
            else :
                negative_score = 0
                positive_score = 0
                compound_score = 0
            number_tweets = worksheet1_input.cell(row_input, 3).value
            date1 = worksheet1_input.cell(row_input, 4).value
            date2 = worksheet1_input.cell(row_input, 10).value
            number_days_membership, mean_tweet_per_day = tweet_per_day (date1, date2, number_tweets)

            C4_fwing_to_fwer.append (fwing_to_fwer) 
            C4_number_days_membership.append (number_days_membership)
            C4_mean_tweet_per_day.append (mean_tweet_per_day)
            C4_negative_score.append (negative_score)
            C4_positive_score.append (positive_score)
            C4_compound_score.append (compound_score)
            C4_fwer.append (fwer)
            C4_fwing.append (fwing)
        

        # entering data to the Category 5        
        elif worksheet1_input.cell(row_input, 28).value == "q" and worksheet1_input.cell(row_input, 27).value[0] == "T":
            C5_id_list.append (worksheet1_input.cell(row_input, 0).value)
            C5_screen_name_list.append (worksheet1_input.cell(row_input, 1).value)
            fwing = int (worksheet1_input.cell(row_input, 9).value)
            fwer = int (worksheet1_input.cell(row_input, 8).value)
            if fwer == 0 :
                fwer = 1 #to avoid devision by zero error for those users who do not have any follower
            fwing_to_fwer = fwing/fwer #following to follower ratio
            description = worksheet1_input.cell(row_input, 2).value
            if description :
                negative_score, positive_score, compound_score = Description_Analysis (description)
            else :
                negative_score = 0
                positive_score = 0
                compound_score = 0
            number_tweets = worksheet1_input.cell(row_input, 3).value
            date1 = worksheet1_input.cell(row_input, 4).value
            date2 = worksheet1_input.cell(row_input, 10).value
            number_days_membership, mean_tweet_per_day = tweet_per_day (date1, date2, number_tweets)

            C5_fwing_to_fwer.append (fwing_to_fwer) 
            C5_number_days_membership.append (number_days_membership)
            C5_mean_tweet_per_day.append (mean_tweet_per_day)
            C5_negative_score.append (negative_score)
            C5_positive_score.append (positive_score)
            C5_compound_score.append (compound_score)
            C5_fwer.append (fwer)
            C5_fwing.append (fwing)


        # entering data to the Category 6        
        elif worksheet1_input.cell(row_input, 28).value == "q" :
            C6_id_list.append (worksheet1_input.cell(row_input, 0).value)
            C6_screen_name_list.append (worksheet1_input.cell(row_input, 1).value)
            fwing = int (worksheet1_input.cell(row_input, 9).value)
            fwer = int (worksheet1_input.cell(row_input, 8).value)
            if fwer == 0 :
                fwer = 1 #to avoid devision by zero error for those users who do not have any follower
            fwing_to_fwer = fwing/fwer #following to follower ratio
            description = worksheet1_input.cell(row_input, 2).value
            if description :
                negative_score, positive_score, compound_score = Description_Analysis (description)
            else :
                negative_score = 0
                positive_score = 0
                compound_score = 0
            number_tweets = worksheet1_input.cell(row_input, 3).value
            date1 = worksheet1_input.cell(row_input, 4).value
            date2 = worksheet1_input.cell(row_input, 10).value
            number_days_membership, mean_tweet_per_day = tweet_per_day (date1, date2, number_tweets)

            C6_fwing_to_fwer.append (fwing_to_fwer) 
            C6_number_days_membership.append (number_days_membership)
            C6_mean_tweet_per_day.append (mean_tweet_per_day)
            C6_negative_score.append (negative_score)
            C6_positive_score.append (positive_score)
            C6_compound_score.append (compound_score)
            C6_fwer.append (fwer)
            C6_fwing.append (fwing)

            

        row_input += 1




    #%%%%%%%%%%%%   G.E.T.T.I.N.G  A.T.R.I.B.U.T.E.S   %%%%%%%%%%%%%%%%%%%%%%%%%%%%
    all_screen_name = list(set(C1_screen_name_list + C2_screen_name_list + C3_screen_name_list + C4_screen_name_list + C5_screen_name_list + C6_screen_name_list))
    number_user_all = len (all_screen_name)
    number_user_1 = len (C1_screen_name_list)
    number_user_2 = len (C2_screen_name_list)
    number_user_3 = len (C3_screen_name_list)
    number_user_4 = len (C4_screen_name_list)
    number_user_5 = len (C5_screen_name_list)
    number_user_6 = len (C6_screen_name_list)
    screen_name_number_of_occurance_all = []
    for screen_name in all_screen_name :
        N_all = []
        N_1 = C1_screen_name_list.count(screen_name)
        N_2 = C2_screen_name_list.count(screen_name)
        N_3 = C3_screen_name_list.count(screen_name)
        N_4 = C4_screen_name_list.count(screen_name)
        N_5 = C5_screen_name_list.count(screen_name)
        N_6 = C6_screen_name_list.count(screen_name)
        N_all.append (N_1)
        N_all.append (N_2)
        N_all.append (N_3)
        N_all.append (N_4)
        N_all.append (N_5)
        N_all.append (N_6)
        screen_name_number_of_occurance_all.append (N_all)

        
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    user_attribute = []
    user_attribute_all = []
    i = 0
    while i < number_user_all :
        if screen_name_number_of_occurance_all[i][0] != 0 :
            i_1 = 0
            while i_1 < number_user_1 :
                if C1_screen_name_list[i_1] == all_screen_name[i] :
                    user_attribute.append (C1_id_list[i_1])
                    user_attribute.append (C1_fwing_to_fwer[i_1])
                    user_attribute.append (C1_number_days_membership[i_1])
                    user_attribute.append (C1_mean_tweet_per_day[i_1])
                    user_attribute.append (C1_negative_score[i_1])
                    user_attribute.append (C1_positive_score[i_1])
                    user_attribute.append (C1_compound_score[i_1])
                    user_attribute.append (C1_fwer[i_1])
                    user_attribute.append (C1_fwing[i_1])
                    user_attribute_all.append (user_attribute)
                    user_attribute = []
                    break

                i_1 += 1

        elif screen_name_number_of_occurance_all[i][1] != 0 :
            i_2 = 0
            while i_2 < number_user_2 :
                if C2_screen_name_list[i_2] == all_screen_name[i] :
                    user_attribute.append (C2_id_list[i_2])
                    user_attribute.append (C2_fwing_to_fwer[i_2])
                    user_attribute.append (C2_number_days_membership[i_2])
                    user_attribute.append (C2_mean_tweet_per_day[i_2])
                    user_attribute.append (C2_negative_score[i_2])
                    user_attribute.append (C2_positive_score[i_2])
                    user_attribute.append (C2_compound_score[i_2])
                    user_attribute.append (C2_fwer[i_2])
                    user_attribute.append (C2_fwing[i_2])
                    user_attribute_all.append (user_attribute)
                    user_attribute = []
                    break
                    
                i_2 += 1
                

        elif screen_name_number_of_occurance_all[i][2] != 0 :
            i_3 = 0
            while i_3 < number_user_3 :
                if C3_screen_name_list[i_3] == all_screen_name[i] :
                    user_attribute.append (C3_id_list[i_3])
                    user_attribute.append (C3_fwing_to_fwer[i_3])
                    user_attribute.append (C3_number_days_membership[i_3])
                    user_attribute.append (C3_mean_tweet_per_day[i_3])
                    user_attribute.append (C3_negative_score[i_3])
                    user_attribute.append (C3_positive_score[i_3])
                    user_attribute.append (C3_compound_score[i_3])
                    user_attribute.append (C3_fwer[i_3])
                    user_attribute.append (C3_fwing[i_3])
                    user_attribute_all.append (user_attribute)
                    user_attribute = []
                    break

                i_3 += 1

        elif screen_name_number_of_occurance_all[i][3] != 0 :
            i_4 = 0
            while i_4 < number_user_4 :
                if C4_screen_name_list[i_4] == all_screen_name[i] :
                    user_attribute.append (C4_id_list[i_4])
                    user_attribute.append (C4_fwing_to_fwer[i_4])
                    user_attribute.append (C4_number_days_membership[i_4])
                    user_attribute.append (C4_mean_tweet_per_day[i_4])
                    user_attribute.append (C4_negative_score[i_4])
                    user_attribute.append (C4_positive_score[i_4])
                    user_attribute.append (C4_compound_score[i_4])
                    user_attribute.append (C4_fwer[i_4])
                    user_attribute.append (C4_fwing[i_4])
                    user_attribute_all.append (user_attribute)
                    user_attribute = []
                    break

                i_4 += 1

        elif screen_name_number_of_occurance_all[i][4] != 0 :
            i_5 = 0
            while i_5 < number_user_5 :
                if C5_screen_name_list[i_5] == all_screen_name[i] :
                    user_attribute.append (C5_id_list[i_5])
                    user_attribute.append (C5_fwing_to_fwer[i_5])
                    user_attribute.append (C5_number_days_membership[i_5])
                    user_attribute.append (C5_mean_tweet_per_day[i_5])
                    user_attribute.append (C5_negative_score[i_5])
                    user_attribute.append (C5_positive_score[i_5])
                    user_attribute.append (C5_compound_score[i_5])
                    user_attribute.append (C5_fwer[i_5])
                    user_attribute.append (C5_fwing[i_5])
                    user_attribute_all.append (user_attribute)
                    user_attribute = []
                    break

                i_5 += 1

        elif screen_name_number_of_occurance_all[i][5] != 0 :
            i_6 = 0
            while i_6 < number_user_6 :
                if C6_screen_name_list[i_6] == all_screen_name[i] :
                    user_attribute.append (C6_id_list[i_6])
                    user_attribute.append (C6_fwing_to_fwer[i_6])
                    user_attribute.append (C6_number_days_membership[i_6])
                    user_attribute.append (C6_mean_tweet_per_day[i_6])
                    user_attribute.append (C6_negative_score[i_6])
                    user_attribute.append (C6_positive_score[i_6])
                    user_attribute.append (C6_compound_score[i_6])
                    user_attribute.append (C6_fwer[i_6])
                    user_attribute.append (C6_fwing[i_6])
                    user_attribute_all.append (user_attribute)
                    user_attribute = []
                    break

                i_6 += 1

        i += 1

    # a simple test to make sure everything is alright ! :)
    if len (user_attribute_all) != len (all_screen_name) or len (user_attribute_all) != len (screen_name_number_of_occurance_all) :
        print ("Something went wrong !!!")

        

    #%%%%%%%%%%%%%  W.R.I.T.I.N.G   T.H.E   R.E.S.U.L.T.S   I.N.T.O    T.H.E    O.U.T.P.U.T    S.H.E.E.T 1   %%%%%%%%%%%%%%%%%%%%%%%%%
    k = 0
    while k < len (all_screen_name) :
        worksheet1_output.write(k+1, 0, user_attribute_all [k][0])
        worksheet1_output.write(k+1, 1, all_screen_name [k])
        worksheet1_output.write(k+1, 2, screen_name_number_of_occurance_all[k][0])
        worksheet1_output.write(k+1, 3, screen_name_number_of_occurance_all[k][1])
        worksheet1_output.write(k+1, 4, screen_name_number_of_occurance_all[k][2])
        worksheet1_output.write(k+1, 5, screen_name_number_of_occurance_all[k][3])
        worksheet1_output.write(k+1, 6, screen_name_number_of_occurance_all[k][4])
        worksheet1_output.write(k+1, 7, screen_name_number_of_occurance_all[k][5])
        worksheet1_output.write(k+1, 8, user_attribute_all [k][1])
        worksheet1_output.write(k+1, 9, user_attribute_all [k][2])
        worksheet1_output.write(k+1, 10, user_attribute_all [k][3])
        worksheet1_output.write(k+1, 11, user_attribute_all [k][4])
        worksheet1_output.write(k+1, 12, user_attribute_all [k][5])
        worksheet1_output.write(k+1, 13, user_attribute_all [k][6])
        worksheet1_output.write(k+1, 14, user_attribute_all [k][7])
        worksheet1_output.write(k+1, 15, user_attribute_all [k][8])
        k += 1
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    

    #%%%%%%%%%%%%%  W.R.I.T.I.N.G   T.H.E   R.E.S.U.L.T.S   I.N.T.O    T.H.E    O.U.T.P.U.T    S.H.E.E.T 2   %%%%%%%%%%%%%%%%%%%%%%%%%
    k = 0
    C1_FWFO = []
    C1_MEM = []
    C1_TWDAY = []
    C1_NEG = []
    C1_POS = []
    C1_COM = []
    C2_FWFO = []
    C2_MEM = []
    C2_TWDAY = []
    C2_NEG = []
    C2_POS = []
    C2_COM = []
    C3_FWFO = []
    C3_MEM = []
    C3_TWDAY = []
    C3_NEG = []
    C3_POS = []
    C3_COM = []
    C4_FWFO = []
    C4_MEM = []
    C4_TWDAY = []
    C4_NEG = []
    C4_POS = []
    C4_COM = []
    C5_FWFO = []
    C5_MEM = []
    C5_TWDAY = []
    C5_NEG = []
    C5_POS = []
    C5_COM = []
    C6_FWFO = []
    C6_MEM = []
    C6_TWDAY = []
    C6_NEG = []
    C6_POS = []
    C6_COM = []

    C1_Pure_FWFO = []
    C2_Pure_FWFO = []
    C3_Pure_FWFO = []
    C4_Pure_FWFO = []
    C5_Pure_FWFO = []
    C6_Pure_FWFO = []

    C1_Pure_screen_name = []
    C2_Pure_screen_name = []
    C3_Pure_screen_name = []
    C4_Pure_screen_name = []
    C5_Pure_screen_name = []
    C6_Pure_screen_name = []
    
    while k < len (all_screen_name) :
        if screen_name_number_of_occurance_all[k][0] != 0 :
            C1_FWFO.append (user_attribute_all [k][1])
            C1_MEM.append (user_attribute_all [k][2])
            C1_TWDAY.append (user_attribute_all [k][3])
            C1_NEG.append (user_attribute_all [k][4])
            C1_POS.append (user_attribute_all [k][5])
            C1_COM.append (user_attribute_all [k][6])
            if screen_name_number_of_occurance_all[k][1] == 0 and screen_name_number_of_occurance_all[k][2] == 0 and screen_name_number_of_occurance_all[k][3] == 0 and screen_name_number_of_occurance_all[k][4] == 0 and screen_name_number_of_occurance_all[k][5] == 0 :
                C1_Pure_FWFO.append (user_attribute_all [k][1])
                C1_Pure_screen_name.append (all_screen_name [k])
                
        if screen_name_number_of_occurance_all[k][1] != 0 :
            C2_FWFO.append (user_attribute_all [k][1])
            C2_MEM.append (user_attribute_all [k][2])
            C2_TWDAY.append (user_attribute_all [k][3])
            C2_NEG.append (user_attribute_all [k][4])
            C2_POS.append (user_attribute_all [k][5])
            C2_COM.append (user_attribute_all [k][6])
            if screen_name_number_of_occurance_all[k][0] == 0 and screen_name_number_of_occurance_all[k][2] == 0 and screen_name_number_of_occurance_all[k][3] == 0 and screen_name_number_of_occurance_all[k][4] == 0 and screen_name_number_of_occurance_all[k][5] == 0 :
                C2_Pure_FWFO.append (user_attribute_all [k][1])
                C2_Pure_screen_name.append (all_screen_name [k])
                
        if screen_name_number_of_occurance_all[k][2] != 0 :
            C3_FWFO.append (user_attribute_all [k][1])
            C3_MEM.append (user_attribute_all [k][2])
            C3_TWDAY.append (user_attribute_all [k][3])
            C3_NEG.append (user_attribute_all [k][4])
            C3_POS.append (user_attribute_all [k][5])
            C3_COM.append (user_attribute_all [k][6])
            if screen_name_number_of_occurance_all[k][0] == 0 and screen_name_number_of_occurance_all[k][1] == 0 and screen_name_number_of_occurance_all[k][3] == 0 and screen_name_number_of_occurance_all[k][4] == 0 and screen_name_number_of_occurance_all[k][5] == 0 :
                C3_Pure_FWFO.append (user_attribute_all [k][1])
                C3_Pure_screen_name.append (all_screen_name [k])
            
        if screen_name_number_of_occurance_all[k][3] != 0 :
            C4_FWFO.append (user_attribute_all [k][1])
            C4_MEM.append (user_attribute_all [k][2])
            C4_TWDAY.append (user_attribute_all [k][3])
            C4_NEG.append (user_attribute_all [k][4])
            C4_POS.append (user_attribute_all [k][5])
            C4_COM.append (user_attribute_all [k][6])
            if screen_name_number_of_occurance_all[k][0] == 0 and screen_name_number_of_occurance_all[k][1] == 0 and screen_name_number_of_occurance_all[k][2] == 0 and screen_name_number_of_occurance_all[k][4] == 0 and screen_name_number_of_occurance_all[k][5] == 0 :
                C4_Pure_FWFO.append (user_attribute_all [k][1])
                C4_Pure_screen_name.append (all_screen_name [k])
                
        if screen_name_number_of_occurance_all[k][4] != 0 :
            C5_FWFO.append (user_attribute_all [k][1])
            C5_MEM.append (user_attribute_all [k][2])
            C5_TWDAY.append (user_attribute_all [k][3])
            C5_NEG.append (user_attribute_all [k][4])
            C5_POS.append (user_attribute_all [k][5])
            C5_COM.append (user_attribute_all [k][6])
            if screen_name_number_of_occurance_all[k][0] == 0 and screen_name_number_of_occurance_all[k][1] == 0 and screen_name_number_of_occurance_all[k][2] == 0 and screen_name_number_of_occurance_all[k][3] == 0 and screen_name_number_of_occurance_all[k][5] == 0 :
                C5_Pure_FWFO.append (user_attribute_all [k][1])
                C5_Pure_screen_name.append (all_screen_name [k])
                
        if screen_name_number_of_occurance_all[k][5] != 0 :
            C6_FWFO.append (user_attribute_all [k][1])
            C6_MEM.append (user_attribute_all [k][2])
            C6_TWDAY.append (user_attribute_all [k][3])
            C6_NEG.append (user_attribute_all [k][4])
            C6_POS.append (user_attribute_all [k][5])
            C6_COM.append (user_attribute_all [k][6])
            if screen_name_number_of_occurance_all[k][0] == 0 and screen_name_number_of_occurance_all[k][1] == 0 and screen_name_number_of_occurance_all[k][2] == 0 and screen_name_number_of_occurance_all[k][3] == 0 and screen_name_number_of_occurance_all[k][4] == 0 :
                C6_Pure_FWFO.append (user_attribute_all [k][1])
                C6_Pure_screen_name.append (all_screen_name [k])

        k += 1
    

    worksheet2_output.write(1, 1, str (np.mean(C1_FWFO)))
    worksheet2_output.write(1, 2, str (np.mean(C1_MEM)))
    worksheet2_output.write(1, 3, str (np.mean(C1_TWDAY)))
    worksheet2_output.write(1, 4, str (np.mean(C1_NEG)))
    worksheet2_output.write(1, 5, str (np.mean(C1_POS)))
    worksheet2_output.write(1, 6, str (np.mean(C1_COM)))
    worksheet2_output.write(2, 1, str (np.mean(C2_FWFO)))
    worksheet2_output.write(2, 2, str (np.mean(C2_MEM)))
    worksheet2_output.write(2, 3, str (np.mean(C2_TWDAY)))
    worksheet2_output.write(2, 4, str (np.mean(C2_NEG)))
    worksheet2_output.write(2, 5, str (np.mean(C2_POS)))
    worksheet2_output.write(2, 6, str (np.mean(C2_COM)))
    worksheet2_output.write(3, 1, str (np.mean(C3_FWFO)))
    worksheet2_output.write(3, 2, str (np.mean(C3_MEM)))
    worksheet2_output.write(3, 3, str (np.mean(C3_TWDAY)))
    worksheet2_output.write(3, 4, str (np.mean(C3_NEG)))
    worksheet2_output.write(3, 5, str (np.mean(C3_POS)))
    worksheet2_output.write(3, 6, str (np.mean(C3_COM)))
    worksheet2_output.write(4, 1, str (np.mean(C4_FWFO)))
    worksheet2_output.write(4, 2, str (np.mean(C4_MEM)))
    worksheet2_output.write(4, 3, str (np.mean(C4_TWDAY)))
    worksheet2_output.write(4, 4, str (np.mean(C4_NEG)))
    worksheet2_output.write(4, 5, str (np.mean(C4_POS)))
    worksheet2_output.write(4, 6, str (np.mean(C4_COM)))
    worksheet2_output.write(5, 1, str (np.mean(C5_FWFO)))
    worksheet2_output.write(5, 2, str (np.mean(C5_MEM)))
    worksheet2_output.write(5, 3, str (np.mean(C5_TWDAY)))
    worksheet2_output.write(5, 4, str (np.mean(C5_NEG)))
    worksheet2_output.write(5, 5, str (np.mean(C5_POS)))
    worksheet2_output.write(5, 6, str (np.mean(C5_COM)))
    worksheet2_output.write(6, 1, str (np.mean(C6_FWFO)))
    worksheet2_output.write(6, 2, str (np.mean(C6_MEM)))
    worksheet2_output.write(6, 3, str (np.mean(C6_TWDAY)))
    worksheet2_output.write(6, 4, str (np.mean(C6_NEG)))
    worksheet2_output.write(6, 5, str (np.mean(C6_POS)))
    worksheet2_output.write(6, 6, str (np.mean(C6_COM)))
    

    #%%%%%%%%%%%%%  W.R.I.T.I.N.G   T.H.E   R.E.S.U.L.T.S   I.N.T.O    T.H.E    O.U.T.P.U.T    S.H.E.E.T 3   %%%%%%%%%%%%%%%%%%%%%%%%%
    worksheet3_output.write(1, 1, str (np.mean(C1_Pure_FWFO)))
    if len(C1_FWFO) == 0 :
        NC1 = 1
    else :
        NC1 = len(C1_FWFO)        
    worksheet3_output.write(1, 2, str (len(C1_Pure_FWFO)/NC1))
    #---
    worksheet3_output.write(2, 1, str (np.mean(C2_Pure_FWFO)))
    if len(C2_FWFO) == 0 :
        NC2 = 1
    else :
        NC2 = len(C2_FWFO)   
    worksheet3_output.write(2, 2, str (len(C2_Pure_FWFO)/NC2))
    #---
    worksheet3_output.write(3, 1, str (np.mean(C3_Pure_FWFO)))
    if len(C3_FWFO) == 0 :
        NC3 = 1
    else :
        NC3 = len(C3_FWFO) 
    worksheet3_output.write(3, 2, str (len(C3_Pure_FWFO)/NC3))
    #---
    worksheet3_output.write(4, 1, str (np.mean(C4_Pure_FWFO)))
    if len(C4_FWFO) == 0 :
        NC4 = 1
    else :
        NC4 = len(C4_FWFO)
    worksheet3_output.write(4, 2, str (len(C4_Pure_FWFO)/NC4))
    #---
    worksheet3_output.write(5, 1, str (np.mean(C5_Pure_FWFO)))
    if len(C5_FWFO) == 0 :
        NC5 = 1
    else :
        NC5 = len(C5_FWFO)
    worksheet3_output.write(5, 2, str (len(C5_Pure_FWFO)/NC5))
    #---    
    worksheet3_output.write(6, 1, str (np.mean(C6_Pure_FWFO)))
    if len(C6_FWFO) == 0 :
        NC6 = 1
    else :
        NC6 = len(C6_FWFO)
    worksheet3_output.write(6, 2, str (len(C6_Pure_FWFO)/NC6))
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    #%%%%%%%%%%%%%  W.R.I.T.I.N.G   T.H.E   R.E.S.U.L.T.S   I.N.T.O    T.H.E    O.U.T.P.U.T    S.H.E.E.T 4   %%%%%%%%%%%%%%%%%%%%%%%%%
    r = 1
    for screen_name in C1_Pure_screen_name :
        worksheet4_output.write(r, 0, screen_name)
        r += 1
        
    r = 1
    for screen_name in C2_Pure_screen_name :
        worksheet4_output.write(r, 1, screen_name)
        r += 1                        
                            
    r = 1
    for screen_name in C3_Pure_screen_name :
        worksheet4_output.write(r, 2, screen_name)
        r += 1

    r = 1
    for screen_name in C4_Pure_screen_name :
        worksheet4_output.write(r, 3, screen_name)
        r += 1

    r = 1
    for screen_name in C5_Pure_screen_name :
        worksheet4_output.write(r, 4, screen_name)
        r += 1

    r = 1
    for screen_name in C6_Pure_screen_name :
        worksheet4_output.write(r, 5, screen_name)
        r += 1

    #---
    
    workbook_output.close()       
    
#----------------------------------

main()
input ("press enter key to exit ...")
