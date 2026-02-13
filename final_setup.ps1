# Git 사용자 설정 (GitHub 익명 이메일 사용)
git config --global user.email "rohbomb@users.noreply.github.com"
git config --global user.name "rohbomb"

# 커밋 재시도
git commit -m "첫 블로그 세팅 완료"

# 원격 저장소 연결 (혹시 안 됐을 경우 대비)
# git remote add origin https://github.com/rohbomb/rohbomb.github.io.git
# 이미 되어있으면 에러 날 수 있으니 주석 처리하거나 무시

# 푸시
git push -u origin main

Write-Host "✅ 설정 완료! https://rohbomb.github.io 접속해보세요!"
