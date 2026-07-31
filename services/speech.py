import os
from typing import Dict
import librosa
import numpy as np
import re

import whisper


LANGUAGE_MAP = {
    "en": "English",
    "hi": "Hindi",
    "de": "German",
    "es": "Spanish",
    "fr": "French",
    "bn": "Bengali",
    "ta": "Tamil",
    "te": "Telugu",
    "mr": "Marathi",
    "gu": "Gujarati",
    "kn": "Kannada",
    "ml": "Malayalam",
    "pa": "Punjabi",
    "ur": "Urdu",
    "ja": "Japanese",
    "ko": "Korean",
    "zh": "Chinese",
    "ru": "Russian",
    "it": "Italian",
    "pt": "Portuguese",
    "ar": "Arabic",
    "tr": "Turkish",
    "nl": "Dutch"
}


class SpeechService:

    def __init__(self):

        print("Loading Whisper Model...")

        # Available models:
        # tiny
        # base
        # small
        # medium
        # large

        self.model = whisper.load_model("small")

        print("Whisper Loaded Successfully!")

    def speech_to_text(self, audio_path: str) -> Dict:
        """
        Converts speech into text and detects the language.
        """

        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        try:

            result = self.model.transcribe(
                audio_path,
                fp16=False
            )

            language_code = result["language"]

            return {
                "processing_status": "success",
                "text": result["text"].strip(),
                "language_code": language_code,
                "language": LANGUAGE_MAP.get(
                    language_code,
                    language_code
                )
            }

        except Exception as e:

            return {
                "processing_status": "failed",
                "error": str(e)
            }

    def transcribe_with_language(
        self,
        audio_path: str,
        expected_language: str = None
    ) -> Dict:
        """
        Converts speech into text and optionally compares
        the detected language with an expected language.
        """

        response = self.speech_to_text(audio_path)

        if response["processing_status"] == "failed":
            return response

        if expected_language is None:

            response["language_match"] = None

        else:

            response["language_match"] = (
                response["language"].lower()
                == expected_language.lower()
            )

        return response
    def get_audio_duration(
        self,
        audio_path: str,
    ):

        audio, sr = librosa.load(
            audio_path,
            sr=None,
        )

        duration = librosa.get_duration(
            y=audio,
            sr=sr,
        )

        return duration
    def calculate_wpm(
    self,
    transcript: str,
    duration: float,
):

        if duration == 0:

            return 0

        words = len(transcript.split())

        minutes = duration / 60

        return round(words / minutes)

    def count_fillers(
        self,
        transcript: str,
    ):

        fillers = [

            "um",

            "uh",

            "like",

            "actually",

            "basically",

            "you know",

            "i mean",
        ]

        text = transcript.lower()

        count = 0

        for filler in fillers:

            count += len(
                re.findall(
                    r"\b" + re.escape(filler) + r"\b",
                    text,
                )
            )

        return count
    
    def calculate_voice_energy(
    self,
    audio_path: str,
):

        audio, sr = librosa.load(
            audio_path,
            sr=None,
        )

        rms = librosa.feature.rms(
            y=audio,
        )[0]

        return float(np.mean(rms))
    
    def count_long_pauses(
    self,
    audio_path: str,
    threshold_db: float = 20,
    minimum_pause: float = 1.0,
):

        audio, sr = librosa.load(
            audio_path,
            sr=None,
        )

        intervals = librosa.effects.split(
            audio,
            top_db=threshold_db,
        )

        pauses = 0

        previous_end = 0

        for start, end in intervals:

            silence = (start - previous_end) / sr

            if silence >= minimum_pause:

                pauses += 1

            previous_end = end

        return pauses
    
    def analyze(
    self,
    audio_path: str,
):

        transcript = self.speech_to_text(
            audio_path
        )

        if transcript["processing_status"] == "failed":

            return transcript

        duration = self.get_audio_duration(
            audio_path
        )

        wpm = self.calculate_wpm(
            transcript["text"],
            duration,
        )

        fillers = self.count_fillers(
            transcript["text"],
        )

        energy = self.calculate_voice_energy(
            audio_path,
        )

        pauses = self.count_long_pauses(
            audio_path,
        )

        return {

            "processing_status": "success",

            "transcript": transcript["text"],

            "language": transcript["language"],

            "duration": round(duration, 2),

            "words_per_minute": wpm,

            "filler_words": fillers,

            "voice_energy": round(energy, 3),

            "long_pauses": pauses,
        }
speech_service = SpeechService()