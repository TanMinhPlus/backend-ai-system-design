def summarize_note(content: str) -> str:
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": f"Summarize the following content concisely in English:\n{content}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"AI summarize failed: {str(e)}")

def ask_about_note(content: str, question: str) -> str:
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": f"Based on the following content:\n{content}\n\nAnswer this question: {question}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"AI Q&A failed: {str(e)}")