from urllib.parse import urljoin, urlparse

def to_absolute_url(base_url, outlink):
    if not base_url:
        return outlink
    if not outlink:
        return None

    try:
        # if outlink is already a absolute url, then return it
        parsed_outlink = urlparse(outlink)
        if parsed_outlink.scheme and parsed_outlink.netloc:
            return outlink

        # try urljoin
        absolute_url = urljoin(base_url, outlink)

        # if no scheme, ...
        parsed_absolute_url = urlparse(absolute_url)
        if not parsed_absolute_url.scheme:
            return None

        # normalize url
        return parsed_absolute_url.geturl()

    except ValueError: # from urlparse
        return None
    except Exception as e:
        print(f"Error joining URL: {e}")
        return None
