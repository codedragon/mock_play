import unittest
import requests
import json
from unittest.mock import patch

from api import Wikipedia, ParseError
from definitions import Definitions

missing_title = "!!!!!-NonExistentArticle"
good_title = "Robots"

def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if kwargs['params']['page'] == missing_title:
        return MockResponse({'error': {'info': "The page you specified doesn't exist"}}, 200)
    else:
        return MockResponse({'parse': {'text': {'*': "Lovely Text"}}}, 200)

        
class WikiDefTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # def test_article_success(self):
    #     article = Definitions.article("Robot")        
    #     self.assertIn("mechanical", article)

    # def test_missing_article_failure(self):
    #     missing_article_title = "!!!!!-NonExistentArticle"
    #     self.assertRaises(ParseError, Definitions.article, missing_article_title)

    @patch.object(requests, 'get', side_effect=mocked_requests_get)
    def test_missing_article_failure(self, mock_get):
        self.assertRaises(ParseError, Definitions.article, missing_title)

    # patch with a decorator
    @patch('definitions.Wikipedia.article')
    def test_article_success_decorator_mocked(self, mock_method):
        article = Definitions.article("Robot")        
        mock_method.assert_called_once_with("Robot")

    @patch.object(Wikipedia, 'article')
    def test_article_success_decorator_mocked(self, mock_method):
        article = Definitions.article("Robot")        
        mock_method.assert_called_once_with("Robot")

    # patch with a context manager
    def test_article_success_context_manager_mocked(self):
        with patch.object(Wikipedia, 'article') as mock_method:
            article = Definitions.article("Robot")        
            mock_method.assert_called_once_with("Robot")
