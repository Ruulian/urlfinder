#!/usr/bin/python3

import argparse
import requests
from customqueue import CustomQueue
from urllib.parse import urlparse
import re
import time
import urllib3
from sys import stdout

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Finder:
    def __init__(self, base_url, cookies={}, headers={}, sleep=0.0, output_file="", no_colors=False):
        self.base_url = base_url

        self.cookies = cookies
        self.headers = headers
        self.sleep = sleep
        self.output_file = output_file
        self.no_colors = no_colors

        self.domain = Finder.get_domain(self.base_url)
        self.urls = CustomQueue()

    # Display

    def banner():
        print(f"""
          _    _      _ ______ _           _           
         | |  | |    | |  ____(_)         | |          
         | |  | |_ __| | |__   _ _ __   __| | ___ _ __ 
         | |  | | '__| |  __| | | '_ \ / _` |/ _ \ '__|
         | |__| | |  | | |    | | | | | (_| |  __/ |   
          \____/|_|  |_|_|    |_|_| |_|\__,_|\___|_|   \x1b[0m\x1b[3m by Ruulian\x1b[0m

        \x1b[4mVersion\x1b[0m: 1.0
        """)
        
    
    def print(file, message="", no_colors=False):
        if no_colors:
            message = re.sub("\x1b[\[]([0-9;]+)m", "", message)
        
        file.write(f"{message}\n")

    def display_url(file, status_code, url, no_colors=False):
        if status_code > 0 and (status_code < 200 or (300 <= status_code and status_code < 400)):
            color = 33
        elif 200 <= status_code and status_code < 300:
            color = 32
        else:
            color = 31

        if status_code == -1:
            status_code = "ERROR"
            
        Finder.print(file, f"[\x1b[{color}m{status_code}\x1b[0m] {url}", no_colors)

    # Finder behavior

    def ping(self, url):
        try:
            r = requests.get(url, cookies=self.cookies, headers=self.headers, allow_redirects=True, verify=False)
            return (r.status_code, r.text)
        
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            return (-1, "")

    def check_presence(self, url) -> bool:
        return url in self.urls

    def check_domain(self, url) -> bool:
        return Finder.get_domain(url) == self.domain

    def get_domain(url):
        return urlparse(url).netloc

    def get_links(self, text) -> CustomQueue:
        res = CustomQueue()
        links = re.findall(r"(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])", text)
        res.add_list([f"{l[0]}://{l[1]}{l[2]}" for l in links])
        return res

    def traverse(self) -> None:
        q = CustomQueue(self.base_url)

        while not q.empty():
            url = q.get()

            status_code, text = self.ping(url)

            Finder.display_url(stdout, status_code, url)

            if self.output_file != "":
                with open(self.output_file, "a") as f:
                    Finder.display_url(f, status_code, url, no_colors=True)

            found_urls = self.get_links(text)

            for u in found_urls:
                if self.check_domain(u) and not self.check_presence(u):
                    q.put(u)
                    self.urls.put(u)
            time.sleep(self.sleep)

def parse_dict_arg(arg:str):
    cookies = {}
    cookies_arg = arg.split(";")
    for c in cookies_arg:
        cookie = c.split("=")
        try:
            cookies[cookie[0]] = cookie[1]
        except IndexError:
            raise argparse.ArgumentTypeError("Cookies must be specified with key=value")
    return cookies

def parse_args():
    parser = argparse.ArgumentParser(add_help=True, description='URLFinder tool')

    required_args = parser.add_argument_group("Required argument")
    required_args.add_argument("-t", "--target", dest="target", help="Specify the target url", required=True)

    setup_args = parser.add_argument_group("Setup")
    setup_args.add_argument("-c", "--cookies", dest="cookies", help="Specify the cookies key1=value1;key2=value2", type=parse_dict_arg, required=False, default={})
    setup_args.add_argument("-H", "--headers", dest="headers", help="Specify the headers key1=value1;key2=value2", type=parse_dict_arg, required=False, default={})
    
    setup_args.add_argument("-o", "--output", dest="output_file", help="Specify output file", type=str, required=False, default="")
    setup_args.add_argument("-s", "--sleep", dest="sleep", help="Specify the sleep between the requests", type=float, required=False, default=0.0)

    setup_args.add_argument("--no-colors", dest="no_colors", action="store_true", help="Disable color mode")
    
    
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    Finder.banner()
    args = parse_args()
    finder = Finder(args.target, args.cookies, args.headers, args.sleep, args.output_file, args.no_colors)
    Finder.print(stdout, "="*74)
    Finder.print(stdout, "[STATUS_CODE] url")
    finder.traverse()
    Finder.print(stdout, "="*74)