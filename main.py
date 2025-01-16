from app_args_loader import *

from url_spider import UrlSpider

def main():
    url_start, max_distance, crawling_mode, filename, proxies = load_app_args()

    url_spider = UrlSpider(proxies=proxies)

    url_spider.record_urls_to_file(url_start, filename=filename, max_distance=max_distance, mode=crawling_mode)

if __name__ == "__main__":
    main()
