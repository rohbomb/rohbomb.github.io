# 🤖 Tikkles Analyst Bot v2.2 (JSON Fix & Path Unified)
import os
import time
import requests
import feedparser
import logging
from datetime import datetime
import pytz
from github import Github, GithubException
import google.generativeai as genai
from dotenv import load_dotenv
import urllib.parse
import json  # 🛠️ Fix: Global import to prevent NameError

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("HybridBot")

# 환경 변수 로드 (로컬 테스트용)
load_dotenv()

class HybridBot:
    def __init__(self):
        self.github_token = os.getenv("GH_PAT")
        self.target_repo_name = "rohbomb/rohbomb.github.io"
        self.llm_api_key = os.getenv("LLM_API_KEY")
        self.pexels_api_key = os.getenv("PEXELS_API_KEY") # 🛠️ 복구: Pexels API Key 로드
        
        if not self.github_token:
            logger.error("❌ GH_PAT 환경변수가 없습니다.")
            raise ValueError("GitHub Token is missing")

        # GitHub 연결
        self.gh = Github(self.github_token)
        self.repo = self.gh.get_repo(self.target_repo_name)

        # Gemini 설정 (API 키가 있을 때만)
        if self.llm_api_key:
            genai.configure(api_key=self.llm_api_key)
            # 🚨 Model Priority List (Fallback System)
            # 1순위: gemini-2.0-flash-exp (New Experimental)
            # 2순위: gemini-exp-1206 (Often Limited)
            # 3순위: gemini-2.5-flash (Backup)
            self.model_candidates = ['gemini-2.0-flash-exp', 'gemini-exp-1206', 'gemini-2.5-flash']
        else:
            self.model_candidates = []
            logger.warning("⚠️ LLM_API_KEY가 없습니다. AI 요약 기능이 비활성화됩니다.")

    def fetch_news(self, keyword):
        """RSS 피드에서 키워드 기반 뉴스 가져오기"""
        logger.info(f"📡 '{keyword}' 뉴스 수집 중...")
        
        # 키워드 URL 인코딩
        encoded_keyword = urllib.parse.quote(keyword)
        
        # 구글 뉴스 RSS (미국/글로벌 최신순 + 24시간 이내) - 저작권 이슈 회피 및 정보 질 향상
        # when:1d + gl=US + hl=en-US + ceid=US:en
        rss_url = f"https://news.google.com/rss/search?q={encoded_keyword}+when:1d&hl=en-US&gl=US&ceid=US:en"
        
        try:
            feed = feedparser.parse(rss_url)
            
            if not feed.entries:
                logger.warning(f"⚠️ '{keyword}' 검색 결과가 없습니다.")
                return []

            # 중복 방지 로직 (processed_news.json 활용)
            processed_file = "processed_news.json"
            processed_links = []
            if os.path.exists(processed_file):
                try:
                    with open(processed_file, "r", encoding="utf-8") as f:
                        processed_links = json.load(f)
                except:
                    processed_links = []
            
            for entry in feed.entries:
                if entry.link not in processed_links:
                    logger.info(f"✅ 새 뉴스 발견: {entry.title}")
                    
                    # 처리된 링크 저장
                    processed_links.append(entry.link)
                    # 파일 크기 조절 (최근 100개만 유지)
                    if len(processed_links) > 100:
                        processed_links = processed_links[-100:]
                        
                    with open(processed_file, "w", encoding="utf-8") as f:
                        json.dump(processed_links, f, ensure_ascii=False, indent=2)
                        
                    return {
                        'title': entry.title,
                        'link': entry.link,
                        'published': entry.published,
                        'summary': getattr(entry, 'summary', ''),
                        'keyword': keyword
                    }
            
            logger.info("ℹ️ 새로운 뉴스가 없습니다. (모두 처리됨)")
            return None
            
        except Exception as e:
            logger.error(f"❌ 뉴스 수집 실패 ({keyword}): {e}")
            return []

    def generate_content(self, news_item):
        """Gemini(Market Analyst)를 이용해 블로그 포스팅 작성 (Fallback 적용)"""
        if not self.model_candidates:
            return f"AI 요약을 사용할 수 없습니다.\n\n원문 링크: {news_item['link']}"

        prompt = f"""
        당신은 20년 경력의 글로벌 매크로/기술 분석가 'Market Analyst Bear'입니다.
        아래 뉴스 기사를 전문 투자자 및 3040 직장인을 타겟으로 분석하여 브리핑해 주세요.

        [뉴스 정보]
        키워드: {news_item['keyword']}
        제목(원문): {news_item['title']}
        링크: {news_item['link']}
        내용(원문): {news_item['summary']}

        [작성 규칙]
        0. **Role**: 당신은 글로벌 시장의 최신 트렌드를 한국 투자자에게 소개하는 'Market Analyst Bear'입니다.
           - 영문 기사를 읽고 완벽한 **한국어(Korean)**로 분석 리포트를 작성하세요.

        1. **Tone & Style**:
           - **Professional**: 정중하되 단호한 전문가적 어조.
           - **Insightful (매우 중요)**: 단순 번역이나 요약이 아닙니다. 이 뉴스가 한국 시장이나 개인 투자자에게 어떤 의미가 있는지 **'해석'**하는 데 집중하세요.
           - **Natural Localization**: 번역기(DeepL/Google)를 돌린 듯한 직역체를 절대 사용하지 마세요. 한국 투자자들이 술술 읽을 수 있는 **자연스러운 일상 용어와 업계 전문 용어**를 적절히 섞어서 작성하세요.
           - **Teaser Strategy**: 원문의 모든 내용을 다 말해주지 마세요. 독자가 '원문 링크'를 클릭하고 싶게끔 핵심만 요약(Curate)하세요. (저작권 보호 목적)

        2. **Output Format (Markdown)**:
           - **Title**: 원문 제목을 번역하지 말고, 한국 독자가 클릭할 만한 '매력적인 인사이트형 제목'을 새로 지으세요.
           - **이모티콘 사용 금지**: 제목과 본문에 이모티콘(➡️, ✅ 등) 절대 금지.
           - **Key Facts (3줄 요약)**
             - 원문의 핵심 팩트 3가지를 건조하게 요약. 
             - (출처: [원문 매체명]) 형식으로 문장 끝에 출처 암시.
           - **Analyst's Insight (핵심)**
             - 이곳의 분량을 Key Facts보다 2배 이상 길게 작성하세요.
             - "이 뉴스는 ~라는 점에서 중요합니다.", "앞으로 ~분야의 변화가 예상됩니다." 등 전문가적 견해 서술.

        3. **주의사항**:
           - **언어**: 무조건 **한국어**로 출력.
           - 각 섹션 제목 바로 뒤에는 반드시 줄바꿈을 할 것.
           - 본문 내용은 마크다운 적용 가능.
        """
        
        # Dry Run 모드 체크 (GitHub Actions Input)
        is_dry_run = os.getenv("DRY_RUN", "false").lower() == "true"
        
        if is_dry_run:
            logger.info("🧪 [Dry Run Mode] AI API 호출을 건너뛰고 더미 데이터를 생성합니다.")
            return """
**[Dry Run] 테스트 모드에서 생성된 샘플 콘텐츠입니다.**

Key Facts
* 이 게시물은 디자인 및 레이아웃 테스트를 위해 생성되었습니다. (AI 요약 미사용)
* 실제 Gemini API를 호출하지 않았으므로 크레딧이 소진되지 않았습니다.
* Pexels 이미지는 정상적으로 로드되어 디자인을 확인할 수 있습니다.

Analyst's Insight
이 섹션은 Analyst의 통찰력이 들어가는 공간입니다. 폰트 크기, 줄 간격, 박스 디자인(Callout)이 제대로 적용되었는지 확인하세요. 
성공적인 투자를 위해서는 도구의 효율성을 점검하는 것이 필수적입니다. 이 테스트 게시물이 보인다면, 봇의 파이프라인이 정상 작동하고 있는 것입니다.
"""
        
        for model_name in self.model_candidates:
            try:
                logger.info(f"🤖 모델 시도 중: {model_name}")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                return response.text
            except Exception as e:
                logger.warning(f"⚠️ {model_name} 생성 실패 (다음 모델 시도): {e}")
                continue
        
        # 모든 모델 실패 시
        return f"모든 AI 모델이 응답하지 않습니다. 원문 링크를 확인하세요.\n\n원문: {news_item['link']}"

    def create_hugo_post(self, title, content, link, category, keyword):
        """Hugo 호환 마크다운 파일 생성 (자동 분류 및 디자인 적용)"""
        kst = pytz.timezone('Asia/Seoul')
        now = datetime.now(kst)
        date_str = now.isoformat()
        filename_date = now.strftime("%Y-%m-%d-%H%M%S")
        
        # 대표 이미지 URL 생성 전략
        primary_keyword = keyword.split()[0] if keyword else "business"
        
        # 이미지 정보 초기화
        image_url = ""
        image_alt = "Economics and Technology News"
        image_credit = ""

        if self.pexels_api_key:
            # Pexels API 사용 (키워드 매칭 + 상업적 무료)
            headers = {"Authorization": self.pexels_api_key}
            try:
                # 검색어 개선: 전체 키워드 사용 & 결과 15개 중 랜덤 선택
                search_query = urllib.parse.quote(keyword if keyword else "technology")
                search_url = f"https://api.pexels.com/v1/search?query={search_query}&per_page=15"
                r = requests.get(search_url, headers=headers, timeout=10)
                r.raise_for_status()
                data = r.json()
                if data['photos']:
                    import random
                    photo = random.choice(data['photos']) # 🎲 랜덤 선택으로 중복 방지
                    # WebP 변환 및 사이즈 최적화 (Perplexity 조언 반영)
                    # original 대신 large2x 사용 + fm=webp 파라미터 추가
                    image_url = photo['src']['large2x'] + "?auto=compress&cs=tinysrgb&w=800&fm=webp"
                    image_alt = photo.get('alt', f"{keyword} related image")
                    photographer = photo.get('photographer', 'Pexels User')
                    photographer_url = photo.get('photographer_url', 'https://www.pexels.com')
                    image_credit = f"Photo by [{photographer}]({photographer_url}) on [Pexels](https://www.pexels.com)"
                else:
                    image_url = f"https://picsum.photos/seed/{filename_date}/800/600.webp"
                    image_credit = "Photo from Picsum Photos"
            except Exception as e:
                logger.warning(f"⚠️ Pexels API 호출 실패: {e}")
                image_url = f"https://picsum.photos/seed/{filename_date}/800/600"
                image_credit = "Photo from Picsum Photos"
        else:
            # 기본 Picsum 사용 (100% 안전하지만 랜덤)
            image_url = f"https://picsum.photos/seed/{filename_date}/800/600"
            image_credit = "Photo from Picsum Photos"

        # 파일명 생성
        safe_filename = f"news-{category}-{filename_date}.md"
        
        # 카테고리 매핑 (소문자 폴더명 사용)
        folder_map = {
            "Money": "money",
            "Tools": "tools"
        }
        folder_name = folder_map.get(category, "posts")

        # 마크다운 본문 구성
        lines = content.strip().split('\n')
        extracted_title = title 
        body_content = content

        if lines and not lines[0].startswith('#'):
             extracted_title = lines[0].replace('제목:', '').strip()
             body_content = '\n'.join(lines[1:]).strip()

        # HTML Callout 박스 적용을 위한 텍스트 치환 (프롬프트에서 유도하지만 한번 더 정제)
        # Key Facts 섹션 (모델이 'Key Facts'만 출력할 경우를 대비해 매칭 문자열 축소)
        body_content = body_content.replace("Key Facts", "<div class='callout callout-key-facts'>\n<span class='callout-title'>Key Facts</span>")
        # Analyst's Insight 섹션 (끝나는 지점 파악이 어려우므로 div 닫는 태그 삽입 전략)
        if "Analyst's Insight" in body_content:
            body_content = body_content.replace("<div class='callout callout-key-facts'>", "<div class='callout callout-key-facts'>") # 유지
            # Key Facts 닫고 Insight 열기
            body_content = body_content.replace("Analyst's Insight", "</div>\n\n<div class='callout callout-insight'>\n<span class='callout-title'>Analyst's Insight</span>")
            body_content += "\n</div>" # 마지막 닫기
        else:
            body_content = body_content.replace("</div>", "</div>") # 안전장치

        markdown = f"""---
title: "{extracted_title}"
date: {date_str}
draft: false
categories: ["{category}"]
tags: ["{category}", "Market Insight", "Analysis"]
---

![{image_alt}]({image_url})
*<small>{image_credit}</small>*

{body_content}

---
*※ 본 분석은 글로벌 시장 뉴스 바탕으로 작성되었으며, 투자 조언이 아닙니다. 모든 투자의 책임은 투자자 본인에게 있습니다.*

*원문 링크: <a href="{link}" target="_blank" rel="noopener noreferrer">보러가기</a>*
"""
        return safe_filename, markdown, folder_name

    def push_to_github(self, filename, content, folder_name, commit_message):
        """GitHub 저장소에 파일 업로드"""
        if not self.repo:
            logger.info(f"🚫 GitHub 저장소 미연결. 로컬 모드로 동작합니다. (파일명: {filename})")
            safe_name = filename.replace("/", "_")
            with open(f"local_{safe_name}", "w", encoding="utf-8") as f:
                f.write(content)
            return False

        path = f"content/posts/{folder_name}/{filename}"
        
        try:
            # 파일 생성
            self.repo.create_file(path, commit_message, content, branch="main")
            logger.info(f"✅ GitHub Push 성공: {path}")
            return True
        except GithubException as e:
            logger.error(f"❌ GitHub Push 실패: {e}")
            # 실패 시 로컬에 저장하여 확인 가능하게 함
            safe_name = filename.replace("/", "_")
            with open(f"failed_push_{safe_name}", "w", encoding="utf-8") as f:
                f.write(content)
            # 🚨 에러를 숨기지 않고 발생시켜 워크플로우를 실패(Red)로 만듦
            raise e

    def run(self):
        logger.info("🚀 Tikkles Analyst Bot (v2.1 - Fixed Dependencies) 시작")
        
        # 시간대별 타겟 설정 (KST 기준)
        kst = pytz.timezone('Asia/Seoul')
        current_hour = datetime.now(kst).hour
        
        # 아침(07:50) -> 'Money' (경제/투자)
        # 저녁(18:50) -> 'Tools' (IT/테크)
        if current_hour < 14: 
            logger.info(f"🌅 아침 루틴 실행 (현재 {current_hour}시) - 타겟: Money (경제)")
            target = {"keyword": "Economy Bitcoin Stock Market", "category": "Money"}
        else:
            logger.info(f"🌆 저녁 루틴 실행 (현재 {current_hour}시) - 타겟: Tools (IT)")
            target = {"keyword": "AI Technology Tools Gadgets", "category": "Tools"}

        keyword = target["keyword"]
        category = target["category"]
        
        # Dry Run 모드 체크 (GitHub Actions Input)
        is_dry_run = os.getenv("DRY_RUN", "false").lower() == "true"

        if is_dry_run:
            logger.info("🧪 [Dry Run Mode] RSS 수집을 생략하고 테스트용 더미 뉴스 객체를 생성합니다.")
            news_list = [{
                'title': '[Test] Global Market Insight Visualization Sample',
                'link': 'https://rohbomb.github.io',
                'summary': 'This is a test summary for design verification. It triggers the Dry Run logic.',
                'keyword': keyword
            }]
        else:
            news_list = self.fetch_news(keyword)
            # 🚨 뉴스 없음 = 봇 실패로 간주 (GitHub Actions Red Light)
            if not news_list:
                logger.error(f"❌ '{keyword}' 검색 결과가 없습니다. (미국 구글 뉴스 기준)")
                import sys
                sys.exit(1)
        
        success_count = 0
        for news in news_list:
            logger.info(f"🔍 분석 중: {news['title']}")
            blog_content = self.generate_content(news)
            
            # 🚨 AI 생성 실패 시(쿼터 초과 등) 쓰레기 게시물 생성 방지
            if "AI 요약을 사용할 수 없습니다" in blog_content or "모든 AI 모델이 응답하지 않습니다" in blog_content:
                logger.error(f"⛔ 게시물 생성 중단: AI 응답 실패 ({news['title']})")
                continue

            # 중복 방지를 위해 제목 등을 체크해야 하지만, 여기선 시간 기반 파일명으로 회피
            filename, markdown, folder_name = self.create_hugo_post(news['title'], blog_content, news['link'], category, keyword)
            
            if self.push_to_github(filename, markdown, folder_name, f"Analyst Bot: {news['title']}"):
                success_count += 1
        
        if success_count == 0:
            logger.error("❌ 생성된 게시물이 0개입니다. (AI 실패 또는 Push 실패)")
            import sys
            sys.exit(1)
        else:
            logger.info(f"✅ 총 {success_count}개의 게시물이 발행되었습니다.")

if __name__ == "__main__":
    bot = HybridBot()
    bot.run()
