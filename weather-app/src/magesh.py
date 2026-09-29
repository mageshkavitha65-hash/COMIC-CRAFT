from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()

const API_KEY = import.meta.env.VITE_API_KEY;

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing in .env")

client = genai.Client(api_key=API_KEY)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate_comic():

    try:
        data = request.get_json()

        topic = data.get("topic", "").strip()
        genre = data.get("genre", "Adventure")
        characters = data.get("characters", "").strip()
        panels = int(data.get("panels", 6))

        if not topic:
            return jsonify({
                "success": False,
                "error": "Please enter a comic story idea."
            }), 400

        prompt = f"""
You are ComicCraft-AI, an AI comic story creator.

Create an original comic story based on the following information.

Story idea:
{topic}

Genre:
{genre}

Characters:
{characters if characters else "Create suitable characters"}

Number of panels:
{panels}

Return ONLY valid JSON.

Use exactly this structure:

{{
  "title": "Comic title",
  "description": "Short story description",
  "characters": [
    {{
      "name": "Character name",
      "description": "Character description"
    }}
  ],
  "panels": [
    {{
      "panel": 1,
      "scene": "Detailed visual scene description",
      "dialogue": "Character dialogue",
      "caption": "Narrator caption",
      "sound_effect": "Optional sound effect"
    }}
  ]
}}

Make the story creative, coherent and suitable for a general audience.
Make exactly {panels} panels.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text.strip()

        # Remove Markdown code fences if Gemini returns them
        if text.startswith("```"):
            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()

        comic = json.loads(text)

        return jsonify({
            "success": True,
            "comic": comic
        })

    except json.JSONDecodeError:
        return jsonify({
            "success": False,
            "error": "Gemini returned an invalid response. Please try again."
        }), 500

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)