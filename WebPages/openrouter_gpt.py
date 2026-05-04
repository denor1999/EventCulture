from openai import OpenAI

OPENROUTER_API_KEY = "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"
BASE_URL = "https://openrouter.ai/api/v1"

YOUR_SITE_URL = "http://127.0.0.1:8000"
YOUR_SITE_NAME = "CultureEvents"

def ask_openrouter(question):
    client = OpenAI(
        base_url=BASE_URL,
        api_key=OPENROUTER_API_KEY,
    )

    try:
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": YOUR_SITE_URL,
                "X-Title": YOUR_SITE_NAME,
            },
            model="openrouter/free",
            messages=[{"role": "user", "content": question}],
            temperature=0.7,
            max_tokens=500
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Ошибка API: {str(e)}"