#-------------------------------------------
#This program gets a series of screen names for twitter accounts as an input and gives the IDs of friends and followers for those accounts.
#-------------------------------------------
def main ():    
    import time
    import tweepy
    import xlrd
    import xlsxwriter
    import math
    from tweepy import API
    from tweepy import Cursor
    from tweepy import OAuthHandler

    #Use your keys
    consumer_key = 'EVqx22v0Yb70v7zxY2szQkbmD'
    consumer_secret = 'zltJQ5ZtUfnoNIPAVzruV4E0y4N8JKwap7H5W1fGjw2WKoHjcP' 
    access_token = '771997625105219584-80jgMmbpd1t7SEEluUk2tTR1OmSL9mS'
    access_secret = 'v80pt8bYgbOhKOG6vkz4uHvlMbV188Uc20olxpbBwmacm'

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = API(auth)

    #Reading ------------------
    my_path_R = 'D:\\Papers\\Social Network Mining\\Analysis_of_Rumor_Dataset\\Step 14\\Rumor_24\\Input\\'
    workbook_input = xlrd.open_workbook(my_path_R + 'Results_Step_10.xlsx')
    worksheet1_input = workbook_input.sheet_by_name('Sheet1')
    Screen_Name = worksheet1_input.col_values(1)
    number_followers = worksheet1_input.col_values(14)
    number_followings = worksheet1_input.col_values(15)
    Screen_Name = worksheet1_input.col_values(1)
    del Screen_Name [0]
    del number_followers [0]
    del number_followings [0]
    
    
    # *******   dividing the input to be able to run program in smaller sesseions  ****** 
    # running this program for each 50 users takes about 1 hour, so we divide the input users in smaller sessions to not be urged to keep laptop on for a long time
    # we break the whole number of screen names to this set of [m:n] i.n.c.l.u.d.i.n.g the screen name with index m, and e.x.c.l.u.d.i.n.g the screen name with index n
    # for example if we have 1000 screen names and we want to run the program for all of it in once we use m = 0 and n = 1000
    # but if want to run the program in sessions for that 1000 users, in which each session not takes more than 2 hours, we should give only 100 users as input to the program in each session
    # so for first run we have m = 0 , n = 100 and for second run we have m = 100 , n = 200 , ... , and m = 900 , n = 1000 for the last session
    m = int (input ("Please enter the beginning index of input, the code should cover  : "))
    n = int (input ("Please enter the ending index of input, the code should cover : "))
    Screen_Name = Screen_Name [m:n] # Just remember the next run of this
    number_followers = number_followers [m:n] #we need this for finding the time we should wait for the crawling
    number_followings = number_followings [m:n] #we need this for finding the time we should wait for the crawling
    total_number_of_users = len (Screen_Name)


    #calculating the number of required columns for saving the data in excel worksheet
    #since the max number of columns in a worksheet is less than 16,384 so we count for each run how many columns would be required to save data
    #and if that be more than 16000 (a little less than the exact amount makes a safe marging for us) then the code asks us to re run the code by shrinking the interval of [m,n)
    #each user naturaly takes 2 columns (one for followings and one for followers) but only if the number of followings and followers be less than 1 M otherwise for each extra 1M we should consider an exxtra column for that user
    number_required_columns = total_number_of_users*2
    for nfr in number_followers :
        number_required_columns = number_required_columns + nfr // 1000000 
    for nfw in number_followings :
        number_required_columns = number_required_columns + nfw // 1000000

    print ("The number of required columns :", number_required_columns)
    if number_required_columns > 16000 :
        print ("Sorry the number of required columns for this run is out of the capacity for one single worksheet, so please re run the code and shrink the interval [m,n)")
    else :
        #calculates the approximate time for crawling the users (from user m to user n-1)
        #we can crawl the id of followers for 15 users (by GET followers/ids endpoint) in every 15 minutes only if the sum of followers for those users is less than 75000, other wise for each extra 75000 we need one more 15 min for the crwal, for example 15 users with 75001 followers need 30 min to be crawled
        #we can crawl the id of followings for 15 users (by GET followings/ids endpoint) in every 15 minutes only if the sum of followings for those users is less than 75000, other wise for each extra 75000 we need one more 15 min for the crwal, for example 15 users with 75001 followings need 30 min to be crawled
        #since we use both followers and followings endpoints in a same program the time we will need for crwal will be equal to the maximum time of them (not sum of them just max of them), for example if followers take 15min and followings take 30 min , we will need to wait for 30 min
        #please note the time we calculate here is approximation because the number of followers and followings that we use for the calculation were achieved by the time running Step5 code and now they migh be changed :)
        t_fr = math.ceil (sum (number_followers) / 75000)
        t_fw = math.ceil (sum (number_followings) / 75000)
        t_user = math.ceil (total_number_of_users/15)
        time_list = []
        time_list.append (t_fr)
        time_list.append (t_fw)
        time_list.append (t_user)
        print ("The crawling takes about :", max(time_list)*15, " min")
        print ("=====================================================")
        answer = input ("Can you wait for that time, untill the code be terminated ? (press y if yes) :  ")
        print ("=====================================================")


        
        if answer == "y" :
                
            #Writing ------------------
            my_path_W = 'D:\\Papers\\Social Network Mining\\Analysis_of_Rumor_Dataset\\Step 14\\Rumor_24\\Output\\'  #address for saving result files (this line need to be re write for new datasets according to the desired address we want to put the results in them)
            name_output = "Results_Step_14" + "_index_" + str (m) + "_to_" + str (n) + ".xlsx" #we put the last index user achieved by the last program on its output, so by looking at its name we can notice right off the bat that the next run should cover which interval 
            workbook_output = xlsxwriter.Workbook(my_path_W + name_output)
            worksheet1_output = workbook_output.add_worksheet()

            #-----
            print ("total_number_of_users : ",total_number_of_users)


            #-------
            #writing the followings to the excell
            #Please note that for saving in excell we have the excell limitations which are as follow :
            #Max number of Rows in a worksheet : 1,048,576
            #Max number of Columns in a worksheet : 16,384
            #These limitations means if we only use one worksheet then we can only save data for up to 16,384 users and for each of them we can save up to 1,048,567 followers or friends names 
            #Since most of Datasets has less than 16,384 users, we dont bother to add the second worksheet in this program however if the number of users will be more than that amount then
            #the program warns at the begining that number of users is more than the space of only one worksheet to save, so asks you to consider the second worksheet in the program
            #Furthermore for those users who have more than 1,048,567 followers or followings, the programs saves the name of them and at the end of running give their name to us so we can crawl their followers or friends seperatly by giving them more than only one column            

            if total_number_of_users < 16384 : #however since we break the input into smaller parts this condition never can be broken !
                print ("**********************************************")
                y = 0
                j = 0 
                while y < total_number_of_users :
                    #getting followers
                    print ("=================")
                    print (y)
                    print (Screen_Name[y])
                    user_exist = 1
                    followers_list_id = []
                    pages_fw = tweepy.Cursor(api.followers_ids, screen_name = Screen_Name[y]).pages()
                    while True:
                        try :
                            page_fw = next(pages_fw)
                        except tweepy.TweepError as e:
                            print (e) #this shows the error, if error is caused by the following three cases then we capture it and the program continues OTHERWISE the error stops the program however we can see what type of error it was and we can bring it here as the 4th case to capture in the program
                            if '404' in e.reason : #This line captures error resulted when the user is not existed anymore  
                                print ("User Does not exist anymore !")
                                user_exist = 0
                                break
                            
                            elif '401' in e.reason : #This line captures error resulted when the user account is protected 
                                print ("User is protected !")
                                user_exist = 0
                                break
                            
                            elif 'Failed to send request:' in e.reason : #This line captures error resulted when the connection or VPN is lost.
                                print ('timeout error caught. machine goes to sleep for 100 seconds, Do not worry :) just make the Connection right...')
                                time.sleep(100)
                                continue

                            elif 'Rate limit exceeded' or '429' in e.reason : #This line captures error resulted when rate limit is reached. it waits in durations of 15 min till the rate limit is over.
                                print ('Rate limit reached, Do not worry :) just wait 15 min ...')
                                time.sleep(60*15)
                                continue
                                
                        except StopIteration:
                            print("StopIteration : No more Tweets!")
                            break

                        if user_exist == 1 :
                            for idd in page_fw:
                                followers_list_id.append(idd)


                           
                    #writing the followers to the excell
                    name_followers = Screen_Name[y] + "_followers"
                    worksheet1_output.write(0, j, name_followers)
                    number_followers = len (followers_list_id)
                    i = 0
                    u = 0
                    row_n = 0
                    while i < number_followers  :
                        worksheet1_output.write(row_n + 1, j, followers_list_id[i]) # i+1, because the first row of each column belong to name label
                        row_n += 1
                        i += 1
                        if i // 1000000 > u : #the max amount of cells in a column in excell (however the max is a little bit more than 1 M but to have a safe margin we set it to 1 M)
                            j += 1
                            u += 1
                            row_n = 0
                            name_followers = Screen_Name[y] + "_followers" + "_" + str (u)
                            worksheet1_output.write(0, j, name_followers)
                                
                            
                                
                    j += 1 #going to the next column for writing followings ids
                    
                    #-------------------------------------------    
                    #get id of followings
                    followings_list_id = []
                    user_exist = 1
                    pages_fr = tweepy.Cursor(api.friends_ids, screen_name = Screen_Name[y]).pages()

                    while True:
                        try :
                            page_fr = next(pages_fr)
                        except tweepy.TweepError as e:
                            print (e) #this shows the error, if error is caused by the following three cases then we capture it and the program continues OTHERWISE the error stops the program however we can see what type of error it was and we can bring it here 
                            if '404' in e.reason : #This line captures error resulted when the user is not existed anymore  
                                print ("User Does not exist anymore ! ")
                                user_exist = 0
                                break

                            elif '401' in e.reason : #This line captures error resulted when the user account is protected 
                                print ("User is protected !")
                                user_exist = 0
                                break
                            
                            elif 'Failed to send request:' in e.reason: #This line captures error resulted when the connection or VPN is lost.
                                print ('timeout error caught. machine goes to sleep for 100 seconds, Do not worry :) just make the Connection right...')
                                time.sleep(100)
                                continue

                            elif 'Rate limit exceeded' or '429' in e.reason: #This line captures error resulted when rate limit is reached. it waits in durations of 15 min till the rate limit is over.
                                print ('Rate limit reached, Do not worry :) just wait 15 min ...')
                                time.sleep(60*15)
                                continue
                                
                        
                        except StopIteration:
                            print("StopIteration : No more Tweets!")
                            break


                        if user_exist == 1 :
                            for idd in page_fr:
                                followings_list_id.append(idd)


                    name_followings = Screen_Name[y] + "_followings"
                    worksheet1_output.write(0, j, name_followings)
                    number_followings = len (followings_list_id)
                    i = 0
                    u = 0
                    row_n = 0
                    while i < number_followings  :
                        worksheet1_output.write(row_n + 1, j, followings_list_id[i]) # i+1, because the first row of each column belong to name label
                        row_n += 1
                        i += 1
                        if i // 1048570 > u : #the max amount of cells in a column in excell (however the max is a little bit more than 1 M but to have a safe margin we set it to 1 M)
                            j += 1
                            u += 1
                            row_n = 0
                            name_followings = Screen_Name[y] + "_followings_" + str (u)
                            worksheet1_output.write(0, j, name_followings)
                    
                    if user_exist == 1 :
                        print ("number of followers : ", number_followers)
                        print ("number of followings : ", number_followings)
                        
                    else :
                        print ("User account is out of reach!")


                    j += 1 #going to the next column for the next user
                    y += 1 #going to the next user
                workbook_output.close()

            else :
                print ("Number of Users is more than capacity of only one excell worksheet, consider the second worksheet in the program")

            

#-----------------------------------------

main ()
print ("################################")
input ("press enter key to exit...")



