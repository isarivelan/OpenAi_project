from openai import AzureOpenAI 
import os
import time
import pandas as pd
import json
import logging
import random
from dotenv import load_dotenv


load_dotenv()

SYSTEM_PROMPT = "You are an AI language model tasked with analyzing academic papers."
INPUT_FILE = r'C:\Users\isarivelan.mani\OneDrive - Wood PLC\Documents\Git\mani\input_file\task1.1\input_data.xlsx'

# Initialize OpenAI client
client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),  
    api_version="2024-02-01",
    azure_endpoint=os.getenv("OPENAI_API_BASE_URL")
)

# Exponential backoff mechanism
def analyze_review(client, review, max_retries=5):
    prompt = f"""
Task: Provide a concise summary, describe the research methodology, list key research questions, and suggest future research directions.

Input: {review}

Output: JSON format with the following keys:
- concise_summary
- research_methodology
- key_research_questions
- future_research_directions

Example output:
{{
    "concise_summary": "brief summary",
    "research_methodology": "methodology description",
    "key_research_questions": ["question1", "question2"],
    "future_research_directions": ["direction1", "direction2"]
}}
    """
    backoff_factor = 2 # Exponential factor for wait time
    initial_wait_time = 1 # Initial wait time in seconds
    retries = 0

    while retries < max_retries:
        try:
            # API call
            response = client.chat.completions.create(
                model=os.getenv("DEPLOYMENT_NAME"), # Replace with your model or deployment name for Azure
                messages=[{"role": "system", "content": SYSTEM_PROMPT},
                          {"role": "user", "content": prompt}]
            )
            # Track tokens and cost
            logging.debug(f"Full response: {response}")
            usage = response.usage
            prompt_tokens = usage.prompt_tokens #TODO minimize intermate var
            completion_tokens = usage.completion_tokens
            total_tokens = usage.total_tokens
            
            cost_per_1k_tokens_input = 0.00015 # Adjust based on OpenAI's pricing for GPT-4
            cost_per_1k_tokens_output = 0.00060
            total_cost = ((prompt_tokens / 1000) * cost_per_1k_tokens_input) + ((completion_tokens/1000) * cost_per_1k_tokens_output)
            
            logging.debug(f"Prompt Tokens: {prompt_tokens}, Completion Tokens: {completion_tokens}, "
                          f"Total Tokens: {total_tokens}, Total Cost: ${total_cost}")

            # Parse JSON response
            message_content = response.choices[0].message.content.strip()
            result = json.loads(message_content)
            logging.debug(f"Parsed result: {result}")
            return result

        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error: {e}")
            return None

        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            raise
        
        retries += 1
        wait_time = initial_wait_time * (backoff_factor ** retries)
        logging.debug(f"Retrying in {wait_time} seconds...")
        time.sleep(wait_time)

    logging.error("Max retries exceeded. Returning None.")
    return None

# Process reviews
def process_reviews(client, INPUT_FILE):
    df = pd.read_excel(INPUT_FILE)
    successful_responses = []
    failed_responses = []

    for index, row in df.iterrows():
        paper_id = row['paper_id']
        review = f"Title: {row['title']}\nAbstract: {row['abstract']}\nPublication Year: {row['publication_year']}"

        try:
            analysis = analyze_review(client, review)
            if analysis:
                analysis['paper_id'] = paper_id
                successful_responses.append(analysis)
            else:
                failed_responses.append({'paper_id': paper_id, 'error': 'Invalid response format'})
        except Exception as e:
            logging.error(f"Failed to analyze review for paper ID {paper_id}: {e}")
            failed_responses.append({'paper_id': paper_id, 'error': str(e)})

    return successful_responses, failed_responses

# Save results
def save_results(successful_responses, failed_responses):
    success_df = pd.DataFrame(successful_responses)
    failed_df = pd.DataFrame(failed_responses)

    success_df.to_excel('successful_responses.xlsx', index=False)
    success_df.to_json('successful_responses.json', orient='records', indent=4)
    #failed_df.to_excel('failed_responses.xlsx', index=False)

# Main function
def main():
    logging.basicConfig(filename="log_file.log", level=logging.DEBUG, filemode="w",
                        format="%(asctime)s - %(levelname)s - %(message)s")
    
    logging.debug("Starting review processing...")
    successful_responses, failed_responses = process_reviews(client, INPUT_FILE)
    save_results(successful_responses, failed_responses)
    logging.debug("Processing complete. Check the output files for results.")

if __name__ == "__main__":
    main()
