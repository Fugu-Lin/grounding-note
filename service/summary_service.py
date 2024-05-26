from vertexai.generative_models import GenerationConfig, GenerativeModel, Tool
from vertexai.preview.generative_models import grounding
import vertexai

class SummaryService:
    def process(self, disorganized_content):
        model  = GenerativeModel(model_name="gemini-1.5-pro-001")

        prompt = self.make_prompt(disorganized_content)

        response = model.generate_content(
            prompt,
            generation_config={
                'temperature': 0.5,
                'top_k': 10,
                'max_output_tokens': 1280
            }
        )

        return response
    
    def make_prompt(self, disorganized_content):
        prompt = ("""
            You are good at summarizing information of the website and return the results in markdown format.
            A markdown document should outline the main features of the answer for users. 
            The document should be structured as follows:
            Title: Use an H1 tag (#) for the title.
            Use H3 tags (###) for the sections and H4 tags (####) for sub-sections.
            Sections should be clearly labeled and easy to navigate.
            Section 1. Introduction
            Provide a brief overview of the user queries and information of the results.
            Section 2. Recommend List
            Each feature should be a bullet point, and any sub-features should be sub-bullets.
            Section 3. Installation Guide
            The steps for installation should be listed in a numbered list. 
            If there are any code snippets required for installation, please include them using code blocks.
            Section 4. Usage
            This section should explain how to use the software product. 
            Any steps should be in a numbered list, and include code snippets where necessary.
            Section 5. FAQ
            Each question should be a bullet point with an H5 tag (#####) for the question, and the answer should be written directly below the question without any special formatting.

            Please ensure that the document is easy to read and navigate, with clear headings and subheadings, bullet points for key points, and numbered lists for any step-by-step instructions."
            Website_conten: '{disorganized_content}'
            ANSWER:
            """).format(disorganized_content=disorganized_content)

