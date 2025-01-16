from bs4 import BeautifulSoup

from html_outlinks_parser import HtmlOutlinksParser

class HtmlOutlinksBeautifulSoupParser(HtmlOutlinksParser):

    def parse(self, html_string: str) -> list[str]:
        if not html_string:
            return []

        soup = BeautifulSoup(html_string, "html.parser")
        # Get all "<a>" tags in html
        a_tags = soup.find_all("a") 
        # Get attr value of "href" in "<a href=...>"
        outlinks = [self.get_href_attr_value_from_a_tag(a_tag) for a_tag in a_tags]
        # Remove None and empty strings
        outlinks = [*filter(lambda x: x and x.strip(), outlinks)]

        return outlinks

    def get_href_attr_value_from_a_tag(self, a_tag):
        href = a_tag.get("href")
        if href:
            return href.strip()
        else:
            return None
        