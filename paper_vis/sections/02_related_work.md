# 2. Related Work

## English

### 2.1 Visual Analytics for Education

Visual analytics has been increasingly applied to educational contexts, spanning higher education, MOOCs, and K-12 settings. Systems such as VisMOOC [Shi et al., 2015] and CourseVis [Mazza & Dimitrova, 2007] visualize student engagement in online courses through clickstream analysis and forum participation patterns. PeerLens [Wang et al., 2016] supports peer review analytics in programming courses. Chen et al. [2019] introduced knowledge graph visualizations for adaptive learning systems in VISPubComPass, and Xia et al. [2022] proposed PeakVizor for visualizing student engagement peaks in online learning.

Most existing educational VA systems focus on **single-modality data**—either forum posts, video interactions, or grade distributions—rather than the multimodal learning activities characteristic of modern AI-integrated platforms. Few systems address **K-12 contexts**, where student populations span multiple schools with varying curricula and teacher expertise levels. More critically, none addresses the analytical challenge introduced by generative AI tools: distinguishing between task performance achieved independently and performance inflated by AI assistance.

### 2.2 Learning Analytics Dashboards

Learning analytics dashboards (LADs) have emerged as the primary interface between learning data and educators [Verbert et al., 2013; Schwendimann et al., 2017]. Commercial platforms such as Canvas Analytics, Google Classroom Insights, and Khan Academy's teacher dashboard provide aggregate metrics including completion rates, time-on-task, and assessment scores.

Research-oriented LADs have explored more sophisticated visualizations. eLAT [Dyckhoff et al., 2012] combines multiple learning indicators into an exploratory analysis tool. Govaerts et al. [2012] proposed the Student Activity Meter for tracking behavioral patterns over time. Mastery Grids [Loboda et al., 2014] visualizes topic-level mastery in intelligent tutoring systems. Matcha et al. [2020] reviewed 53 LADs and found that most focus on summative indicators rather than process-level learning patterns.

Despite these advances, current LADs exhibit three key limitations: (1) they rarely support **multi-level drill-down** from institutional overview to individual student, (2) they do not visualize **competency development trajectories** across structured curricula, and (3) they lack support for analyzing **AI tutor interaction patterns**, which are increasingly prevalent in modern learning platforms.

### 2.3 Multimodal Learning Analytics

