import json
import requests
import base64
import io
import os
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import pandas as pd
import boto3
from threading import Thread
import base64

# Load environment variables from the .env file
load_dotenv()
TEXT_MODEL = os.getenv("TEXT_MODEL_ICMS")
SERVICE_NAME = os.getenv("AWS_SERVICE_NAME_ICMS")
REGION_NAME = os.getenv("AWS_REGION_NAME_ICMS")
ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ICMS")
ACCESS_SECRET_KEY = os.getenv("AWS_SECRET_KEY_ICMS")
MAPS_API_KEY = os.getenv("MAPS_API_KEY")

client = boto3.client(service_name=SERVICE_NAME,
                       region_name = REGION_NAME,
                       aws_access_key_id=ACCESS_KEY_ID,
                       aws_secret_access_key=ACCESS_SECRET_KEY)



def generate_creatives(payload):
    try:
        project_details = payload

        site_root = os.path.realpath(os.path.dirname(__file__))
        html_url = os.path.join(site_root, "templates", "template.html")

        if not os.path.isfile(html_url):
            raise FileNotFoundError(f"HTML file not found at {html_url}")

        with open(html_url, "r", encoding="utf-8") as html_file:
            html_content = html_file.read()

        combined_html = f"{html_content}"
        replacements = {
            "event": project_details.get("event", ""),
            "creative_image": project_details.get("creative_image", ""),
            "content": project_details.get("creative_content", ""),
            "website": project_details.get("website", ""),
            "phone": project_details.get("contact_number", ""),
            "project_logo": project_details.get("project_logo", "")
        }

        for placeholder, value in replacements.items():
            if value is None:
                value = ""
            combined_html = combined_html.replace("{{" + placeholder + "}}", value)

        output_html_path = os.path.join(site_root, "output", "creatives.html")
        os.makedirs(os.path.dirname(output_html_path), exist_ok=True)

        with open(output_html_path, 'w', encoding='utf-8') as html_output_file:
            html_output_file.write(combined_html)

        html_base64 = base64.b64encode(combined_html.encode("utf-8")).decode("utf-8")

        return {
            "success": "HTML generated successfully",
            "creatives_html": html_base64,
            "status": "Success",
            "file_path": output_html_path
        }
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e), "status": "Error"}