import os
import sys
import yaml
import logging
from datetime import datetime
import pytz
from dotenv import load_dotenv
import feedparser
import urllib.parse
from github import Github

# 내부 모듈 임포트
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from modules.ai_handler import AIHandler
from modules.hugo_builder import HugoBuilder

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("HybridBot")

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def get_target_category(config):
    kst = pytz.timezone('Asia/Seoul')
    now = datetime.now(kst)
    hour = now.hour
    
    # 오전 7~10시 사이면 Money (오전 뉴스), 그 외엔 Tools (오후 뉴스)
    if 7 <= hour <= 10:
        return config['rss']['sources']['money']['category'], config['rss']['sources']['money']['keyword']
    else:
        return config['rss']['sources']['tools']['category'], config['rss']['sources']['tools']['keyword']

def fetch_rss_news(keyword):
    logger.info(f"📰 구글 뉴스 (영문) 검색 시작. 키워드: {keyword}")
    encoded_keyword = urllib.parse.quote(keyword)
    url = f"https://news.google.com/rss/search?q={encoded_keyword}&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(url)
    
    if not feed.entries:
        logger.warning("검색된 뉴스가 없습니다.")
        return []
    
    news_list = []
    # 최신 뉴스 1개만 추출
    for entry in feed.entries[:1]:
        news_list.append({
            'title': entry.title,
            'link': entry.link,
            'summary': entry.description if hasattr(entry, 'description') else "No Summary",
            'keyword': keyword
        })
    return news_list

def push_to_github(safe_filename, markdown_content, folder_name, config):
    is_dry_run = os.getenv("DRY_RUN", "false").lower() == "true"
    if is_dry_run:
        # 로컬 저장
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        file_path = os.path.join(root_dir, safe_filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        logger.info(f"💾 [Dry Run] 포스트 로컬 저장 완료: {file_path}")
        return True

    github_token = os.getenv("GH_PAT")
    if not github_token:
        logger.error("❌ GitHub 토큰(GH_PAT)이 없습니다.")
        return False

    repo_name = config['github']['target_repo_name']
    path = f"content/posts/{folder_name}/{safe_filename}"
    commit_message = f"Analyst Bot: Add post {safe_filename} (V3.0)"
    
    try:
        g = Github(github_token)
        repo = g.get_repo(repo_name)
        repo.create_file(path, commit_message, markdown_content, branch="main")
        logger.info(f"✅ GitHub {repo_name} 저장소에 파일 푸시 성공: {path}")
        return True
    except Exception as e:
        logger.error(f"❌ GitHub 푸시 실패 (Exception): {e}")
        import sys
        sys.exit(1)

def main():
    load_dotenv()
    config = load_config()
    category, keyword = get_target_category(config)
    
    logger.info(f"🚀 Tikkles Analyst Bot (v3.0 - Modular JSON Architecture) 시작")
    logger.info(f"🎯 타겟 카테고리: {category} | 키워드: {keyword}")

    is_dry_run = os.getenv("DRY_RUN", "false").lower() == "true"
    if is_dry_run:
        logger.info("🧪 [Dry Run Mode] RSS 수집을 생략하고 테스트용 더미 객체를 생성합니다.")
        news_list = [{
            "title": "Dummy AI News for V3.0 Testing",
            "link": "https://example.com/dummy",
            "summary": "This is a dummy news summary to verify the new JSON pipeline.",
            "keyword": keyword
        }]
    else:
        news_list = fetch_rss_news(keyword)

    if not news_list:
        logger.warning("처리할 뉴스가 없습니다.")
        return

    ai_handler = AIHandler(api_key=os.getenv("LLM_API_KEY"))
    hugo_builder = HugoBuilder(pexels_api_key=os.getenv("PEXELS_API_KEY"))

    for news in news_list:
        logger.info(f"📝 1단계: 뉴스 수집 완료 - {news['title']}")
        
        # 2단계: AI 분석 (JSON 강제화 획득)
        ai_json = ai_handler.generate_content(news)
        if not ai_json:
            logger.error("❌ AI 분석 실패 또는 JSON 파싱 오류")
            continue
            
        logger.info("🧱 2단계: JSON 구조화 분석 완료")
        
        # 3단계: Hugo 마크다운 조립
        safe_filename, markdown_content, folder_name = hugo_builder.create_post(ai_json, news['link'], category, keyword)
        logger.info("📄 3단계: Hugo Markdown 템플릿 조립 완료")
        
        # 4단계: 배포 (또는 로컬 저장)
        push_to_github(safe_filename, markdown_content, folder_name, config)

if __name__ == "__main__":
    main()
