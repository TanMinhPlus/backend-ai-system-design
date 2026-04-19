from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def summarize_note(content: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": f"Tóm tắt ngắn gọn nội dung sau bằng tiếng Việt:\n{content}"}
        ]
    )
    return response.choices[0].message.content

def ask_about_note(content: str, question: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": f"Dựa vào nội dung sau:\n{content}\n\nTrả lời câu hỏi: {question}"}
        ]
    )
    return response.choices[0].message.content