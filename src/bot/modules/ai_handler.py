import os
import json
import logging
import google.generativeai as genai

logger = logging.getLogger("HybridBot")

class AIHandler:
    def __init__(self, api_key):
        self.api_key = api_key
        if self.api_key:
            genai.configure(api_key=self.api_key)
            # Fallback priority list (restored from working v2.8)
            self.model_candidates = ['gemini-2.0-flash-exp', 'gemini-exp-1206', 'gemini-2.5-flash']
        else:
            self.model_candidates = []

    def _load_prompt_template(self):
        prompt_path = os.path.join(os.path.dirname(__file__), '..', 'prompts', 'prompt_bear.md')
        try:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"❌ 프롬프트 파일을 읽는 중 오류 발생: {e}")
            raise e

    def generate_content(self, news_item):
        """Gemini(Market Analyst)를 이용해 블로그 포스팅 내용 JSON으로 반환"""
        is_dry_run = os.getenv("DRY_RUN", "false").lower() == "true"
        
        if is_dry_run and not self.api_key:
            logger.info("🧪 [Dry Run Mode] AI API 호출 없이 더미 JSON 데이터를 반환합니다.")
            return {
                "title": "[Dry Run] 글로벌 시장 인사이트 시각화 테스트",
                "key_facts": [
                    "이것은 디자인 확인용 테스트 문구입니다.",
                    "실제 AI API를 호출하지 않아 비용이 발생하지 않습니다.",
                    "(출처: TIKKLES Dummy News)"
                ],
                "insight": "이 섹션은 Analyst의 통찰력이 들어가는 공간입니다. 폰트 크기, 줄 간격, 박스 디자인(Callout)이 제대로 적용되었는지 확인하세요.\n\n| 구분 | 테스트 1 | 테스트 2 |\n|---|---|---|\n| 수치 | 100% | 200% |\n\n성공적인 투자를 위해서는 도구의 효율성을 점검하는 것이 필수적입니다.",
                "seo_tags": ["dummy test", "ai automation", "local testing"],
                "pexels_query": "server room"
            }

        if not self.model_candidates:
            logger.error("❌ LLM_API_KEY가 없습니다.")
            return None

        template = self._load_prompt_template()
        prompt = template
        prompt = prompt.replace("{keyword}", str(news_item.get('keyword', '')))
        prompt = prompt.replace("{title}", str(news_item.get('title', '')))
        prompt = prompt.replace("{link}", str(news_item.get('link', '')))
        prompt = prompt.replace("{summary}", str(news_item.get('summary', '')))

        for model_name in self.model_candidates:
            try:
                logger.info(f"🤖 모델 시도 중: {model_name}")
                model = genai.GenerativeModel(model_name)
                
                # JSON 강제 출력 설정 및 response_schema 도입
                generation_config = genai.types.GenerationConfig(
                    response_mime_type="application/json",
                    response_schema={
                        "type": "OBJECT",
                        "properties": {
                            "is_valid_article": {"type": "BOOLEAN"},
                            "title": {"type": "STRING"},
                            "summary": {"type": "STRING"},
                            "key_facts": {
                                "type": "ARRAY",
                                "items": {"type": "STRING"}
                            },
                            "insight": {"type": "STRING"},
                            "tags": {
                                "type": "ARRAY",
                                "items": {"type": "STRING"}
                            },
                            "pexels_query": {"type": "STRING"}
                        },
                        "required": ["is_valid_article", "title", "summary", "key_facts", "insight", "tags", "pexels_query"]
                    }
                )
                
                response = model.generate_content(prompt, generation_config=generation_config)
                response_text = response.text
                
                try:
                    result_json = json.loads(response_text)
                    
                    # 🚨 가비지 뉴스 필터: AI가 저품질로 판별한 경우 안전하게 스킵
                    if not result_json.get("is_valid_article", True):
                        logger.info("🗑️ 가비지/광고 뉴스로 판별되어 포스팅을 건너뜁니다 (is_valid_article: false).")
                        return None
                        
                    return result_json
                except json.JSONDecodeError:
                    logger.warning(f"⚠️ {model_name} JSON 디코딩 실패. Raw text:\n{response_text}")
                    # Markdown block 제거 재시도 (혹시나 백틱이 포함된 경우)
                    import re
                    json_str = re.sub(r'```json\n?(.*?)\n?```', r'\1', response_text, flags=re.DOTALL).strip()
                    try:
                        return json.loads(json_str)
                    except json.JSONDecodeError as e:
                        logger.error(f"❌ JSON 파싱 최종 실패: {e}")
                        continue
                        
            except Exception as e:
                logger.warning(f"⚠️ {model_name} 생성 실패 (다음 모델 시도): {e}")
                continue
        
        logger.error("❌ 모든 AI 모델이 응답에 실패했거나 JSON 변환에 실패했습니다.")
        return None
