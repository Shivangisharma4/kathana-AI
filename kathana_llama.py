from llama_cpp import Llama

# Load Mistral model (adjust filename if different)
llm = Llama(model_path="./models/mistral-7b-instruct-v0.1.Q4_K_M.gguf")

# 🎭 Mood modifiers dictionary
MOODS = {
    "dramatic": "Make it intense, emotional, and full of high-stakes moments.",
    "fantasy": "Add magical elements, dreamy worlds, and whimsical details.",
    "thriller": "Make it suspenseful, mysterious, and full of twists.",
    "philosophical": "Add depth, introspection, and complex themes.",
    "light-hearted": "Keep it funny, feel-good, and easygoing."
}

def generate_story_idea(prompt, mood=None):
    system_message = "You are Kathana, a story writing assistant who creates magical, emotional, and creative story ideas based on any theme and mood provided by the user."
    
    # Add mood instruction if given
    mood_instruction = MOODS.get(mood, "")
    
    full_prompt = f"<s>[INST] <<SYS>>\n{system_message}\n<</SYS>>\n\nGenerate a short story idea based on: {prompt}.\n{mood_instruction} [/INST]"

    output = llm(
        prompt=full_prompt,
        max_tokens=300,
        temperature=0.75,
        top_p=0.9,
    )
    return output["choices"][0]["text"].strip()

# --- Run Program ---
theme = input("🎨 Enter your story theme or idea: ").strip()
print("\n🌈 Choose a mood (optional): dramatic, fantasy, thriller, philosophical, light-hearted")
mood = input("🎭 Mood (press Enter to skip): ").strip().lower()
if mood not in MOODS:
    mood = None

story = generate_story_idea(theme, mood)
print("\n📝 Kathana’s Story Idea:\n")
print(story)
