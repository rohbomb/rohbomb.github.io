# 기존 포스팅 커버 이미지 패치 스크립트
# 본문 첫번째 이미지 → frontmatter cover.image 로 자동 등록
# hiddenInSingle: true → 포스팅 본문 상단엔 안뜨고 리스트 카드에만 썸네일로 표시

$files = Get-ChildItem -Path "content/ko/post" -Filter "*.md" -Recurse
$patched = 0
$skipped = 0

foreach ($file in $files) {
    $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8
    
    # 이미 cover: 있으면 스킵
    if ($content -match '(?m)^cover:') {
        $skipped++
        Write-Host "SKIP (cover exists): $($file.Name)"
        continue
    }
    
    # 본문 첫번째 이미지 URL 추출 (https:// 로 시작하는 것만)
    if ($content -match '!\[.*?\]\((https?://[^\s\)]+)\)') {
        $imageUrl = $Matches[1]
        
        # 프론트매터 닫는 --- 바로 앞에 cover 삽입
        $coverBlock = "cover:`n  image: `"$imageUrl`"`n  alt: `"Post cover`"`n  hiddenInSingle: true`n"
        $newContent = $content -replace '(---\s*\n)(?!.*---)', { "$($_.Value)" }
        # 두번째 --- 바로 앞에 삽입
        $newContent = [regex]::Replace($content, '(?s)(---\n)(.*?)(---\n)', {
            param($m)
            $m.Groups[1].Value + $m.Groups[2].Value + $coverBlock + $m.Groups[3].Value
        }, [System.Text.RegularExpressions.RegexOptions]::Singleline)
        
        [System.IO.File]::WriteAllText($file.FullName, $newContent, [System.Text.Encoding]::UTF8)
        $patched++
        Write-Host "PATCHED: $($file.Name)"
    } else {
        $skipped++
        Write-Host "SKIP (no image): $($file.Name)"
    }
}

Write-Host ""
Write-Host "완료! 패치: $patched 개 / 스킵: $skipped 개"
