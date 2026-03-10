# 3. Background and Design Requirements

## English

### 3.1 The Codle Platform

Codle is a web-based integrated learning platform designed for K-12 data science education. Originally developed by Team Monolith and subsequently deployed in collaboration with the Korea Foundation for the Advancement of Science and Creativity (한국과학창의재단), the platform provides a structured learning environment where students progress through themed data science curricula.

**Deployment Scale.** As of 2025, Codle has been deployed across 49 schools in South Korea (40 high schools, 9 middle schools), serving 709 students through three thematic curricula:
- **Ocean Debris (해양쓰레기)**: Environmental data analysis focused on marine pollution
- **Climate Change (기후변화)**: Climate data exploration and pattern recognition
- **Food Security (식량안보)**: Agricultural data analysis and food supply chain modeling

**Curriculum Structure.** Each curriculum consists of 15 sessions following a structured competency progression:
- Sessions 1–3: **Understanding** (DC) — PDF reading, video watching, foundational concepts
- Sessions 4–7: **Analysis** (DA) — CODAP interactive analysis, introductory coding
- Sessions 8–11: **Coding** (CT, DV) — Python programming, library usage, visualization
- Sessions 12–15: **Synthesis** (DI) — Data interpretation, presentation, final assessment

**Activity Types.** The platform supports nine distinct activity types: PdfActivity, VideoActivity, StudioActivity (Python coding), CodapActivity (interactive data tool), SheetActivity (spreadsheet), BoardActivity (discussion), QuizActivity, EmbeddedActivity (pre/post assessments), and EntryActivity (block-based programming).

**AI Tutor Integration.** Codle integrates an LLM-powered AI tutor that students can invoke during coding and data analysis tasks. The AI tutor provides error explanations, debugging hints, and conceptual guidance. Usage is logged with three categories: error-help (code error explanation), sheet-help (spreadsheet assistance), and sheet-filter (data filtering guidance).

**Five Core Competencies.** The platform tracks five data literacy competencies aligned with the national AI education framework:
- **DC** (Data Comprehension): Understanding data types, sources, and representations
- **DA** (Data Analysis): Performing statistical and exploratory analysis
- **DV** (Data Visualization): Creating and interpreting visual representations
- **DI** (Data Interpretation): Drawing conclusions and communicating findings
- **CT** (Computational Thinking): Algorithmic problem-solving and programming

### 3.2 Design Study Process

We conducted a design study following the nine-stage framework of Sedlmair et al. [2012]. Over a four-month period (November 2025 – February 2026), we engaged with five K-12 teachers (T1–T5) who had used Codle in their classrooms and three education researchers (R1–R3) specializing in learning analytics.

**Participants:**
- T1–T3: High school teachers with 3–10 years of data science teaching experience
- T4–T5: Middle school teachers introducing data science for the first time
- R1–R2: Learning analytics researchers with expertise in educational dashboards
- R3: AI in education researcher focusing on LLM-based tutoring systems

**Process:** We conducted three rounds of semi-structured interviews (each 60–90 minutes), interspersed with prototype demonstrations and feedback sessions. The first round focused on understanding current pain points and workflows. The second round presented initial visualization designs and gathered feedback. The third round evaluated the near-final prototype with realistic data.

### 3.3 Design Requirements

From our interviews, we derived five design requirements:

**DR1: Multi-level comparative overview.** Teachers managing multiple classrooms and administrators overseeing multiple schools need to compare performance at different granularities. *"I need to see which schools are falling behind at a glance, then zoom into specific classrooms to understand why."* (T1)

**DR2: Competency development trajectory tracking.** The five competencies develop at different rates across the 15-session curriculum. Teachers need to see not just final scores but the trajectory of growth. *"Some students start strong in data comprehension but struggle when we reach computational thinking. I need to see this transition."* (T3)

**DR3: Student-level behavioral pattern identification.** Teachers need to identify students who are silently struggling, disengaging, or exhibiting counterproductive patterns (e.g., skipping activities, over-relying on AI help). *"I want to spot the student who completed session 1–6 perfectly but then disappeared."* (T4)

**DR4: AI tutor usage analysis.** With AI tutors becoming integral to the learning experience, teachers need visibility into how students use these tools—whether strategically for learning or as a crutch to avoid thinking. *"Some students ask the AI for every single error. I worry they're not learning to debug on their own."* (T2)

**DR5: Curriculum effectiveness evaluation.** Administrators and curriculum designers need evidence of educational impact, particularly pre/post competency assessment comparisons and engagement patterns. *"We need to show the foundation that this program actually works—with data, not anecdotes."* (R1)

---

## 한글

### 3.1 코들(Codle) 플랫폼

