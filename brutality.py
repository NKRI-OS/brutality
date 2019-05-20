#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from threading import Thread
import argparse
import re
import time
import sys
from yaml import load
import md5
from termcolor import colored

def getBanner():
	print '''
	
 ▄▄▄▄   ██▀███  █    ██▄▄▄█████▓▄▄▄      ██▓    ██▄▄▄█████▓██   ██▓
▓█████▄▓██ ▒ ██▒██  ▓██▓  ██▒ ▓▒████▄   ▓██▒   ▓██▓  ██▒ ▓▒▒██  ██▒
▒██▒ ▄█▓██ ░▄█ ▓██  ▒██▒ ▓██░ ▒▒██  ▀█▄ ▒██░   ▒██▒ ▓██░ ▒░ ▒██ ██░
▒██░█▀ ▒██▀▀█▄ ▓▓█  ░██░ ▓██▓ ░░██▄▄▄▄██▒██░   ░██░ ▓██▓ ░  ░ ▐██▓░
░▓█  ▀█░██▓ ▒██▒▒█████▓  ▒██▒ ░ ▓█   ▓██░██████░██░ ▒██▒ ░  ░ ██▒▓░
░▒▓███▀░ ▒▓ ░▒▓░▒▓▒ ▒ ▒  ▒ ░░   ▒▒   ▓▒█░ ▒░▓  ░▓   ▒ ░░     ██▒▒▒ 
▒░▒   ░  ░▒ ░ ▒░░▒░ ░ ░    ░     ▒   ▒▒ ░ ░ ▒  ░▒ ░   ░    ▓██ ░▒░ 
 ░    ░  ░░   ░ ░░░ ░ ░  ░       ░   ▒    ░ ░   ▒ ░ ░      ▒ ▒ ░░  
 ░        ░       ░                  ░  ░   ░  ░░          ░ ░     
      ░                                                    ░ ░     

A Fuzzer for any GET entries - ManhNho
Version: 0.1

	'''

def checkURL(url):
	regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
        r'localhost|' # localhost...
        r'(?:2(?:5[0-5]|[0-4][0-9])|[0-1]?[0-9]{1,2})(?:\.(?:2(?:5[0-5]|[0-4][0-9])|[0-1]?[0-9]{1,2})){3})' # IP...
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
	if re.match(regex,url) != None:
		pass
	else:
		print 'Please re-check input >> %s << \nExit...'%(url)
		sys.exit(0)

