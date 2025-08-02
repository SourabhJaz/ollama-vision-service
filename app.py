import base64
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import requests

load_dotenv()
OLLAMA_API_BASE = os.getenv("OLLAMA_API_BASE")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
FLASK_PORT = int(os.getenv("FLASK_PORT"))
app = Flask(__name__)

def build_ollama_payload(base64_image, custom_context=None):
  return {
    "model": OLLAMA_MODEL,
    "messages": [
        {
            "role": "user",
            "content": custom_context or "Describe this image:",
            "images": [
                base64_image
            ]
        }
    ],
    "stream": False
  }

def call_ollama_api(payload):
  try:
    response = requests.post(
        f"{OLLAMA_API_BASE}/api/chat",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    response.raise_for_status()
    return response.json()["message"]["content"]
  except requests.RequestException as e:
    print(f"Error calling OLLAMA API: {e}")
    return None


@app.route('/describe', methods=['POST'])
def describe_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    image_file = request.files['image']
    image_data = image_file.read()
    base64_image = base64.b64encode(image_data).decode('utf-8')

    payload = build_ollama_payload(base64_image)
    description = call_ollama_api(payload)

    return jsonify({'description': description})

@app.route('/ocr', methods=['POST'])
def ocr_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    image_file = request.files['image']
    image_data = image_file.read()
    base64_image = base64.b64encode(image_data).decode('utf-8')
    custom_context = "Extract all text visible in this image. Do not describe what you see or add any commentary. Return just the text as it appears, line by line. If there are multiple text elements, list them in the order they appear. Do not repeat any text."
    payload = build_ollama_payload(base64_image, custom_context)
    description = call_ollama_api(payload)

    return jsonify({'description': description})  

if __name__ == '__main__':
    app.run(debug=True, port=FLASK_PORT)