import subprocess

def call_ollama(prompt: str, model: str = "qwen2.5-coder:0.5b") -> str:
    command = ['ollama', 'run', model, prompt]
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.strip()

def summarize_news(chunks: list):
    news_text =""
    for idx,chunk in chunks:
        news_text += f"[ARTICLE {idx+1}]\n{chunk['text']}\nImages: {chunk['images']}\n\n"
    prompt = f"""
You are a worlds top payed newspaper analyst.The following content is from an e-newspaper. Your job is to:

1. Identify distinct news topics.
2. Group connected articles under one topic name (object).
3. For each topic, create:
   - A title
   - A short summary (2 lines)
   - A detailed summary (1 paragraph)
   - List any image captions or notable visuals if found

Return a JSON array like:
[
  {{
    "object": "topic name",
    "title": "...",
    "short_summary": "...",
    "detailed_summary": "...",
    "image_links": ["..."],
    "time_updated": "ISO 8601 time"
  }},
  ...
]

Content:
{news_text}
"""
    return call_ollama(prompt)





