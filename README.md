# AI-Powered Academic Paper Analysis
## Overview
This project utilizes Azure OpenAI to analyze academic papers. It reads data from an Excel file containing academic paper details, processes each paper to generate a summary, describe the research methodology, list key research questions, and suggest future research directions. The analyzed data is saved in Excel and JSON formats.

## Features
1. Analyzes academic papers using Azure OpenAI.

2. Handles multiple retries with exponential backoff to manage API rate limits.

3. Logs detailed information about the process.

4. Saves the cleaned and analyzed data to Excel and JSON formats.

## Installation
Clone the repository:

bash
git clone <https://github.com/yourusername/academic-paper-analysis.git>
cd academic-paper-analysis
## Install the required libraries:
bash
pip install pandas openpyxl azure-openai python-dotenv
## Configuration
Create a .env file in the root directory of the project and add the following environment variables:

- OPENAI_API_KEY=your_openai_api_key
- OPENAI_API_BASE_URL=your_azure_openai_base_url
- DEPLOYMENT_NAME=your_deployment_name
- Update the INPUT_FILE path in the script with the path to your input Excel file.

## Usage
Place your input Excel file (input_data.xlsx) in the appropriate directory.

## Run the script:

bash
 > python script_name.py
 >
 > Script Details
 >
 >Initialization
>
**Load environment variables:** Uses python-dotenv to load API keys and endpoint URLs.

**Initialize OpenAI client:** Creates an instance of the Azure OpenAI client with the provided API key and endpoint.

**Analyzing Reviews**
**Exponential Backoff Mechanism:** Implements retries with exponential backoff to handle transient errors and rate limits.

**Analyze Review Function:** Sends a prompt to Azure OpenAI to generate a summary, research methodology, key research questions, and future research directions for each paper.

## Processing Reviews
**Read input data:** Loads academic paper details from an Excel file.

**Process each review:** Calls the analyze_review function for each paper.

**Handle errors:** Logs any errors encountered during the analysis.

## Saving Results
**Save to Excel and JSON:** Writes the successfully analyzed data to successful_responses.xlsx and successful_responses.json.

**Log file**: Detailed logs are written to log_file.log.

## Logging
The script logs detailed information about each step of the process to log_file.log. The logging level is set to DEBUG to capture all details.

## Example Output
**successful_responses.xlsx:** Contains the successfully analyzed and cleaned data.

**successful_responses.json:** Contains the analyzed data in indented JSON format.