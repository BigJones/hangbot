import asyncio
import datetime
from datetime import timedelta, datetime
from fractions import Fraction
import glob
import json
import os
import random
import threading
from urllib import parse, request
from bs4 import BeautifulSoup
from dateutil import parser
import hangups
import re
import requests
from Core.Commands.Dispatcher import DispatcherSingleton
from Core.Util import UtilBot
from Libraries import Genius
#lunsj command
from html.parser import HTMLParser
import urllib.request, urllib.error, urllib.parse


reminders = []

@DispatcherSingleton.register
def botisback(bot, event, *args):
	segments = [hangups.ChatMessageSegment("I'm back bitches", is_bold=True),
	hangups.ChatMessageSegment('\n', hangups.SegmentType.LINE_BREAK),
	hangups.ChatMessageSegment("Suck a dick.")]
	bot.send_message_segments(event.conv, segments)

@DispatcherSingleton.register
def whatsnew(bot, event, *args):
	segments = [hangups.ChatMessageSegment("Whats new?", is_bold=True),
	hangups.ChatMessageSegment('\n', hangups.SegmentType.LINE_BREAK),
	hangups.ChatMessageSegment("v0.4: Upated for new sio menu"),
	hangups.ChatMessageSegment('\n', hangups.SegmentType.LINE_BREAK),
	hangups.ChatMessageSegment("(this shit is static)")]
	bot.send_message_segments(event.conv, segments)

@DispatcherSingleton.register
def bane(bot, event, *args):
	segments = [	hangups.ChatMessageSegment("T-bane", is_bold=True),
					hangups.ChatMessageSegment('\n', hangups.SegmentType.LINE_BREAK),
				]	

	bot.send_message_segments(event.conv, segments)
	print("%s", args[0])
	ruter_url = 'http://reisapi.ruter.no/stopvisit/getdepartures/3010370?json=true'
	ruter_json = json.load(urllib2.urlopen(ruter_url))

	print(ruter_json)

	if args[0] == "west":
		segments = [hangups.ChatMessageSegment("t-bane, west")]
		bot.send_message_segments(event.conv, segments)
	elif args[0] == "east": 
		segments = [hangups.ChatMessageSegment("t-bane, east")]
		bot.send_message_segments(event.conv, segments) 

@DispatcherSingleton.register
def udefine(bot, event, *args):
	if ''.join(args) == '?':
		segments = [hangups.ChatMessageSegment('Urbanly Define', is_bold=True),
		hangups.ChatMessageSegment('\n', hangups.SegmentType.LINE_BREAK),
		hangups.ChatMessageSegment(
			'Usage: /udefine <word to search for> <optional: definition number [defaults to 1st]>'),
			hangups.ChatMessageSegment('\n', hangups.SegmentType.LINE_BREAK),
			hangups.ChatMessageSegment('Purpose: Define a word.')]
		bot.send_message_segments(event.conv, segments)

	else:
		api_host = 'http://urbanscraper.herokuapp.com/search/'
		num_requested = 0
		returnall = False
	if len(args) == 0:
		bot.send_message(event.conv, "Invalid usage of /udefine.")
		return
	else:
		if args[-1] == '*':
			args = args[:-1]
			returnall = True
	if args[-1].isdigit():
	# we subtract one here because def #1 is the 0 item in the list
		num_requested = int(args[-1]) - 1
		args = args[:-1]

	term = parse.quote('.'.join(args))
	response = requests.get(api_host + term)
	error_response = 'No definition found for \"{}\".'.format(' '.join(args))

	if response.status_code != 200:
		bot.send_message(event.conv, error_response)
		result = response.content.decode()
		result_list = json.loads(result)
		num_requested = min(num_requested, len(result_list) - 1)
		num_requested = max(0, num_requested)
		result = result_list[num_requested].get(
			'definition', error_response)
	if returnall:
		segments = []
	for string in result_list:
		segments.append(hangups.ChatMessageSegment(string))
		segments.append(hangups.ChatMessageSegment('\n', hangups.SegmentType.LINE_BREAK))
		bot.send_message_segments(event.conv, segments)
	else:
		segments = [hangups.ChatMessageSegment(' '.join(args), is_bold=True),
		hangups.ChatMessageSegment('\n', hangups.SegmentType.LINE_BREAK),
		hangups.ChatMessageSegment(result + ' [{0} of {1}]'.format(
				num_requested + 1, len(result_list)))]

		bot.send_message_segments(event.conv, segments)


