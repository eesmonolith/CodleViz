# 1. Introduction

## English

Data science education is rapidly expanding into K-12 classrooms worldwide, driven by the recognition that data literacy is a fundamental competency for the 21st century [ref]. Countries including the United States, United Kingdom, and South Korea have begun integrating data science concepts into their national curricula, introducing students to data collection, analysis, visualization, and computational thinking as early as middle school [ref].

This expansion brings unprecedented challenges for educators. Unlike traditional subjects where student progress can be assessed through periodic tests, data science education involves **multimodal learning activities**—students write code, manipulate interactive data tools, watch instructional videos, collaborate on discussion boards, and increasingly interact with AI-powered tutoring systems. A single 15-session curriculum may generate thousands of heterogeneous learning events per classroom, creating a data deluge that overwhelms conventional assessment approaches.

**The Codle platform** exemplifies this new paradigm. Developed as an integrated web-based environment for K-12 data science education, Codle has been deployed across 49 schools in South Korea, serving 709 students through three thematic curricula (Ocean Debris, Climate Change, and Food Security). Each curriculum spans 15 sessions and encompasses nine distinct activity types: PDF reading, video viewing, coding (Python), CODAP data analysis, spreadsheet work, discussion boards, quizzes, embedded assessments, and Entry (block-based programming). The platform also integrates an LLM-powered AI tutor that provides on-demand assistance during coding and data analysis tasks.

While Codle successfully captures rich, multimodal learning data, **teachers currently lack tools to make sense of this data**. Existing learning management system (LMS) dashboards typically offer only aggregate completion rates or grade distributions, which fail to answer critical pedagogical questions:

- How do students' five core competencies (Data Comprehension, Analysis, Visualization, Interpretation, and Computational Thinking) develop across the 15-session curriculum?
- Which students are struggling silently, and which are over-relying on AI tutoring tools?
- How do learning patterns differ across schools, curricula, and student populations?
- Where in the curriculum do students consistently disengage, and why?

These questions demand more than simple dashboards—they require **visual analytics techniques** that can reveal hidden patterns in complex, multimodal educational data. In particular, three analytical challenges remain unaddressed by existing Learning Analytics Dashboards (LADs):

1. **AI dependency detection**: As AI tutors become ubiquitous, distinguishing between students who use AI strategically (scaffolding) versus those who develop dependency (outsourcing thinking) requires simultaneous visualization of completion rates and AI usage patterns—a combination no existing LAD provides.

2. **Pedagogical transition barrier identification**: Curriculum designers need to know where students systematically struggle during phase transitions (e.g., from data analysis to coding). Manual inspection of session-level completion trends is tedious and prone to oversight, especially across 49 schools.

3. **Cross-school trajectory comparison**: Comparing learning trajectories across schools with different baseline levels and class sizes requires normalization and alignment techniques that go beyond simple line chart overlays.

To address these challenges, we present **CodleViz**, a visual analytics system designed through a two-phase design study methodology [Sedlmair et al., 2012] in collaboration with K-12 teachers and education researchers. CodleViz provides a coordinated multi-view dashboard with four-level drill-down exploration—from a national overview of all 49 schools down to individual student learning trajectories. Beyond standard visualization components, CodleViz introduces three novel visual analytics techniques specifically designed for AI-integrated educational data:

- The **AI Dependency Glyph** simultaneously encodes completion rate, AI tutor usage frequency, and reliance trend within a single composite glyph, enabling teachers to visually classify students into four behavioral quadrants (independent learner, AI-dependent, disengaged, struggling).

- The **Coding Cliff Detector** automatically identifies pedagogical transition barriers by computing cliff severity and recovery rates, annotating them directly on the learning journey timeline and aggregating patterns across schools in a cliff heatmap.

- The **Trajectory Alignment View** enables meaningful cross-school comparison through baseline-normalized small multiples, curriculum-level trajectory envelopes, phase-aligned sparklines, and DTW-based trajectory clustering.

Our contributions are as follows:

1. **A two-phase design study** characterizing the visualization needs of K-12 data science educators, resulting in five design requirements derived from iterative interviews with domain experts (Phase 1: design requirements elicitation; Phase 2: system evaluation).

2. **Three novel visual analytics techniques** for AI-integrated educational data: the AI Dependency Glyph for revealing hidden AI reliance patterns, the Coding Cliff Detector for automatic pedagogical barrier identification, and the Trajectory Alignment View for cross-school comparative analysis.

