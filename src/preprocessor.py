import re


def clean_text(text):
    text = text.replace('\ufeff', '')
    text = re.sub(r'(?:\xa0)+', ' ', text)
    text = re.sub(r"위 도움말이 도움이 되었나요\?.*?도움말 닫기", '', text, flags=re.DOTALL)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_related_questions(text):
    match = re.search(r"관련 도움말/키워드\s*(.*?)도움말 닫기", text, flags=re.DOTALL)
    if not match:
        return []
    lines = match.group(1).strip().splitlines()
    return [line.strip("-• ").strip() for line in lines if line.strip()]


def preprocess_faqs(faqs):
    result = []
    for i, (question, answer) in enumerate(faqs.items()):
        result.append({
            "question": question,
            "answer": clean_text(answer),
            "related_questions": extract_related_questions(answer)
        })
    return result