@DispatcherSingleton.register
def lunsj(bot, event, *args):
	print("LUNSJ")
	usage = [		hangups.ChatMessageSegment('USAGE:', is_bold=True),
			hangups.ChatMessageSegment('\n', hangups.SegmentType.LINE_BREAK),
			hangups.ChatMessageSegment('/lunsj ifi (Informatikkafeen)'),
			hangups.ChatMessageSegment('\n', hangups.SegmentType.LINE_BREAK),
			hangups.ChatMessageSegment('/lunsj fred <dagens/vegetar/halal> (Frederikke spiseri)')
			]

	#Fredrikke cafe url
	urlFred = 'http://www.sio.no/wps/portal/!ut/p/c5/04_SB8K8xLLM9MSSzPy8xBz9CP0os3gDfwNvJ0dTP0NXAyNDA38TC3cDKADKR2LKmyDkidGNAzgS0h0Oci1-28HyuM3388jPTdUvyA2NMMgyUQQAAcWpkQ!!/dl3/d3/L0lDU0lKSWdrbUEhIS9JRFJBQUlpQ2dBek15cXchLzRCRWo4bzBGbEdpdC1iWHBBRUEhLzdfME8wS0JBNU4xRTBNSDJWMzVQMDAwMDAwMDAvN2x0YlQ2Mzk3MDAxOQ!!/?WCM_PORTLET=PC_7_0O0KBA5N1E0MH2V35P00000000000000_WCM&WCM_GLOBAL_CONTEXT=/wps/wcm/connect/migration/sio/mat+og+drikke/dagens+middag/frederikke+spiseri'
