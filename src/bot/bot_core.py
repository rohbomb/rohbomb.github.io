# 🤖 Tikkles Analyst Bot v2.7 (Dry Run API Isolation)
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
import json as sys_json # 🛠️ Fix: Use alias to avoid naming conflict

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
            if os.getenv("DRY_RUN", "false").lower() == "true":
                logger.info("🧪 [Dry Run] GH_PAT 누락 무시. 로컬 테스트를 진행합니다.")
                self.gh = None
                self.repo = None
            else:
                logger.error("❌ GH_PAT 환경변수가 없습니다.")
                raise ValueError("GitHub Token is missing")
        else:
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
                        processed_links = sys_json.load(f)
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
                        sys_json.dump(processed_links, f, ensure_ascii=False, indent=2)
                        
                    return [{
                        'title': entry.title,
                        'link': entry.link,
                        'published': entry.published,
                        'summary': getattr(entry, 'summary', ''),
                        'keyword': keyword
                    }]
            
            logger.info("ℹ️ 새로운 뉴스가 없습니다. (모두 처리됨)")
            return []
            
        except Exception as e:
            logger.error(f"❌ 뉴스 수집 실패 ({keyword}): {e}")
            return []

    def generate_content(self, news_item, category="Money"):
        """Gemini(Market Analyst)를 이용해 블로그 포스팅 작성 (Fallback 적용)"""
        if not self.model_candidates:
            return f"AI 요약을 사용할 수 없습니다.\n\n원문 링크: {news_item['link']}"

        disclaimer = ""
        if category == "Money":
            disclaimer = "\n\n※ 본 분석은 글로벌 시장 뉴스 바탕으로 작성되었으며, 투자 조언이 아닙니다. 모든 투자의 책임은 투자자 본인에게 있습니다."
            
        prompt = f"""
        당신은 20년 경력의 글로벌 매크로/기술 분석가 'Market Analyst Bear'입니다.
        아래 뉴스 기사를 냉철하고 객관적인 시각에서 분석하여 전문적인 리포트로 작성해 주세요.

        [뉴스 정보]
        키워드: {news_item['keyword']}
        제목(원문): {news_item['title']}
        링크: {news_item['link']}
        내용(원문): {news_item['summary']}

        [작성 규칙]
        0. **Role**: 당신은 글로벌 시장의 최신 트렌드를 한국 투자자에게 소개하는 'Market Analyst Bear'입니다.
           - 영문 기사를 읽고 완벽한 **한국어(Korean)**로 분석 리포트를 작성하세요.

        1. **Tone & Style (Critical/YMYL Compliance)**:
           - **Neutral Objective**: 독자(투자자, 직장인 등)를 직접 지칭하거나 부르지 마세요. (예: "투자자 여러분" 금지)
           - **Third-Person Perspective**: 모든 분석은 "시장 참여자", "산업계", "데이터" 등을 주체로 하여 제3자 관점에서 서술하세요. 1인칭 주관적 표현("제가 보기엔", "추천합니다")은 절대 금지합니다.
           - **Analysis over Advice**: 투자 조언이나 지시형 어투 대신 현상을 드라이하게 분석하는 어투를 사용하세요. 
             - "~하시길 권합니다" (X) -> "~로 분석됩니다", "~할 전망입니다" (O)
             - "~투자의 기회입니다" (X) -> "~의 성장 잠재력이 주목받고 있습니다" (O)
           - **Natural Localization**: 번역기 말투가 아닌 한국 금융 전문 저널(HBR, Bloomberg) 수준의 냉철하고 절제된 톤앤매너를 유지하세요.

        2. **Output Format (Markdown)**:
            - **Title**: 원문 제목을 번역하지 말고, 한국 독자가 클릭할 만한 '매력적인 인사이트형 제목'을 새로 지으세요. 출력 시 반드시 **제목: [생성한 제목]** 형식을 지켜주세요.
            - **이모티콘 사용 금지**: 제목과 본문에 이모티콘(➡️, ✅ 등) 절대 금지.
           - **Key Facts (3줄 요약)**
             - 원문의 핵심 팩트 3가지를 건조하게 요약. 
             - (출처: [원문 매체명]) 형식으로 문장 끝에 출처 암시.
           - **Data Visualization (필수 아님, 수치 데이터 존재 시)**
             - 뉴스 내용 중 주가, 매출액, 성장률 등 의미 있는 **수치 데이터**가 2개 이상 존재할 경우, 이를 한눈에 보기 쉽게 마크다운 **표(Table)**로 정리하세요.
             - 표의 제목을 간결하게 붙이고 본문(Key Facts 이후)에 자연스럽게 삽입하세요.
           - **Analyst's Insight (핵심)**
             - 이곳의 분량을 Key Facts보다 2배 이상 길게 작성하세요.
             - "이 뉴스는 ~라는 점에서 중요합니다.", "앞으로 ~분야의 변화가 예상됩니다." 등 전문가적 견해 서술.
           - **SEO_TAGS (필수)**
             - 본문 분석을 마친 후, 마크다운의 마지막 줄에 `SEO_TAGS:`로 시작하여 3~5개의 콤마(,)로 구분된 영문 소문자 태그를 출력하세요.
             - 태그는 다음의 [3단계 태그 시스템] 규칙을 엄격히 따릅니다:
               1. 핵심 타겟 키워드: 본문 내 실제 검색 수요가 높은 구체적 제품명/고유명사 (예: coinbase, nvidia)
               2. 기술/산업 카테고리: 해당 기술의 대분류 (예: fintech, ai, semiconductor)
               3. 사용자 의도: 독자가 정보를 찾는 목적 (예: investment, analysis, review)
             - 주의: `analysis`, `market insight` 등 식상한 범용 태그는 배제하고, 무조건 모두 **소문자(Lowercase)**로만 작성하세요.
             - 출력 예시: `SEO_TAGS: coinbase, fintech, earnings, investment`

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
                    # SEO 고도화: 기존 Pexels 설명에 검색 키워드(keyword)와 분석(analysis) 단어 조합
                    base_alt = photo.get('alt', f"{keyword} related image")
                    image_alt = f"{base_alt} - {keyword} trends & {category} analysis"
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

        if lines:
             import re
             # 정규표현식으로 '제목' 라벨 제거 패턴 정의
             # ^: 시작, [\*\#]*: 강조/헤더 기호, \s*: 공백, 제목: '제목' 문자열, \s*: 공백, [: ]*: 콜론 등, \s*: 공백
             title_pattern = re.compile(r'^[\*\#]*\s*제목\s*[:\.]?\s*[\*\#]*\s*', re.IGNORECASE)
             
             # 첫 줄부터 탐색하여 제목 라인 식별
             for i, line in enumerate(lines[:3]): # 상위 3줄까지만 탐색
                 clean_line = line.strip()
                 # '제목'으로 시작하거나, 패턴에 매칭되는 경우
                 if title_pattern.match(clean_line) or clean_line.startswith("title:"):
                     # 패턴 제거 후 제목 추출
                     extracted_title = title_pattern.sub('', clean_line)
                     # 끝부분의 불필요한 특수문자 제거 (** 등)
                     extracted_title = re.sub(r'[\*\#]+$', '', extracted_title).strip()
                     # 따옴표 제거
                     extracted_title = extracted_title.strip('"').strip("'")
                     
                     body_content = '\n'.join(lines[i+1:]).strip()
                     break
             else:
                 # '제목:' 라벨을 못 찾았을 경우, 첫 줄을 제목으로 간주하되 정제 시도
                 potential_title = lines[0].strip()
                 # 혹시라도 첫 줄에 '**' 같은 게 붙어있을 수 있으므로 제거
                 extracted_title = re.sub(r'^[\*\#]+|[\*\#]+$', '', potential_title).strip()
                 extracted_title = extracted_title.strip('"').strip("'")
                 
                 if len(extracted_title) > 5:
                     # 첫 줄이 제목 같으면 본문은 두 번째 줄부터
                     body_content = '\n'.join(lines[1:]).strip()
                 else:
                     # 첫 줄이 너무 짧으면(제목이 아닐 확률 높음), 원문 제목 유지하고 본문 전체 사용
                     extracted_title = title # 원문 제목 Fallback
                     body_content = content

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

        # SEO_TAGS 파싱 및 동적 프론트매터 적용
        # 정규식 패턴: 'SEO_TAGS:' 로 시작하고 뒷부분 텍스트 추출 (대소문자 무관)
        seo_tags_pattern = re.compile(r'^SEO_TAGS\s*:\s*(.+)$', re.IGNORECASE | re.MULTILINE)
        match = seo_tags_pattern.search(body_content)
        
        if match:
            # 매칭된 태그 문자열 가져오기 (예: "coinbase, fintech, investment")
            raw_tags = match.group(1).strip()
            # 쉼표 기준으로 나누고 앞뒤 공백 제거 후 소문자로 변환하여 리스트 생성
            tag_list = [tag.strip().lower() for tag in raw_tags.split(',')]
            # 카테고리 태그(Money/Tools)는 무조건 기본으로 포함
            if category.lower() not in tag_list:
                tag_list.insert(0, category)
            # 파이썬 리스트를 겹따옴표 처리된 JSON 배열 형태의 문자열로 변환
            import json
            tags_str = json.dumps(tag_list)
            
            # 본문에 남아있는 SEO_TAGS 라인을 깔끔하게 삭제하여 사용자에게 노출 방지
            body_content = seo_tags_pattern.sub('', body_content).strip()
        else:
            # 혹시라도 AI가 태그를 못 만들었을 때를 대비한 Fallback (이전 로직)
            if category == "Money":
                tags_str = f'["{category}", "market insight", "finance"]'
            else:
                tags_str = f'["{category}", "tech trends", "innovation"]'

        markdown = f"""---
title: "{extracted_title}"
date: {date_str}
draft: false
categories: ["{category}"]
tags: {tags_str}
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
        logger.info("🚀 Tikkles Analyst Bot (v2.7 - Dry Run API Isolation) 시작")
        
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
            
            if is_dry_run:
                logger.info("🧪 [Dry Run] AI API를 호출하지만 GitHub 푸시는 생략하고 로컬에 저장합니다.")
                blog_content = self.generate_content(news, category=category)
            else:
                blog_content = self.generate_content(news, category=category)
            
            # 🚨 AI 생성 실패 시(쿼터 초과 등) 쓰레기 게시물 생성 방지
            if not is_dry_run and ("AI 요약을 사용할 수 없습니다" in blog_content or "모든 AI 모델이 응답하지 않습니다" in blog_content):
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
