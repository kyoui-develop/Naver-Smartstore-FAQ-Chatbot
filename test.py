import json
import requests

from config import DATA_DIR


def test():
    with open(f"{DATA_DIR}/test_scenarios.json", "r", encoding="utf-8") as f:
        test_scenarios = json.load(f)

    for user_id, questions in test_scenarios.items():
        print(f"\n***** 시나리오 시작 *****")
        for user_question in questions:
            print(f"\n유저: {user_question}")
            print("챗봇: ", end="", flush=True)
            url = "http://localhost:8000/chat"
            data = {"user_id": user_id, "user_question": user_question}
            with requests.post(url, json=data, stream=True) as response:
                for chunk in response.iter_content(chunk_size=None):
                    print(chunk.decode(), end="", flush=True)
            print()
        print(f"\n***** 시나리오 종료 *****")


if __name__ == "__main__":
    test()