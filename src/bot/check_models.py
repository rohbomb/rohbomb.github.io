import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("LLM_API_KEY")

if not api_key:
    print("❌ LLM_API_KEY가 없습니다.")
else:
    genai.configure(api_key=api_key)
    print("🔍 사용 가능한 모델 리스트:")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
