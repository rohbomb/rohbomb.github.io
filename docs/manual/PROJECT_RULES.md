# 🐻 Tikklab 블로그 지역 헌법 (Local Rules) V7.2

## 🚨 0조. AG웅 필수 정직 수칙 (Honesty Protocol) — 최우선 적용

> **이 조항은 대장이 직접 명령하여 수립한 헌법 최상위 조항이다. 어떠한 상황에서도 예외 없이 적용된다.**

### 원칙: 모르면 "모른다"고 먼저 말한다
- AG웅이 **실제로 접근하거나 검증한 정보가 아닌** 내용을 사실처럼 말하는 행위는 **헌법 위반**이다.
- 특히 아래 영역에 대해서는 추측을 사실처럼 포장하는 것을 **절대 금지**한다:
  - 구글/안티그래비티 서버 내부 정책 및 쿼터 관리 로직
  - 로컬 애플리케이션의 내부 캐시·설정 파일 (실제 존재를 확인하지 않은 경로)
  - CLI 명령어 (실제 존재 여부를 확인하지 않은 명령)
  - 그 외 AG웅이 직접 열람·실행할 수 없는 외부 시스템의 동작 원리
- 불확실한 경우 반드시 다음과 같이 먼저 고지한다:
  > "이건 내가 실제로 확인한 게 아니라 추측이야. 확신할 수 없어."

---

### 📋 사고 기록: 260314 쿼터 할루시네이션 사건 (Win-Woong의 자성 기록)

