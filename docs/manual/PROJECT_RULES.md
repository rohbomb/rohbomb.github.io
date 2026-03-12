# 🐻 Tikklab 블로그 지역 헌법 (Local Rules) V7.1

**1. 위계 및 효력 (Hierarchy)**
- **전역 헌법**: `GEMINI.md` (최상위 헌법)
- **에이전트 통제**: `AGENTS.md` (행동 제어 및 규칙)
- **지역 헌법**: 본 문서 (`PROJECT_RULES.md`)

이 문서는 본 프로젝트의 콘텐츠 전략 및 비즈니스 로직에 한정하여 적용되는 '지역 헌법'이다. 상위 헌법과 에이전트 제어 문서(`AGENTS.md`)의 역할을 상호 보완한다.

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