코들은 K-12 데이터 사이언스 교육을 위해 설계된 웹 기반 통합 학습 플랫폼이다. 팀모노리스(Team Monolith)에 의해 개발되고 이후 한국과학창의재단과 협력하여 배포되었으며, 학생들이 주제별 데이터 사이언스 커리큘럼을 단계적으로 학습하는 체계적 학습 환경을 제공한다.

**배포 규모.** 2025년 기준, 코들은 한국 전역 49개 학교(고등학교 40개, 중학교 9개)에 배포되어 3개 주제별 커리큘럼을 통해 709명의 학생에게 서비스하고 있다:
- **해양쓰레기**: 해양 오염에 초점을 맞춘 환경 데이터 분석
- **기후변화**: 기후 데이터 탐색 및 패턴 인식
- **식량안보**: 농업 데이터 분석 및 식량 공급망 모델링

**커리큘럼 구조.** 각 커리큘럼은 체계적 역량 진행에 따른 15차시로 구성된다:
- 1–3차시: **이해** (DC) — PDF 읽기, 영상 시청, 기초 개념
- 4–7차시: **분석** (DA) — CODAP 인터랙티브 분석, 초급 코딩
- 8–11차시: **코딩** (CT, DV) — 파이썬 프로그래밍, 라이브러리 활용, 시각화
- 12–15차시: **종합** (DI) — 데이터 해석, 발표, 최종 평가

**활동 유형.** 플랫폼은 9가지 활동 유형을 지원: PDF, 영상, 스튜디오(파이썬 코딩), CODAP(인터랙티브 데이터 도구), 시트(스프레드시트), 보드(토론), 퀴즈, 임베디드(사전/사후 평가), 엔트리(블록 코딩).

**AI 튜터 통합.** 코들은 학생이 코딩 및 데이터 분석 과제 중 호출할 수 있는 LLM 기반 AI 튜터를 통합하고 있다. AI 튜터는 에러 설명, 디버깅 힌트, 개념 안내를 제공하며, 활용은 에러 도움, 시트 도움, 시트 필터의 세 범주로 로그된다.

**5대 핵심 역량.** 국가 AI 교육 프레임워크에 맞춰 5개 데이터 리터러시 역량을 추적한다:
- **DC** (데이터 이해), **DA** (데이터 분석), **DV** (데이터 시각화), **DI** (데이터 해석), **CT** (컴퓨팅 사고)

### 3.2 디자인 스터디 과정

Sedlmair et al. [2012]의 9단계 프레임워크에 따라 디자인 스터디를 수행하였다. 4개월간(2025년 11월 ~ 2026년 2월) 코들을 교실에서 사용한 K-12 교사 5명(T1~T5)과 학습 분석 전문 교육 연구자 3명(R1~R3)과 협력하였다.

3라운드의 반구조화 인터뷰(각 60~90분)를 수행하고, 프로토타입 시연과 피드백 세션을 교차 진행하였다.

### 3.3 디자인 요구사항

인터뷰를 통해 5개 디자인 요구사항을 도출하였다:

**DR1: 다단계 비교 개요.** 교사와 관리자는 서로 다른 세분화 수준에서 성과를 비교해야 한다. *"어떤 학교가 뒤처지는지 한눈에 보고, 특정 학급으로 들어가서 이유를 파악해야 합니다."* (T1)

**DR2: 역량 발달 궤적 추적.** 15차시에 걸쳐 5개 역량이 서로 다른 속도로 발달한다. 최종 점수뿐 아니라 성장 궤적을 볼 필요가 있다. *"데이터 이해는 잘하다가 컴퓨팅 사고에서 어려워하는 학생이 있어요. 이 전환을 봐야 합니다."* (T3)

**DR3: 학생 수준 행동 패턴 식별.** 조용히 어려움을 겪거나, 이탈하거나, 비생산적 패턴을 보이는 학생을 식별해야 한다. *"1~6차시는 완벽하게 하다가 사라진 학생을 찾고 싶어요."* (T4)

**DR4: AI 튜터 활용 분석.** AI 튜터를 학습을 위해 전략적으로 사용하는지, 사고를 회피하는 수단으로 사용하는지 파악해야 한다. *"모든 에러마다 AI에게 물어보는 학생이 있어요. 스스로 디버깅을 배우지 못할까 걱정됩니다."* (T2)

**DR5: 커리큘럼 효과성 평가.** 관리자와 커리큘럼 설계자는 교육적 영향의 증거, 특히 사전/사후 역량 평가 비교와 참여 패턴이 필요하다. *"이 프로그램이 실제로 효과가 있다는 것을 재단에 데이터로 보여줘야 합니다."* (R1)
