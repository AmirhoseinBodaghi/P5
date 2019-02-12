def Retweet (my_path, worksheet1, worksheet9, my_path_judge) :
    from collections import defaultdict
    from operator import itemgetter
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
    import matplotlib as mpl


    
    tweet_number = worksheet9.cell(1, 0).value
    retweet_number = worksheet9.cell(1, 2).value
    Tweet_ID = worksheet1.col_values(21)
    Retweet_ID = worksheet1.col_values(23)
    ind= defaultdict(list)
    for i ,v in enumerate(Retweet_ID):
        ind[v].append(i)
    element_repeated_index = dict (ind)
    del element_repeated_index['Retweet ID']
    del element_repeated_index['Not a Retweet']
    pure_retweet_number = len(element_repeated_index) #number of origin retweets in dataset
    RT_LIST = []
    local_local_list = []
    local_list = []
    for i in element_repeated_index :
        local_list.append(i)
        local_list.append(element_repeated_index[i])
        local_list.append(len(element_repeated_index[i]))
        for j in Tweet_ID :
            if j==i :
                local_local_list.append (Tweet_ID.index(j))
        local_list.append(local_local_list)
        RT_LIST.append (local_list)
        local_local_list = []
        local_list = []

    for jjj in RT_LIST : #for those retweets which has their original tweet in the dataset we add 1 to the number of occurance
        if jjj[3]:
            jjj[2] = jjj[2] + 1
            
    RT_LIST_sorted = sorted (RT_LIST, key=itemgetter(2), reverse=True) #RT_LIST_sorted = [['retweet_id',[the row number of tweets in excel file (sheet1) that are this retweet],length of previous list ([the row number of tweets in excel file (sheet1) that are this retweet]), the row number of tweet that is pure and origin of this retweet (in the sheet1)],...] ,this list is sorted from the elements with maximum lenght of [the row number of tweets in excel file (sheet1) that are this retweet] to the minimum    
    number_retweet_with_their_origin_tweet_in_the_dataset = 0
    nnnn = 0
    for i in RT_LIST_sorted :
        nnnn += i[2]
        if i[3]:
            number_retweet_with_their_origin_tweet_in_the_dataset += 1


    #---- plot 1 ---- Frequency of Retweet Types + Size of Dataset With and Without Repeated Retweets -------
    fig = plt.figure ()
    gs = gridspec.GridSpec(2,2)
    mpl.rcParams['font.size'] = 6


    #-------
    fig1 = plt.subplot(gs[0,0])
    fig1.set_title ("a) Percentage of Retweet Types" , size=8)
    group_names_1 = ['Pure Retweet with Origin','Pure Retweet without Origin','Repeated Retweets']
    group_size_1 = [number_retweet_with_their_origin_tweet_in_the_dataset, (pure_retweet_number - number_retweet_with_their_origin_tweet_in_the_dataset), (retweet_number - pure_retweet_number)]
    fig1 = plt.pie (group_size_1, colors=['limegreen','aqua', 'orange'], autopct = '%1.1f%%')
    
    
    # change the position of the legend
    leg = plt.legend(fig1[0],  group_names_1 , bbox_to_anchor=(0.38,0.85) , prop={'size': 5})



    #--------
    fig2 = plt.subplot(gs[0,1])
    fig2.set_title ("b) Percentage of Repeated Retweet Types", size=8)
    group_size_2 = []
    x = "OK"


    if len(RT_LIST_sorted) > 2 :
        group_size_2.append (RT_LIST_sorted[0][2] - 1)
        group_size_2.append (RT_LIST_sorted[1][2] - 1)
        group_size_2.append ((retweet_number - pure_retweet_number) - RT_LIST_sorted[0][2] - RT_LIST_sorted[1][2]  + 2)
        group_names_2 = ['1stRepRetweet','2ndRepRetweet', 'The Rest' ]

    elif len(RT_LIST_sorted) > 1 :
        group_size_2.append (RT_LIST_sorted[0][2] - 1)
        group_size_2.append ((retweet_number - pure_retweet_number) - RT_LIST_sorted[0][2]  + 1)
        group_names_2 = ['1stRepRetweet', 'The Rest' ]

    else :
        x = "Not enought Retweet to Have this pie plot"
        
        
    if x !=  "Not enought Retweet to Have this pie plot" :
        fig2 = plt.pie (group_size_2,  autopct = '%1.1f%%')
        leg_2 = plt.legend(fig2[0],  group_names_2 , bbox_to_anchor=(0.89 ,0.85) ,  prop={'size': 5})



    #--------------    
    fig3 = plt.subplot(gs[1,:])
    fig3.set_title ("c) Size of Dataset With and Without Repeated Retweets", size=8)
    x = [0,1]
    group_names_3 = ['With Repeated Retweets', 'Without Repeated Retweets']
    SWORR = tweet_number - retweet_number + (pure_retweet_number - number_retweet_with_their_origin_tweet_in_the_dataset) #Size of dataset Without Repeated Retweets
    PNRT = tweet_number - retweet_number - number_retweet_with_their_origin_tweet_in_the_dataset #number of pure non_reTweet (ie not even original tweet of retweets
    
    PRT = SWORR - PNRT #number of pure retweet (ie even with their original tweets)
    group_size_3 = [tweet_number, SWORR]
    plt.xticks(x , group_names_3)
    plt.ylabel('number of tweets')
    plt.bar(x, group_size_3, color="steelblue")

    #--------------

    plt.savefig (my_path_judge + 'Retweet_Types_And_Effects_On_Size_Dataset.png',figsize=(30,30),dpi=2000) 
    plt.show()
    #--------------


    return RT_LIST_sorted, pure_retweet_number , PNRT, PRT
