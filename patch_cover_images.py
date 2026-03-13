import os
import re

post_dir = r"content\ko\post"
patched = 0
skipped = 0

for fname in os.listdir(post_dir):
    if not fname.endswith(".md"):
        continue
    
    fpath = os.path.join(post_dir, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 이미 cover: 있으면 스킵
    if re.search(r'^cover:', content, re.MULTILINE):
        skipped += 1
        print(f"SKIP (cover exists): {fname}")
        continue
    
    # 본문 첫번째 https 이미지 URL 추출
    img_match = re.search(r'!\[.*?\]\((https?://[^\s)]+)\)', content)
    if not img_match:
        skipped += 1
        print(f"SKIP (no image): {fname}")
        continue
    
    image_url = img_match.group(1)
    
    # frontmatter 닫는 두번째 --- 앞에 cover 블록 삽입
    cover_block = f"cover:\n  image: \"{image_url}\"\n  alt: \"Post cover\"\n  hiddenInSingle: true\n"
    
    # 정규식으로 두번째 --- 앞에 삽입
    new_content = re.sub(
        r'(?s)(---\n)(.*?)(---\n)',
        lambda m: m.group(1) + m.group(2) + cover_block + m.group(3),
        content,
        count=1
    )
    
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    patched += 1
    print(f"PATCHED: {fname}")

print(f"\n완료! 패치: {patched}개 / 스킵: {skipped}개")
