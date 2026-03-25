# 3. Background and Design Requirements

## English

### 3.1 The Codle Platform

Codle is a web-based integrated learning platform designed for K-12 data science education. Originally developed by Team Monolith and subsequently deployed in collaboration with the Korea Foundation for the Advancement of Science and Creativity, the platform provides a structured learning environment where students progress through themed data science curricula.

**Deployment Scale.** As of 2025, Codle has been deployed across 49 schools in South Korea (40 high schools, 9 middle schools), serving 709 students through three thematic curricula:
- **Ocean Debris**: Environmental data analysis focused on marine pollution
- **Climate Change**: Climate data exploration and pattern recognition
- **Food Security**: Agricultural data analysis and food supply chain modeling

**Curriculum Structure.** Each curriculum consists of 15 sessions organized into a three-tier difficulty progression that scaffolds students from visual programming to text-based coding:

- **Tier 1 -- Foundation (Sessions 1--5):** Students begin with **Entry block-based programming**, a visual coding environment where learners compose logic by snapping blocks together. This low-floor approach ensures accessibility for students with no prior programming experience. Foundational sessions also include PDF reading, video watching, and introductory data concepts (DC).
- **Tier 2 -- Intermediate (Sessions 6--10):** Students transition to **CODAP**, an interactive data analysis tool, where they perform exploratory data analysis through direct manipulation of datasets---filtering, grouping, and visualizing without writing code. This stage develops data analysis (DA) and visualization (DV) competencies through a code-free yet analytically rigorous environment.
- **Tier 3 -- Advanced (Sessions 11--15):** Students progress to **Python programming**, where they write code using data science libraries (e.g., pandas, matplotlib) to perform computational analysis, create custom visualizations, and synthesize findings. This final tier targets computational thinking (CT) and data interpretation (DI) competencies.

This three-tier progression---block coding, interactive data tool, text-based programming---mirrors established CS education scaffolding principles [Grover & Pea, 2013; Weintrop et al., 2016], gradually increasing cognitive complexity while maintaining engagement at each level.

**Activity Types.** The platform supports nine distinct activity types: PdfActivity, VideoActivity, StudioActivity (Python coding), CodapActivity (interactive data tool), SheetActivity (spreadsheet), BoardActivity (discussion), QuizActivity, EmbeddedActivity (pre/post assessments), and EntryActivity (block-based programming).

**AI Tutor Integration.** Codle integrates an LLM-powered AI tutor available across all three programming tiers---including block-based coding, CODAP data analysis, and Python coding. During Entry block coding, the AI tutor assists students with block selection, logic debugging, and conceptual scaffolding; during CODAP sessions, it provides data filtering guidance and analytical hints; and during Python sessions, it offers error explanations, debugging support, and code suggestions. Usage is logged with categories including: error-help (code error explanation), block-help (block coding assistance), sheet-help (spreadsheet assistance), and sheet-filter (data filtering guidance). This cross-tier AI tutor deployment enables analysis of how AI dependency patterns evolve as students progress through increasing levels of difficulty (Section 4).

**Five Core Competencies.** The platform tracks five data literacy competencies aligned with the national AI education framework:
- **DC** (Data Comprehension): Understanding data types, sources, and representations
- **DA** (Data Analysis): Performing statistical and exploratory analysis
- **DV** (Data Visualization): Creating and interpreting visual representations
- **DI** (Data Interpretation): Drawing conclusions and communicating findings
- **CT** (Computational Thinking): Algorithmic problem-solving and programming

### 3.2 Domain Immersion and Analytical Need Identification

The first author co-developed the Codle platform beginning in October 2021 and has operated it across 49 schools for over four years. This sustained domain immersion---encompassing platform engineering, curriculum co-design, teacher training workshops, and direct observation of classroom deployments---provided deep familiarity with the data landscape and the analytical challenges educators face. In terms of Sedlmair et al.'s [2012] design study methodology, this extended engagement satisfies the *gatekeeper* and *front-line analyst* roles: the first author had direct access to all platform data, ongoing relationships with educators, and firsthand experience with the limitations of existing reporting tools.

During this period, recurring analytical pain points became apparent through platform operation:

