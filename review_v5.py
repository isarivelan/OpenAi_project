from openai import AzureOpenAI, RateLimitError
import os
import time
import pandas as pd
import json
import logging
import random
from dotenv import load_dotenv
import backoff
from utils3 import  total_cost_calc

load_dotenv()

SYSTEM_PROMPT = "You are an AI language model tasked with analyzing academic papers."
INPUT_FILE = r'C:\Users\isarivelan.mani\OneDrive - Wood PLC\Documents\Git\mani\input_file\task1.1\input_data.xlsx'


# Initialize OpenAI client
client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),  
    api_version="2024-02-01",
    azure_endpoint=os.getenv("OPENAI_API_BASE_URL")
)

# Exponential backoff mechanism   TODO : 
@backoff.on_exception(backoff.expo, RateLimitError)
def analyze_review(client, review):
    global prompt_tokens, completion_tokens
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

    try:
        # API call with backoff
        
        response = client.chat.completions.create(
            model=os.getenv("DEPLOYMENT_NAME"), 
            messages=[{"role": "system", "content": SYSTEM_PROMPT},
                      {"role": "user", "content": prompt}]
        )
                  
        # Parse JSON response
        usage = response.usage
        prompt_tokens = usage.prompt_tokens #TODO minimize intermate var
        completion_tokens = usage.completion_tokens
      
        message_content = response.choices[0].message.content.strip()
        result = json.loads(message_content)
        logging.debug(f"Parsed result: {result}")
        result['usage'] = { 'prompt_tokens': prompt_tokens, 'completion_tokens': completion_tokens }
        
        return result

    except json.JSONDecodeError as e:
        logging.error(f"JSON decode error: {e}")
        return None

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise

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
    success__res_df = pd.DataFrame(successful_responses)
    
    if 'usage' in success__res_df.columns:
        success_df = success__res_df.drop(columns=['usage'])
    else:
        print("Column 'usage' not found in DataFrame.")
    
    failed_df = pd.DataFrame(failed_responses)

    success_df.to_excel('successful_responses.xlsx', index=False)
    success_df.to_json('successful_responses.json', orient='records', indent=4)
    failed_df.to_excel('failed_responses.xlsx', index=False)

# Main function
def main():
    start_time = time.time()
   
    logging.basicConfig(filename="log_file.log", level=logging.DEBUG, filemode="w",
                        format="%(asctime)s - %(levelname)s - %(message)s")

    logging.debug("Starting review processing...")
    successful_responses, failed_responses = process_reviews(client, INPUT_FILE)
    #cost_calc(successful_responses)
    all_prompt_tokens = [resp['usage']['prompt_tokens'] for resp in successful_responses] 
    all_completion_tokens = [resp['usage']['completion_tokens'] for resp in successful_responses]
    total_cost_calc(all_prompt_tokens, all_completion_tokens)
    save_results(successful_responses, failed_responses)
    logging.debug("Processing complete. Check the output files for results.")
    end_time = time.time()
    
    duration = end_time - start_time
    
    print(f"Duration is : {duration} secs")
   

if __name__ == "__main__":
    main()
