# P5
An Analysis on Newly Emerged Rumors on Twitter

This is an eleven-stage project that has been devised to first make a newyly-emerged rumor dataset out of Twitter and then do a set of analysis (Micro + Macro) on it. These eleven stages (from S4 to S14), each one comes with a distinct python code with the following short decription for each one :

S4 : This code crawls the tweets related to the rumor we want to hunt. But prior to the running of the code we should have made a Twitter API so the API keys be set in the code. Also we would need to set the queries (key words related to the rumor) in the code, so to capture only those tweets that include the queries. The output which is the collection of all tweets related to the rumor will be ready in a .jsonl file.

S5 : This code by getting the S4 output as its input, seperates the data into meaningful pieces of information and then organizes them in an excell file. This excell file assigns one distinct row for each tweet and save its information (including tweet ID, User ID, Date amd Time and ...) in the columns.

S6 : This code by getting the S5 output as its input, picks up a set of tweets to then get used for human annotation. The seleccting strategies is based on the fact that tweets with more ferequencies of occures in the dataset are in priority since annotating them by human would have left less tweets for machine and the overall accuracy of the dataset would be higher. However the specified size for this pack of selected tweets and the desire to have tweets from all kinds (even those with less frequency) lead the code to choose the most appropriate tweets. This code also provides another output that is the collection of all tweets of the dataset minus the repetitive versions. This collection can be used when human anotators want to annotate whole the dataset all by their own as we would see in S6-1 (without using machine)

S6-1 : The output of S6, the one that includes the whole tweets of the dataset minus the repetetive versions, afte being anotated by the anotators will be given to this code as the input so the annotations will be assigned to the repetetive versions of tweets and the final dataset would be ready as the output.

S7 :  The output of S6, the one that includes only a selected collection of the whole tweets, afte being anotated by the anotators will be given to this code as the inputs (two input excell files) to this code, and this code checks if the entries (r: rumor, a: anti-rumor, q: related to the rumor, n: not related to the rumor) are given correctly and if so then by computing the Kappa coeficient examines the conformity between the anotatores. The output is the excell file ready to get used for extracting of the learning features. 

S8 :  This code by getting the S7 output as its input, extracts all the unigrams and bigrams from all the tweets in the collection. And then yeilds out an excell file in which for each tweet (in a distinct row) it clarifies the existence of each feature (in a distinct column) by 1 and 0 numbers. The output is the excell file ready to get used for machine learning.

S9 : This code by getting the S8 output as its input, and using the random forest algorithm, learns the machine to be able to annotate the rest of the tweets. Indeed by running this code we would have all the tweets anotated and finally the accuracy of the dataset would be calculated by the code. The output of this code is final anotated excell file of the dataset.

S10 :
