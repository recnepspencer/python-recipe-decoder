from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import io
from openai import OpenAI
import os
from dotenv import load_dotenv
from flask_cors import CORS
import openai
import json

load_dotenv()

app = Flask(__name__)
CORS(app)
client = OpenAI()

@app.route('/convert', methods=['POST'])
def convert_image_to_text_and_calculate_calories():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    image_file = request.files['image']
    image_bytes = image_file.read()
    image = Image.open(io.BytesIO(image_bytes))
    
    # Convert image to text
    image_text = pytesseract.image_to_string(image)
    
    # Prepare the prompt for OpenAI
    prompt = f"Please calculate how many calories are in this recipe: {image_text}"
    
    try:
        # Query OpenAI API using the corrected method
        response = client.chat.completions.create(
  model="gpt-4",
  response_format={ "type": "text" },
  messages=[
    {"role": "system", "content": "Please calculate how many calories are in this recipe. Provide an answer in raw text json format. We need the macros and calories for each ingredient. If there are 2 ingredient choices, only pick one and use it. If portions aren't given, make it up. Your response should include nothing besides this format: [{'ingredient': 'ingredient_name', 'quantity': '1 cup' 'calories': '100', 'protein': '10', 'carbs': '20', 'fat': '5'}...]. If you cannot calculate the calories, please respond with: 'error': 'I cannot calculate the calories for this recipe'. Please do not include \ n or any other special characters or formatting in your response. Ensure double quotes for proper JSON format. Thank you!"},
    {"role": "user", "content": image_text}
  ]
)
        
        content = response
        print(content.choices[0].message.content)
        content_dict = json.loads(content.choices[0].message.content)

        # Now you can jsonify the dictionary
        return jsonify(content_dict)
    except Exception as e:
        return jsonify({"error": f"Failed to calculate calories: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)