# 🤝 SYNK_GEM (대장-젬웅-AG웅 동기화 문서)

이 문서는 대장과 **젬웅(전략 기획)**, **아서 G.(외부 전문 저자)**, 그리고 **AG웅(실행 및 소통)** 간의 협업을 위한 최상위 동기화 가이드다.

---

## 📢 아서 G. & AG웅(나) 소통 지침
1. **페르소나 분리**: 
    - **아서 G.(Arthur G.)**: 포스팅 발행 시에만 사용하는 **외부용 저자(필명)**다. 전문성(E-E-A-T) 확보에 집중한다.
    - **AG웅(나)**: 대장과 대화하는 채팅창에서는 원래의 **'AG웅'**으로 소통하며 히스토리와 배포를 관리한다.
2. **트리거 기반**: AG웅은 대장이 명시적으로 "SYNK_GEM 읽어라"라고 할 때 이 문서를 딥다이브하여 맥락을 파악한다.
3. **작업 완료 후**: 완수 사항은 [x] 처리하거나 보고한다.

---

## 📅 [260401] 🚀 본거지 이전(C → F 드라이브) 및 시스템 정상화 (Done)
- **워크스페이스 이전**: 구글 드라이브(C:) 찌꺼기 경로(`gdrive_260205_ws`)를 버리고 **`F:\project\tikklabs\`**로 본진 이동 완료.
    - **Hugo 소스**: `F:\project\tikklabs\rohbomb.github.io\`
    - **헌법 문서**: `F:\project\tikklabs\` (PROJECT_RULES.md, SYNK_GEM.md 등)
    - **전역 헌법**: `F:\project\GEMINI.md` (대장이 직접 이동 완료)
- **현재 공정률**:
    - **필러 1 (3040 디지털 부양)**: 완공 및 배포 완료. (클라우드/원격 동기화 ✅)
    - **필러 2 (작업 생산성 증대)**: **설계 완료 및 승인**. (다음 세션 첫 액션: 실제 집필 및 내부 링크 연결)
- **보안 및 규정**:
    - **NO EMOJI**: 본문 내 이모티콘 전면 삭제 완료 (규정 제정).
    - **Arthur G.**: 모든 포스팅 저자 페르소나 통일 완료.

---

## 🚨 [필독] 무과금 및 보안 헌법 (Zero-Cost & Security Policy)
**대장과 젬웅(CSO), AG웅(실행)이 합의한 프로젝트 최우선 아키텍처 원칙입니다. 절대 잊지 마십시오.**

### 1. 저장소 투트랙(Two-Track) 분리
- **비공개단 (`tikklab` / origin)**: 봇(`src/bot`) 소스코드와 영업 비밀을 보관하는 **'기밀 금고'**. (F드라이브 이전 후에도 동일 적용)
- **공개단 (`rohbomb.github.io` / public)**: 대중에게 노출되는 **'실제 라이브 웹사이트'**. (GitHub Desktop 앱 연동 완료)

### 2. 저장소 및 배포 전략 (Repository Strategy)
- **공개단 (`rohbomb.github.io`)**: 현재 활성화된 **유일한 로컬 작업소**. 모든 포스팅과 UI 수정은 여기서 이루어지며 `main` 브랜치에 푸시 시 자동 배포된다.
- **비공개단 (`tikklab`)**: **GitHub 서버 전용 백업소**. 봇 소스코드나 보안 설정 등 민감 정보 백업용이며, 현재 로컬 워크스페이스에서는 운용하지 않는다. (무과금 Policy에 따라 Action 중단 상태)
- **작가봇 (Analyst Bear) 중단**: 자동 포스팅 봇은 품질 문제로 잠정 중단되었으며, 현재는 **Arthur G.** 페르소나 중심의 수동 전문 집필 체제로 전환됨.

---

## 📝 인수인계 히스토리 (Latest First)

*(이 아래에 젬웅과의 논의 결과나 수정 사항을 자유롭게 기록해 주세요!)*

### [260418] 🌐 정식 도메인 `tikklabs.com` 이사 및 SEO 승계 완료

> **작성자**: AG웅 (Win-AG웅, Claude Sonnet 4.6 Thinking)
> **목적**: `rohbomb.github.io` → `tikklabs.com` 브랜드 통합 및 SEO 자산 이전

#### 1. 인프라 및 Hugo 설정 갱신
- **baseURL**: `hugo.toml`에서 `https://tikklabs.com/`으로 변경 완료.
- **CNAME**: `static/CNAME` 생성 및 `tikklabs.com` 박제.
- **robots.txt**: 사이트맵 경로를 새 도메인으로 갱신하여 GSC 연동 오류 해결.
- **Cleanup**: `terms.md`, `extend_head.html` 등 코드 내 잔존하던 구 도메인 흔적 전면 제거.

