# 2. Related Work

## English

### 2.1 Visual Analytics for Education

Visual analytics has been increasingly applied to educational contexts, spanning higher education, MOOCs, and K-12 settings. Systems such as VisMOOC [Shi et al., 2015] and CourseVis [Mazza & Dimitrova, 2007] visualize student engagement in online courses through clickstream analysis and forum participation patterns. PeerLens [Wang et al., 2016] supports peer review analytics in programming courses. More recently, VISKnowledge [ref] introduced knowledge graph visualizations for adaptive learning systems.

However, most existing educational VA systems focus on **single-modality data**—either forum posts, video interactions, or grade distributions—rather than the multimodal learning activities characteristic of data science education. Furthermore, few systems address **K-12 contexts**, where student populations span multiple schools with varying curricula and teacher expertise levels.

### 2.2 Learning Analytics Dashboards

Learning analytics dashboards (LADs) have emerged as a primary interface between learning data and educators [Verbert et al., 2013; Schwendimann et al., 2017]. Commercial platforms such as Canvas Analytics, Google Classroom Insights, and Khan Academy's teacher dashboard provide aggregate metrics including completion rates, time-on-task, and assessment scores.

Research-oriented LADs have explored more sophisticated visualizations. eLAT [Dyckhoff et al., 2012] combines multiple learning indicators into an exploratory analysis tool. The Student Activity Dashboard [ref] tracks behavioral patterns over time. Mastery Grids [Loboda et al., 2014] visualizes topic-level mastery in intelligent tutoring systems.

Despite these advances, current LADs exhibit three key limitations: (1) they rarely support **multi-level drill-down** from institutional overview to individual student, (2) they do not visualize **competency development trajectories** across structured curricula, and (3) they lack support for analyzing **AI tutor interaction patterns**, which are increasingly prevalent in modern learning platforms.

### 2.3 Multimodal Learning Analytics

Multimodal learning analytics (MMLA) integrates data from diverse sources—video, audio, physiological sensors, log data—to provide holistic understanding of learning processes [Blikstein & Worsley, 2016; Ochoa & Worsley, 2016]. Recent work has explored combining gaze tracking with system logs [Sharma et al., 2020], integrating discourse analysis with behavioral patterns [ref], and fusing code analysis with problem-solving trajectories [ref].

In the context of programming education, tools such as ProgSnap [Price et al., 2017] and CodeWorkout [ref] capture fine-grained coding interactions. However, **data science education** differs fundamentally from programming—it encompasses not only code but also data manipulation tools (CODAP, spreadsheets), visual analysis, collaborative interpretation, and AI-assisted exploration.

CodleViz addresses the intersection of these three areas by providing a visual analytics system specifically designed for **multimodal K-12 data science education**, supporting multi-level exploration of learning patterns that span code, behavior, and competency dimensions.

---

## 한글

### 2.1 교육을 위한 시각적 분석

시각적 분석은 고등교육, MOOC, K-12 환경을 아우르며 교육 분야에 점점 더 많이 적용되고 있다. VisMOOC [Shi et al., 2015]과 CourseVis [Mazza & Dimitrova, 2007] 같은 시스템은 클릭스트림 분석과 포럼 참여 패턴을 통해 온라인 강좌에서의 학생 참여도를 시각화한다. PeerLens [Wang et al., 2016]는 프로그래밍 수업에서 동료 평가 분석을 지원한다. 최근에는 VISKnowledge [ref]가 적응형 학습 시스템을 위한 지식 그래프 시각화를 도입하였다.

그러나 대부분의 기존 교육 VA 시스템은 데이터 사이언스 교육의 특성인 멀티모달 학습 활동이 아닌, **단일 모달리티 데이터**(포럼 게시물, 영상 상호작용, 성적 분포 중 하나)에 초점을 맞추고 있다. 또한 다양한 커리큘럼과 교사 전문성 수준을 가진 여러 학교에 걸친 학생 집단이 존재하는 **K-12 맥락**을 다루는 시스템은 거의 없다.

### 2.2 학습 분석 대시보드

학습 분석 대시보드(LAD)는 학습 데이터와 교육자 사이의 주요 인터페이스로 부상하였다 [Verbert et al., 2013; Schwendimann et al., 2017]. Canvas Analytics, Google Classroom Insights, Khan Academy 교사 대시보드 등 상용 플랫폼은 완료율, 학습 시간, 평가 점수 등 집계 지표를 제공한다.

연구 지향 LAD는 더 정교한 시각화를 탐구해 왔다. eLAT [Dyckhoff et al., 2012]는 다수의 학습 지표를 탐색적 분석 도구로 결합한다. Mastery Grids [Loboda et al., 2014]는 지능형 튜터링 시스템에서 주제별 숙달도를 시각화한다.

이러한 발전에도 불구하고, 현재 LAD는 세 가지 핵심 한계를 보인다: (1) 기관 전체 개요에서 개별 학생까지의 **다단계 드릴다운**을 거의 지원하지 않고, (2) 체계적 커리큘럼 전반에 걸친 **역량 발달 궤적**을 시각화하지 않으며, (3) 현대 학습 플랫폼에서 점점 더 보편화되고 있는 **AI 튜터 상호작용 패턴** 분석을 지원하지 않는다.

### 2.3 멀티모달 학습 분석

멀티모달 학습 분석(MMLA)은 영상, 오디오, 생리 센서, 로그 데이터 등 다양한 소스의 데이터를 통합하여 학습 과정에 대한 전체적 이해를 제공한다 [Blikstein & Worsley, 2016; Ochoa & Worsley, 2016].

프로그래밍 교육 맥락에서 ProgSnap [Price et al., 2017]과 CodeWorkout [ref] 같은 도구가 세밀한 코딩 상호작용을 포착한다. 그러나 **데이터 사이언스 교육**은 프로그래밍과 근본적으로 다르다—코드뿐 아니라 데이터 조작 도구(CODAP, 스프레드시트), 시각적 분석, 협업적 해석, AI 지원 탐색을 포괄한다.

CodleViz는 **멀티모달 K-12 데이터 사이언스 교육**을 위해 특별히 설계된 시각적 분석 시스템을 제공함으로써, 코드, 행동, 역량 차원에 걸친 학습 패턴의 다단계 탐색을 지원하여 이 세 영역의 교차점을 다룬다.