- **Teachers repeatedly requested cross-classroom comparisons** that the platform's built-in grade reports could not provide. Aggregate completion rates obscured performance differences across curricula and schools.
- **AI tutor usage data existed in raw log form** but was never surfaced to educators. Teachers had no visibility into how---or how much---students relied on AI assistance, making it impossible to distinguish independent mastery from AI-supported completion.
- **Performance drops at curriculum tier transitions** (particularly the shift from CODAP to Python at session 11) were reported anecdotally by multiple teachers, but no systematic method existed to detect, quantify, or compare these patterns across schools.

These operational observations, combined with the literature gaps identified in Section 2, formed the basis for the design requirements described below. The requirements were subsequently validated through the formative evaluation with 10 domain experts (Section 6), who confirmed both the relevance of the identified needs and the effectiveness of the proposed solutions.

### 3.3 Design Requirements

Five design requirements emerged from the combination of operational experience and literature analysis:

**DR1: Multi-level comparative overview.** Teachers managing multiple classrooms and administrators overseeing multiple schools need to compare performance at different granularities. The platform's flat grade reports do not support hierarchical exploration. The learning analytics literature consistently identifies multi-level drill-down as a gap in existing LADs [Verbert et al., 2013; Schwendimann et al., 2017], and our operational experience confirmed this: teachers frequently asked for the ability to identify underperforming schools at a glance, then drill into specific classrooms to understand the causes.

**DR2: Competency development trajectory tracking.** The five competencies develop at different rates across the 15-session curriculum, and final assessment scores alone cannot capture this developmental dynamic. Research on formative assessment [Black & Wiliam, 1998] emphasizes the value of process-level feedback over summative metrics. Operationally, teachers reported that students sometimes performed well in early competencies (Data Comprehension) but struggled during the transition to later competencies (Computational Thinking)---a temporal pattern invisible in aggregate scores.

**DR3: Student-level behavioral pattern identification.** Teachers need to identify students who are silently struggling, disengaging, or exhibiting counterproductive patterns (e.g., skipping activities, over-relying on AI help). Research on early warning systems in education [Jayaprakash et al., 2014] highlights the importance of individual-level behavioral signals. In our platform data, patterns such as consistent high completion followed by sudden disengagement were common but required manual inspection of individual student records to detect.

**DR4: AI tutor usage analysis.** With AI tutors integrated across all curriculum tiers, teachers need visibility into how students use these tools---whether strategically for learning or as a substitute for independent thinking. The AI literacy measurement literature [Long & Magerko, 2020; Ng et al., 2021] calls for behavioral assessment of AI engagement, yet no existing dashboard provides this capability. Our platform logged 6,270 AI tutor interactions, but this data was never surfaced in an interpretable form.

**DR5: Curriculum effectiveness evaluation.** Administrators and curriculum designers need evidence of educational impact, particularly pre/post competency assessment comparisons and engagement patterns across different curricula. Educational evaluation frameworks [Kirkpatrick & Kirkpatrick, 2016] emphasize the need for multi-level evidence of program effectiveness. Three different curricula were deployed across 49 schools, creating a natural comparison opportunity that existing tools could not exploit.

---

## 한글

### 3.1 코들(Codle) 플랫폼

코들은 K-12 데이터 사이언스 교육을 위해 설계된 웹 기반 통합 학습 플랫폼이다. 팀모노리스(Team Monolith)에 의해 개발되고 이후 한국과학창의재단과 협력하여 배포되었으며, 학생들이 주제별 데이터 사이언스 커리큘럼을 단계적으로 학습하는 체계적 학습 환경을 제공한다.

**배포 규모.** 2025년 기준, 코들은 한국 전역 49개 학교(고등학교 40개, 중학교 9개)에 배포되어 3개 주제별 커리큘럼을 통해 709명의 학생에게 서비스하고 있다:
- **해양쓰레기**: 해양 오염에 초점을 맞춘 환경 데이터 분석
- **기후변화**: 기후 데이터 탐색 및 패턴 인식
- **식량안보**: 농업 데이터 분석 및 식량 공급망 모델링

**커리큘럼 구조.** 각 커리큘럼은 15차시로 구성되며, 시각적 프로그래밍에서 텍스트 기반 코딩으로 이어지는 3단계 난이도 체계를 따른다:

