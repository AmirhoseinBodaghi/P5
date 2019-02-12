#-------------------------------------------
#This program gets two input :
#1- final Dataset achieved by the end of Step 9 (which was the input for Step 10)
#2- The output of Step 10 named Results_Step_10
#And gives us 7 outputs but before going to explain outputs remember this abrivation :
#1- C1 (Category belongs to users who published rumor tweet) 
#2- C2 (Category belongs to users who published antirumor tweet)
#3- C3 (Category belongs to users who published rumor retweet)
#4- C4 (Category belongs to users who published antirumor rettweet)
#5- C5 (Category belongs to users who published rumor related tweet such as question)
#6- C6 (Category belongs to users who published rumor related retweet such as question)
# and we have every combination of these categories for example C125 belongs to users who have published "rumor tweet" and "antirumor tweet" and "rumor related tweet such as question"
# now lets go to explain the 7 outputs of this program :
#1- Pie chart for Users who belong to C1 (only C1 shows as Pure in Pie chart) AND any ccombination of C1 with other categories
#2- Pie chart for Users who belong to C2 (only C2 shows as Pure in Pie chart) AND any ccombination of C2 with other categories
#3- Pie chart for Users who belong to C3 (only C3 shows as Pure in Pie chart) AND any ccombination of C3 with other categories
#4- Pie chart for Users who belong to C4 (only C4 shows as Pure in Pie chart) AND any ccombination of C4 with other categories
#5- plot chart of tweets per hour which shows number of tweets (all tweets no matter in which category, they can even be "n" tweets ie not related tweets of dataset). Infact this plot is exactly the same as we achieved as an output for Step 5)
#6- plot chart of rumor tweets per hour which shows number of tweets (only tweets which are labled as "r" in dataset, that can be even origin rumor or retweet rumor)
#7- plot chart of antirumor tweets per hour which shows number of tweets (only tweets which are labled as "a" in dataset, that can be even origin antirumor or retweet antirumor)
#-------------------------------------------
def main ():
    import xlrd
    import xlsxwriter
    import numpy as np
    import tweepy
    import time
    import math
    import random
    import matplotlib as plt
    from tweepy import API
    from tweepy import Cursor
    from tweepy import OAuthHandler
    from collections import Counter

    
    #Reading ------------------
    my_path_R = 'D:\\Papers\\Social Network Mining\\Analysis_of_Rumor_Dataset\\Step 13\\Rumor_25\\Input\\'
    workbook_input = xlrd.open_workbook(my_path_R + 'Results_Step_10.xlsx')
    worksheet1_input = workbook_input.sheet_by_name('Sheet1')
    worksheet4_input = workbook_input.sheet_by_name('Sheet4')
    workbook_main_input = xlrd.open_workbook(my_path_R + 'DATASET.xlsx')
    worksheet1_main_input = workbook_main_input.sheet_by_name('Sheet1')
    #Writing ------------------
    my_path_W = 'D:\\Papers\\Social Network Mining\\Analysis_of_Rumor_Dataset\\Step 13\\Rumor_25\\Output\\'
    #---
    Screen_Name = worksheet1_input.col_values(1)
    C1 = worksheet1_input.col_values(2)
    C2 = worksheet1_input.col_values(3)
    C3 = worksheet1_input.col_values(4)
    C4 = worksheet1_input.col_values(5)
    C5 = worksheet1_input.col_values(6)
    C6 = worksheet1_input.col_values(7)

    del Screen_Name [0]
    del C1 [0]
    del C2 [0]
    del C3 [0]
    del C4 [0]
    del C5 [0]
    del C6 [0]

    number_all_users = len (Screen_Name)
    j = 0
    state_of_all_screen_name = []
    state_single_user = []

    while j < number_all_users :
        if C1 [j] != 0 :
            state_single_user.append (1)
        else :
            state_single_user.append (0)
            
        if C2 [j] != 0 :
            state_single_user.append (1)
        else :
            state_single_user.append (0)
            
        if C3 [j] != 0 :
            state_single_user.append (1)
        else :
            state_single_user.append (0)
            
        if C4 [j] != 0 :
            state_single_user.append (1)
        else :
            state_single_user.append (0)
            
        if C5 [j] != 0 :
            state_single_user.append (1)
        else :
            state_single_user.append (0)
            
        if C6 [j] != 0 :
            state_single_user.append (1)
        else :
            state_single_user.append (0)

        state_of_all_screen_name.append (state_single_user)
        state_single_user = []
        j += 1


    l = []
    y = Counter(tuple(item) for item in state_of_all_screen_name)
    for i in y.items() :
        l.append (i)

    
    #Writing ------------------
    workbook_output = xlsxwriter.Workbook(my_path_W + 'Results_Step_13.xlsx')
    worksheet1_output = workbook_output.add_worksheet() #Sheet 1 (Spearman and Pearson Correlations)

    worksheet1_output.set_column (0,1,30) #extend the width of columns 
    worksheet1_output.write(0, 0, "User_States: [C1,C2,C3,C4,C5,C6]")
    worksheet1_output.write(0, 1, "Frequency")
    k = 0
    number_states = len (l)
    while k < number_states :
        user_state = list (l[k][0])
        frequency = l[k][1]
        worksheet1_output.write(k+1, 0, str (user_state))
        worksheet1_output.write(k+1, 1, str (frequency))
        k += 1

