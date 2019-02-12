#----------------------------------------------------------------------
def get_the_judge_decisions (worksheet1_amir,worksheet1_jonice) :

    #for the following data, it does not matter if we get them from Jonice file or Amir file , because they are same
    Tweet_ID_List = worksheet1_amir.col_values(0) 
    Frequency_List = worksheet1_amir.col_values(1)
    Retweet_ID_List = worksheet1_amir.col_values(2)
    Text_List = worksheet1_amir.col_values(3)
    Retweet_Text_List = worksheet1_amir.col_values(4)
    Quote_Text_List = worksheet1_amir.col_values(5)

    Amir_vote_List = worksheet1_amir.col_values(6)
    
    Jonice_vote_List = worksheet1_jonice.col_values(6)

    del Tweet_ID_List[0] #to delete the label of column
    del Frequency_List[0]
    del Retweet_ID_List[0]
    del Text_List[0]
    del Retweet_Text_List[0]
    del Quote_Text_List[0]
    del Amir_vote_List[0] #to delete the label of column
    del Jonice_vote_List[0] #to delete the label of column

    number_tweet = len (Amir_vote_List)
    k = 0
    Amir_vote = []
    Jonice_vote = []
    while k < number_tweet :
        Amir_vote.append (Amir_vote_List[k].lower())
        Jonice_vote.append (Jonice_vote_List[k].lower())
        k += 1
        
    i = 0
    accepted_letters = ["r","a","q","n"]
    x = "Dataset is Ok"
    while i < number_tweet :
        if Amir_vote[i] not in accepted_letters :
            print ("Non Standard Letter in Amir's votes is :", Amir_vote[i])
            print ("Non Standard Letter in Amir's votes is in Row Number :", i + 2)
            x = "Dataset Needs to be corrected"

        if Jonice_vote[i] not in accepted_letters :
            print ("Non Standard Letter in Jonice's vote is :", Jonice_vote[i])
            print ("Non Standard Letter in Jonice's is in Row Number :", i + 2)
            x = "Dataset Needs to be corrected"
            
        i += 1
         

    return Amir_vote,Jonice_vote,number_tweet,x,Tweet_ID_List,Frequency_List, Retweet_ID_List, Text_List, Retweet_Text_List, Quote_Text_List
    
#----------------------------------------------------------------------
def kappa_cohen_coefficient (Amir_vote,Jonice_vote,number_tweet) :
    import sklearn
    from sklearn.metrics import cohen_kappa_score
    j = 0
    non_match_votes = [] #number of row in excel table
    while j < number_tweet :
        if Amir_vote[j] != Jonice_vote[j] :
            non_match_votes.append (j+2)
            
            
        j += 1

    labels = ["r","a","q","n"]
            
    cks = cohen_kappa_score (Amir_vote, Jonice_vote, labels)
    print ("cohen_kappa_score :", cks)
    if cks > 0.4 : #according to Feliss standard
        print (" Congratulations, Datasets are appropriate for giving to machine.")
        wow = "inter-rater agreement is acceptable"
    else :
        print (" Sorry! , inter-rater agreement is not acceptable.")
        print (" Please, let judges work again on the votes which their row number in the excel table come as follow :")
        print (non_match_votes)
        wow = "inter-rater agreement is not acceptable"

    return wow

