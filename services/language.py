from langdetect import detect, LangDetectException


class LanguageService:

    def detect_language(self, text: str) -> str:

        try:
            language = detect(text)

            language_map = {
                "en": "English",
                "hi": "Hindi",
                "bn": "Bengali",
                "ta": "Tamil",
                "te": "Telugu",
                "mr": "Marathi",
                "gu": "Gujarati",
                "kn": "Kannada",
                "ml": "Malayalam",
                "pa": "Punjabi",
                "ur": "Urdu",
                "es": "Spanish",
                "de": "German",
                "fr": "French",
                "it": "Italian",
                "pt": "Portuguese",
                "ja": "Japanese",
                "ko": "Korean",
                "zh-cn": "Chinese",
                "zh-tw": "Chinese"
            }

            return language_map.get(language, "English")

        except LangDetectException:
            return "English"


language_service = LanguageService()