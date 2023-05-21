import requests
from customqueue import CustomQueue
from urllib.parse import urlparse
from display import Display
import re

class Finder:
    def __init__(self, base_url):
        self.base_url = base_url
        self.domain = Finder.get_domain(self.base_url)
        self.urls = CustomQueue()

    def ping(url):
        try:
            r = requests.get(url)
            return (r.status_code, r.text)
        
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            return (404, "")

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

            status_code, text = Finder.ping(url)

            Display.display_url(status_code, url)

            found_urls = self.get_links(text)

            for u in found_urls:
                if self.check_domain(u) and not self.check_presence(u):
                    q.put(u)
                    self.urls.put(u)


# TODO : Enable subdomain
f = Finder("https://root-me.org/")
f.traverse()