class performReq(Thread):
	def __init__(self, url, excpt, rmv, proxy, custom, word):
		Thread.__init__(self)
		try:
			global browser 
			browser = requests.session()
			self.word = word.split('\n')[0].strip() 
			self.newURL = url.replace('FUZZ', self.word) # Replace 'FUZZ' to word from wordlist
			self.url = self.newURL
			self.excpt = excpt
			self.rmv = rmv
			#import pdb; pdb.set_trace()
			self.custom = {'User-Agent':'Mozilla/5.0 (Mobile; rv:26.0) Gecko/26.0 Firefox/26.0'}
			self.custom = dict(self.custom)
			if custom != None:
				self.custom = dict(custom)
			for key,value in self.custom.iteritems():
				browser.headers[key] = value
			self.proxy = ''
			if proxy != None:
				self.proxy = proxy
				protocol = ''.join(re.findall(r'(?:http)s?://',self.proxy)).split(':')[0]
				browser.proxies[protocol] = self.proxy
		except Exception, e:
			raise e

	def run(self):
		try:
			start = time.time()
			r = browser.get(self.url) #, verify = False)
			stop = time.time()
			totalTime = str(stop-start)
			lines = str(r.content.count('\n'))
			chars = len(r.content)
			code = int(r.status_code)
			hasher = md5.new(r.content).hexdigest()
			if r.history != []:
				firstStatus = r.history[0]
				code = int(firstStatus.status_code)
			else:
				pass
			if self.excpt and self.rmv:
				if self.excpt != code and self.rmv != int(chars):
					print '%s \t %s \t %s \t %s \t %s \t %s' %(totalTime, colored(str(code),'green'), colored(str(chars),'yellow'), lines, hasher, self.url)
			elif not self.rmv and self.excpt:
				if self.excpt != code:
					if 200 <= code < 300:
						print '%s \t %s \t %s \t %s \t %s \t %s' %(totalTime, colored(str(code),'green'), chars, lines, hasher, self.url)
					if 300 <= code < 400:
						print '%s \t %s \t %s \t %s \t %s \t %s' %(totalTime, colored(str(code),'blue'), chars, lines, hasher, self.url)
					if 400 <= code < 500:
						print '%s \t %s \t %s \t %s \t %s \t %s' %(totalTime, colored(str(code),'red'), chars, lines, hasher, self.url)
			elif not self.excpt and self.rmv:
				if self.rmv != int(chars):
					if 200 <= code < 300:
						print '%s \t %s \t %s \t %s \t %s \t %s' %(totalTime, colored(str(code),'green'), colored(str(chars),'yellow'), lines, hasher, self.url)
					if 300 <= code < 400:
						print '%s \t %s \t %s \t %s \t %s \t %s' %(totalTime, colored(str(code),'blue'), colored(str(chars),'yellow'), lines, hasher, self.url)
					if 400 <= code < 500:
						print '%s \t %s \t %s \t %s \t %s \t %s' %(totalTime, colored(str(code),'red'), colored(str(chars),'yellow'), lines, hasher, self.url)
			else:
					if 200 <= code < 300:
						print '%s \t %s \t %s \t %s \t %s \t %s' %(totalTime, colored(str(code),'green'), chars, lines, hasher, self.url)
					if 300 <= code < 400:
						print '%s \t %s \t %s \t %s \t %s \t %s' %(totalTime, colored(str(code),'blue'), chars, lines, hasher, self.url)
					if 400 <= code < 500:
						print '%s \t %s \t %s \t %s \t %s \t %s' %(totalTime, colored(str(code),'red'), chars, lines, hasher, self.url)
			counter[0] = counter[0] - 1 # remove 1 thread from counter
		except Exception, e:
			raise e

def launchThreads(url, thrd, excpt, rmv, proxy, custom, words):
	global counter
	counter = []
	resultList = []
	counter.append(0)
	print '*'*120
	print 'Time \t\t Code \t Chars \t Lines \t MD5 \t\t\t\t\t URLs'
	print '*'*120
	for i in range(0,len(words)-1):
		try:
			if counter[0] < thrd:
				word = words[i]
				counter[0] = counter[0] + 1
				thread = performReq(url, excpt, rmv, proxy, custom, word)
				thread.start()
		except KeyboardInterrupt:
			print 'Keyboard interrupted by user. Finish attack!'
			sys.exit()
		i+=1
		thread.join()
	return

def main():
	getBanner()
	parser = argparse.ArgumentParser() # Create ArgumentParser object
	parser.add_argument('-u','--url', type=str, required=True, help='Target website with FUZZ params, for exapmle: \'http://abc.com/index.php?p=FUZZ\'')
	parser.add_argument('-t','--thread', type=int, default=3, dest='thrd', help='Set working threads, default: 3')
	parser.add_argument('-f','--file', type=str, default='./wordlist/simple_dirs.txt', help='Set wordlist')
	parser.add_argument('-e','--exception', type=int, choices=[200,302,401,403,404,500], help='Set status code for hidding, \
		choose from provided list')
	parser.add_argument('-r','--remove', type=int, help='Set Chars length for hidding')
	parser.add_argument('-p','--proxy', type=str, help='Set network proxy, such as: http://127.0.0.1:8080')
	parser.add_argument('-c','--custom', type=load, help='Custom header by adding json value, for example: \
		"{\'User-Agent\':\'Firefox\', \'Cookies\':\'abcdef\'}"')
	args = parser.parse_args() # Return opts and args
	url = args.url
	checkURL(url) # Check valid input url address
	thrd = args.thrd
	excpt = args.exception
	rmv = args.remove
	proxy = args.proxy
	if proxy != None:
		checkURL(proxy) # Check valid input proxy address
	custom = args.custom
	inputfile = args.file
	try:
		f = open(inputfile, 'r')
		words = f.readlines()
	except:
		print 'Failed to open >> %s << file! Exit...'%(inputfile)
		sys.exit(0)
	launchThreads(url, thrd, excpt, rmv, proxy, custom, words)

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print 'Keyboard interrupted by user, stop working...!'
