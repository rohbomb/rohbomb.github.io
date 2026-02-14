import os
import glob

# 설정
base_path = "content/posts"
target_strings = ["분석 중 오류가 발생했습니다", "[에러 메시지]"]

cleaned_count = 0

print("🔍 에러 게시물 검색 및 삭제 시작...")

for root, dirs, files in os.walk(base_path):
    for filename in files:
        if filename.endswith(".md"):
            filepath = os.path.join(root, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # 에러 문구 확인
                is_error = any(s in content for s in target_strings)
                
                if is_error:
                    print(f"🗑️ 삭제 중: {filepath}")
                    f.close() # 윈도우 파일 잠금 방지
                    os.remove(filepath)
                    cleaned_count += 1
            except Exception as e:
                print(f"⚠️ 파일 처리 실패 ({filename}): {e}")

print(f"✅ 총 {cleaned_count}개의 에러 게시물을 삭제했습니다.")
