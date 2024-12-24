import logging

def cost_calc(successful_responses):
    total_prompt_tokens = 0
    total_completion_tokens = 0
    total_cost = 0

    cost_per_1k_tokens_input = 0.00015  # Adjust based on OpenAI's pricing for GPT-4
    cost_per_1k_tokens_output = 0.00060

    for response in successful_responses:
        usage = response.usage
        prompt_tokens = usage.prompt_tokens
        completion_tokens = usage.completion_tokens
        total_tokens = usage.total_tokens
        
        input_cost = (prompt_tokens / 1000) * cost_per_1k_tokens_input
        output_cost = (completion_tokens / 1000) * cost_per_1k_tokens_output
        total_response_cost = input_cost + output_cost
        
        logging.debug(f"Prompt Tokens: {prompt_tokens}, Completion Tokens: {completion_tokens}, "
                      f"Total Tokens: {total_tokens}, Input Cost: ${input_cost:.5f}, Output Cost: ${output_cost:.5f}, Total Cost: ${total_response_cost:.5f}")
        print(f"Prompt Tokens: {prompt_tokens}, Completion Tokens: {completion_tokens}, Total Tokens: {total_tokens}, Input Cost: ${input_cost:.5f}, Output Cost: ${output_cost:.5f}, Total Cost: ${total_response_cost:.5f}")

        total_prompt_tokens += prompt_tokens
        total_completion_tokens += completion_tokens
        total_cost += total_response_cost
    
    logging.debug(f"Total Prompt Tokens: {total_prompt_tokens}, Total Completion Tokens: {total_completion_tokens}, "
                  f"Total Cost: ${total_cost:.5f}")
    print(f"Total Prompt Tokens: {total_prompt_tokens}, Total Completion Tokens: {total_completion_tokens}, Total Cost: ${total_cost:.5f}")

