#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from threading import Thread
import re
import time
import sys
from hashlib import md5
from termcolor import colored

from arguments_parser import args


def get_banner():
    print(
        '''
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
    )


def check_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'(?:2(?:5[0-5]|[0-4][0-9])|[0-1]?[0-9]{1,2})(?:\.(?:2(?:5[0-5]|[0-4][0-9])|[0-1]?[0-9]{1,2})){3})'  # IP...
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE
    )
    if re.match(regex, url):
        pass
    else:
        print('Please re-check input >> %s << \nExit...' % url)
        sys.exit(0)


class PerformReq(Thread):
    def __init__(self, url, excpt, rmv, proxy, custom, word):
        Thread.__init__(self)
        try:
            global browser
            browser = requests.session()
            self.word = word.split('\n')[0].strip()
            # Replace 'FUZZ' to word from wordlist
            self.newURL = url.replace('FUZZ', self.word)
            self.url = self.newURL
            self.excpt = excpt
            self.rmv = rmv
            self.custom = {
                'User-Agent': 'Mozilla/5.0 (Mobile; rv:26.0) Gecko/26.0 Firefox/26.0'   # noqa
            }
            self.custom = dict(self.custom)
            if custom:
                self.custom = dict(custom)
            for key, value in self.custom.items():
                browser.headers[key] = value
            self.proxy = ''
            if proxy:
                self.proxy = proxy
                protocol = ''.join(
                    re.findall(r'(?:http)s?://', self.proxy)
                ).split(':')[0]
                browser.proxies[protocol] = self.proxy
        except Exception:
            raise Exception

    def run(self):
        try:
            start = time.time()
            r = browser.get(self.url)  # , verify = False)
            stop = time.time()
            total_time = str(stop - start)
            lines = str(r.content.decode("utf-8").count('\n'))
            chars = len(r.content)
            code = int(r.status_code)
            hasher = md5(r.content).hexdigest()
            if r.history:
                first_status = r.history[0]
                code = int(first_status.status_code)
            else:
                pass
            if self.excpt and self.rmv:
                if self.excpt != code and self.rmv != int(chars):
                    # TODO define a function
                    print(
                        '%s \t %s \t %s \t %s \t %s \t %s' % (
                            total_time, colored(str(code), 'green'),
                            colored(str(chars), 'yellow'), lines, hasher,
                            self.url
                        )
                    )
            elif not self.rmv and self.excpt:
                if self.excpt != code:
                    if 200 <= code < 300:
                        # TODO define a function
                        print(
                            '%s \t %s \t %s \t %s \t %s \t %s' % (
                                total_time, colored(str(code), 'green'), chars,
                                lines, hasher, self.url
                            )
                        )
                    if 300 <= code < 400:
                        print(
                            '%s \t %s \t %s \t %s \t %s \t %s' % (
                                total_time, colored(str(code), 'blue'), chars,
                                lines, hasher, self.url
                            )
                        )
                    if 400 <= code < 500:
                        print(
                            '%s \t %s \t %s \t %s \t %s \t %s' % (
                                total_time, colored(str(code), 'red'), chars,
                                lines, hasher, self.url
                            )
                        )
            elif not self.excpt and self.rmv:
                if self.rmv != int(chars):
                    if 200 <= code < 300:
                        print('%s \t %s \t %s \t %s \t %s \t %s' % (
                            total_time, colored(str(code), 'green'),
                            colored(str(chars), 'yellow'), lines, hasher,
                            self.url))
                    if 300 <= code < 400:
                        print('%s \t %s \t %s \t %s \t %s \t %s' % (
                            total_time, colored(str(code), 'blue'),
                            colored(str(chars), 'yellow'), lines, hasher,
                            self.url))
                    if 400 <= code < 500:
                        print('%s \t %s \t %s \t %s \t %s \t %s' % (
                            total_time, colored(str(code), 'red'),
                            colored(str(chars), 'yellow'), lines, hasher,
                            self.url))
            else:
                if 200 <= code < 300:
                    print('%s \t %s \t %s \t %s \t %s \t %s' % (
                        total_time, colored(str(code), 'green'), chars, lines,
                        hasher, self.url))
                if 300 <= code < 400:
                    print('%s \t %s \t %s \t %s \t %s \t %s' % (
                        total_time, colored(str(code), 'blue'), chars, lines,
                        hasher, self.url))
                if 400 <= code < 500:
                    print(
                        '%s \t %s \t %s \t %s \t %s \t %s' % (
                            total_time, colored(str(code), 'red'), chars,
                            lines, hasher, self.url
                        )
                    )
            counter[0] = counter[0] - 1  # remove 1 thread from counter
        except Exception:
            raise Exception


def launch_threads(url, thrd, excpt, rmv, proxy, custom, words):
    global counter
    counter = list()
    counter.append(0)
    print('*' * 120)
    print('Time \t\t Code \t Chars \t Lines \t MD5 \t\t\t\t\t URLs')
    print('*' * 120)
    for i in range(0, len(words) - 1):
        try:
            if counter[0] < thrd:
                word = words[i]
                counter[0] = counter[0] + 1
                thread = PerformReq(url, excpt, rmv, proxy, custom, word)
                thread.start()
        except KeyboardInterrupt:
            print('Keyboard interrupted by user. Finish attack!')
            sys.exit()
        i += 1
        thread.join()
    return


def main():
    get_banner()

    url = args.url
    check_url(url)  # Check valid input url address
    thrd = args.thrd
    excpt = args.exception
    rmv = args.remove
    proxy = args.proxy
    if proxy:
        check_url(proxy)  # Check valid input proxy address
    custom = args.custom
    input_file = args.file
    try:
        f = open(input_file, 'r')
        words = f.readlines()
    except:
        print('Failed to open >> %s << file! Exit...' % input_file)
        sys.exit(0)
    launch_threads(url, thrd, excpt, rmv, proxy, custom, words)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Keyboard interrupted by user, stop working...!')
