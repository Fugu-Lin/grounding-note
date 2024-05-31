from vertexai.generative_models import GenerationConfig, GenerativeModel, Tool
from vertexai.preview.generative_models import grounding
from bs4 import BeautifulSoup
import requests
import os

class GroundingSearchService:

    def __init__(self) -> None:
        self.api_key = os.getenv('API_KEY')
        self.cse_id  = os.getenv('CSE_ID')
        
    def fetch_article_content(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.get_text()
            return content
        except Exception as e:
            return f"Error fetching content from {url}: {e}"
        
    def google_search(self, query):
        url = 'https://www.googleapis.com/customsearch/v1'
        params = {'q': query, 'key': self.api_key, 'cx': self.cse_id}
        response = requests.get(url, params=params)
        result = response.json()
        return result

    def process(self, search_keywords):        
        responses = []
        i = 1
        for keyword in search_keywords:
            response = self.google_search(keyword)
            response = f"The {i} th article: {response}"
            i += 1
            responses.append(response)
        return ', '.join(response for response in responses)