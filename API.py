#!/usr/bin/python2.7
import time
import json
import urllib2
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener
import sys
import threading




api_key='*************************************'
url = 'http://api.openweathermap.org/data/2.5/weather?units=metric&mode=json'
location = "San Jose"
location1 = location.replace(' ', '%20')

def publish_callback(result, status):
	pass    #print "Message trasnmitted \n"
    # Handle PNPublishResult and PNStatus
	#	print status
	#print result

def recv ():
	while 1:
		result = my_listener.wait_for_message_on('awesomeChannel')
		print(result.message)
		if str(result.message)=="{u'text': u'exit'}":
			break

def send ():
	print "You are now online and can send and receive messages in real time\n"
	while 1:	
		print "\nTo Send Message Type - s\nTo Exit Type - e"
		time.sleep(2)		
		s = raw_input("\n\n Input -->")
		if s=='s':
			msg = raw_input("\nEnter the message :")
			msg1 = "User 1 - " + msg
			pubnub.publish().channel('awesomeChannel').message(msg1).async(publish_callback)
		elif s=='e':
			break
	#	elif s=='w' :
			
	#		weather()
					
	#		print "Temp ="msg1
	#		msg2 = str(msg1)
	#		pubnub.publish().channel('awesomeChannel').message(msg2).async(publish_callback)
def time1():
	while 1:
		data = time.localtime(time.time())
		rng = [0,10,20,30,40,50,60]
		if  data.tm_min in rng:
	       		weather()
			time.sleep(60)

def weather():
	url1 = url + "&q=" + location1 + "&appid=" + api_key
	data =  urllib2.urlopen(url1)
	data1= json.load(data)
#	print data1
	#print "\n The Weather Report of " + location + " is -->>"
	msg1 = "\nWeather Report of San Jose\n\n"
	pubnub.publish().channel('awesomeChannel').message(msg1).async(publish_callback) 
	temp1 = data1['main']['temp']
	temp1 = "Temp=" +str(temp1)
	pubnub.publish().channel('awesomeChannel').message(temp1).async(publish_callback)
	pressure = data1['main']['pressure']
	pressure1 =  "Press = " + str(pressure)
	pubnub.publish().channel('awesomeChannel').message(pressure1).async(publish_callback)
	humidity = data1['main']['humidity']
	humidity1 = "Hdty= " + str(humidity)
	pubnub.publish().channel('awesomeChannel').message(humidity1).async(publish_callback)
	
#	wthr = data1['weather']
#	print "\n Weather = " + str(wthr[1:])
if __name__ == '__main__':
	
	pnconfig = PNConfiguration()
	pnconfig.publish_key = 'pub-c-***********************' #publish key 
	pnconfig.subscribe_key = 'sub-c-*******************' #subscribe key
	pubnub = PubNub(pnconfig)

	
	my_listener = SubscribeListener()
	pubnub.add_listener(my_listener)
 
	pubnub.subscribe().channels('awesomeChannel').execute()
	my_listener.wait_for_connect()
	print('connected')

	
	t = threading.Thread(name='Recv', target=recv)
	d = threading.Thread(name='Send', target=send)
	w = threading.Thread(name='wthr', target=time1)	
        d.start()
        t.start()
	w.start()
        d.join()
	pubnub.unsubscribe().channels("awesomeChannel").execute()
	print "Channel is Unsubscribed and now closing the porgram"
	quit()
        
        
