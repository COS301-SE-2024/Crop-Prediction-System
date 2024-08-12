from dotenv import load_dotenv
import os

load_dotenv()

import google.generativeai as genai

class Gemini:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            system_instruction="Convert this to a short, concise, informative farmer-specific weather summary that is specific to one field in 50 words",
        )

    def start_chat(self):
        return self.model.start_chat(history=[
            {
                "role": "user",
                "parts": [
                    "The current weather is clear with a temperature of 15°C and a slight breeze with a wind speed of 3 meters per second. The humidity is at 71% and the pressure is at 1024 hPa. The visibility is at 10,000 meters and the UV index is 5. It feels like 14°C, and the dew point is at 10°C. There are no clouds in the sky, providing clear visibility. Overall, it's a pleasant day with comfortable temperatures and clear skies, making it a great time to enjoy outdoor activities.",
                ],
            },
            {
                "role": "model",
                "parts": [
                    "Field conditions are favorable today with clear skies, a pleasant 15°C temperature, and a gentle breeze. Humidity is at 71%, so keep an eye on potential for dew development. Enjoy the good weather and clear visibility for fieldwork. \n",
                ],
            },
        ])

    def send_message(self, message):
        chat_session = self.start_chat()
        result = chat_session.send_message(message)
        return result.candidates[0].content.parts[0].text