#IFI cafe url

	urlIFI = 'http://www.sio.no/wps/portal/!ut/p/c5/04_SB8K8xLLM9MSSzPy8xBz9CP0os3gDfwNvJ0dTP0NXAyNDA38TC3cDKADKR2LKmyDkidGNAzgS0h0Oci1-28HyuM3388jPTdUvyA2NMMgyUQQAAcWpkQ!!/dl3/d3/L0lDU0lKSWdrbUEhIS9JRFJBQUlpQ2dBek15cXchLzRCRWo4bzBGbEdpdC1iWHBBRUEhLzdfME8wS0JBNU4xRTBNSDJWMzVQMDAwMDAwMDAvN2x0YlQ2Mzk3MDAxOQ!!/?WCM_PORTLET=PC_7_0O0KBA5N1E0MH2V35P00000000000000_WCM&WCM_GLOBAL_CONTEXT=/wps/wcm/connect/migration/sio/mat+og+drikke/dagens+middag/informatikkafeen'

	class MLStripper(HTMLParser):
			def __init__(self):
				super().__init__()
				self.reset()
				self.fed = []
				self.addFlag = False
			def handle_data(self, d):
				if self.addFlag:
					self.fed[-1] += d
					self.addFlag = False
				else:
					self.fed.append(d)

			def handle_entityref(self, ref):
				self.fed[-1] += self.unescape("&%s;" % ref)
				self.addFlag = True

			def get_data(self):
				return self.fed

	enToNo = {'Monday':'Mandag', 'Tuesday':'Tirsdag', 'Wednesday':'Onsdag', 'Thursay':'Torsdag', 'Friday':'Fredag'}

	def strip_tags(html):
		s = MLStripper()
		s.feed(html)
		return s.get_data()

	#Format function for fredrikke
	#Returns  a formatted string
	def format_fred(data):
		tmp = [x for x in data if x not in ['\xa0', ' ', '\n']]
		print(tmp)
		dict = {}

		tmp = [s.replace(u'\xa0', '') for s in tmp] # remove all the 8s

		iD = tmp.index("Dagens:")	#Finds index of Dagens/Vegetar/Halal
		iV = tmp.index("Vegetar:")
		iH = tmp.index("Halal: ")

		print("%d::%d::%d", iD, iV, iH)


		dict[tmp[:iV][0][:-1].lower()] = tmp[:iV][1:]	
		dict[tmp[iV:][0][:-2].lower()] = tmp[iV:iH][1:] 
		dict[tmp[iH:][0][:-1].lower()] = tmp[iH:][1:]

		segments = [	hangups.ChatMessageSegment(args[1].upper() + ":", is_bold=True),
						hangups.ChatMessageSegment('\n', hangups.SegmentType.LINE_BREAK)
						]		

		for i in dict[args[1].lower()]:
			segments.append(hangups.ChatMessageSegment(i))
			segments.append(hangups.ChatMessageSegment('\n', hangups.SegmentType.LINE_BREAK))
		return segments

	#Used to translate current day to norwegian for dict-key purposes.
	enToNo = {'Monday':'Mandag', 'Tuesday':'Tirsdag', 'Wednesday':'Onsdag', 'Thursday':'Torsdag', 'Friday':'Fredag'}

	def format_ifi(data):
		print("IFI")
		#.encode('utf8', 'ignore') if characters bugs
		data = [x for x in data if x not in [ '\n\n', '\n', '\xc2\xa0', '\xa0', 'Dagens: ', ' ', 'Dagens:', 'Vegetar:']]
		print(data)

		days = data[:5]
		food = data[5:]
		food.append("No veggie today D:") #Incase dagens and vegetar are the same on fridays.

		result = {}
		day = datetime.today().strftime("%A")
		for i in range(len(days)):
			result[days[i]] = (food[i*3], food[i*3+1], food[i*3+2]) #Two foods pr day

		segments = [	hangups.ChatMessageSegment(enToNo[day], is_bold=True),
						hangups.ChatMessageSegment('\n', hangups.SegmentType.LINE_BREAK),
						hangups.ChatMessageSegment('\tDagens: ' + result[enToNo[day]][0]),
						hangups.ChatMessageSegment('\n', hangups.SegmentType.LINE_BREAK),
						hangups.ChatMessageSegment('\tFisk: ' + result[enToNo[day]][1]),
						hangups.ChatMessageSegment('\n', hangups.SegmentType.LINE_BREAK),
						hangups.ChatMessageSegment('\tVegetar: ' + result[enToNo[day]][2]),
					]

		if(day == "Friday"):
			segments = [ hangups.ChatMessageSegment(enToNo[day], is_bold=True),
						hangups.ChatMessageSegment('\n', hangups.SegmentType.LINE_BREAK),
						hangups.ChatMessageSegment('\tDagens: ' + result[enToNo[day]][0]),
						hangups.ChatMessageSegment('\tVegetar: ' + result[enToNo[day]][1]),
						]

		return segments



	url = ""
	format_func = ""
	if len(args) < 1:
		bot.send_message_segments(event.conv, usage)
		return
	elif args[0].lower() == "ifi":
		url = urlIFI
		format_func = format_ifi
	elif args[0].lower() == "fred":
		if len(args) < 2 or args[1].lower() not in ['dagens', 'vegetar', 'halal']:
			bot.send_message_segments(event.conv, usage)
			return
		url = urlFred
		format_func = format_fred
	else:
		bot.send_message_segments(event.conv, usage)
		return

	#Opens given url and returns html
	try:
		page = urllib.request.urlopen(url, timeout=10)
	except urllib.error.HTTPError as err:
		if err.code == 404:
			hangups.ChatMessageSegment('HTTP error' + err.code)
			return

	#Html parsing
	soup = BeautifulSoup(page)

	#Finds the data we are looking for and feeds that to the formatting function.
	divtag = soup.find_all('div', {'class': 'sioArticleBodyText'})
	if len(divtag) > 0:
		tabletag = divtag[0].find_all('table')
		trtag = tabletag[0].find_all('tr')	   
		text = str.join('',list(map(str,trtag)))
		data = strip_tags(text)
		bot.send_message_segments(event.conv, format_func(data))
	else:
		print("ERROR")
	page.close()
