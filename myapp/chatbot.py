import csv
import cohere
import os

COHERE_API_KEY="ckc6CNJ37YTHNoSxvkc2invpu10MDhtQqChAraz6"

client = cohere.Client(api_key=COHERE_API_KEY)
dataset = []

# def load_dataset_from_csv(file_path):
#     with open(file_path, 'r') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             dataset.append(row)
#     return dataset

def generate_api_response(query):
    try:
        response = client.generate(
            prompt=query,
            max_tokens=500,
            temperature=0.5
        )
        api_response = response.generations[0].text
        return api_response
    except Exception as e:
        return f"Error: {str(e)}"