#-------------------------------------------
#This program gets the output of Step11 (Result_step_11) as input and uses its first sheet which includes user who were chosen randomly from pure users in each of the four categories (not all six categories because cat5 and cat6 are not important for us)
#Indeed this program calculates "eta squared" to find corelation between user category and each of the followings features of the users :
#1- Mean Percentage of Pure Tweets
#2- Mean of Favorited per Tweet
#3- Mean of Favorited per Follower
#4- Mean of Retweeted per Tweet
#5- Mean of Retweeted per Follower
#Please note that we used "eta squared" because this kind of correlation fits for finding relation between two variables that one of them is nominal (user category) and the other is interval (each of the five above mentioned user featured )
#-------------------------------------------
def eta_squared (x,y): #x values of dependent variable and y values of nominal (independent) variable , note that we know y has 4 category
    import numpy as np
    number_all = len (x)
    i = 0
    cat_1 = []
    cat_2 = []
    cat_3 = []
    cat_4 = []
    while i < number_all :
        if y[i] == 1 :
            cat_1.append (x[i])
        elif y[i] == 2 :
            cat_2.append (x[i])   
        elif y[i] == 3 :
            cat_3.append (x[i])
        elif y[i] == 4 :
            cat_4.append (x[i])
        i += 1
        
    Mean = np.mean(x)
    i = 0
    SS_E = 0
    while i < number_all :
        SS_E += (x[i] - Mean)**2
        i += 1

    nc1 = len(cat_1)
    nc2 = len(cat_2)
    nc3 = len(cat_3)
    nc4 = len(cat_4)
    
    SS_TR = (nc1*((np.mean(cat_1)- Mean)**2)) + (nc2*((np.mean(cat_2)- Mean)**2)) + (nc3*((np.mean(cat_3)- Mean)**2)) + (nc4*((np.mean(cat_4)-Mean)**2))
    SS_Total = SS_E + SS_TR
    eta_squared = SS_TR/SS_Total

    
    return eta_squared

def main ():
    import xlrd
    import xlsxwriter
    import numpy as np
    from scipy.stats import pearsonr
    from scipy.stats import spearmanr

    #Reading ------------------
    my_path_R = 'D:\\Papers\\Social Network Mining\\Analysis_of_Rumor_Dataset\\Step 12\\Rumor_13\\Input\\'  #address for saving result files (this line need to be re write for new datasets according to the desired address we want to put the results in them)
    workbook_input = xlrd.open_workbook(my_path_R + 'Results_Step_11.xlsx')
    worksheet1_input = workbook_input.sheet_by_name('Sheet1')
    User_Existence = worksheet1_input.col_values(1)
    Percentage_of_Pure_Tweets = worksheet1_input.col_values(2)
    Favorited_per_Tweet = worksheet1_input.col_values(3)
    Favorited_per_Follower = worksheet1_input.col_values(4)
    Retweeted_per_Tweet = worksheet1_input.col_values(5)
    Retweeted_per_Follower = worksheet1_input.col_values(6)
    User_Category = worksheet1_input.col_values(7)

    del User_Existence [0]
    del Percentage_of_Pure_Tweets [0]
    del Favorited_per_Tweet [0]
    del Favorited_per_Follower [0]
    del Retweeted_per_Tweet [0]
    del Retweeted_per_Follower [0]
    del User_Category [0]
    
    
    i = 0
    number_user = len (User_Category)
    index_of_deleted_rows = []

    while i < number_user :
        if (User_Existence[i] == "NO") or (Favorited_per_Tweet[i] == "NAN/INF") or (Favorited_per_Follower[i] == "NAN/INF") or (Retweeted_per_Tweet[i] == "NAN/INF") or (Retweeted_per_Follower[i] == "NAN/INF") or (User_Category[i] == 6) or (User_Category[i] == 5) :
            index_of_deleted_rows.append (i)
        i += 1

    for j in sorted(index_of_deleted_rows, reverse=True):
        del Percentage_of_Pure_Tweets [j]
        del Favorited_per_Tweet [j]
        del Favorited_per_Follower [j]
        del Retweeted_per_Tweet [j]
        del Retweeted_per_Follower [j]
        del User_Category [j]

    

    # eta_squared correlation
    PPT_to_UC_eta = eta_squared (Percentage_of_Pure_Tweets,User_Category) 
    FT_to_UC_eta = eta_squared (Favorited_per_Tweet,User_Category) 
    FF_to_UC_eta = eta_squared (Favorited_per_Follower,User_Category) 
    RT_to_UC_eta = eta_squared (Retweeted_per_Tweet,User_Category) 
    RF_to_UC_eta = eta_squared (Retweeted_per_Follower,User_Category) 
    

    #Writing ------------------
    my_path_W = 'D:\\Papers\\Social Network Mining\\Analysis_of_Rumor_Dataset\\Step 12\\Rumor_13\\Output\\'  #address for saving result files (this line need to be re write for new datasets according to the desired address we want to put the results in them)
    workbook_output = xlsxwriter.Workbook(my_path_W + 'Results_Step_12.xlsx')
    worksheet1_output = workbook_output.add_worksheet() #Sheet 1 (Spearman and Pearson Correlations)

    worksheet1_output.set_column (0,1,45) #extend the width of columns 
    worksheet1_output.write(0, 1, "eta_squared Correlation")


    worksheet1_output.write(1, 0, "'Percentage of Pure Tweet' to 'User Category'")
    worksheet1_output.write(2, 0, "'Favorite per Tweet' to 'User Category'")
    worksheet1_output.write(3, 0, "'Favorite per Follower' to 'User Category'")
    worksheet1_output.write(4, 0, "'Retweet per Tweet' to 'User Category'")
    worksheet1_output.write(5, 0, "'Retweet per Follower' to 'User Category'")
    #------------------
    worksheet1_output.write(1, 1, PPT_to_UC_eta)
    worksheet1_output.write(2, 1, FT_to_UC_eta)
    worksheet1_output.write(3, 1, FF_to_UC_eta)
    worksheet1_output.write(4, 1, RT_to_UC_eta)
    worksheet1_output.write(5, 1, RF_to_UC_eta)


#-------------------------------------------
main ()
input ("Press enter to exit ... ")

    



    
    