#----------------------------------------------------------------------
def give_final_judgment (Amir_vote, Jonice_vote, number_tweet, Tweet_ID_List, Frequency_List, Retweet_ID_List, Text_List, Retweet_Text_List, Quote_Text_List):
    import xlsxwriter
    my_path_judge = 'D:\\Papers\\Social Network Mining\\Creating_Dataset\\Step7\\False Rumors\\False_Rumor_24\\Output\\'
    j = 0
    final_vote = [] #number of row in excel table
    while j < number_tweet :
        if Amir_vote[j] == Jonice_vote[j] :
            final_vote.append (Amir_vote[j])        
        else :
            if Amir_vote[j] == 'r' and Jonice_vote[j] == 'a' :
                final_vote.append ('q')
            elif Amir_vote[j] == 'r' and Jonice_vote[j] == 'q' :
                final_vote.append ('r')
            elif Amir_vote[j] == 'r' and Jonice_vote[j] == 'n' :
                final_vote.append ('q')
            elif Amir_vote[j] == 'a' and Jonice_vote[j] == 'r' :
                final_vote.append ('q')
            elif Amir_vote[j] == 'a' and Jonice_vote[j] == 'q' :
                final_vote.append ('a')
            elif Amir_vote[j] == 'a' and Jonice_vote[j] == 'n' :
                final_vote.append ('q')
            elif Amir_vote[j] == 'q' and Jonice_vote[j] == 'r' :
                final_vote.append ('r')
            elif Amir_vote[j] == 'q' and Jonice_vote[j] == 'a' :
                final_vote.append ('a')
            elif Amir_vote[j] == 'q' and Jonice_vote[j] == 'n' :
                final_vote.append ('n')
            elif Amir_vote[j] == 'n' and Jonice_vote[j] == 'a' :
                final_vote.append ('q')
            elif Amir_vote[j] == 'n' and Jonice_vote[j] == 'r' :
                final_vote.append ('q')
            elif Amir_vote[j] == 'n' and Jonice_vote[j] == 'q' :
                final_vote.append ('n')

        j += 1

    workbook_final_judgment = xlsxwriter.Workbook(my_path_judge + 'final_judgment.xlsx')
    worksheet1_final_judgment = workbook_final_judgment.add_worksheet()
    worksheet1_final_judgment.set_column (0,2,20) #this line is just for beauty of excell file, to extend the cells
    worksheet1_final_judgment.write(0, 0, 'Tweet ID') #the ID of tweet
    worksheet1_final_judgment.write(0, 1, '#Frequency')#the frequency of occurance in the dataset
    worksheet1_final_judgment.write(0, 2, 'Retweet ID')#the ID of Retweet
    worksheet1_final_judgment.set_column (3,5,260) #this line is just for beauty of excell file, to make big cells for writing TEXT data (increasing the width of Text columns)
    worksheet1_final_judgment.write(0, 3, 'Text') #the text of tweet
    worksheet1_final_judgment.write(0, 4, 'Retweet Text') #the ID of Retweet
    worksheet1_final_judgment.write(0, 5, 'Quote Text') #the text of Quote
    worksheet1_final_judgment.set_column (6,6,15)
    worksheet1_final_judgment.write(0, 6, 'State')#the frequency of occurance in the dataset

    row_n = 0
    while row_n < number_tweet :
        worksheet1_final_judgment.write(row_n + 1, 0, Tweet_ID_List[row_n])
        worksheet1_final_judgment.write(row_n + 1, 1, Frequency_List[row_n])
        worksheet1_final_judgment.write(row_n + 1, 2, Retweet_ID_List[row_n])
        worksheet1_final_judgment.write(row_n + 1, 3, Text_List[row_n])
        worksheet1_final_judgment.write(row_n + 1, 4, Retweet_Text_List[row_n])
        worksheet1_final_judgment.write(row_n + 1, 5, Quote_Text_List[row_n])
        worksheet1_final_judgment.write(row_n + 1, 6, final_vote[row_n])
        row_n += 1
        
        
#----------------------------------------------------------------------
def main ():
    import xlrd
    my_path = 'D:\\Papers\\Social Network Mining\\Creating_Dataset\\Step7\\False Rumors\\False_Rumor_24\\Input\\'

    workbook_amir = xlrd.open_workbook(my_path + 'after_judge_amir.xlsx')
    worksheet1_amir = workbook_amir.sheet_by_name('Sheet1')
    
    workbook_jonice = xlrd.open_workbook(my_path + 'after_judge_jonice.xlsx')
    worksheet1_jonice = workbook_jonice.sheet_by_name('Sheet1')

    Amir_vote,Jonice_vote,number_tweet,x,Tweet_ID_List,Frequency_List, Retweet_ID_List, Text_List, Retweet_Text_List, Quote_Text_List = get_the_judge_decisions (worksheet1_amir,worksheet1_jonice)
    if x == "Dataset is Ok" :
        wow = kappa_cohen_coefficient (Amir_vote,Jonice_vote,number_tweet)
        if wow == "inter-rater agreement is acceptable" :
            give_final_judgment (Amir_vote, Jonice_vote, number_tweet, Tweet_ID_List, Frequency_List, Retweet_ID_List, Text_List, Retweet_Text_List, Quote_Text_List)
    else :
        print ("Please Correct your datasets and then run this program again!")
#----------------------------------------------------------------------
main()
input ("press enter key to exit ...")
#------------
