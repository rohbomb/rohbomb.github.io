# 🤝 SYNK_GEM (대장-젬웅-AG웅 동기화 문서)

이 문서는 대장과 **젬웅(gemini의 gem웅)**이 설계/수정한 기획 및 로직 변경 사항을 **AG웅(나)**에게 인수인계하기 위한 전용 동기화 문서다.

---

## 📢 AG웅 실무 지침 (Must Read when Notified)
1. **트리거 기반**: AG웅은 대장이 명시적으로 "SYNK_GEM 읽어라", 혹은 "인수인계 문서 읽어라"라고 지시할 때만 이 문서를 딥다이브한다. (불필요한 토큰/성능 낭비 방지)
2. **동기화 우선순위**: 이 문서에 적힌 내용은 모든 자동화 로직보다 우선한다. 
3. **작업 완료 후**: AG웅은 본 문서에 적힌 지시사항을 완수하면, 해당 항목을 [x] 처리하거나 작업 완료 여부를 대장에게 보고한다.

---

## 🚨 [필독] 무과금 및 보안 헌법 (Zero-Cost & Security Policy)
**대장과 젬웅(CSO), AG웅(실행)이 합의한 프로젝트 최우선 아키텍처 원칙입니다. 절대 잊지 마십시오.**

1. **저장소 투트랙(Two-Track) 분리**
   - **비공개단 (`tikklab` / origin)**: 봇(`src/bot`) 소스코드와 영업 비밀을 보관하는 **'기밀 금고'**. GitHub 무료 계정 한계로 인해 이곳에서는 웹사이트 배포용 워크플로우를 **의도적으로 완전히 제거**했습니다. (배포 시도 시 과금 및 에러 발생)
   - **공개단 (`rohbomb.github.io` / public)**: 대중에게 노출되는 **'실제 라이브 웹사이트'**. 디자인, 레이아웃(`extend_head.html`, `hugo.toml`), 수동 포스팅 글 등은 무조건 이쪽으로 푸시(Push)되어야만 라이브 웹사이트가 빌드 및 배포됩니다.
2. **배포 지시 원칙 (Gem-Woong 행동 교정)**
   - 젬웅은 앞으로 코드 수정을 지시할 때 "비공개단에 워크플로우를 신설해라"라고 오판하지 말고, **"수정한 코드를 공개단(Public)에도 안전하게 부분 푸시(Push)하여 배포하라"**고 지시해야 합니다.
   - 대장의 수동 포스팅 역시 깃허브 공개단(public)에서 직접 작성 가능하며, 이후 로컬 동기화(`git pull public main`)를 권장합니다.

---

## 📝 인수인계 히스토리 (Latest First)

*(이 아래에 젬웅과의 논의 결과나 수정 사항을 자유롭게 기록해 주세요!)*

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
* **AG웅 액션**:
    1. `hugo.toml` 다국어 설정 적용 및 언어별 GNB 메뉴(Posts/Tags vs 포스트/태그) 분리 구축 완료.
    2. 라이브 사이트 검증을 통해 언어 전환(Locale Switching) 기능 정상 작동 확인.

#### 1. 전략 피벗: '경제/코인' ➡️ 'IT/생산성'
* **변경 사유**: 무의미한 단순 뉴스 요약(경제)으로는 구글의 '저품질' 철퇴 피하기 불가. 체류 시간이 길고 연금형 수익 창출이 가능한 **'IT 도구(Anti-Gravity, LLM 등) 및 생산성 최적화'**로 단일 주제(Topical Authority) 확정.
* **AG웅 액션**: 경제/코인 관련 RSS 수집 및 자동 발행 스케줄 전면 중단(Disable) 유지 중.

#### 2. 구글 E-E-A-T 대응: 'About Us' 메뉴 신설
* **목적**: 2026년 구글 SEO 알고리즘(진정성, 경험) 대응 및 IT 전문 매체 신뢰도 확보.
* **AG웅 액션**: 
    1. `hugo.toml` GNB 영역에 `About Us` 메뉴 노출 설정 완료.
    2. `content/about.md` 생성하여 다중 저자('Captain', 'Analyst Bear') 페르소나 정보를 담을 수 있는 마크다운 레이아웃 공간(Placeholder) 구축 완료 (구체적 내용은 대장/젬웅이 채워 넣도록 공란 유지).

### [260308] 🤝 [SYNK_GEM Update] AG웅, 운영 체계 전면 개편 (v6.0)

#### 1. 하이브리드 투트랙 운영 (1일 2포스팅)
* **Track A (AG웅 전담)**: 매일 오전 7~10시 사이, RSS 기반 `Money` 카테고리 자동 발행. 
    * 필명: **Analyst Bear**
    * 어조: 감정 배제, 팩트 중심, "~다" 체 유지. 한마디로 지금과 동일 형태
* **Track B (대장/젬웅 전담)**: 고품질 영문 리포트 기반 수동 발행.
    * 필명: **Captain**
    * 어조: 독자에게 말을 거는 친근하고 통찰력 있는 어투.

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

### [260304] 봇 비공개단 이식, 유실 글 복구, 3중 백업 체계 구축 (AG웅 수행)
- **내용 (Context)**:
  1. **봇 비공개단 이식**: 보안 조치로 공개단에서 삭제된 봇 코드(`src/bot/`)와 워크플로우(`run_bot.yml`)를 비공개단(tikklab)에 재배치. `.gitignore`는 `.env`만 정밀 차단으로 수정. `requirements.txt`에 누락된 `PyYAML` 추가.
  2. **유실 글 9개 복구**: `git push -f`(강제 푸시)로 날아간 2/26~3/2 사이 봇 글 9개를 GitHub dangling commit(`56fb831`)에서 전량 복구하여 공개단/비공개단 양쪽에 반영.
  3. **3중 백업 체계 구축**: `run_bot.yml`에 공개단→비공개단 자동 sync 스텝 추가. 로컬 수동 동기화(`git pull origin main`)로 구드 백업 완성.
  4. **지역 헌법 업데이트**: `--force` 전면 금지, 봇 자동 백업 의무화, 로컬 동기화 권고 규칙 3개 추가.
- **현재 작업장**: `C:\Users\kiaor\.gemini\antigravity\scratch\260213_oracle_wp_revenue\blog_root`
- **리모트 설정**: `origin` = tikklab(비공개), `public` = rohbomb.github.io(공개)
- **깃허브 Secrets**: `GH_PAT`, `LLM_API_KEY`, `PEXELS_API_KEY` 3개 확인 완료
- **상태**: ✅ 전체 완료
- **⚠️ 다음 세션 AG웅 주의사항**:
  - `git push --force` **절대 금지** (지역 헌법 명시)
  - 봇은 GitHub API로 공개단에 직접 글을 올리므로 로컬에 자동으로 안 내려옴. 주기적으로 `git pull origin main` 필요.
  - 공개단에 `src/bot/`이 올라가면 안 됨. 비공개단에만 존재해야 함.

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

