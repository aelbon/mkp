import csv
import io
import requests
from django.conf import settings
from .models import Document, DocumentSection

class LLMService:
    """Service to handle communication with the LLM API"""
    
    @staticmethod
    def analyze_document(document):
        """
        Send document to LLM API and process the response
        
        Args:
            document: Document model instance
        
        Returns:
            List of DocumentSection objects
        """
        # Read document file
        # document_content = document.file.read().decode('utf-8')
        document_content = None
        
        # Call LLM API
        response = LLMService._call_llm_api(document_content)
        
        # Process CSV response
        sections = LLMService._process_csv_response(response, document)
        
        return sections
    
    @staticmethod
    def _call_llm_api(document_content):
        """
        Send document content to LLM API
        
        In production, replace this with your actual API call
        """
        # from utils import bot_completion

        # # model = "gpt-4o"
        # model = "gpt-3.5-turbo-0125"

        # # Prompt the user for input
        # # prompt = input("Please enter a prompt: ")

        # prompt = """Hallo hoe gaat het?"""
        
        # # Call the bot_completion function
        # respond, cost = bot_completion(prompt, model)
        
        # # API configuration
        # api_key = settings.LLM_API_KEY
        # api_endpoint = settings.LLM_API_ENDPOINT
        
        # # For demo: return mock CSV
        # # In production: uncomment this code and configure the API call
        # """
        # headers = {
        #     'Authorization': f'Bearer {api_key}',
        #     'Content-Type': 'application/json'
        # }
        
        # payload = {
        #     'document': document_content,
        #     'options': {
        #         'output_format': 'csv'
        #     }
        # }
        
        # response = requests.post(api_endpoint, headers=headers, json=payload)
        # response.raise_for_status()
        
        # return response.text
        # """
        
        # Mock response for development
        mock_csv = """section,content,x,y,width,height
Header,Document Title,0.1,0.1,0.8,0.5
"""
# Summary,Executive summary text,0.1,0.15,0.8,0.15
# MainContent,Main document content here,0.1,0.3,0.8,0.4
# Sidebar,Additional information,0.7,0.3,0.2,0.4
# Footer,Page 1 of 10,0.1,0.9,0.8,0.05"""

        
        return mock_csv
    
    @staticmethod
    def _process_csv_response(csv_content, document):
        """
        Process CSV response from LLM API and create DocumentSection objects
        """
        csv_file = io.StringIO(csv_content)
        reader = csv.DictReader(csv_file)
        
        sections = []
        for row in reader:
            section = DocumentSection(
                document=document,
                section_name=row['section'],
                content=row['content'],
                x_position=float(row['x']),
                y_position=float(row['y']),
                width=float(row['width']),
                height=float(row['height'])
            )
            sections.append(section)
        
        return sections