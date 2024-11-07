from app.services.gemini_service import GeminiService

class LabelProcessor:


    def __init__(self):
        self.gemini_service = GeminiService()


    def process_label(self, label_text: str):

        result = self.gemini_service.analyze_label(label_text)

        return result