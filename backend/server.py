import sys
import os  # <-- ADDED THIS
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- 1. Initialize Flask App ---
app = Flask(__name__)
CORS(app)

print("--- Gemini API Server is starting ---")

# --- 2. Create an API Endpoint ---
@app.route('/optimize', methods=['POST'])
def optimize_code():
    print("\n--- Received a request ---")
    
    if not request.json or 'code' not in request.json:
        print("Request error: No 'code' key in JSON.")
        return jsonify({'error': 'No code provided'}), 400

    # This 'user_prompt' contains your full "Expert" prompt from VS Code
    user_prompt = request.json['code']
    print(f"Received prompt length: {len(user_prompt)} chars") 

    try:
        # --- 3. Call the Gemini API ---
        
        # --- THIS IS THE FIX ---
        # It now reads the secret key you just saved
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise Exception("GOOGLE_API_KEY secret is not set.")
        # --- END FIX ---
            
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={api_key}"

        # Construct the payload for Gemini
        payload = {
            "contents": [{
                "parts": [{ "text": user_prompt }]
            }]
        }

        print("Sending request to Gemini API...")
        
        # Make the API call
        response = requests.post(api_url, json=payload, headers={'Content-Type': 'application/json'})
        response.raise_for_status() # Raise an error if the request failed
        
        result = response.json()

        # Extract the optimized code from Gemini's response
        optimized_code = result['candidates'][0]['content']['parts'][0]['text']
        
        print("Optimization generated successfully.")
        
        return jsonify({'optimization': optimized_code})

    except Exception as e:
        print(f"--- ERROR during Gemini API call: {e} ---")
        return jsonify({'error': f'Prediction failed: {e}'}), 500

# --- 4. Run the Server ---
if __name__ == '__main__':
    # Listen on 0.0.0.0 to allow external connections
    app.run(host='0.0.0.0', port=7860)
