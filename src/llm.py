import os, re, time
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.environ["LLM_API_KEY"])
MODEL = os.environ["LLM_MODEL"]
FAST = os.environ.get("LLM_MODEL_FAST", MODEL)

def llm(prompt: str, fast: bool = False, retries: int = 2) -> str:
    for attempt in range(retries):
        try:
            r = client.chat.completions.create(
                model=FAST if fast else MODEL,
                temperature=0,
                messages=[{"role": "user", "content": prompt}]
            )

            text = r.choices[0].message.content or ""
            return re.sub(
                r"<think>.*?</think>",
                "",
                text,
                flags=re.DOTALL
            ).strip()

        except Exception as e:
            if attempt == retries - 1:
                raise

            wait = 10 * (attempt + 1)
            print(f"LLM rate limit/error. Retrying in {wait}s...")
            time.sleep(wait)

if __name__ == "__main__":
    print(llm("Say hello in five words."))