3. **The CodleViz system**, a coordinated multi-view visual analytics dashboard integrating nine visualization views with four-level drill-down exploration, deployed on the Codle platform serving 49 schools and 709 students.

4. **Three case studies and expert evaluation** demonstrating how CodleViz reveals actionable insights about competency development patterns, AI tool usage, and curriculum effectiveness.

---

## 한글

데이터 사이언스 교육은 데이터 리터러시가 21세기 핵심 역량이라는 인식에 힘입어 전 세계 K-12 교실로 빠르게 확대되고 있다 [ref]. 미국, 영국, 한국 등 여러 국가가 국가 교육과정에 데이터 사이언스 개념을 통합하기 시작하였으며, 중학교부터 데이터 수집, 분석, 시각화, 컴퓨팅 사고를 도입하고 있다 [ref].

이러한 확대는 교육자에게 전례 없는 도전을 가져온다. 정기 시험으로 학생 진도를 평가할 수 있는 전통적 과목과 달리, 데이터 사이언스 교육은 **멀티모달 학습 활동**을 수반한다—학생들은 코드를 작성하고, 인터랙티브 데이터 도구를 조작하며, 교육 영상을 시청하고, 토론 게시판에서 협업하며, 점점 더 AI 기반 튜터링 시스템과 상호작용한다.

**코들(Codle) 플랫폼**은 이 새로운 패러다임을 잘 보여준다. K-12 데이터 사이언스 교육을 위한 통합 웹 기반 환경으로 개발된 코들은 한국 전역 49개 학교에 배포되어 3개 주제별 커리큘럼(해양쓰레기, 기후변화, 식량안보)을 통해 709명의 학생에게 서비스하고 있다. 또한 코딩 및 데이터 분석 과제 중 즉각적 도움을 제공하는 LLM 기반 AI 튜터가 통합되어 있다.

코들은 풍부한 멀티모달 학습 데이터를 수집하지만, **교사들은 이 데이터를 이해하기 위한 도구가 부족하다**. 이러한 질문은 단순 대시보드를 넘어, 복잡한 멀티모달 교육 데이터에서 숨겨진 패턴을 드러낼 수 있는 **시각적 분석 기법**을 요구한다. 특히 기존 학습 분석 대시보드(LAD)가 해결하지 못하는 세 가지 분석적 과제가 있다:

1. **AI 의존도 감지**: AI 튜터가 보편화됨에 따라, 전략적 AI 활용과 의존적 AI 활용을 구별하려면 완료율과 AI 사용 패턴의 동시 시각화가 필요하다.
2. **교수학적 전환 장벽 식별**: 커리큘럼 설계자는 학생들이 단계 전환(예: 데이터 분석→코딩)에서 체계적으로 어디서 어려움을 겪는지 알아야 한다.
3. **학교 간 궤적 비교**: 기준선 수준과 학급 크기가 다른 학교 간 학습 궤적 비교에는 정규화와 정렬 기법이 필요하다.

이러한 도전을 해결하기 위해 **CodleViz**를 제안한다. K-12 교사 및 교육 연구자와 협력하여 2단계 디자인 스터디 방법론에 따라 설계하였다. 표준 시각화 구성요소 외에 AI 통합 교육 데이터를 위해 특별히 설계된 3개의 새로운 시각적 분석 기법을 도입한다:

- **AI 의존도 글리프**: 완료율, AI 튜터 사용 빈도, 의존도 추세를 단일 복합 글리프에 동시 인코딩
- **코딩 절벽 감지기**: 심각도와 회복률을 계산하여 교수학적 전환 장벽을 자동 감지, 주석 처리
- **궤적 정렬 뷰**: 기준선 정규화, 궤적 포락선, DTW 기반 클러스터링을 통한 학교 간 비교

본 논문의 기여:

1. **2단계 디자인 스터디**: K-12 교육자의 시각화 요구를 특성화하고, 5개 디자인 요구사항을 도출 (1단계: 요구사항 도출, 2단계: 시스템 평가).

2. **3개 새로운 시각적 분석 기법**: AI 의존도 글리프, 코딩 절벽 감지기, 궤적 정렬 뷰.

3. **CodleViz 시스템**: 9개 시각화 뷰를 갖춘 연동형 다중 뷰 시각적 분석 대시보드. 49개 학교 709명 학생에게 배포.

4. **3개 사례 연구 및 전문가 평가**: 역량 발달 패턴, AI 도구 활용, 커리큘럼 효과성에 대한 실행 가능한 인사이트 시연.
