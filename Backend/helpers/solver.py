import google.generativeai as genai
import logging
import time
import os

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, encoding='utf-8')

# Load API key securely (Set this as an environment variable)
API_KEY = os.getenv("GEMINI_API_KEY")  # Replace with actual API key
genai.configure(api_key=API_KEY)

# Initialize the Gemini model once
model = genai.GenerativeModel("gemini-1.5-flash")

def solve_questions(questions, max_retries=3, retry_delay=2):
    """
    Solves a list of questions using Google's Gemini Generative AI.

    Args:
        questions (list): A list of questions to be solved.
        max_retries (int): Number of retry attempts for API failures.
        retry_delay (int): Initial delay (seconds) for retry attempts.

    Returns:
        list: A list of answers corresponding to the input questions.
    """
    answers = []
    
    for question in questions:
        attempt = 0
        while attempt < max_retries:
            try:
                response = model.generate_content(question)
                answers.append(response.text)
                break  # Exit retry loop on success
            except Exception as e:
                if "429" in str(e):
                    wait_time = retry_delay * (2 ** attempt)  # Exponential backoff
                    logger.warning(f"Rate limit reached. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Error generating answer: {str(e)}")
                    answers.append("Error: Failed to generate answer.")
                    break  # Exit loop on non-429 errors
            attempt += 1

    return answers

# Example usage
if __name__ == "__main__":
    sample_questions = ["What is the capital of France?", "Explain the concept of gravity."]
    solved_answers = solve_questions(sample_questions)

    for i, answer in enumerate(solved_answers, start=1):
        print(f"Q{i}: {sample_questions[i-1]}\nA: {answer}\n")
