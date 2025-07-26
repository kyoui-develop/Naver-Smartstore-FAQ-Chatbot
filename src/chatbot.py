from openai import OpenAI

from src.retriever import Retriever
from src.prompts import SYSTEM_PROMPT, USER_PROMPT
from config import MODEL_NAME


class Chatbot:
    def __init__(self, model=MODEL_NAME, temperature=0.7, retriever=Retriever()):
        self.client = OpenAI()
        self.model = model
        self.temperature = temperature
        self.retriever = retriever

    def get_context(self, user_question):
        return self.retriever.retrieve(user_question)

    def build_messages(self, user_question, context, chat_history):
        faqs = "\n\n".join(
        f"Q: {faq['question']}\nA: {faq['answer']}" for faq in context
        )
        related_questions = [q for faq in context for q in faq["related_questions"]]
        related_questions = "\n".join(f"- {q}" for q in related_questions) if related_questions else ""

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        if chat_history:
            messages.extend(chat_history)
            
        messages.append({
            "role": "user",
            "content": USER_PROMPT.format(
                user_question=user_question,
                faqs=faqs,
                related_questions=related_questions
            )
        })

        return messages

    def response(self, user_question, chat_history=None):
        context = self.get_context(user_question)
        messages = self.build_messages(user_question, context, chat_history)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            stream=True,
        )

        for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                yield content