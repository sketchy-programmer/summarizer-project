import openai
import traceback
from config import API_KEY

class SummarizerError(Exception):
    """Custom exception for summarization errors."""
    pass

def summarize_text(text, max_length=150, min_length=100):
    """
    Summarizes the selected text using the OpenAI API.
    
    Args:
        text (str): Text to summarize
        max_length (int): Maximum summary length
        min_length (int): Minimum summary length
    
    Returns:
        str: Summarized text
    """
    try:
        # Validate input
        if not text or len(text.strip()) < 50:
            raise SummarizerError("Text is too short to summarize.")

        client = openai.OpenAI(api_key=API_KEY)
        response = client.chat.completions.create(
            model="gpt-4.5-preview",
            messages=[
                {
                    "role": "system", 
                    "content": f"Provide a concise summary between {min_length}-{max_length} words. Capture the key points and main ideas."
                },
                {"role": "user", "content": f"Summarize the following text:\n\n{text}"}
            ],
            max_tokens=500,
            temperature=0.7
        )
        summary = response.choices[0].message.content.strip()
        
        # Additional validation
        if len(summary) < min_length:
            raise SummarizerError("Generated summary is too short.")
        
        return summary
    
    except SummarizerError as e:
        return f"Summarization Error: {str(e)}"
    except Exception as e:
        traceback.print_exc()
        return f"Unexpected Error: {str(e)}"