Multimodal learning analytics (MMLA) integrates data from diverse sources—video, audio, physiological sensors, log data—to provide holistic understanding of learning processes [Blikstein & Worsley, 2016; Ochoa & Worsley, 2016]. Recent work has explored combining gaze tracking with system logs [Sharma et al., 2020], integrating discourse analysis with behavioral patterns [D'Mello et al., 2021], and fusing code analysis with problem-solving trajectories [Emerson et al., 2020].

In the context of programming education, tools such as ProgSnap [Price et al., 2017] and CodeWorkout [Edwards et al., 2020] capture fine-grained coding interactions. However, **data science education** differs fundamentally from programming—it encompasses not only code but also data manipulation tools (CODAP, spreadsheets), visual analysis, collaborative interpretation, and AI-assisted exploration.

### 2.4 AI Tutoring and Dependency in Education

The rapid adoption of LLM-powered AI tutors in educational settings has raised concerns about student dependency [Kasneci et al., 2023; Becker et al., 2023]. While AI tutors can provide effective scaffolding—reducing frustration and enabling independent problem-solving [Koedinger & Aleven, 2007]—overreliance may inhibit deep learning and metacognitive development [Deci & Ryan, 2000]. Recent studies have documented the "automation complacency" phenomenon in AI-assisted coding education, where students with high AI usage show comparable short-term performance but lower transfer and retention [Prather et al., 2023; Finnie-Ansley et al., 2023].

Despite growing concern, **no existing visualization tool provides educators with the ability to monitor and classify AI tutor usage patterns at scale**. Current AI tutor interfaces report aggregate usage counts but do not distinguish between productive scaffolding use and counterproductive dependency—a gap that CodleViz's AI Dependency Glyph directly addresses.

### 2.5 AI Literacy: Definitions and Measurement Challenges

AI literacy—broadly defined as the competencies needed to critically evaluate, effectively use, and communicate with AI technologies [Long & Magerko, 2020]—has become a central concern as generative AI permeates education and professional work. Ng et al. [2021] proposed a four-dimensional framework encompassing knowing and understanding AI, using and applying AI, evaluating and creating AI, and AI ethics. Laupichler et al. [2022] conducted a systematic review identifying knowledge-based, competency-based, and attitude-based approaches to AI literacy measurement.

Current measurement instruments are overwhelmingly survey-based: self-reported questionnaires that assess perceived knowledge or attitudes toward AI [Wang et al., 2022; Carolus et al., 2023]. These instruments capture declarative knowledge ("I understand how machine learning works") but cannot capture procedural competence—how people actually behave when given access to AI tools during authentic tasks. The gap between self-reported AI understanding and actual AI usage behavior is well documented in adjacent fields [Kruger & Dunning, 1999].

A behavioral approach to AI literacy measurement requires analyzing what learners *do* with AI tools, not what they *say* about them. This demands log-level data from platforms where AI tools are embedded in authentic tasks—precisely the data environment that CodleViz operates in. Our system addresses AI literacy measurement not through surveys but through behavioral analytics: jointly visualizing task performance and AI interaction patterns to classify learners along dimensions of competence and AI reliance.

### 2.6 Summary and Positioning

CodleViz addresses the intersection of these five areas by providing a visual analytics system that integrates generative AI usage logs with multimodal task performance data for **behavioral AI literacy measurement**. Table 1 summarizes how CodleViz extends beyond the capabilities of existing systems across six dimensions.

| System | Multi-level | Competency | AI Usage | Multimodal | Cross-school | AI Literacy |
|--------|:-----------:|:----------:|:--------:|:----------:|:------------:|:-----------:|
| VisMOOC | — | — | — | — | — | — |
| CourseVis | — | partial | — | — | — | — |
| eLAT | partial | — | — | partial | — | — |
| Mastery Grids | — | partial | — | — | — | — |
| Survey instruments | — | — | — | — | — | partial |
| CodleViz | full | full | full | full | full | full |

The critical gap in the literature is the absence of systems that measure AI literacy through behavioral data rather than self-report. CodleViz is the first VA system to jointly analyze task performance and generative AI interaction logs, enabling educators to distinguish genuine competence from AI-inflated performance.

---

## 한글

### 2.1 교육을 위한 시각적 분석

시각적 분석은 고등교육, MOOC, K-12 환경을 아우르며 교육 분야에 점점 더 많이 적용되고 있다. VisMOOC [Shi et al., 2015]과 CourseVis [Mazza & Dimitrova, 2007]은 클릭스트림 분석과 포럼 참여 패턴을 통해 학생 참여도를 시각화한다. PeerLens [Wang et al., 2016]는 동료 평가 분석을, Chen et al. [2019]의 VISPubComPass는 지식 그래프 시각화를, Xia et al. [2022]의 PeakVizor는 온라인 학습 참여 피크 시각화를 도입하였다.

대부분의 기존 교육 VA 시스템은 **단일 모달리티 데이터**에 초점을 맞추며, **K-12 맥락**을 다루는 시스템은 거의 없다. 더 중요한 것은, 생성형 AI 도구가 도입한 분석적 도전—독립적으로 달성한 과제 성과와 AI 도움으로 부풀려진 성과를 구별하는 것—을 다루는 시스템이 없다는 점이다.

### 2.2 학습 분석 대시보드

LAD는 학습 데이터와 교육자 사이의 주요 인터페이스로 부상하였다 [Verbert et al., 2013; Schwendimann et al., 2017]. eLAT [Dyckhoff et al., 2012]는 탐색적 분석 도구를, Govaerts et al. [2012]의 Student Activity Meter는 행동 패턴 추적을, Mastery Grids [Loboda et al., 2014]는 주제별 숙달도 시각화를 제공한다. Matcha et al. [2020]의 53개 LAD 리뷰에 따르면 대부분이 과정 수준 학습 패턴이 아닌 총괄 지표에 초점을 맞추고 있다.

현재 LAD의 핵심 한계: (1) **다단계 드릴다운** 미지원, (2) **역량 발달 궤적** 미시각화, (3) **AI 튜터 상호작용 패턴** 분석 미지원.

### 2.3 멀티모달 학습 분석

MMLA는 다양한 소스의 데이터를 통합하여 학습 과정의 전체적 이해를 제공한다 [Blikstein & Worsley, 2016; Ochoa & Worsley, 2016]. 시선 추적+시스템 로그 결합 [Sharma et al., 2020], 담화 분석+행동 패턴 통합 [D'Mello et al., 2021], 코드 분석+문제해결 궤적 융합 [Emerson et al., 2020] 등이 탐구되었다. ProgSnap [Price et al., 2017]과 CodeWorkout [Edwards et al., 2020]은 세밀한 코딩 상호작용을 포착하나, **데이터 사이언스 교육**은 코드, 데이터 도구, 시각적 분석, AI 지원 탐색을 포괄하여 근본적으로 다르다.

### 2.4 교육에서의 AI 튜터링과 의존도

LLM 기반 AI 튜터의 급속한 도입은 학생 의존도에 대한 우려를 제기하였다 [Kasneci et al., 2023; Becker et al., 2023]. AI 튜터는 효과적 스캐폴딩을 제공할 수 있으나 [Koedinger & Aleven, 2007], 과의존은 깊은 학습과 메타인지 발달을 저해할 수 있다 [Deci & Ryan, 2000]. 최근 연구는 AI 지원 코딩 교육에서 "자동화 안주" 현상을 기록—높은 AI 사용 학생이 동등한 단기 성과를 보이나 전이와 보유에서 낮은 결과를 보인다 [Prather et al., 2023; Finnie-Ansley et al., 2023]. 그러나 **기존 시각화 도구 중 AI 튜터 사용 패턴을 대규모로 모니터링하고 분류하는 기능을 제공하는 것은 없다**—CodleViz의 AI 의존도 글리프가 직접 해결하는 공백이다.

### 2.5 AI 리터러시: 정의와 측정의 도전

AI 리터러시는—AI 기술을 비판적으로 평가하고, 효과적으로 사용하며, 소통하는 데 필요한 역량으로 광범위하게 정의되며 [Long & Magerko, 2020]—생성형 AI가 교육과 직업에 스며들면서 핵심 관심사가 되었다. Ng et al. [2021]은 AI 이해, AI 활용·적용, AI 평가·생성, AI 윤리의 4차원 프레임워크를 제안하였다. Laupichler et al. [2022]은 체계적 리뷰를 통해 지식 기반, 역량 기반, 태도 기반 AI 리터러시 측정 접근법을 식별하였다.

현재 측정 도구는 압도적으로 설문 기반이다: AI에 대한 인지된 지식이나 태도를 평가하는 자기보고식 설문지 [Wang et al., 2022; Carolus et al., 2023]. 이러한 도구는 선언적 지식("기계학습의 작동 원리를 이해한다")을 포착하나, 절차적 역량—실제 과제에서 AI 도구에 접근할 때 사람들이 어떻게 행동하는지—은 포착하지 못한다. 자기보고된 AI 이해와 실제 AI 사용 행동 간의 격차는 인접 분야에서 잘 기록되어 있다 [Kruger & Dunning, 1999].

AI 리터러시의 행동적 측정 접근법은 학습자가 AI 도구에 대해 *말하는* 것이 아니라 AI 도구로 *하는* 것을 분석하는 것을 요구한다. 이는 AI 도구가 실제 과제에 내장된 플랫폼의 로그 수준 데이터를 필요로 한다—정확히 CodleViz가 작동하는 데이터 환경이다. 본 시스템은 설문이 아닌 행동 분석을 통해 AI 리터러시 측정을 다룬다: 과제 성과와 AI 상호작용 패턴을 통합 시각화하여 역량과 AI 의존도 차원을 따라 학습자를 분류한다.

### 2.6 요약 및 포지셔닝

CodleViz는 이 다섯 분야의 교차점에서, 생성형 AI 사용 로그와 멀티모달 과제 성과 데이터를 통합하여 **행동적 AI 리터러시 측정**을 위한 시각적 분석 시스템을 제공한다. 표 1은 CodleViz가 6개 차원에서 기존 시스템의 역량을 어떻게 확장하는지 요약한다.

| 시스템 | 다단계 | 역량 | AI 사용 | 멀티모달 | 학교 간 | AI 리터러시 |
|--------|:------:|:----:|:-------:|:--------:|:-------:|:-----------:|
| VisMOOC | — | — | — | — | — | — |
| CourseVis | — | 부분 | — | — | — | — |
| eLAT | 부분 | — | — | 부분 | — | — |
| Mastery Grids | — | 부분 | — | — | — | — |
| 설문 도구 | — | — | — | — | — | 부분 |
| CodleViz | 전체 | 전체 | 전체 | 전체 | 전체 | 전체 |

문헌의 핵심 공백은 자기보고가 아닌 행동 데이터를 통해 AI 리터러시를 측정하는 시스템의 부재이다. CodleViz는 과제 성과와 생성형 AI 상호작용 로그를 통합 분석하여 진정한 역량과 AI로 부풀려진 성과를 구별할 수 있게 하는 최초의 VA 시스템이다.