- **1단계 -- 기초 (1--5차시):** 학생들은 **엔트리(Entry) 블록코딩**으로 시작한다. 블록을 조합하여 로직을 구성하는 시각적 코딩 환경으로, 프로그래밍 경험이 없는 학생도 접근할 수 있다. 기초 차시에는 PDF 읽기, 영상 시청, 데이터 기초 개념(DC)도 포함된다.
- **2단계 -- 중급 (6--10차시):** 학생들은 **CODAP** 인터랙티브 데이터 분석 도구로 전환하여, 코드를 작성하지 않고 직접 조작 방식으로 데이터를 필터링, 그룹화, 시각화하며 탐색적 데이터 분석을 수행한다. 이 단계에서 데이터 분석(DA)과 시각화(DV) 역량을 개발한다.
- **3단계 -- 심화 (11--15차시):** 학생들은 **파이썬 프로그래밍**으로 진행하여, 데이터 사이언스 라이브러리(pandas, matplotlib 등)를 활용한 계산적 분석, 맞춤형 시각화 제작, 결과 종합을 수행한다. 이 단계에서 컴퓨팅 사고(CT)와 데이터 해석(DI) 역량을 목표로 한다.

이 3단계 진행---블록코딩, 인터랙티브 데이터 도구, 텍스트 기반 프로그래밍---은 확립된 CS 교육 스캐폴딩 원칙 [Grover & Pea, 2013; Weintrop et al., 2016]을 반영하며, 각 단계에서 참여를 유지하면서 인지적 복잡도를 점진적으로 높인다.

**활동 유형.** 플랫폼은 9가지 활동 유형을 지원: PDF, 영상, 스튜디오(파이썬 코딩), CODAP(인터랙티브 데이터 도구), 시트(스프레드시트), 보드(토론), 퀴즈, 임베디드(사전/사후 평가), 엔트리(블록 코딩).

**AI 튜터 통합.** 코들은 3단계 프로그래밍 환경 전체에 걸쳐 사용 가능한 LLM 기반 AI 튜터를 통합하고 있다. 엔트리 블록코딩에서는 블록 선택, 로직 디버깅, 개념 스캐폴딩을 지원하고, CODAP 세션에서는 데이터 필터링 안내와 분석 힌트를 제공하며, 파이썬 세션에서는 에러 설명, 디버깅 지원, 코드 제안을 제공한다. 활용은 에러 도움, 블록 도움, 시트 도움, 시트 필터 등의 범주로 로그된다. 이 전 단계 AI 튜터 배포는 학생이 난이도가 높아짐에 따라 AI 의존 패턴이 어떻게 변화하는지 분석할 수 있게 한다(Section 4).

**5대 핵심 역량.** 국가 AI 교육 프레임워크에 맞춰 5개 데이터 리터러시 역량을 추적한다:
- **DC** (데이터 이해), **DA** (데이터 분석), **DV** (데이터 시각화), **DI** (데이터 해석), **CT** (컴퓨팅 사고)

### 3.2 도메인 몰입 및 분석 요구 식별

제1저자는 2021년 10월부터 코들 플랫폼을 공동 개발하여 4년 이상 49개 학교에서 운영해 왔다. 이러한 지속적 도메인 몰입---플랫폼 엔지니어링, 커리큘럼 공동 설계, 교사 연수 워크숍, 교실 배포 직접 관찰을 포괄---은 데이터 환경과 교육자가 직면하는 분석적 도전에 대한 깊은 이해를 제공하였다. Sedlmair et al. [2012]의 디자인 스터디 방법론 관점에서, 이 장기 참여는 *gatekeeper*와 *front-line analyst* 역할을 충족한다: 제1저자는 모든 플랫폼 데이터에 직접 접근하고, 교육자들과 지속적 관계를 유지하며, 기존 보고 도구의 한계를 직접 경험하였다.

이 기간 동안, 플랫폼 운영을 통해 반복적인 분석적 문제점이 명확해졌다:

