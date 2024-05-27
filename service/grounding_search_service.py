import vertexai
from vertexai.generative_models import GenerationConfig, GenerativeModel, Tool
from vertexai.preview.generative_models import grounding

class GroundingSearchService:

    def __init__(self) -> None:
        # Use Google Search for grounding
        self.tool = Tool.from_google_search_retrieval(grounding.GoogleSearchRetrieval())
        # vertexai.init(project='peaceful-surge-383202', location="us-central1")

    def process(self, search_keywords):
        model = GenerativeModel(model_name="gemini-1.5-pro-001")
        
        responses = []

        i = 1
        for keyword in search_keywords:
            response = model.generate_content(
                keyword,
                tools=[self.tool],
                generation_config=GenerationConfig(
                    temperature=0.0,
                ),
            )
            response = response.candidates[0].text

            response = f"The {i} th article: {response}"

            i += 1
            responses.append(response)

            
        return ', '.join(response for response in responses)