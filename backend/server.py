import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline

# --- 1. Initialize Flask App ---
app = Flask(__name__)
CORS(app)

# --- 2. Load Your Models ---
print("--- Server is starting ---")
print(f"Python version: {sys.version}")

optimizer_pipeline = None

# --- Hugging Face Model Loading ---
try:
    # This is the specialist model for Python code generation
    model_name = 'model_name = Salesforce/codegen-2B-mono'
    
    print(f"Loading {model_name} model...")
    
    # Note: We use 'text-generation' for this model type
    hf_task = 'text-generation' 
    
    optimizer_pipeline = pipeline(hf_task, model=model_name)
    
    print("Hugging Face model loaded successfully.")
    print("--- Server is ready. ---")
    
except Exception as e_hf:
    print(f"--- CRITICAL ERROR loading Hugging Face model: {e_hf} ---")
    print("--- Server will not work. ---")


# --- 3. Create an API Endpoint ---
@app.route('/optimize', methods=['POST'])
def optimize_code():
    print("\n--- Received a request ---")
    
    if not request.json or 'code' not in request.json:
        print("Request error: No 'code' key in JSON.")
        return jsonify({'error': 'No code provided'}), 400

    # This 'code_snippet' contains your full "Expert" prompt from VS Code
    code_snippet = request.json['code']
    print(f"Received prompt length: {len(code_snippet)} chars") 

    response_data = {}

    try:
        # --- Use Optimizer (Hugging Face) ---
        if optimizer_pipeline:
            print("Running Hugging Face model...")
            
            # Run the model. 
            # max_new_tokens=200 gives it enough space to write the optimized code
            opt_result = optimizer_pipeline(code_snippet, max_new_tokens=200)
            
            # Get the full generated text
            full_response = opt_result[0]['generated_text']
            
            # Clean up: We only want the part AFTER "Optimized Code:"
            if "Optimized Code:" in full_response:
                clean_optimization = full_response.split("Optimized Code:")[-1].strip()
            else:
                clean_optimization = full_response

            response_data['optimization'] = clean_optimization
            print("Optimization generated successfully.")
            
        else:
            print("Optimizer model is not loaded.")
            response_data['optimization'] = "Error: Optimizer model is not loaded on server."
        
        return jsonify(response_data)

    except Exception as e:
        print(f"--- ERROR during prediction: {e} ---")
        return jsonify({'error': f'Prediction failed: {e}'}), 500

# --- 4. Run the Server ---
if __name__ == '__main__':
    print("Starting Flask server on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)