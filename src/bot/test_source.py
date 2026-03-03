import os
import urllib.parse
import feedparser
import requests
import random
from dotenv import load_dotenv

# 로컬 테스트용 환경변수 로드
load_dotenv()

def test_rss_fetch(keyword="IT 인공지능 툴"):
    print(f"\n📡 Testing RSS Fetch for '{keyword}'...")
    encoded_keyword = urllib.parse.quote(keyword)
    # when:1d 추가된 URL
    rss_url = f"https://news.google.com/rss/search?q={encoded_keyword}+when:1d&hl=ko&gl=KR&ceid=KR:ko"
    print(f"   URL: {rss_url}")
    
    feed = feedparser.parse(rss_url)
    if feed.entries:
        print(f"✅ Fetched {len(feed.entries)} items.")
        print(f"   Top 1: {feed.entries[0].title}")
        print(f"   Link:  {feed.entries[0].link}")
        print(f"   Date:  {feed.entries[0].published}")
        
        # 중복 방지 시뮬레이션
        print("   --- Duplication Check ---")
        for i, entry in enumerate(feed.entries[:3]):
            print(f"   [{i+1}] {entry.title}")
    else:
        print("❌ No entries found.")

def test_pexels_image(keyword="technology"):
    print(f"\n🖼️ Testing Pexels Search for '{keyword}'...")
    api_key = os.getenv("PEXELS_API_KEY")
    if not api_key:
        print("❌ Skipped: No PEXELS_API_KEY found.")
        return

    headers = {"Authorization": api_key}
    search_query = urllib.parse.quote(keyword)
    # per_page=15 확인
    search_url = f"https://api.pexels.com/v1/search?query={search_query}&per_page=15"
    
    try:
        r = requests.get(search_url, headers=headers, timeout=10)
        data = r.json()
        if data.get('photos'):
            print(f"✅ Found {len(data['photos'])} photos.")
            # Random choice verification
            photo1 = random.choice(data['photos'])
            photo2 = random.choice(data['photos'])
            print(f"   Random Check 1: ID {photo1['id']} - {photo1['photographer']}")
            print(f"   Random Check 2: ID {photo2['id']} - {photo2['photographer']}")
            if photo1['id'] != photo2['id']:
                print("   ✨ Randomization works! (Different IDs selected)")
            else:
                print("   ⚠️ Same ID selected (Could be unlucky or logic issue)")
        else:
            print("❌ No photos found.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Starting Logic Verification (No Quota Usage)")
    test_rss_fetch("경제 전망")
    test_pexels_image("money")
    print("\n-------------------------------------------")
    test_rss_fetch("IT 인공지능 툴")
    test_pexels_image("technology")
