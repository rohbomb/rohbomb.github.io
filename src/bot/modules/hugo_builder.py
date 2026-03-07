import os
import re
import json
import logging
import requests
from datetime import datetime
import pytz
import random

logger = logging.getLogger("HybridBot")

class HugoBuilder:
    def __init__(self, pexels_api_key=None):
        self.pexels_api_key = pexels_api_key

    def _get_pexels_image(self, pexels_query, category):
        """Pexels API를 이용해 관련 이미지 URL과 저작권자 정보, SEO Alt 태그를 가져옴"""
        image_url = "https://picsum.photos/seed/{}/800/600".format(datetime.now().strftime("%Y-%m-%d-%H%M%S"))
        photographer = "Picsum Photos"
        photographer_url = "https://picsum.photos"
        
        image_alt = f"{pexels_query} trends & {category} analysis"
        image_credit = f"Photo from Picsum Photos"

        if not self.pexels_api_key:
            return image_url, image_alt, image_credit
            
        headers = {"Authorization": self.pexels_api_key}
        # 상위 5개 이미지를 가져와서 중복 방지를 위해 랜덤으로 1개 선택
        url = f"https://api.pexels.com/v1/search?query={pexels_query}&per_page=5"
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data.get('photos'):
                    photo = random.choice(data['photos'])
                    image_url = photo['src']['landscape']
                    photographer = photo['photographer']
                    photographer_url = photo['photographer_url']
                    
                    alt_desc = photo.get('alt', '')
                    if not alt_desc:
                        alt_desc = "Stock photo representing market trends"
                    
                    image_alt = f"{alt_desc} - {pexels_query} trends & {category} analysis"
                    image_credit = f"Photo by [{photographer}]({photographer_url}) on [Pexels](https://www.pexels.com)"
                    return image_url, image_alt, image_credit
        except Exception as e:
            logger.error(f"❌ Pexels API 호출 실패: {e}")
            
        return image_url, image_alt, image_credit

    def create_post(self, ai_json, link, category, keyword):
        """JSON 데이터를 받아 Hugo 마크다운 형식으로 조립"""
        kst = pytz.timezone('Asia/Seoul')
        now = datetime.now(kst)
        date_str = now.isoformat()
        
        folder_name = category.lower()
        safe_filename = f"news-{category}-{now.strftime('%Y-%m-%d-%H%M%S')}.md"
        
        # 제미나이가 생성해준 pexels_query 추출 (없으면 기본값)
        pexels_query = ai_json.get("pexels_query", "technology")
        
        # Pexels 이미지 가져오기
        is_dry_run = os.getenv("DRY_RUN", "false").lower() == "true"
        if is_dry_run and not self.pexels_api_key:
            image_url = f"https://picsum.photos/seed/{now.strftime('%Y%m%d%H%M%S')}/800/600"
            image_alt = f"Economics and Technology News"
            image_credit = f"Photo from Picsum Photos"
        else:
            image_url, image_alt, image_credit = self._get_pexels_image(pexels_query, category)

        # AI가 생성한 데이터 추출 (JSON 키 이름 확인)
        title = ai_json.get("title", "Market Update")
        # 따옴표/특수문자로 인한 프론트매터 파싱 에러 방지용 따옴표 이스케이프 제거
        safe_title = title.replace('"', '\\"').replace("\n", " ")
        key_facts = ai_json.get("key_facts", [])
        insight = ai_json.get("insight", "")
        # tags와 categories는 ai_json에서 직접 가져올 수도 있으나, 현재 create_post 인자로 받고 있음
        # seo_tags는 기존 로직 유지 (ai_json에서 가져와서 처리)
        seo_tags = ai_json.get("tags", []) # 프롬프트의 'tags' 키와 맞춤
        
        # 기본 카테고리 태그 보장 (소문자)
        cat_lower = category.lower()
        if cat_lower not in [t.lower() for t in seo_tags]:
            seo_tags.insert(0, cat_lower)
            
        tags_str = json.dumps([t.lower() for t in seo_tags], ensure_ascii=False)

        # Markdown 조립 (Key Facts)
        key_facts_md = ""
        for fact in key_facts:
            key_facts_md += f"* {fact}\n"

        markdown = f"""---
title: "{safe_title}"
date: {date_str}
draft: false
categories: ["{category}"]
tags: {tags_str}
---

![{image_alt}]({image_url})
*<small>{image_credit}</small>*

<div class='callout callout-key-facts'>
<span class='callout-title'>Key Facts</span>
{key_facts_md.strip()}
</div>

<div class='callout callout-insight'>
<span class='callout-title'>Analyst's Insight</span>
{insight.strip()}
</div>

---
*※ 본 분석은 글로벌 시장 뉴스 바탕으로 작성되었으며, 투자 조언이 아닙니다. 모든 투자의 책임은 투자자 본인에게 있습니다.*

*원문 링크: <a href="{link}" target="_blank" rel="noopener noreferrer">보러가기</a>*
"""
        return safe_filename, markdown, folder_name