#---------------------------------
# the following function gives us an excel judge file which has whole the tweets inside (but only not redundent) to be given to an amazing judge who wants to judge all the tweets manualy to achieve 100 percent accuracy
def excel_judge_for_whole_tweets (my_path_judge, RT_LIST_sorted, worksheet1, worksheet1_w_all) :
    import xlsxwriter

    worksheet1_w_all.set_column (0,2,20) #this line is just for beauty of excell file, to extend the cells
    worksheet1_w_all.write(0, 0, 'Tweet ID') #the ID of tweet
    worksheet1_w_all.write(0, 1, '#Frequency')#the frequency of occurance in the dataset
    worksheet1_w_all.write(0, 2, 'Retweet ID')#the ID of Retweet
    worksheet1_w_all.set_column (3,5,260) #this line is just for beauty of excell file, to make big cells for writing TEXT data (increasing the width of Text columns)
    worksheet1_w_all.write(0, 3, 'Text') #the text of tweet
    worksheet1_w_all.write(0, 4, 'Retweet Text') #the ID of Retweet
    worksheet1_w_all.write(0, 5, 'Quote Text') #the text of Quote
    worksheet1_w_all.set_column (6,6,15)
    worksheet1_w_all.write(0, 6, 'Judge_decision') #the Judge's decision  (r = rumor , a = anti-rumor , q = related to rumor but not a rumor not an anti-rumor , n = none related to rumor)

    
    retweet_id_list = []
    
    for j in RT_LIST_sorted :
        retweet_id_list.append (j[0])


    row = 1        
    for sss in RT_LIST_sorted :
        tweet_ID = "Not a Tweet"
        if sss[3]:
            frequency = len(sss[1]) + 1
        else :
            frequency = len(sss[1])    
        retweet_ID = sss[0]
        text = worksheet1.cell((int(sss[1][0])), 20).value
        rt_tex =  worksheet1.cell((int(sss[1][0])), 22).value
        qt_text = worksheet1.cell((int(sss[1][0])), 24).value
        
        worksheet1_w_all.write(row, 0, tweet_ID)
        worksheet1_w_all.write(row, 1, frequency)
        worksheet1_w_all.write(row, 2, retweet_ID)
        worksheet1_w_all.write(row, 3, text)
        worksheet1_w_all.write(row, 4, rt_tex)
        worksheet1_w_all.write(row, 5, qt_text)

        row += 1

    Tweet_ID = worksheet1.col_values(21)
    number_tweets = len (Tweet_ID)
    i = 1
    while i < number_tweets :
        if (worksheet1.cell(i, 21).value not in retweet_id_list) and (worksheet1.cell(i, 23).value not in retweet_id_list) :
            worksheet1_w_all.write(row, 0, worksheet1.cell(i, 21).value)
            worksheet1_w_all.write(row, 1, 1)
            worksheet1_w_all.write(row, 2, "Not a Retweet")
            worksheet1_w_all.write(row, 3, worksheet1.cell(i, 20).value)
            worksheet1_w_all.write(row, 4, worksheet1.cell(i, 22).value)
            worksheet1_w_all.write(row, 5, worksheet1.cell(i, 24).value)

            row += 1
                
        i += 1



             

