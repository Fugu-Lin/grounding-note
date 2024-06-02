from vertexai.generative_models import GenerationConfig, GenerativeModel, Tool
from bs4 import BeautifulSoup
import requests
import os

class GroundingSearchService:

    def __init__(self) -> None:
        self.api_key = os.getenv('API_KEY')
        self.cse_id  = os.getenv('CSE_ID')
        
    def fetch_article_content(self, url):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
                
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.get_text()
            return content
        except Exception as e:
            return f"Error fetching content from {url}: {e}"
        
    def google_search(self, query):
        url = 'https://www.googleapis.com/customsearch/v1'
        params = {'q': query, 'key': self.api_key, 'cx': self.cse_id, 'num': 3}
        response = requests.get(url, params=params)
        result = response.json()
        
        web_contents = ''
        
        # Parse and extract information
        cnt = 0
        if 'items' in result:
            for item in result['items']:
                title   = item.get('title')
                link    = item.get('link')
                snippet = item.get('snippet')
                cnt += 1
                # print(f"Title: {title}")
                # print(f"Link: {link}")
                # print(f"Snippet: {snippet}")
                # print()
                
                web_content = self.fetch_article_content(link).strip()
                
                web_contents += web_content
        else:
            print("No results found.")
        
        return web_contents

    def process(self, search_keywords):
        model = GenerativeModel(model_name="gemini-1.5-pro-001")
        responses = []
        i = 1
        
        for keyword in search_keywords:
            response = self.google_search(keyword)
            response = f"The {i} th search result: {response}"
            i += 1
            responses.append(response)
        return ', '.join(response for response in responses)

if __name__ == '__main__':
    search_keyword = ['AI video marketing tutorial Medium']
    groundingSearchService = GroundingSearchService()
    groundingSearchService.process(search_keyword)