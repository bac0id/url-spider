import abc

class HtmlOutlinksParser(abc.ABC):
    
    def parse(self, html_string):
        """
        Parse html string and return all `href` attr values in `<a>` tags.
        """
        pass
