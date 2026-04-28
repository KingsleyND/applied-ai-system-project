import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env from the parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

KNOWLEDGE_BASE_PATH = os.path.join(os.path.dirname(__file__), "assets", "Comprehensive_Dog_Breeds_Care.json")

def _load_knowledge_base():
    with open(KNOWLEDGE_BASE_PATH, "r") as f:
        return json.load(f)

def retrieve_breed_facts(breed: str) -> dict | None:
    """Look up a breed in the knowledge base. Returns the matching entry or None."""
    data = _load_knowledge_base()
    breed_lower = breed.lower().strip()
    for entry in data:
        # entry["name"] looks like "3. Golden Retriever" — strip the number prefix
        entry_name = entry["name"].split(". ", 1)[-1].lower()
        if breed_lower in entry_name or entry_name in breed_lower:
            return entry
    return None

def _age_stage(age: int) -> str:
    if age <= 2:
        return "young"
    elif age <= 7:
        return "mid"
    else:
        return "old"

def get_ai_suggestions(breed: str, age: int) -> str:
    """
    Retrieve facts for the breed from the knowledge base, then ask Gemini
    to surface 2-3 care facts and suggest 3 tasks based on the pet's age.
    Returns Gemini's response as a plain string.
    """
    entry = retrieve_breed_facts(breed)

    if entry:
        stage = _age_stage(age)
        retrieved = (
            f"Breed: {entry['name']}\n"
            f"Key fact 1: {entry['fact1']}\n"
            f"Key fact 2: {entry['fact2']}\n"
            f"Age-specific note ({stage}): {entry[stage]}"
        )
    else:
        retrieved = f"No specific data found for '{breed}'. Use general dog care knowledge."

    prompt = f"""You are a pet care assistant. A user has a {breed} that is {age} year(s) old.

Here is what the knowledge base says about this breed:
{retrieved}

Based on this, do two things:
1. Share 2-3 short, specific care facts about this breed and age.
2. Suggest exactly 3 tasks the owner should add to their daily care schedule. For each task, give:
   - Task name (short, e.g. "Morning walk - 30 min")
   - Reason (one sentence tied directly to the retrieved facts above)

Keep your response concise and practical."""

    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text
