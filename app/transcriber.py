from google import genai
import tempfile
import os

SUPPORTED_AUDIO_MIME = {
    "mp3": "audio/mpeg",
    "mp4": "audio/mp4",
    "wav": "audio/wav",
    "m4a": "audio/mp4",
    "ogg": "audio/ogg",
    "flac": "audio/flac",
}

def transcribe_audio(audio_file, api_key: str) -> str:
    """
    Transcribes an uploaded audio file using Gemini's native audio understanding.
    audio_file: Streamlit UploadedFile object
    Returns: transcript as plain text string
    """
    client = genai.Client(api_key=api_key)

    # Determine MIME type from extension
    ext = audio_file.name.rsplit(".", 1)[-1].lower()
    mime_type = SUPPORTED_AUDIO_MIME.get(ext, "audio/mpeg")

    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
        tmp.write(audio_file.read())
        tmp_path = tmp.name

    try:
        # Upload file to Gemini Files API
        uploaded = client.files.upload(
            file=tmp_path,
            config={"mime_type": mime_type}
        )

        prompt = """
Please transcribe this audio recording of a meeting accurately.
- Include speaker labels if you can detect different speakers (Speaker 1, Speaker 2, etc.)
- Preserve natural pauses with line breaks
- Do not summarize — provide the full verbatim transcript
- Format: SPEAKER: dialogue
"""
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[uploaded, prompt]
        )
        return response.text.strip()

    except Exception as e:
        return f"[Transcription error: {str(e)}]"

    finally:
        # Clean up temp file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)