- **교사들이 반복적으로 학급 간 비교를 요청**하였으나, 플랫폼의 기본 성적 보고서는 이를 지원하지 못하였다. 집계 완료율은 커리큘럼과 학교 간 성과 차이를 가렸다.
- **AI 튜터 사용 데이터는 원시 로그 형태로 존재**하였으나 교육자에게 표면화되지 않았다. 교사는 학생이 AI 지원에 얼마나, 어떻게 의존하는지 파악할 수 없어, 독립적 숙달과 AI 지원 완료를 구별하는 것이 불가능하였다.
- **커리큘럼 단계 전환 시 성과 하락**(특히 10차시 CODAP에서 11차시 파이썬으로의 전환)이 여러 교사에 의해 보고되었으나, 이러한 패턴을 학교 간에 체계적으로 감지, 정량화, 비교하는 방법은 존재하지 않았다.

이러한 운영적 관찰은 Section 2에서 식별된 문헌 공백과 결합하여 아래 기술하는 디자인 요구사항의 기반을 형성하였다. 요구사항은 이후 10명 도메인 전문가 대상 형성 평가(Section 6)를 통해 검증되었으며, 전문가들은 식별된 요구의 적합성과 제안된 해결책의 효과성을 모두 확인하였다.

### 3.3 디자인 요구사항

운영 경험과 문헌 분석의 결합으로부터 5개 디자인 요구사항이 도출되었다:

**DR1: 다단계 비교 개요.** 복수 학급을 관리하는 교사와 복수 학교를 감독하는 관리자는 서로 다른 세분화 수준에서 성과를 비교해야 한다. 플랫폼의 평면적 성적 보고서는 계층적 탐색을 지원하지 않는다. 학습 분석 문헌은 일관되게 다단계 드릴다운을 기존 LAD의 공백으로 식별하며 [Verbert et al., 2013; Schwendimann et al., 2017], 운영 경험도 이를 확인하였다: 교사들은 저성과 학교를 한눈에 식별한 후 특정 학급으로 드릴다운하여 원인을 파악하는 기능을 빈번히 요청하였다.

**DR2: 역량 발달 궤적 추적.** 5개 역량은 15차시 커리큘럼에 걸쳐 서로 다른 속도로 발달하며, 최종 평가 점수만으로는 이 발달 역학을 포착할 수 없다. 형성 평가에 관한 연구 [Black & Wiliam, 1998]는 총괄 지표보다 과정 수준 피드백의 가치를 강조한다. 운영적으로, 교사들은 학생이 초기 역량(데이터 이해)에서는 잘 수행하다가 후기 역량(컴퓨팅 사고)으로의 전환에서 어려움을 겪는 경우를 보고하였다---집계 점수에서는 보이지 않는 시간적 패턴이다.

**DR3: 학생 수준 행동 패턴 식별.** 교사는 조용히 어려움을 겪거나, 이탈하거나, 비생산적 패턴(예: 활동 건너뛰기, AI 도움 과의존)을 보이는 학생을 식별해야 한다. 교육에서의 조기 경보 시스템 연구 [Jayaprakash et al., 2014]는 개인 수준 행동 신호의 중요성을 강조한다. 플랫폼 데이터에서 일관된 높은 완료율 후 갑작스러운 이탈과 같은 패턴이 흔하였으나, 감지를 위해서는 개별 학생 기록의 수동 검토가 필요하였다.

**DR4: AI 튜터 활용 분석.** AI 튜터가 전 커리큘럼 단계에 통합된 상황에서, 교사는 학생이 이 도구를 학습을 위해 전략적으로 사용하는지, 독립적 사고의 대체물로 사용하는지 파악해야 한다. AI 리터러시 측정 문헌 [Long & Magerko, 2020; Ng et al., 2021]은 AI 참여의 행동적 평가를 요구하나, 기존 대시보드 중 이 기능을 제공하는 것은 없다. 플랫폼에서 6,270건의 AI 튜터 상호작용이 로그되었으나, 이 데이터는 해석 가능한 형태로 표면화된 적이 없었다.

**DR5: 커리큘럼 효과성 평가.** 관리자와 커리큘럼 설계자는 교육적 영향의 증거, 특히 사전/사후 역량 평가 비교와 서로 다른 커리큘럼 간 참여 패턴이 필요하다. 교육 평가 프레임워크 [Kirkpatrick & Kirkpatrick, 2016]는 프로그램 효과성에 대한 다단계 증거의 필요성을 강조한다. 49개 학교에 3개 서로 다른 커리큘럼이 배포되어 자연적 비교 기회를 만들었으나, 기존 도구는 이를 활용할 수 없었다.
