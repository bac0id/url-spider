from collections import deque
import requests
import time
import datetime
from urllib.parse import urlparse, urljoin, urldefrag

from html_outlinks_parser import HtmlOutlinksParser
from html_outlinks_regex_parser import HtmlOutlinksRegexParser
from outlink_converter import to_absolute_url

class UrlSpider():
    
    def __init__(self, html_outlinks_parser=HtmlOutlinksRegexParser(), proxies=None):
        self.proxies = proxies
        self.html_outlinks_parser = html_outlinks_parser

    def get_absolute_http_outlinks_from_url(self, url):
        try:
            response = requests.get(url, timeout=5, proxies=self.proxies)
            response.raise_for_status()
            response.encoding = response.apparent_encoding

            outlinks = self.html_outlinks_parser.parse(response.text)

            http_outlinks = [*filter(lambda outlink: not outlink.startswith("javascript") and not outlink.startswith("mailto"), outlinks)]
            absolute_http_outlinks = [*map(lambda http_outlink: to_absolute_url(base_url=url, outlink=http_outlink), http_outlinks)]
            distinct_absolute_http_outlinks = list(set(absolute_http_outlinks))
        except Exception as e:
            print(f"Exception: {e}")
            return []

        return distinct_absolute_http_outlinks

    def is_url_to_record(self, url):
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname
        
        # if not current domain and sub-domain
        if not hostname.endswith(self.parsed_url_start.hostname):
            return False
        return True

    def is_url_to_expand(self, url):
        parsed_url = urlparse(url)
        path = parsed_url.path
        
        # if not http nor https
        if not parsed_url.scheme.startswith("http"):
            return False
        # if not a web page (not exactly)
        if path.endswith(".pdf") or path.endswith(".doc") or path.endswith(".docx") or path.endswith(".xls") or path.endswith(".xlsx"):
            return False
        return True

    def get_urls_in_distance(self, url_start, max_distance=1):
        if max_distance < 0:
            raise ValueError("Must have max_distance >= 0.")

        self.parsed_url_start = urlparse(url_start)

        urls_closed_set = set([url_start])
        urls_open_queue = deque([url_start])
        urls_open_set = set([url_start]) # use set for efficient search
        
        urls_result = set()

        for current_distance in range(max_distance+1):
            queue_size = len(urls_open_queue)
            for _ in range(queue_size):
                current_url = urls_open_queue.popleft()
                urls_open_set.remove(current_url)
                urls_closed_set.add(current_url)
                print(f"dist: {current_distance}, url: {current_url}")

                if self.is_url_to_record(current_url):
                    urls_result.add(current_url)

                if self.is_url_to_expand(current_url):
                    absolute_http_outlinks = self.get_absolute_http_outlinks_from_url(current_url)

                    for outlink in absolute_http_outlinks:
                        if outlink in urls_closed_set: continue
                        if outlink in urls_open_set: continue
                        if not self.is_url_to_record(outlink): continue
                        urls_open_queue.append(outlink)
                        urls_open_set.add(outlink)

        return urls_result

    def get_default_filename_for_record(self, url):
        parsed_url = urlparse(url)
        now_datetime = datetime.datetime.now()
        filename = f"url-spider-{url.hostname}-{now_datetime}.txt"
        return filename

    def record_urls_to_file(self, url_start, mode=0, filename=None, max_distance=1):
        if not url_start:
            raise ValueError("Must have url_start.")
        if not filename:
            filename = self.get_default_filename_for_record(url_start)
        if max_distance < 0:
            raise ValueError("Must have max_distance >= 0.")


        urls = self.load_urls_from_txt(filename=filename, create_file_if_file_not_found=True)

        previous_urls = set(urls)

        if mode == 0:
            current_urls = self.get_urls_in_distance(url_start=url_start, max_distance=max_distance)
            self.save_as_txt(previous_urls, filename=filename)
        else:
            # current_max_distance increase by 1 after call for get_urls_in_distance()
            # until it reaches max_distance
            current_max_distance = 1
            while True:
                current_urls = self.get_urls_in_distance(url_start=url_start, max_distance=current_max_distance)

                diff_urls = current_urls.difference(previous_urls)
                print(f"count_of_diff_urls: {len(diff_urls)}")
                
                # Union differences
                previous_urls = previous_urls.union(diff_urls)
                # Save to file
                self.save_as_txt(previous_urls, filename=filename)

                if current_max_distance + 1 <= max_distance:
                    current_max_distance += 1
        
    def save_as_txt(self, urls, filename="urls.txt"):
        try:
            with open(filename, "w") as f:
                for url in urls:
                    f.write(url+"\n")
        except Exception as e:
            print(f"Exception: {e}")

    def save_as_html(urls, filename="urls.html"):
        try:
            with open(filename, "w") as f:
                f.write("<!DOCTYPE html>\n")
                f.write("<html>\n")
                f.write("<head>\n")
                f.write("</head>\n")
                f.write("<body>\n")
                f.write("<ul>\n")
                for url in urls:
                    f.write(f'<li><a href="{url}">{url}</a></li>\n')
                f.write("</ul>\n")
                f.write("</body>\n")
                f.write("</html>\n")
            print(f"Saved as html: {filename}")
        except Exception as e:
            print(f"Exception: {e}")

    def load_urls_from_txt(self, filename="urls.txt", create_file_if_file_not_found=False):
        urls_str = ""
        try:
            with open(filename, "r") as f:
                urls_str = f.read()
        except FileNotFoundError:
            if create_file_if_file_not_found:
                with open(filename, "w") as f:
                    print(f"File created: {filename}")
        except Exception as e:
            print(f"Exception: {e}")

        urls = urls_str.strip().split()
        return urls