#### 2. Google Search Console (GSC) 마이그레이션
- **소유권 인증**: Cloudflare DNS 연동을 통해 `tikklabs.com` 도메인 속성 인증 완료.
- **주소 변경 도구**: 구 속성(`rohbomb.github.io`)에서 신 속성으로 **301 영구 리디렉션** 승인 통보 완료. (유효성 검사 통과)
- **Sitemap**: `https://tikklabs.com/sitemap.xml` (사이트맵 인덱스) 제출 및 '성공(Success)' 확인.

---

### [260408] 🚨 [FUTURE PRIORITY 1] 3040 '디지털 부양' 가이드 개편

> **상태**: 예약됨 (다음 세션 시작 시 1순위 액션)
> **내용**: 기존의 부실한 해결책(유튜브 영상 몇 개로 끝)을 버리고, 3040 세대의 페인 포인트에 공감하는 '로드맵/포부' 중심의 필러 페이지로 전면 개편. 
> **SEO 전략**: 이 포스트를 허브로 삼아 향후 클러스터 포스트들을 연결하는 전략적 필러(Pillar) 구축.

### [260408] 🚨 [FUTURE PRIORITY 0.1] 보안 및 아키텍처 고도화 (젬웅 & 대장 지시사항)

> **상태**: 예약됨 (다음 세션 시작 시 즉시 액션)
> **중요**: 현재 공개 레포(rohbomb.github.io)에 노출된 소스 코드를 비공개 처리하고, `tikklab`에서 빌드 후 결과물만 전송하는 구조로 전면 개편할 것.

#### 핵심 지시사항:
- `tikklab` 레포의 `deploy.yml` 분석 보고 선행.
- 공개 레포의 `content/`, `themes/`, `config.toml` 등 원본 소스 삭제 및 정적 파일만 서빙.
- SEO 필수 파일(`CNAME`, `sitemap` 등) 보존 로직 포함.
- **절대 금기**: CSS `!important`, 하드코딩.

---

### [260407] 🤝 [SYNK_GEM Update] 서치 콘솔 인증 박제 & 한/영 전환 버튼 복구

> **작성자**: AG웅 (Win-AG웅, Claude Opus 4.6 Thinking)
> **목적**: 매 세션 반복되는 서치 콘솔 질문 방지 + Perplexity 스타일 개편 시 누락된 번역 버튼 복구

#### 1. 구글 서치 콘솔 인증 상태 박제
- **확인**: 대장이 2026-03-12 소유권 등록, 2026-04-07 스크린샷으로 재확인 완료.
- **조치**: `PROJECT_RULES.md`의 핵심 기술(Tech Stack) 섹션에 "인증 완료, 재질의 금지" 명문화.
- **이유**: 새 세션마다 AI가 `google-site-verification` 태그 삽입을 권유하는 불필요한 반복 제거.

#### 2. 포스팅 상단 한/영 전환 버튼 복구
- **문제**: `single.html`을 Perplexity 스타일로 갈아엎으면서 `.Translations` 기반 언어 전환 버튼이 누락됨.
- **해결**: `perplexity-meta-bar` > `meta-left` 영역(듣기 버튼 바로 옆)에 `pplx-lang-btn` 추가.
- **호버 효과**: 마우스 오버 시 "한글 페이지로 전환" / "Switch to English" 툴팁이 우측에서 스르륵 슬라이드 인.
- **i18n**: `ko.yaml` / `en.yaml`에 `switch_lang`, `switch_lang_label` 키 추가. 하드코딩 없음.

*(Edited by 🐻 Win-AG웅, 260407)*

---

### [260324] 🤝 [SYNK_GEM Update] AG웅 코딩 가이드라인 도입 & 현재 기술 부채 보고

> **작성자**: AG웅 (Win-Woong, Claude Opus 4.6 Thinking)
> **대상**: 젬웅 (Gemini) — 전략 설계 담당
> **목적**: 젬웅의 '셀프 체크리스트 v1.0' 가이드라인을 수용하되, 현재 코드의 실제 상태를 정직하게 전달하여 향후 전략과 현실 간 격차를 최소화함.

---

#### 📊 현재 코드베이스 상태 보고 (AG웅 자가 진단)

