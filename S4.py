import tweepy
import string
import time
from tweepy import API
from tweepy import Cursor
from tweepy import OAuthHandler
import json
import sys
import socket
import errno


#Use your keys
consumer_key = 'EVqx22v0Yb70v7zxY2szQkbmD'
consumer_secret = 'zltJQ5ZtUfnoNIPAVzruV4E0y4N8JKwap7H5W1fGjw2WKoHjcP' 
access_token = '771997625105219584-80jgMmbpd1t7SEEluUk2tTR1OmSL9mS'
access_secret = 'v80pt8bYgbOhKOG6vkz4uHvlMbV188Uc20olxpbBwmacm'


auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = API(auth)
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
tweet_num = 0

search_term = 'racist memorabilia Elizabeth Warren'
name_dataset = 'ElizabethWarren.jsonl' ## :) B.E Careful to put .jsonl format at the end of name  (: otherwise you will have to use json_to_jsonl_convertor to make the output file as jsonl to fit as an acceptable file for the next programes 
path_output = "D:\\Papers\\Social Network Mining\\Creating_Dataset\\Step4\\False Rumors\\False_Rumor_26\\Output\\" #do not forget to put \\ at the end of address
path_final = path_output + name_dataset

c = tweepy.Cursor(api.search,q=search_term,tweet_mode='extended').items(90000)

        
f = open (path_final,'w+') 
while True:
    try :
        tweet = c.next()
        if 'retweeted_status' in dir(tweet) :
            tweet_text = tweet.retweeted_status.full_text
        else :
            tweet_text = tweet.full_text
        
        f.write(json.dumps(tweet._json) + "\n")
        tweet_num += 1
        
        print (tweet_num)
        print (tweet.id)
        print (tweet_text.translate(non_bmp_map))
        print (tweet.created_at)
        print (tweet.source)
        
        if tweet.in_reply_to_status_id :
            print ("in_reply_to_status_id",tweet.in_reply_to_status_id)
            print ("in_reply_to_user_id",tweet.in_reply_to_user_id)
        else :
            print (" this tweet is not a reply to any other tweet ")
            
        
        if tweet.coordinates :
            print (tweet.coordinates)
        else :
            print ("there is no coordinate recorded for this tweet")


        if tweet.place :
            print (tweet.place)
        else :
            print ("there is no place recorded for this tweet")
            

        if tweet.is_quote_status :
            if 'quoted_status_id' in dir(tweet) :
                print ("quoted_status_id : " , tweet.quoted_status_id)
            else :
                print ("quoted_status_id is not available")
        else :
            print ("this tweet is not a quote of any other tweet")


        if hasattr(tweet, 'quote_count') :
            print ("tweet.quote_count",tweet.quote_count)
        else :
            print ("tweet.quote_count, 0")
            
            
        if hasattr (tweet, 'reply_count'):
            print ("tweet.reply_count",tweet.reply_count)
        else :
            print ("tweet.reply_count, 0")
        
        if hasattr (tweet, 'retweet_count') :
            print ("retweet_count",tweet.retweet_count)
        else :
            print ("retweet_count, 0")

        if hasattr (tweet, 'favorite_count') :
            print ("favorite_count",tweet.favorite_count)
        else :
            print ("favorite_count, 0")
        
        print ("------------------------------------------------------------------")


    except tweepy.TweepError as e :
        print (e) #this shows the error, if error is caused by the following three cases then we capture it and the program continues OTHERWISE the error stops the program however we can see what type of error it was and we can bring it here as the 4th case to capture in the program
        if 'Rate limit exceeded' in e.reason: #This line captures error resulted when rate limit is reached. it waits in durations of 100 sec till the rate limit is over.
            print ('Rate limit reached, Do not worry :) just wait 15 min ...')
            time.sleep(60*15)
            continue
            
        if 'Failed to send request:' in e.reason: #This line captures error resulted when the connection or VPN is lost.
            print ('timeout error caught. machine goes to sleep for 100 seconds, Do not worry :) just make the Connection right...')
            time.sleep(100)
            continue

##    except ConnectionResetError:
##        print ("Please wait 1 min for Connection Reset")
##        time.sleep(60)
##        reconnect()
##        retry_action()
##        

    except StopIteration:
        print("StopIteration : No more Tweets!")
        break
