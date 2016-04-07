import requests


class ParseError(Exception):
    pass


class Wikipedia(object):
    """Wikipedia API interface"""

    api_endpoint = "http://en.wikipedia.org/w/api.php?"

    @classmethod
    def article(cls, title):
        """Return contents of article
    
        arguments:
    
        title -- title of article
        """
        data = {'action': 'parse', 'format': 'json', 'prop':'text', 'page': title}
        response = requests.get(cls.api_endpoint, params=data)
        json_response = response.json()

        if 'parse' in json_response:
            contents = json_response['parse']['text']['*']
        else:
            raise ParseError(json_response['error']['info'])

        return contents