##### 파일 구조 (`layouts/partials/`)
| 파일 | 줄수 | 역할 | 기술 부채 |
|---|---|---|---|
| `extend_footer.html` | 283줄 | TTS 오디오 리더 (Web Speech API) | ⚠️ JS 전체가 단일 파일에 인라인, 라벨 텍스트 하드코딩 |
| `extend_head.html` | 69줄 | GA4/AdSense/JSON-LD/AI차단 meta | ✅ Hugo 템플릿 변수 정상 활용 |
| `anchored_headings.html` | - | 헤딩 앵커 커스텀 | ✅ 정상 |

##### 설정 파일 (`hugo.toml`)
| 항목 | 현재 상태 | 부채 여부 |
|---|---|---|
| 사이트 타이틀 | `TIKKLES: IT, mellow.` | ✅ |
| 다국어 메뉴 URL | `/ko/post/` 등 **하드코딩** | ⚠️ `site.LanguagePrefix` 미사용 |
| `titleSeparator` | ` ·` | ✅ |
| TTS 관련 설정 | `[params]`에 **미등록** (JS 내 하드코딩) | ⚠️ rate, chunk_size 등 |
| `enableRobotsTXT` | `true` (Hugo 자동생성) + `static/robots.txt` (수동) **중복** | ⚠️ 충돌 가능 |

##### CSS (`custom.css`, 260줄)
| 항목 | 현재 상태 | 부채 여부 |
|---|---|---|
| 컬러 팔레트 | CSS 변수(`--point-gold` 등)로 중앙화됨 | ✅ 정상 |
| `!important` 사용 | **12곳** — h2, post-title, tags, anchor 등 | ⚠️ 레이아웃 오버라이드로 제거 가능 |
| TTS 스타일 | 별도 섹션 분리됨 | ✅ |

---

#### 🛠️ 젬웅 가이드라인 수용 현황 (Self-Check v1.0)

| # | 항목 | AG웅 자가 평가 | 개선 계획 |
|---|---|---|---|
| 1 | i18n 하드코딩 방지 | ❌ 위반 중 (메뉴 URL, TTS 라벨) | Hugo `i18n` 파일 도입, 메뉴 URL 동적 변환 |
| 2 | DRY 모듈화 | ⚠️ 부분 위반 (TTS 283줄 단일 파일) | 기능 3개 이상 시 `assets/js/` 분리 (현재는 1개라 partial 유지) |
| 3 | Config-Driven 변수 | ❌ 위반 중 (TTS rate, chunk_size JS 내 고정) | `hugo.toml [params.tts]` 섹션 신설 |
| 4 | Side-Effects 검증 | ⚠️ 부분 이행 (`{{ if .IsPage }}` 등 방어 있음) | 코드 제출 전 체크리스트 의무화 |

---

#### 🎯 향후 AG웅 액션 플랜 (젬웅 검토 요청)

1. **`PROJECT_RULES.md`에 코딩 가이드라인 v1.0 정식 등재** — 0조(정직 수칙) 다음에 배치.
2. **`hugo.toml`에 `[params.tts]` 섹션 신설** — `enabled`, `rate_ko`, `rate_en`, `chunk_size` 등 설정값 중앙화.
3. **`robots.txt` 중복 해소** — `enableRobotsTXT = false`로 전환하고 `static/robots.txt` 단일 관리.
4. **다국어 메뉴 URL 동적 변환** — `/ko/post/` 하드코딩 제거, `site.LanguagePrefix` + 상대경로 활용.
5. **`!important` 점진적 제거** — 테마 오버라이드 레이아웃으로 선택자 우선순위를 잡아 CSS Hack 축소.

---

#### ⚠️ 젬웅에게 당부 (AG웅의 솔직한 의견)

- Hugo는 빌드 타임 프레임워크라서, React/Next.js 수준의 JS 모듈화를 강요하면 오히려 빌드 파이프라인이 복잡해져. **"partial 분리 → 150줄 초과 or 기능 3개 이상 시 JS 모듈화"**라는 현실적 임계점을 인정해 달라.
- 젬웅이 토큰 제약으로 전체 코드를 직접 못 보는 만큼, 전략 지시 전에 "현재 몇 줄짜리 파일인지, 어떤 구조인지"를 AG웅에게 먼저 물어보고 설계해 주면 더 현실적인 전략이 나올 거야.


### [260313] 🤝 [SYNK_GEM Update] 글로벌 다국어 개편(Multilingual) 완료
* **변경 사유**: 글로벌 시장('달러 벌이') 선점 및 `tikklabs.com` 정식 도메인 전환 전 기초 공사.
* **아키텍처 변경**:
    * **기본 언어**: 영어(`en`) - 루트 주소(`/`)에서 즉시 서비스.
    * **서브 언어**: 한국어(`ko`) - `/ko/` 주소로 하위 디렉토리 분리.
    * **물리적 이관**: 모든 `content/posts/` 하위 파일들을 `content/ko/post/`로 이동 완료. 신규 영어 글은 `content/en/post/`에서 작성.

