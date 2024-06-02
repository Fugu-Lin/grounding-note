from vertexai.generative_models import GenerationConfig, GenerativeModel, Tool
from vertexai.preview.generative_models import grounding

class SummaryService:
    def process(self, disorganized_content):
        model  = GenerativeModel(model_name="gemini-1.5-pro-001")

        response = model.generate_content(
            self.make_prompt(disorganized_content),
            generation_config={
                'temperature': 0.5,
                'top_k': 10,
                'max_output_tokens': 1280
            }
        )

        return response.candidates[0].text
    
    def make_prompt(self, disorganized_content):
        prompt = ("""
You are skilled at summarizing information from websites and presenting the results in markdown format.

Objective: Create a markdown document that outlines the main features of the answer for users. The document should be easy to read and navigate, with clear headings and subheadings, bullet points for key points, and numbered lists for any step-by-step instructions.

Structure:

Title: Use an H1 tag (#) for the title.
Sections: Use H3 tags (###) for sections and H4 tags (####) for sub-sections.
Sections should be clearly labeled and easy to navigate.
Sections:

Introduction

Provide a brief overview of the user queries and information from the results.
Recommend List

Each feature should be a bullet point.
Sub-features should be indented as sub-bullets.
Installation Guide

List the steps for installation in a numbered list.
Include any required code snippets using code blocks.
Usage

Explain how to use the software product.
Provide steps in a numbered list.
Include code snippets where necessary.
FAQ

Each question should be a bullet point with an H5 tag (#####).
Write the answer directly below the question without any special formatting.

Input:
Website_content: '{disorganized_content}'
Output:
            """).format(disorganized_content=disorganized_content)
        return prompt