#---------------------------------------------
def main ():
    import xlrd
    import random
    import xlsxwriter
    
    
    my_path = 'D:\\Papers\\Social Network Mining\\Creating_Dataset\\Step6\\False Rumors\\False_Rumor_25\\Input\\'
    my_path_judge = 'D:\\Papers\\Social Network Mining\\Creating_Dataset\\Step6\\False Rumors\\False_Rumor_25\\Output\\'

    workbook = xlrd.open_workbook(my_path + 'excel_results.xlsx')
    worksheet1 = workbook.sheet_by_name('Sheet1')
    worksheet9 = workbook.sheet_by_name('Sheet9')

    workbook_w = xlsxwriter.Workbook(my_path_judge + 'excel_judge.xlsx')
    worksheet1_w = workbook_w.add_worksheet()

    workbook_w_all = xlsxwriter.Workbook(my_path_judge + 'excel_judge_whole.xlsx')
    worksheet1_w_all = workbook_w_all.add_worksheet()

    tweet_number = worksheet9.cell(1, 0).value


    RT_LIST_sorted, pure_retweet_number, PNRT, PRT = Retweet (my_path, worksheet1, worksheet9, my_path_judge)

    
    # -- Defining the number of tweets we want to give to the judges to have it as the learning dataset -- (the numbers made by an estimation of power the judges can put on the work ...)
    if tweet_number < 2000 :
        tweet_number_learning_dataset_whole = 100
    elif tweet_number < 5000 :
        tweet_number_learning_dataset_whole = 150
    elif tweet_number < 10000 :
        tweet_number_learning_dataset_whole = 200
    elif tweet_number < 50000 :
        tweet_number_learning_dataset_whole = 250
    else :
        tweet_number_learning_dataset_whole = 300
    #-----------------------------
    
    # defining the share of retweets (retweets and original tweets of them in pure tweets) and non_retweets (pure, qoute, reply, retweet&quote, retweet&quote&reply, reply&quote) in the learning dataset   
    retweet_percentage = worksheet9.cell(2, 2).value
    retweet_percentage_without_percentage_sign = retweet_percentage.replace ('%','')
    retweet_percentage_float = float (retweet_percentage_without_percentage_sign)
    tweet_number_learning_dataset_retweet = round ((retweet_percentage_float*tweet_number_learning_dataset_whole)/100) #for giving to the judges we just choose retweets that are pure 
    tweet_number_learning_dataset_nonretweet = round (((100 - retweet_percentage_float)*tweet_number_learning_dataset_whole)/100) #for giving to the judges we just choose retweets that are pure 
    if PRT < tweet_number_learning_dataset_retweet : #in special cases when this situation happens then the size of out learning dataset changes
        tweet_number_learning_dataset_retweet = PRT     
    if PNRT < tweet_number_learning_dataset_nonretweet : #in special cases when this situation happens then the size of out learning dataset changes
        tweet_number_learning_dataset_nonretweet = PNRT

    tweet_number_learning_dataset_whole = tweet_number_learning_dataset_retweet + tweet_number_learning_dataset_nonretweet #if any changes happens to dataset this line update the size of dataset
    
    #------------------------------    
    # selecting tweets for the learning Dataset
    import_tweets_index = []
    removed_tweets_index = []
    #------------------------------
    # selecting retweets for the learning dataset (** IT IS NOT BY RANDOM, IT IS BY ORDER OF MOST REPETEAD RETWEETS IN THE DATASET **)
    # -------------------------------------------
    ii = 0

    all_retweet_index = [] #   index of retweets (only retweets ie not retweet-quote & retweet-rply & ...) + index of their origin 
    for eee in RT_LIST_sorted :
        for eeee in eee[1]:
            all_retweet_index.append(eeee)
        if eee[3]:
            all_retweet_index.append(eee[3][0])
    
        
    same_tweets_global = []
    while ii < tweet_number_learning_dataset_retweet :
        if RT_LIST_sorted[ii][1][0] not in removed_tweets_index :
            import_tweets_index.append (RT_LIST_sorted[ii][1][0])
            removed_tweets_index_local = []
            for j in RT_LIST_sorted[ii][1]:
                removed_tweets_index.append (j)
                removed_tweets_index_local.append (j)
            if RT_LIST_sorted[ii][3]:
                removed_tweets_index.append (RT_LIST_sorted[ii][3][0])
                removed_tweets_index_local.append (RT_LIST_sorted[ii][3][0])
            same_tweets_global.append (removed_tweets_index_local)
            
        ii += 1


    # -------------------------------------------
    # selecting non_retweets for the learning dataset (** IT IS BY RANDOM **)
    # -------------------------------------------
    jj = 0
    while jj < tweet_number_learning_dataset_nonretweet :
        xx = random.randint (1,(tweet_number-1)) 
        while (xx in all_retweet_index) or (xx in import_tweets_index) :
            xx = random.randint (1,(tweet_number-1))
        import_tweets_index.append(xx)
        removed_tweets_index.append(xx)
        jj += 1







    
    # -------------------------------------------
    row = 1 #because row=0 is for titles


    # Sheet1 for giving to judge 
    worksheet1_w.set_column (0,2,20) #this line is just for beauty of excell file, to extend the cells
    worksheet1_w.write(0, 0, 'Tweet ID') #the ID of tweet
    worksheet1_w.write(0, 1, '#Frequency')#the frequency of occurance in the dataset
    worksheet1_w.write(0, 2, 'Retweet ID')#the ID of Retweet
    worksheet1_w.set_column (3,5,260) #this line is just for beauty of excell file, to make big cells for writing TEXT data (increasing the width of Text columns)
    worksheet1_w.write(0, 3, 'Text') #the text of tweet
    worksheet1_w.write(0, 4, 'Retweet Text') #the ID of Retweet
    worksheet1_w.write(0, 5, 'Quote Text') #the text of Quote
    worksheet1_w.set_column (6,6,15)
    worksheet1_w.write(0, 6, 'Judge_decision') #the Judge's decision  (r = rumor , a = anti-rumor , q = related to rumor but not a rumor not an anti-rumor , n = none related to rumor)


    #--- W.R.I.T.H ---Retweet --- D.A.T.A --------
    for listt in same_tweets_global:
        tweet_ID = worksheet1.cell((listt[0]), 21).value
        frequency = len(listt)
        retweet_ID = worksheet1.cell((listt[0]), 23).value
        text = worksheet1.cell((listt[0]), 20).value
        rt_tex =  worksheet1.cell((listt[0]), 22).value
        qt_text = worksheet1.cell((listt[0]), 24).value


        # writing to worksheet1_w ---        
        worksheet1_w.write(row, 0, tweet_ID)
        worksheet1_w.write(row, 1, frequency)
        worksheet1_w.write(row, 2, retweet_ID)
        worksheet1_w.write(row, 3, text)
        worksheet1_w.write(row, 4, rt_tex)
        worksheet1_w.write(row, 5, qt_text)

        row += 1

    
    #--- W.R.I.T.H ---nonRetweet --- D.A.T.A --------
    while row < tweet_number_learning_dataset_whole + 1  :
        tweet_ID = worksheet1.cell((import_tweets_index [row - 1]), 21).value
        frequency = 1
        retweet_ID = 'Not a Retweet Only'
        text = worksheet1.cell((import_tweets_index [row - 1]), 20).value
        rt_tex =  worksheet1.cell((import_tweets_index [row - 1]), 22).value
        qt_text = worksheet1.cell((import_tweets_index [row - 1]), 24).value


        # writing to worksheet1_w ---        
        worksheet1_w.write(row, 0, tweet_ID)
        worksheet1_w.write(row, 1, frequency)
        worksheet1_w.write(row, 2, retweet_ID)
        worksheet1_w.write(row, 3, text)
        worksheet1_w.write(row, 4, rt_tex)
        worksheet1_w.write(row, 5, qt_text)

        row += 1

    #--- making the whole tweets dataset        
    excel_judge_for_whole_tweets (my_path_judge, RT_LIST_sorted, worksheet1, worksheet1_w_all) 

        
    workbook_w.close()
    workbook_w_all.close()
    # -------------------------------------------
      


main()
input ("press any key to exit...")