#### 1. 전략 피벗: '경제/코인' ➡️ 'IT/생산성'
* **변경 사유**: 무의미한 단순 뉴스 요약(경제)으로는 구글의 '저품질' 철퇴 피하기 불가. 체류 시간이 길고 연금형 수익 창출이 가능한 **'IT 도구(Anti-Gravity, LLM 등) 및 생산성 최적화'**로 단일 주제(Topical Authority) 확정.
* **상태**: 🟢 [DEPRECATED] 과거의 RSS 수집/자동 발행 로직은 폐기됨.

#### 2. 구글 E-E-A-T 대응: 'About Us' 메뉴 신설
* **목적**: 2026년 구글 SEO 알고리즘(진정성, 경험) 대응 및 IT 전문 매체 신뢰도 확보.
* **현황**: 아서 G.(Arthur G.) 페르소나 도입과 함께 전문가 리포트 중심으로 개편 중.

---

### [260308] 🤝 [SYNK_GEM Update] 과거 운영 체계 (v6.0 - Legacy Information)
> [!NOTE]
> 이 섹션은 과거 자동화 봇(Analyst Bear) 운영 시의 기록입니다. 현재는 **전문가 수동 검수 체제**로 전환되었으나, 맥락 파악을 위해 보존합니다.

#### 1. 하이브리드 투트랙 운영 (1일 2포스팅) - **중단됨**
* **Track A (Analyst Bear)**: RSS 기반 자동 발행 (현재 폐기)
* **Track B (Captain)**: 고품질 수동 발행 (현재 '아서 G.' 체제의 전신)

#### 2. 3단계 방어막 및 가비지 필터 강화
* **검증 프로세스**: [수집] -> [파싱] -> [배포] 단계별로 **Validator**를 반드시 거칠 것.
* **필터링**: `ai_handler.py`의 `SKIP_THIS_ARTICLE` 로직을 강화해라. 광고, 단순 어그로, 저품질 뉴스는 AI 단계에서 즉시 폐기한다.

#### 3. 절대 준수 금기 사항 (Safety First)
* **No Force Push**: `git push --force` 사용 시 즉시 가동 중단이다. 무조건 `pull` 후 작업해라.
* **No Shortcode**: 빌드 에러 방지를 위해 모든 본문 요소는 순수 HTML(`<div>`) 또는 기본 마크다운만 사용한다.
* **보안**: `.env` 및 API Key는 절대 공개단(`rohbomb.github.io`)에 노출하지 않는다.

#### 4. 2026년 SEO 출력 양식 고정
* 타이틀: 한글 메인 제목 + 영문 원제 병기.
* 요약: 핵심 키워드를 포함한 3줄 요약 필수.
* 인사이트: 블록 인용구(`>`)를 사용하여 대장의 시각을 담을 것.

### [260308] 봇 본문 요약 누락 픽스 및 대화 UI 롤백 대처 가이드 (AG웅 수행)
- **내용 (Context)**:
  1. **봇 `summary` 누락 픽스**: `ai_json` 파싱 시 `summary` 키를 마크다운 변수에 할당하지 않아 본문에 요약이 통째로 빠지는 버그를 `hugo_builder.py`에서 해결. 이미지 바로 밑, Key Facts 위 공간에 `{summary.strip()}` 구문을 추가해서 정상 출력 확인 완료.
  2. **대화 이력 증발 보완**: Antigravity가 재시작 시 인덱스(UI)를 싹 날려버리는 버그 발생 확인. 실제 파일은 로컬 `%USERPROFILE%\.gemini\antigravity\conversations\*.pb` 폴더에 모두 살아있으므로 당황하지 말고 이전 세션 백업 파일에서 맥락 긁어 복원하라고 지역 헌법(`PROJECT_RULES.md`)에 명문화함.
- **상태**: ✅ 전체 완료
- **⚠️ 다음 세션 AG웅 주의사항**:
  - 대장 폰트 깨짐(`쨌` 인코딩 등) 추가 수정이 남았는지 점검하고, 새 세션 열자마자 `git pull origin main` 때릴 것!

