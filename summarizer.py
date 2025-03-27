import openai
import traceback
from config import API_KEY

def summarize_text(text):
    """Summarizes the selected text using the OpenAI API."""
    try:
        client = openai.OpenAI(api_key=API_KEY)
        response = client.chat.completions.create(
            model="gpt-4.5-preview",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text. Provide a summary between 100-150 words."},
                {"role": "user", "content": f"Summarize the following text:\n\n{text}"}
            ],
            max_tokens=500,
            temperature=1.2
        )
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        traceback.print_exc()
        return f"Error: {str(e)}"
