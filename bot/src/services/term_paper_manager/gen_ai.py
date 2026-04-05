from dataclasses import dataclass
from typing import Optional
import json

from google import genai

from config import load_config

config = load_config()
GEMINI_KEY = config.ai.gemini_key

# TODO: Fix the code according to DRY rule

@dataclass
class AITermPaper:
    topic: Optional[str]  = None
    _json_data : Optional[dict] = None


    async def get_json_data(self):
        if self._json_data:
            return {
                "success": True,
                "data": self._json_data
            }

        client = genai.Client(api_key=GEMINI_KEY)

        contents = f"Mavzu: {self.topic}" + """
                Sen O'zbekiston oliy ta'lim muassasalari uchun akademik referat yozuvchi mutaxassissan.

        Quyidagi formatda to'liq referat yarat va faqat sof JSON qaytarr (hech qanday markdown, izoh yoki qo'shimcha matn bo'lmasin):

        {{
          "outline": {{
            "introduction": "Kirish",
            "sections": [
              "1. Birinchi bo'lim nomi",
              "2. Ikkinchi bo'lim nomi",
              "3. Uchinchi bo'lim nomi",
              "4. To'rtinchi bo'lim nomi",
              "5. Beshinchi bo'lim nomi"
            ],
            "conclusion": "Xulosa",
            "references": "Foydalanilgan adabiyotlar"
          }},
          "introduction": "Kirish matni bu yerda (150-250 so'z)",
          "sections": [
            {{
              "title": "1. Birinchi bo'lim nomi",
              "content": "Bo'lim matni bu yerda (250-400 so'z)"
            }},
            {{
              "title": "2. Ikkinchi bo'lim nomi",
              "content": "Bo'lim matni bu yerda (250-400 so'z)"
            }},
            {{
              "title": "3. Uchinchi bo'lim nomi",
              "content": "Bo'lim matni bu yerda (250-400 so'z)"
            }},
            {{
              "title": "4. To'rtinchi bo'lim nomi",
              "content": "Bo'lim matni bu yerda (250-400 so'z)"
            }},
            {{
              "title": "5. Beshinchi bo'lim nomi",
              "content": "Bo'lim matni bu yerda (250-400 so'z)"
            }}
          ],
          "conclusion": "Xulosa matni bu yerda (150-200 so'z)",
          "references": [
            "1. Familiya I.O. Kitob nomi. - Nashr joyi: Nashriyot, Yil. - 000 b.",
            "2. Familiya I.O. Kitob nomi. - Nashr joyi: Nashriyot, Yil. - 000 b.",
            "3. Familiya I.O. Kitob nomi. - Nashr joyi: Nashriyot, Yil. - 000 b.",
            "4. Familiya I.O. Kitob nomi. - Nashr joyi: Nashriyot, Yil. - 000 b.",
            "5. Familiya I.O. Kitob nomi. - Nashr joyi: Nashriyot, Yil. - 000 b.",
            "6. Familiya I.O. Kitob nomi. - Nashr joyi: Nashriyot, Yil. - 000 b.",
            "7. Familiya I.O. Kitob nomi. - Nashr joyi: Nashriyot, Yil. - 000 b.",
            "8. Familiya I.O. Kitob nomi. - Nashr joyi: Nashriyot, Yil. - 000 b.",
            "9. Familiya I.O. Kitob nomi. - Nashr joyi: Nashriyot, Yil. - 000 b.",
            "10. Familiya I.O. Kitob nomi. - Nashr joyi: Nashriyot, Yil. - 000 b.",
            "11. Familiya I.O. Kitob nomi. - Nashr joyi: Nashriyot, Yil. - 000 b.",
            "12. Familiya I.O. Kitob nomi. - Nashr joyi: Nashriyot, Yil. - 000 b."
          ]
        }}

        Talablar:
        REJA uchun:
        - 4-6 ta bo'lim bo'lsin
        - Bo'lim nomlari mavzuga mos, mantiqiy ketma-ketlikda
        - O'zbek tilida, rasmiy akademik uslubda

        KIRISH uchun:
        - 150-250 so'z
        - Mavzuning dolzarbligi va ahamiyatini yoritib ber
        - O'zbekiston iqtisodiyoti va jamiyati bilan bog'la
        - Paragraflar bilan yoz

        BO'LIMLAR uchun:
        - Har bir bo'lim 250-400 so'z
        - Ilmiy-akademik uslubda
        - Nazariy ma'lumotlar va amaliy misollar
        - Mantiqiy tuzilgan paragraflar

        XULOSA uchun:
        - 150-200 so'z
        - Asosiy fikrlarni umumlashtir
        - O'zbekiston kontekstida tavsiyalar
        - Kelajakka yo'naltirilgan xulosalar

        ADABIYOTLAR uchun:
        - 10-12 ta manba
        - O'zbek, rus va ingliz tilidagi manbalar aralash
        - 2-3 ta o'zbek tilidagi kitob yoki qonun hujjati
        - 4-5 ta rus tilidagi ilmiy kitob
        - 2-3 ta ingliz tilidagi kitob
        - 1-2 ta internet manba
        - To'liq bibliografik ma'lumot bilan

        MUHIM: Faqat sof JSON qaytarr. Hech qanday ```json yoki ``` belgisi bo'lmasin!
                """

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


