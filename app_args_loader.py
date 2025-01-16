import argparse

def load_app_args():
    parser = argparse.ArgumentParser(description="URL Spider")
    parser.add_argument("url_start", help="Start URL")
    parser.add_argument("-d", "--max-distance", type=int, default=1, help="Max distance. (default=1)")
    parser.add_argument("-f", "--filename", help="File to save URLs.")
    parser.add_argument("-m", "--mode", type=int, default=0, help="Mode of crawling. Single crawling=0, continuous crawling=1. (default=0)")
    parser.add_argument("-p", "--proxy", default=None, help="Http(s) proxy.")

    try:
        args = parser.parse_args()
    except SystemExit as e:
        if e.code != 0:
            parser.print_help()
            return None
        else:
            return None

    url_start = args.url_start
    filename = args.filename.strip()
    max_distance = args.max_distance
    crawling_mode = args.mode
    proxy = args.proxy
    if proxy is not None:
        proxy = proxy.strip()
        proxies = {
            "http": proxy,
            "https": proxy,
        }
    else:
        proxies = None
    
    if max_distance <= 0:
        print("Error: must have max_distance >= 0")
        return None

    return url_start, max_distance, crawling_mode, filename, proxies
