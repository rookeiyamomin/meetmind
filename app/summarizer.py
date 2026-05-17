from google import genai
import json
import re

STYLE_PROMPTS = {
    "Concise (3–5 bullets)": "Provide a concise overview using 3-5 bullet points.",
    "Detailed (paragraph)": "Provide a detailed paragraph-style overview covering all major topics.",
    "Executive Brief": "Provide a crisp executive-level brief: what was discussed, what was decided, what's next."
}

def summarize_transcript(transcript: str, style: str, language: str, api_key: str) -> dict:
    """
    Summarizes a meeting transcript using Gemini.
    Returns a structured dict with overview, decisions, action_items, tone, topics.
    """
    client = genai.Client(api_key=api_key)

    style_instruction = STYLE_PROMPTS.get(style, STYLE_PROMPTS["Concise (3–5 bullets)"])

    lang_instruction = {
        "English": "Respond entirely in English.",
        "Hindi": "Respond entirely in Hindi (Devanagari script).",
        "Hinglish": "Respond in Hinglish (a natural mix of Hindi and English, written in Roman script)."
    }.get(language, "Respond entirely in English.")

    prompt = f"""
You are an expert meeting analyst. Analyze the following meeting transcript and return a structured JSON summary.

INSTRUCTIONS:
- {style_instruction}
- {lang_instruction}
- Extract all action items with owner names if mentioned (use "Team" if no specific owner).
- Identify the overall tone/sentiment of the meeting (e.g., Productive, Tense, Collaborative, Inconclusive).
- List the main topics discussed.

TRANSCRIPT:
\"\"\"
{transcript[:15000]}
\"\"\"

Return ONLY valid JSON in this exact format (no markdown, no backticks):
{{
  "overview": "string",
  "decisions": ["decision 1", "decision 2"],
  "action_items": [
    {{"task": "task description", "owner": "person name or Team"}},
    {{"task": "task description", "owner": "person name or Team"}}
  ],
  "tone": "string describing meeting tone",
  "topics": ["topic1", "topic2", "topic3"]
}}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        raw = response.text.strip()

        # Strip markdown code fences if present
        raw = re.sub(r"^```(?:json)?", "", raw).strip()
        raw = re.sub(r"```$", "", raw).strip()

        result = json.loads(raw)
        return result

    except json.JSONDecodeError as e:
        return {
            "overview": f"Could not parse structured response. Raw output:\n\n{response.text}",
            "decisions": [],
            "action_items": [],
            "tone": "Unknown",
            "topics": []
        }
    except Exception as e:
        return {
            "overview": f"Error calling Gemini API: {str(e)}",
            "decisions": [],
            "action_items": [],
            "tone": "Unknown",
            "topics": []
        }