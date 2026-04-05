from dataclasses import dataclass
from typing import Optional
import json

from google import genai

from config import load_config

config = load_config()
GEMINI_KEY = config.ai.gemini_key

# TODO: Fix the code according to DRY rule

@dataclass
class AIPresentation:
    topic: Optional[str]  = None
    author: Optional[str] = None
    lang: Optional[str] = "uz"
    slides: Optional[int] = 8
    chars_per_content: Optional[int] = 300
    _json_data : Optional[dict] = None


    async def get_json_data(self):
        if self._json_data:
            return {
                "success": True,
                "data": self._json_data
            }

        client = genai.Client(api_key=GEMINI_KEY)

        contents = """
        Generate a JSON array describing presentation slides.

Rules:
- Return ONLY valid JSON array — no extra text, no markdown, no explanations.
- Each object in the array represents one slide.
- "layoutSlideNum" starts from 2 and increases sequentially (2, 3, 4, ...)
- Every slide must have exactly these fields:
  - "layoutSlideNum": integer (starting from 2)
  - "header": short slide title/header (maximum 10 characters)
  - "contents": array of objects (minimum 3 items per slide)

Special rule for the first slide (layoutSlideNum = 2):
- "header" must be exactly: "Reja"
- "contents" must contain exactly 4 items
- Each item has only "title" (short part name in Uzbek, e.g. "Kirish")
- No "content" field allowed in these 4 items (use null or omit the field)
- the first content must be same as header

For all other slides (layoutSlideNum ≥ 3):
- Each of the minimum 3 "contents" items must have:
  - "title": very short title (maximum 10 characters)
  - "content": detailed text
- Content must be rich, explanatory, with examples where possible — never short or summary-like.

Example structure (do not copy content, just follow format):

[
  {
    "layoutSlideNum": 2,
    "header": "Reja",
    "contents": [
      {"title": "Reja"},
      {"title": "Kirish"},
      {"title": "Asosiy qism"},
      {"title": "Xulosa"}
    ]
  },
  {
    "layoutSlideNum": 3,
    "header": "Mavzu nomi",
    "contents": [
      {"title": "Band 1", "content": "Juda batafsil matn bu yerda... (800–1000 belgi)"},
      {"title": "Band 2", "content": "Yana batafsil matn... (800–1000 belgi)"},
      {"title": "Band 3", "content": "Uchinchi batafsil matn... (800–1000 belgi)"}
    ]
  }
  // more slides...
]
""" + f"""
Topic: [insert your topic here, e.g. "Sun'iy intellektning O'zbekistondagi kelajagi"]

Generate at least {self.slides} slides total (excluding the Reja slide).
Make sure every "content" field is {self.chars_per_content} characters.
Use natural, high-quality literary {self.lang}."""

        response = await client.aio.models.generate_content(
            model="gemini-3-flash-preview", contents=contents
        )
        try:
            json_data = json.loads(response.text)
            self._json_data = json_data
            return {
                "success": True,
                "data": self._json_data
            }
        except ValueError:
            return {
                "success": False,
                "data": "AI did not return proper json"
            }