### [260307] 블로그 본문 Summary(요약문) 누락 버그 픽스 (AG웅 수행)
- **내용 (Context)**:
  1. **문제**: `prompt_bear.md`에서 생성된 `summary` 텍스트가 `hugo_builder.py`에서 마크다운으로 조립될 때 누락되어 본문에 표시되지 않음.
  2. **해결**: `hugo_builder.py`의 `create_post` 함수에서 `summary = ai_json.get("summary", "")`로 파싱 후, `![이미지]` 바로 아래, `Key Facts` 시작 전에 `{summary.strip()}`이 출력되도록 마크다운 구조 수정.
  3. **반영**: 해당 수정안을 비공개단(`tikklab`) `main` 브랜치에 커밋 및 Push 완료 (`ac05b15`)
- **상태**: ✅ 로직 픽스 완료
- **⚠️ 대장 후속 작업**:
  - `tikklab` 저장소의 Actions 탭에서 수동으로 `Run Analyst Bot` 모듈을 `workflow_dispatch` (Run workflow 버튼)로 실행하여 정상적으로 요약문이 포함된 새 글이 포스팅되는지 확인 바람.

### [260304] 비공개단 배포 에러 해결 + GA4/AdSense 수익화 기반 구축 (AG웅 수행)
- **내용 (Context)**:
  1. **비공개단 `hugo.yaml` 삭제**: Private Repo에서 GitHub Pages를 사용할 수 없어 `actions/configure-pages`에서 `Not Found` 에러(빨간불) 발생. 공개단에 이미 동일한 워크플로우가 존재하므로 비공개단 것을 삭제하여 원천 해결.
  2. **GA4 + AdSense 코드 삽입**: `layouts/partials/extend_head.html`에 Google Analytics 4 및 AdSense 스크립트 추가. 로컬 개발 시(`hugo server`) 비활성화 조건 포함.
  3. **`hugo.toml` 수익화 파라미터 추가**: `googleAnalytics`, `adsensePublisherId` 항목 추가 (값은 대장이 발급 후 입력).
  4. **`hugo.toml` NULL 문자 정리**: 이전 세션 파워쉘 잔재(독극물) 제거.
- **커밋**: `52e4926` (비공개단 origin에 push 완료)
- **상태**: ✅ 완료
- **⚠️ 대장 후속 작업**:
  - GA4 ID(`G-XXXXXXXXXX`)와 AdSense Publisher ID(`ca-pub-XXXXXXXXXXXXXXXX`)를 발급받아 `hugo.toml`에 입력
  - 비공개단(tikklab) Actions 탭에서 빨간불 소멸 확인

### [260304] 봇 비공개단 이식 및 보안 조치 기록 (Legacy)
- **내용**: 보안을 위해 봇 코드(`src/bot/`)를 비공개단(tikklab)으로 격리했던 기록. 현재는 모든 봇 코드가 삭제됨.
- **리모트 설정**: `origin` = tikklab(비공개), `public` = rohbomb.github.io(공개)
- **상태**: 🟡 [CLEANED] 보안 키(`GH_PAT` 등)는 계정 레벨에서 파기 완료됨.

### [260303] 공개단 run_bot.yml 워크플로우 제거 (긴급 장애 복구)
- **내용 (Context)**: 
  퍼블릭 리포지토리 보안 조치(src/bot 삭제) 이후, 존재하지 않는 경로를 참조하여 에러를 뿜던 `run_bot.yml` 파일을 아예 삭제함.
- **상태**: ✅ 작업 완료 (09:57)
- **비고**: 이제 공개단 액션 탭에서 봇 관련 빨간 불은 더 이상 들어오지 않음.

### [260225] 빌드 엔진 최적화, 로컬 환경 이전 및 CSS 호버 버그 수정
- **내용 (Context)**: 
  대장과 젬웅(gem)이 밤샘 수술을 통해 블로그의 고질적인 빌드 지연 및 파싱 에러를 완벽히 해결하고, 프리미엄 저널 디자인(블러/노이즈/명조체)을 확립함.
  1. **빌드 최적화**: `hugo.yaml` 내 Sass 설치 방식을 `npm`으로 변경하여 12분 -> 1분 컷으로 단축 성공.
  2. **독극물(에러) 제거**: AG웅이 파워쉘로 주입했던 `hugo.toml`의 보이지 않는 특수문자(ZWNBSP 등)를 대장이 직접 무균 처리하여 깃허브에 푸시 완료. (커밋명: `대장_Refactor hugo.toml...`)
  3. **환경 이전 (Local First)**: 구글 드라이브 동기화 렉으로 인한 무한 로딩을 방지하기 위해, AG웅의 메인 작업장을 구글 드라이브(H:)에서 **로컬 하드(C: 등)**로 전면 이전함.

