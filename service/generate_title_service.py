from vertexai.generative_models import GenerativeModel
import vertexai
import re

class GenerateTitleService:
    def process(self, markdown_content):
        model  = GenerativeModel(model_name="gemini-1.5-pro-001")

        response = model.generate_content(
            self.make_prompt(markdown_content),
            generation_config={
                'temperature': 0.5,
                'top_k': 10,
                'max_output_tokens': 1280
            }
        )
        title = response.candidates[0].text
        title = self.clean_title(title)
        return title
    
    def make_prompt(self, markdown_content):
        prompt = ("""
You are skilled at summarizing information from markdown format.

Objective: Create a concise and accurate title for the markdown document. If the title contains spaces, replace them with underscores. Only include English alphabets and underscores in the title.

Input:
{markdown_content}

Output:
            """).format(markdown_content=markdown_content)
        return prompt

    def clean_title(self, title):
        pattern = re.compile(r"[^a-zA-Z_]+")
        return pattern.sub("_", title)