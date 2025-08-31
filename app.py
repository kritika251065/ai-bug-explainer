import configparser
import os
import csv
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

#get config file parameters
path_current_directory = os.path.dirname(os.path.abspath(__file__))
path_config_file = path_current_directory + '\\config\\config.cg'
config = configparser.ConfigParser()
config.read(path_config_file)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def explain_bug(error_message: str, use_ai: bool = True):
    try:
        csv_file = config.get("Settings", "error_list")
        with open(csv_file, mode = 'r', encoding = 'utf-8-sig') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                if row["error_message"] == error_message:
                    return f"Explanation: {row['explanation']}"
            # If not found, try AI
            if use_ai:
                try:
                    return ai_explain_error(error_message)
                except Exception as e:
                    return f"No explanation found in dictionary. AI fallback failed: {e}"
        return f"No explanation found for: {error_message}"
    except Exception as exe:
        return f"Error reading CSV: {exe}" 


def ai_explain_error(error_message):
    prompt = f"""
    Explain this error in simple terms and suggest how to fix it.
    Error: {error_message}
    """
    
    response = client.responses.create(
        model="gpt-5",
        input = prompt
    )
    return response.output_text

if __name__ == "__main__":
    print("=== AI Bug Explainer 🐞 ===")
    print("Type an error message (or 'exit' to quit)\n")
    while True:
        user_input = input("Know About Your Bug: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye 👋")
            break
        print(explain_bug(user_input))
        print("-" * 50)
