from vertexai.generative_models import GenerativeModel
import vertexai
import re
import os

class QueryRewriteService:

    def process(self, prompt):
        # start with gemini model
        model = GenerativeModel('gemini-1.5-pro-001')
        
        prompt = self.make_prompt_user(prompt)
        
        response = model.generate_content(
            self.make_prompt_user(prompt),
            generation_config={
                'temperature': 0.5,
                'top_k': 10,
            }
        )
        
        text = response.candidates[0].text
        
        keywords = self.parser_rewrite_keywords(text)

        return keywords
    
    # prompt for the User imput
    def make_prompt_user(self, query):
        prompt = ("""
You excel at extracting main points from a paragraph and further generating keywords for Google searches. Your task is to discern the user's intent from the provided paragraph and formulate at least five distinct sets of keywords in both the input language and English.

Optimize these keywords according to the rules of each language system.
If the user's intent is unclear, ask for more information.
If the user requests information unrelated to AI tool recommendations, respond with: "Sorry, I can only search for information about AI tools."
For tutorial-related requests, append relevant platforms such as Medium, Reddit, YouTube, Wiki, or other reputable journalism sites to the end of the search query.
Ensure the search queries are relevant to the user's paragraph and include tool tutorials.
Finally, return the finalized keywords in the following format:

EXAMPLE:
QUESTION: I need an AI tool to help me plan my trip. I need detailed tutorials. Any recommended tools? Preferably free tools.
ANSWER: [AI trip planner free tutorial YouTube, best free AI trip planning tools Reddit, how to use AI for trip planning Medium, free AI itinerary generator tutorial Wiki, AI travel assistant free tutorial]

REAL QUESTION: '{query}'
ANSWER:
                    """).format(query=query)

        return prompt
    
    def parser_rewrite_keywords(self, text):
        text = text.replace("[", "").replace("]", "")
        # Split the string by comma and strip any leading/trailing whitespace from each keyword
        keywords = [keyword.strip() for keyword in text.split(",")]
        return keywords
