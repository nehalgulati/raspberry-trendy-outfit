############################################################################
## Theme: E-Wearable Workshop
## Topic: Visualising #TrendyOutfit using Twitter
## Timeline: 1 week
## P.S: Need error handling and futher implementation clarifications. 
############################################################################

import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from tweepy import API
from Tkinter import *
import Tkinter as tk
#from PIL import Image, ImageTk
from textblob import TextBlob
import requests
import csv
import struct
import datetime
import serial
import os
import time
import json
import nltk

#import lcd_16x2_1      #python file for gathering input from LCD Raspberry pi

tweets = 0
hashes  = []
item = ''


arduinoData = serial.Serial('/dev/ttyACM0', baudrate = 9600, timeout = 1)
print arduinoData.readline()  

arduinoValues = 3
dataList = [0]*arduinoValues
rgb_list = [0]*arduinoValues


access_token = "your-access-token"
access_secret = "your-access-secret"
consumer_key = "your-consumer-key"
consumer_secret = "your-consumer-secret"


###################### For Listening to Authenticator through Twitter Stream API ########################


class MyListener(StreamListener):

    def __init__(self, api=None):
        super(MyListener, self).__init__()
        self.num_tweets = 0
        self.fd = open('tweet1_custom.txt', 'w')
        self.writer = csv.writer(self.fd)

    def on_data(self, data):
        try:
            data = json.loads(data)
            user_info = data["user"]
            
            row = [(user_info["followers_count"]), (user_info["friends_count"]), (user_info["statuses_count"]), (user_info["followers_count"])%255, (user_info["friends_count"])%255, (user_info["statuses_count"])%255]
            self.writer.writerow(row)
            
            for i in range(0,arduinoValues):
                values = [row[3],row[4],row[5]]

            for j in values: 
                arduinoData.write(struct.pack('>B',j))

            #If followers_count becomes more than less than 100, between 100 - 3500, more than 3500, blinking state becomes slower, normal, faster 
            #If statuses_count becomes more than less than 100, between 100 - 3500, more than 3500, brightness state becomes more, normal and rainbow color()
            #If freinds_count becomes more than less than 100, between 100 - 3500, more than 3500, brightness state becomes faster
            
            #print(data["text"])
            
            blob = TextBlob(data["text"])
            for sentence in blob.sentences:
                print(sentence.sentiment.polarity)

            self.fd.flush()
            print values

        except BaseException as e:
            print('Error occurred', e)

        return True


    def on_error(self, status):
        print(status)
        return True

    def on_status(self, status):
        record = {'Text': status.text, 'Created At': status.created_at}
        print(record)
        self.num_tweets += 1
        if self.num_tweets < 10:
            collection.insert(record)
            return True
        else:
            self.fd.close()
            raise SystemExit

    def deleteContent(fd):
        os.ftruncate(fd, 0)
        os.lseek(fd, 0, os.SEEK_SET)
        #os.flush()




auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = API(auth)

twitter_stream = Stream(auth, MyListener())


################################### For testing #####################################

#noHashtag = input('How many hashtags do you want to search for? ')
#number = ''

#for i in range(int(noHashtag)):
# Hashtag = raw_input('Enter a hashtag with # ')
# if item == '':
#     item = item + Hashtag
# else:
#     item = item + ', ' + Hashtag



################################### For GUI display #####################################

def check_hashtag(hashtag_entry):
    print("%s" %hashtag_entry)


def get_tweets(hashtag_entry):
    print("Searching tweets for %s...\n" %hashtag_entry)
    twitter_stream.filter(track=[hashtag_entry])


def format_response(tweet_data): #something wrong here#
    #tweet_data = user_info["text"]
    return str(tweet_data)

def clear_entry(event, entry):
    entry.delete(0, END)

def close_window():
	 root.destroy()
	 

root = tk.Tk()
root.wm_attributes('-fullscreen','true')

w, h = root.winfo_screenwidth(), root.winfo_screenheight()
#root.geometry("%dx%d+0+0" % (w, h))

mycanvas = Canvas(root,height=h,width=w)
mycanvas.config(background="#000000")
mycanvas.pack(fill='none')

myframe = Frame(root)
myframe.config(background="#000000")
myframe.place(bordermode=INSIDE,relx=0.25,rely=0.25,relwidth=0.5,relheight=0.5)
#myframe.pack(fill='none')

L1 = tk.Label(myframe, text="Search what's trending hashtag",bg='#000000', font=("HelveticaNeue Light", 24),pady=10,fg='#ffffff')
L1.pack(expand=0)

E1 = tk.Entry(myframe, bd=0,justify=CENTER,selectborderwidth=100,font=("HelveticaNeueLTStd-Bd", 64),bg='#000000', foreground='#ffffff',borderwidth=0, highlightthickness=0, )
E1.pack(expand=0, fill='both')

B1 = tk.Button(myframe, text=" Search ", border=0, bd=0, bg='red',font=("Heebo-Regular", 16),foreground='#ffffff', highlightbackground='#000000', command=lambda: get_tweets(E1.get()))
B1.place(relx=0.45,rely=0.45,relwidth=.1,relheight=.1)

B2 = tk.Button(myframe, text=" Exit ", border=0, bd=0, bg='#000000',font=("Heebo-Regular", 16),foreground='#ffffff', highlightbackground='red', command=close_window)
B2.place(relx=0.45,rely=0.60,relwidth=.1,relheight=.1)

#output_frame = Frame(myframe,bg='red')
#output_frame.place(relx=1,rely=0.8,relwidth=1,relheight=1,anchor='e')

#L2 = tk.Label(output_frame)
#L2.place(relwidth=1,relheight=1)

root.mainloop()
