from vertexai.generative_models import GenerativeModel
import vertexai
import re
import os

class QueryRewriteService:

    def process(self, prompt):
        # start with gemini model
        model = GenerativeModel.GenerativeModel('gemini-1.5-pro-001')

        response = model.generate_content(
            self.make_prompt_user(prompt),
            generation_config={
                'temperature': 0.5,
                'top_k': 10,
            }
        )

        keywords = self.parser_rewrite_keywords(response)

        return keywords
    
    # prompt for the User imput
    def make_prompt_user(self, query):
        prompt = ("""
                    You are excel at extracting main points from a paragraph and further generating keywords for googling. 
                    Your job is to discern the users' intent from the paragraph and formulate keywords in both input language and English, 
                    producing at least 5 distinct results seperatly.
                    These keywords are for getting most relevant results from Google search.
                    Optimizing these keywords according to the rules of each different language systems.
                    If users' intent is not clear, you should ask for more information.
                    If the user requests information unrelated to AI tool recommendations, return 
                    "Sorry, I can only search for information about AI tools".
                    For information related to tutorials, append Medium, Reddit, Youtube, Wiki or other reputable journalism sites to the 
                    end of the search query. Ensure that the search results of queries are relevant to the paragraph and 
                    include tool tutorials. Finally, return the finalized keywords in following type.
                    QUESTION: '{query}'
                    ANSWER: keyword1\nkeyword2\nkeyword3
                    """).format(query=query)
        return prompt
    
    def parser_rewrite_keywords(self, response):
        keywords = re.findall(r'keyword\d+: \*\*(.*?)\*\*', response)
        return keywords
