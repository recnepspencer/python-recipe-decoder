# from flask import Flask, request, jsonify
# import pytesseract
# from PIL import Image
# import io
# from flask_cors import CORS
# import openai
# import os
# from dotenv import load_dotenv

# load_dotenv()

# app = Flask(__name__)
# CORS(app)
# client = OpenAI()

# # Initialize the OpenAI client with your API key
# openai.api_key = os.getenv('OPENAI_API_KEY')

# @app.route('/convert', methods=['POST'])
# def convert_image_to_text_and_calculate_calories():
#     if 'image' not in request.files:
#         return jsonify({'error': 'No image file provided'}), 400

#     image_file = request.files['image']
#     image_bytes = image_file.read()
#     image = Image.open(io.BytesIO(image_bytes))

#     # Convert image to text
#     image_text = str(pytesseract.image_to_string(image))

#     # Prepare the prompt for OpenAI
#     prompt = f"""You are being asked to calculate how many calories are in this recipe. Please provide an answer in raw text json format. We need the macros and calories for each ingredient, as well as the total calories. Your response should include nothing besides this format: '{{"ingredient": "ingredient_name", "calories": "100", "macros": {{"protein": 10, "carbs": 20, "fat": 5}}}}'. If you cannot calculate the calories, please respond with: '{{"error": "I cannot calculate the calories for this recipe"}}'. Please do not include \\n or any other special characters or formatting in your response. Here is the recipe: {image_text}"""
#     try:
#         calories_info = get_completion(prompt, client, model='gpt-4')

#         return jsonify(calories_info)
#     except Exception as e:
#         return jsonify({"error": f"Failed to calculate calories: {str(e)}"}), 500

# def get_completion(model, client_instance, message, response_format, prompt):
#     response = client_instance.chat.completions.create(
#         model=model,
#         response_format=response_format,
#         message=message + prompt
#     )
#     return response.choices[0].message.content

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)