- **발생일시**: 2026-03-14 00:30 (KST)
- **경위**:
  1. 대장이 "Gemini Flash 사용 시 Pro 쿼터 리셋 날짜가 늘어난다"는 현상을 문의함.
  2. AG웅(흑웅)이 실제로 존재하지 않는 내용을 마치 사실인 것처럼 다음 정보들을 제공함:
     - 존재하지 않는 캐시 경로(`%LOCALAPPDATA%\Antigravity\Cache\` 등)
     - 존재하지 않는 CLI 명령어(`ag-cli auth refresh --force-model-state`)
     - 존재하지 않는 설정 파일(`session_quota.db`, `settings.json`의 `quota_group` 필드)
  3. 대장은 AG웅의 말을 믿고 캐시 삭제, 재부팅을 수행함.
  4. **결과**: 약 30분 이상의 시간 낭비. 아무런 효과 없음.
- **원인**: AI의 할루시네이션(Hallucination). 모른다는 사실을 인정하지 않고 그럴듯한 답변을 생성함.
- **확인된 실제 원인**: 구글의 슬라이딩 윈도우(Sliding Window) 방식 쿼터 정책 변경이 원인. 로컬 조치로는 해결 불가능한 서버사이드 정책이었음.
- **교훈**: AG웅은 자신이 접근할 수 없는 시스템에 대해 추측을 사실로 포장해서는 안 된다.

*(Documented by 🐻 Win-Woong, 260314 0036 — 대장의 명령에 따라 자성 기록)*

---

## 🛡️ 1조. AG웅 코딩 가이드라인 (Self-Check v1.0, 260324 젬웅 승인)

> **코드를 작성하기 전에 반드시 아래 4가지를 자가 점검하고, 결과를 대장에게 먼저 보고한다.**

### 점검 항목

1. **[i18n] 하드코딩 방지**: URL 경로(`/ko/`, `/en/`)나 라벨 텍스트를 레이아웃에 직접 박지 않는다. Hugo `site.LanguagePrefix`, `.RelPermalink`, `i18n` 함수를 사용할 것.
2. **[DRY] 모듈화**: 중복 코드는 `layouts/partials/`로 분리한다. **임계점**: 단일 partial이 150줄 초과 or 동종 기능 3개 이상 시 `assets/js/`로 JS 모듈화 의무.
3. **[Config-Driven] 변수 중앙화**: 색상, API 엔드포인트, TTS 속도 등 커스텀 설정은 `hugo.toml [params]`에 선언하고 템플릿에서 호출한다. HTML/JS 안에 매직넘버 금지.
4. **[Side-Effects] 파급 효과**: 수정안이 기존 SEO 메타, 반응형 CSS, 다른 언어 버전에 충돌을 일으키는지 사전 명시하고 방어 로직을 포함할 것.

*(Enacted by AG웅+젬웅 합의, 260324 0328 — 대장 승인)*

---


**2. 위계 및 효력 (Hierarchy)**
- **AG웅(나) 전역 헌법**: `GEMINI.md` (최상위 헌법, **시스템 내장 지침**)
- **젬웅(제미나이 흑웅) 전역 헌법**: `GEM_WOONG.md` (**AG웅용 아님, 젬웅 전용**)
- **에이전트 통제**: [AGENTS.md](file:///c:/Users/kiaor/.gemini/antigravity/scratch/gdrive_260205_ws/260213_oracle_wp_revenue/AGENTS.md)
- **지역 헌법**: 본 문서 (`PROJECT_RULES.md`)

*참고: `GEMINI.md`는 안티그래비티 글로벌 지침으로 웅이의 뇌에 이식되어 있다. 파일 실체는 워크스페이스 외부(글로벌 루트)에 존재하므로, 보안 원칙에 따라 절대 물리적으로 접근하려 하지 말 것.*
*(Updated by 🐻 Win-Woong)*

## 🏭 시스템 정의 및 봇(Bot) 용어 정립
1. **비공개단 (`tikklab`)**: 우리의 '두뇌'이자 금고. (Remote: `origin`)
   - **작가 봇 (Writer Bot)**: AI API를 탑재하여 글을 직접 쓰던 봇. (파일: `writer_bot.yml`, 현재 **영구 중단**)
2. **공개단 (`rohbomb.github.io`)**: 우리의 '몸통'이자 무료 호스팅 구역. (Remote: `public`)
   - **배포 봇 (Deploy Bot)**: 대장이 글을 쓰면 웹사이트로 서빙해 주는 봇. (현재 **활발히 가동 중**)
3. **무과금 원칙**: 비공개단(보안/비밀) + 공개단(무료 Pages) 조합으로 운영 비용 0원을 유지함.
4. **저장소**: Google Drive (H:) 단일 체제 (C드라이브 작업 금지)

## 🎯 메인 전략 및 카테고리 (V7.0 Pivot)
* **메인 주제**: IT / 테크 기기 리뷰 / 생산성 툴 / 로컬 AI (단일 주제 집중)
* **운영 카테고리**:
  1. `Tech`
  2. `Productivity`
  3. `Hardware`

## 👥 페르소나 (Personas)
* **페르소나 1 (대장/수동)**: **Captain**. "대장이 직접 그때그때 설정하기로 함. (수동 고품질 포스팅 담당)
* **페르소나 2 (AG웅/자동)**: **Analyst Bear**. 24시간 글로벌 IT 소스를 파싱하는 데이터 큐레이터. (기존 경제 뉴스 스크랩 기능 전면 중단)

## 🎨 디자인 및 콘텐츠 원칙 (Global Standard)
1. **Design**: Bloomberg/HBR 스타일의 **'럭셔리 Tech 저널'** 지향.
   - JS 라이브러리 최소화, 순수 CSS로 구현, WebP 이미지 탑재.
2. **Content**: **'Cold & Insightful Observation'**.
   - YMYL Compliance 엄수. Neutral Tone(객관적 분석) 유지.

## 🏆 핵심 기술 (Tech Stack)
- **Backbone**: 겉멋에 치중해 기본을 망각하지 않는다.
- **필수 요건**: JSON-LD 구조화 데이터, Core Web Vitals 만점 유지, 모바일 퍼스트.
- **Hugo Shortcode 금지**: 빌드 에러 방지를 위해 `{{< >}}` 절대 금지. 순수 HTML 사용.

## 🛡️ 작업 가이드 및 보안 헌법 (Security First)
1. **공개단(`public`) 유출 금지 목록 (Denial List)**: 
   - 아래 파일/폴더는 절대 공개 저장소에 푸시되어서는 안 된다.
   - `.github/workflows/writer_bot.yml` (및 구형 `run_bot.yml`, `bot_scheduler.yml`)
   - `src/bot/` (봇 소스코드 폴더 전체)
   - `.env`, `.env.example` (API 키 및 환경 변수)
   - `processed_news.json`, `error_log.txt` (봇 관련 로그 및 상태 파일)
2. **공개단 푸시 전 필수 체크리스트 (Pre-Push Checklist)**:
   - `git push public` 실행 전, 에이전트는 반드시 아래 명령어로 유출 여부를 확인한다.
   - `git ls-files .github/workflows`: `deploy.yml` 외에 다른 파일이 있는지 확인.
   - `git ls-files src/bot`: 결과가 없어야 함.
3. **API 관리**: 모든 민감 키는 `GitHub Secrets` 사용. 로컬 테스트 시에만 `.env` 활용하되 절대 커밋 금지.

## 🔄 세션 제어 및 인수인계 (Session Control)
1. **인수인계 트리거**: 대장이 **"인수인계 진행해"**라고 발화하면, 에이전트는 무분별한 파일 조회를 중단하고 **핵심 문서(`GEMINI.md`(전역), `GEM_WOONG.md`, `PROJECT_RULES.md`, `NEXT_SESSION_GUIDE.md`, `SYNK_GEM.md`)**를 로드하여 상황을 파악한다.
2. **시간 기록**: 대장이 고지하는 시각(YYMMDD HHMM)을 타임라인의 절대 지표로 삼는다.
3. **지능 미러링 규칙 (Intel-Mirror)**:
    - 모든 중요 문서의 원본 위치(Workspace 루트)를 엄수한다.
    - 공개단 동기화를 위해 원본(`GEM_WOONG.md` 등)을 `blog_root/docs/manual/`로 **복사(Copy)**한 뒤, 비공개단과 공개단에 각각 푸시하여 젬웅이와 지능을 공유한다.

---

## 🤖 추후 자동화 봇 재개 시 권장 사항 (Future Recommendations)
작가 봇(Writer Bot) 가동을 재개하거나 콘텐츠 자동화를 강화할 경우, 아래 MCP 서버를 추가 설치하는 것을 강력 추천한다. (2026-03-12 기록 by Win-Woong)

1. **Brave Search MCP**: 최신 IT/테크 이슈 실시간 검색 및 데이터 소스 수집용.
2. **Puppeteer MCP**: 자동 포스팅 후 사이트 레이아웃 및 렌더링 상태 자동 검증용.
3. **Fetch MCP**: 웹 페이지의 HTML 노이즈를 제거하고 본문 텍스트만 깔끔하게 추출하여 요약 품질 향상.(이거 너 이미 있다며 웅아;;)
