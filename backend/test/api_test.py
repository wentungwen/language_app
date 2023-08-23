import os
import requests
from google.cloud import translate_v2 as translate

## google translate
# GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
# api_endpoint = "https://translation.googleapis.com/language/translate/v2"

# print(GOOGLE_APPLICATION_CREDENTIALS)

# def translate_text(text, source_language, target_language):
#     translate_client = translate.Client.from_service_account_json(GOOGLE_APPLICATION_CREDENTIALS)
#     result = translate_client.translate(text, source_language=source_language, target_language=target_language)
#     return result["translatedText"]

# if __name__ == "__main__":
#     text_to_translate = "Bonjour, tout le monde!"  # French text
#     source_language = "fr"  # Source language: French
#     target_language = "nl"  # Target language: Dutch

#     translated_text = translate_text(text_to_translate, source_language, target_language)
#     print("Original Text (French): ", text_to_translate)
#     print("Translated Text (Dutch): ", translated_text)


# gpt testing
GPT_API_ENDPOINT = "https://api.openai.com/v1/completions"
GPT_APIKEY = os.environ.get("GPT_APIKEY")

prompt = f'Generate a  jap conversation. Difficulty levels: b1. About love. In Json format, ex:[{{"sender": "A","content": "...",}},]'
request_headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {GPT_APIKEY}",
}
request_data = {
    "model": "text-davinci-003",
    "prompt": prompt,
    "max_tokens": 1000,
    "temperature": 0.7,
}

response = requests.post(
    GPT_API_ENDPOINT, headers=request_headers, json=request_data
)
if response.status_code == 200:
    generated_conversations = response.json()["choices"][0]["text"]
    stripped_res = generated_conversations.strip()
    print(stripped_res)
else:
    print(
        f"Request failed with status code: {str(response.status_code), response.text}"
    )