#------- T.W.E.E.T    P.E.R     H.O.U.R ------------------
    D_T_P_L_S = worksheet1_main_input.col_values(10)
    States = worksheet1_main_input.col_values(28)
    del D_T_P_L_S [0]
    del States [0]
    tweet_number = len (D_T_P_L_S)
    D_T_P_L = []
    for DP in D_T_P_L_S :
        year = DP[2] + DP[3] + DP[4] + DP[5]
        month = DP[10] + DP[11] + DP[12]
        day = DP[17] + DP[18]
        time = DP[23] + DP[24] + DP[25] + DP[26] + DP[27] + DP[28] + DP[29] + DP[30] 
        D_T_P_L_i = []
        D_T_P_L_i.append (year)
        D_T_P_L_i.append (month)
        D_T_P_L_i.append (day)
        D_T_P_L_i.append (time)
        D_T_P_L.append (D_T_P_L_i)
        
    Date_Time_Analysis (D_T_P_L, my_path_W, States)

    

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

# ----------------
def Date_Time_Analysis (D_T_P_L, my_path_W, States): #this function calculates the total number of days it last from the first tweet of dataset to the last tweet of dataset (in other word the difference between the date of first tweet of dataset and the date of the last tweet of the dataset in terms of day)
    begining_1, ending_1, begining_2, ending_2 = hour_analysis (D_T_P_L, my_path_W)
    hour_analysis_rumor (D_T_P_L, my_path_W, States, begining_1, ending_1, begining_2, ending_2)
    hour_analysis_antirumor (D_T_P_L, my_path_W, States, begining_1, ending_1, begining_2, ending_2)
    
    # ----------------
#------------------------------------------
def hour_analysis (D_T_P_L, my_path_W): #this function seperate tweets by day, in other word all tweets that published in a same day get togather as a list, so each list include all tweets published in a specific day, and seperate_days (the result of this function) will be a list (list of lists) which includes all the mentioned lists  
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
             
    list.reverse (hour_info_1) 
    e_1 = len (hour_info_1) - 1
    begining_1 = hour_info_1[0]
    ending_1 = hour_info_1[e_1]
    
    list.reverse (hour_info_1)
    

    list.reverse (hour_info_2) #because we started to capture tweets from the last tweet in our time and went back through the time, now for ploting we need to start from the begining time so we inverse the list
    e_2 = len (hour_info_2) - 1
    begining_2 = hour_info_2[0]
    ending_2 = hour_info_2[e_2]
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
    plt.savefig (my_path_W + 'time_hour.png',dpi=500) # here we give high dpi to save figures with great quality
    plt.show()

    return begining_1, ending_1, begining_2, ending_2 #we give these data so we can plot tweet/hour for rumor and antirumor from the begining to the ending point same as those in the general plot (in which all tweets exist)
