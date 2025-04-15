from flask import Flask, request, jsonify
from flask_cors import CORS # Import CORS
from llama_cpp import Llama

app = Flask(__name__)

# --- Simplified CORS Configuration ---
# Apply CORS globally, allowing requests specifically from your frontend origin
# and enabling automatic OPTIONS handling by Flask-CORS.
# You can also specify methods and headers if defaults aren't enough,
# but often just the origin is sufficient if you don't need credentials.
CORS(app, origins="http://localhost:5173")

# --- Your Llama setup and MOODS dictionary ---
# (Keep your llm initialization and MOODS dictionary here)
llm = Llama(model_path="./models/mistral-7b-instruct-v0.1.Q4_K_M.gguf")
MOODS = {
    "dramatic": "Make it intense, emotional, and full of high-stakes moments.",
    "fantasy": "Add magical elements, dreamy worlds, and whimsical details.",
    "thriller": "Make it suspenseful, mysterious, and full of twists.",
    "philosophical": "Add depth, introspection, and complex themes.",
    "light-hearted": "Keep it funny, feel-good, and easygoing."
}
# --- ---

# --- Modify the /generate route ---
# Explicitly add 'OPTIONS' to the allowed methods for this route.
# Flask-CORS should intercept OPTIONS, but this makes it clearer.
@app.route('/generate', methods=['POST', 'OPTIONS'])
def generate():
    # Flask-CORS usually handles the OPTIONS response automatically.
    # If the request method is OPTIONS, Flask-CORS should respond before your code runs.
    # If it's POST, your existing logic will run.
    if request.method == 'POST':
        data = request.json
        theme = data.get("theme")
        mood = data.get("mood", "").lower() # Mood comes from frontend now

        if not theme:
            return jsonify({"error": "Theme is required"}), 400

        if mood and mood not in MOODS:
            return jsonify({"error": f"Invalid mood. Available moods are: {', '.join(MOODS.keys())}"}), 400

        system_message = "You are Kathana, a story writing assistant who creates magical, emotional, and creative story ideas based on any theme and mood provided by the user."
        mood_instruction = MOODS.get(mood, "")

        full_prompt = f"<s>[INST] <<SYS>>\n{system_message}\n<</SYS>>\n\nGenerate a short story idea based on: {theme}.\n{mood_instruction} [/INST]"

        try:
            output = llm(
                prompt=full_prompt,
                max_tokens=300,
                temperature=0.75,
                top_p=0.9,
            )
            story = output["choices"][0]["text"].strip()
            return jsonify({"story": story})
        except Exception as e:
            # Log the full error server-side for better debugging
            app.logger.error(f"Error generating story: {str(e)}")
            return jsonify({"error": "An error occurred while generating the story."}), 500
    else:
        # Handle cases if OPTIONS isn't automatically handled (though it should be)
        # Flask-CORS should handle this implicitly, returning a 2xx response
        # If you ever needed manual OPTIONS handling it would go here, but rely on Flask-CORS first.
        return '', 204


@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Kathana backend is alive 🚀"})

if __name__ == "__main__":
    # Make sure your server listens on 0.0.0.0 if accessing from different devices/containers
    # For typical localhost development, 127.0.0.1 or default is fine.
    # Port 5000 is assumed based on your frontend fetch URL.
    app.run(debug=True, port=5000) # Ensure port is 5000