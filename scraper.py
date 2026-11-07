import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import instructor
import requests
from google import genai
from models import ProductData

load_dotenv()

client = instructor.from_provider("google/gemini-3.5-flash")


def scrape_product(url:str) -> ProductData:
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    response = requests.get(url,headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    clean_text = soup.get_text()


    product_data = client.chat.completions.create(
        model="gemini-3.7-flash",
        response_model=ProductData,
        messages=[
            {"role":"user",
             "content":(
                 f"extract product details from this text:\n\n{clean_text}"
             )
             }
        ]
    )
    return product_data