###---------------------------------------------------
def hour_analysis_rumor (D_T_P_L, my_path_W, States, begining_1, ending_1, begining_2, ending_2): #this function seperate tweets by day, in other word all tweets that published in a same day get togather as a list, so each list include all tweets published in a specific day, and seperate_days (the result of this function) will be a list (list of lists) which includes all the mentioned lists  
    import matplotlib.pyplot as plt
    from datetime import datetime
    from dateutil import relativedelta
    seperate_hours = []
    hour = []
    hour_info_1 = []
    hour_info_2 = []
    y = []
    x = []
    x_str = []

    #to find the first hour a rumor tweet published and delete all the tweets before that
    for date_time_processed_each in D_T_P_L :
        if States [D_T_P_L.index(date_time_processed_each)] == "r" :
            delete_index = D_T_P_L.index(date_time_processed_each)
            del D_T_P_L [:delete_index]
            del States [:delete_index]
            break
            
    hour_current = D_T_P_L[0][3][0] + D_T_P_L[0][3][1]

    for date_time_processed_each in D_T_P_L :
        h_c = date_time_processed_each[3][0] + date_time_processed_each[3][1]
        if States [D_T_P_L.index(date_time_processed_each)] == "r" :
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

    #adding the first and last hour to the plot , because even though they existed in the general plot (all tweets) they might not exist in the anti rumor plot
    list.reverse (hour_info_1)
    e_1 = len (hour_info_1)
    if begining_1[0] not in hour_info_1 [:][0]:
        begining_1[1] = 0
        hour_info_1.insert (0 , begining_1)
    if ending_1[0] not in hour_info_1 [:][0]:
        ending_1[1] = 0
        hour_info_1.insert (e_1 , ending_1)         
    list.reverse (hour_info_1)

    list.reverse (hour_info_2)
    e_2 = len (hour_info_2)
    if begining_2 [0] not in hour_info_2 [:][0] :
        begining_2[1] = 0
        hour_info_2.insert (0 , begining_2)
    if ending_2 [0] not in hour_info_2[:][0] :
        ending_2[1] = 0
        hour_info_2.insert (e_2 , ending_2)
        
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
    plt.bar(x, y,  width=0.5, color="red")
    plt.xticks(x , x_str) # this is for avoiding the show of other numbers on the x axis except the number of exact hours
    plt.xlabel('time (hour)')
    plt.ylabel('number of tweets')
    plt.savefig (my_path_W + 'time_hour_r.png',dpi=500) # here we give high dpi to save figures with great quality
    plt.show()

###---------------------------------------------------
def hour_analysis_antirumor (D_T_P_L, my_path_W, States, begining_1, ending_1, begining_2, ending_2): #this function seperate tweets by day, in other word all tweets that published in a same day get togather as a list, so each list include all tweets published in a specific day, and seperate_days (the result of this function) will be a list (list of lists) which includes all the mentioned lists  
    import matplotlib.pyplot as plt
    from datetime import datetime
    from dateutil import relativedelta
    seperate_hours = []
    hour = []
    hour_info_1 = []
    hour_info_2 = []
    y = []
    x = []
    x_str = []

    #to find the first hour an antirumor tweet published and delete all the tweets before that
    for date_time_processed_each in D_T_P_L :
        if States [D_T_P_L.index(date_time_processed_each)] == "a" :
            delete_index = D_T_P_L.index(date_time_processed_each)
            del D_T_P_L [:delete_index]
            del States [:delete_index]
            break
            
    hour_current = D_T_P_L[0][3][0] + D_T_P_L[0][3][1]


    for date_time_processed_each in D_T_P_L :
        h_c = date_time_processed_each[3][0] + date_time_processed_each[3][1]
        if States [D_T_P_L.index(date_time_processed_each)] == "a" :
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


    #adding the first and last hour to the plot , because even though they existed in the general plot (all tweets) they might not exist in the anti rumor plot
    list.reverse (hour_info_1)
    e_1 = len (hour_info_1)
    if begining_1[0] not in hour_info_1 [:][0]:
        begining_1[1] = 0
        hour_info_1.insert (0 , begining_1)
    if ending_1[0] not in hour_info_1 [:][0]:
        ending_1[1] = 0
        hour_info_1.insert (e_1 , ending_1)         
    list.reverse (hour_info_1)

    list.reverse (hour_info_2)
    e_2 = len (hour_info_2)
    if begining_2 [0] not in hour_info_2 [:][0] :
        begining_2[1] = 0
        hour_info_2.insert (0 , begining_2)
    if ending_2 [0] not in hour_info_2[:][0] :
        ending_2[1] = 0
        hour_info_2.insert (e_2 , ending_2)
        
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
##    x_teeth = []
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
    plt.bar(x, y,  width=0.5, color="green")
    plt.xticks(x , x_str) # this is for avoiding the show of other numbers on the x axis except the number of exact hours
    plt.xlabel('time (hour)')
    plt.ylabel('number of tweets')
    plt.savefig (my_path_W + 'time_hour_a.png',dpi=500) # here we give high dpi to save figures with great quality
    plt.show()

main ()
input ("press enter key to exit ...")
