# 1. Introduction

## English

Generative AI tools are transforming how people learn, work, and solve problems. Students use LLM-powered tutors to debug code; professionals rely on AI assistants to draft reports; everyday users consult chatbots for medical and financial decisions. Yet a fundamental measurement gap persists: completion rates and task scores—the dominant metrics in learning platforms—cannot distinguish a person who builds genuine competence from one who silently outsources their thinking to an AI. Two students may both score 95% on a data science curriculum while exhibiting a 9x difference in AI tutor reliance. This gap is not merely academic. As AI tools become embedded in education and professional training, the inability to measure *how* people engage with AI—not just *what* they produce—undermines assessment validity, intervention design, and policy decisions about AI integration.

Measuring AI literacy at this level of granularity demands jointly analyzing three heterogeneous data streams: tabular performance records across sessions, temporal skill trajectories that reveal learning dynamics, and textual logs of human-AI interaction that expose reliance patterns. Existing learning analytics dashboards (LADs) were designed for a simpler era. Commercial platforms such as Canvas Analytics and Google Classroom Insights report aggregate completion rates and time-on-task. Research-oriented systems like eLAT [Dyckhoff et al., 2012] and Mastery Grids [Loboda et al., 2014] offer richer visualizations but still operate on single-modality data. None integrates generative AI usage logs with performance data in a unified analytical environment, and none provides the multi-level drill-down—from institutional overview to individual student—that educators need to act on patterns they discover.

Three specific analytical challenges remain unaddressed:

1. **AI dependency detection.** As AI tutors become ubiquitous, distinguishing productive scaffolding from counterproductive dependency requires simultaneous visualization of completion rates and AI usage patterns. No existing LAD provides this combination.

2. **Learning transition barrier identification.** Curricula with progressive difficulty structures (e.g., visual programming to text-based coding) create predictable but hard-to-locate performance drops. Manual inspection of session-level trends across dozens of classrooms is tedious and prone to oversight.

3. **Cross-classroom trajectory comparison.** Comparing learning trajectories across classrooms with different baseline levels and class sizes requires normalization and alignment techniques that go beyond simple line chart overlays.

We present **CodleViz**, a visual analytics system designed to measure AI literacy by integrating nine coordinated views with SHAP-based explainable diagnostics. CodleViz is built on data from an AI-integrated educational platform serving 709 students across 49 classrooms, with 6,270 LLM tutor interaction logs collected over 15 sessions of three thematic data science curricula. The system structures analysis as a four-level drill-down workflow (overview, school, classroom, student), enabling educators to move from pattern detection to root-cause reasoning to intervention decisions within a single environment. Beyond standard visualization components, CodleViz introduces three techniques:

- The **AI Dependency Glyph** simultaneously encodes completion rate, AI usage frequency, and reliance trend within a single composite glyph, classifying students into four behavioral quadrants and surfacing AI literacy differences invisible in completion data alone.

- The **Performance Cliff Detector** automatically identifies learning transition barriers by computing cliff severity and recovery rates in session-level temporal data, with SHAP-based causal explanations that link detected cliffs to specific contributing factors.

- The **Trajectory Alignment View** enables meaningful cross-classroom comparison through baseline-normalized small multiples, IQR trajectory envelopes, phase-aligned sparklines, and DTW-based trajectory clustering.

Our contributions are:

1. **The first visual analytics system integrating generative AI usage logs with task performance data for AI literacy measurement**—a domain not previously addressed in the visual analytics literature. The system combines tabular, temporal, and textual data streams from a live AI-embedded platform into a unified analytical environment.

2. **Three novel visual analytics techniques** that address gaps unmet by existing LADs: (a) the *AI Dependency Glyph*, a composite glyph encoding completion, AI usage frequency, and reliance trend to classify learners into four behavioral quadrants; (b) the *Performance Cliff Detector*, which automatically identifies and quantifies learning transition barriers with SHAP-based causal explanations; and (c) the *Trajectory Alignment View*, combining baseline normalization, IQR envelopes, and DTW-based clustering for cross-classroom comparison.

3. **CodleViz**, a coordinated multi-view system with four-level drill-down, nine views, and advanced features including linked brushing, at-risk student auto-detection, student comparison mode, session slider for temporal exploration, and configurable settings for AI-adjusted scores, XAI insights, and recommendations.

4. **A formative evaluation with 10 domain experts** (6 educators who taught on the platform, 4 external specialists including a university professor and education researchers) validated through structured decision tasks (70% accuracy on cliff detection, 70% on SHAP factor identification, 100% on at-risk student identification), a SUS usability score of 65.8, per-view usefulness ratings up to 4.8/5.0, and iterative refinement from v0.5 to v1.0 incorporating seven system improvements.

---

## 한글

생성형 AI 도구가 사람들의 학습, 업무, 문제 해결 방식을 근본적으로 바꾸고 있다. 학생은 LLM 기반 튜터로 코드를 디버깅하고, 전문가는 AI 어시스턴트로 보고서를 작성하며, 일반 사용자는 챗봇에 의료·재무 상담을 의뢰한다. 그러나 핵심적인 측정 공백이 지속되고 있다: 학습 플랫폼의 지배적 지표인 완료율과 과제 점수로는 진정한 역량을 쌓는 사람과 사고를 AI에 조용히 위임하는 사람을 구별할 수 없다. 데이터 사이언스 커리큘럼에서 두 학생 모두 95%를 달성하면서도 AI 튜터 의존도에서 9배 차이를 보일 수 있다. 이 공백은 학문적 문제에 그치지 않는다. AI 도구가 교육과 직업 훈련에 내장됨에 따라, 사람들이 AI와 *어떻게* 상호작용하는지—단순히 *무엇을* 생산하는지가 아닌—를 측정하지 못하는 것은 평가의 타당성, 개입 설계, AI 통합 정책 결정을 훼손한다.

이 수준의 세밀한 AI 리터러시 측정은 세 가지 이질적 데이터 스트림의 통합 분석을 요구한다: 세션별 테이블형 성과 기록, 학습 역학을 드러내는 시계열 역량 궤적, 의존 패턴을 노출하는 인간-AI 상호작용 텍스트 로그. 기존 학습 분석 대시보드(LAD)는 더 단순한 시대를 위해 설계되었다. Canvas Analytics, Google Classroom Insights 등 상용 플랫폼은 집계 완료율과 학습 시간을 보고한다. eLAT [Dyckhoff et al., 2012], Mastery Grids [Loboda et al., 2014] 등 연구 기반 시스템은 더 풍부한 시각화를 제공하나 여전히 단일 모달리티 데이터에서 작동한다. 생성형 AI 사용 로그와 성과 데이터를 통합 분석 환경에서 결합한 시스템은 없으며, 교육자가 발견한 패턴에 행동을 취하는 데 필요한 다단계 드릴다운(기관 개요부터 개별 학생까지)을 제공하는 시스템도 없다.

세 가지 구체적 분석 과제가 미해결로 남아 있다:

1. **AI 의존도 감지.** AI 튜터가 보편화됨에 따라, 생산적 스캐폴딩과 비생산적 의존을 구별하려면 완료율과 AI 사용 패턴의 동시 시각화가 필요하다. 기존 LAD 중 이 조합을 제공하는 것은 없다.

2. **학습 전환 장벽 식별.** 난이도 체계가 점진적인 커리큘럼(예: 시각적 프로그래밍에서 텍스트 기반 코딩으로의 전환)은 예측 가능하나 위치 파악이 어려운 성과 하락을 만든다. 수십 개 학급의 세션별 추세를 수동으로 검토하는 것은 번거롭고 누락이 발생하기 쉽다.

3. **학급 간 궤적 비교.** 기준선 수준과 학급 크기가 다른 학급 간 학습 궤적을 비교하려면 단순 라인 차트 중첩을 넘어서는 정규화와 정렬 기법이 필요하다.

본 논문은 9개 연동 뷰와 SHAP 기반 설명 가능 진단을 결합하여 AI 리터러시를 측정하도록 설계된 시각적 분석 시스템 **CodleViz**를 제안한다. CodleViz는 49개 학급 709명 학생이 참여하는 AI 통합 교육 플랫폼의 데이터를 기반으로 구축되었으며, 3개 주제별 데이터 사이언스 커리큘럼 15차시에 걸쳐 수집된 6,270건의 LLM 튜터 상호작용 로그를 포함한다. 분석 과정을 4단계 드릴다운 워크플로우(개요→학교→학급→학생)로 구조화하여, 교육자가 패턴 탐지에서 원인 추론, 개입 결정까지 단일 환경에서 수행할 수 있도록 한다. 표준 시각화 구성요소 외에 세 가지 기법을 도입한다:

- **AI 의존도 글리프**는 완료율, AI 사용 빈도, 의존 추세를 단일 복합 글리프에 동시 인코딩하여 학생을 4개 행동 사분면으로 분류하고, 완료 데이터만으로는 보이지 않는 AI 리터러시 차이를 드러낸다.

- **성과 절벽 감지기**는 세션별 시계열 데이터에서 절벽 심각도와 회복률을 계산하여 학습 전환 장벽을 자동 감지하며, 감지된 절벽을 특정 기여 요인에 연결하는 SHAP 기반 원인 설명을 제공한다.

- **궤적 정렬 뷰**는 기준선 정규화 스몰 멀티플, IQR 궤적 포락선, 단계별 스파크라인, DTW 기반 궤적 클러스터링을 통해 학급 간 의미 있는 비교를 가능하게 한다.

본 논문의 기여:

1. **생성형 AI 사용 로그와 과제 성과 데이터를 AI 리터러시 측정을 위해 통합한 최초의 시각적 분석 시스템**—시각적 분석 문헌에서 이전에 다루어지지 않은 도메인. 실제 AI 내장 플랫폼의 테이블형, 시계열, 텍스트 데이터 스트림을 통합 분석 환경으로 결합한다.

2. **기존 LAD의 공백을 해소하는 3개 새로운 시각적 분석 기법**: (a) *AI 의존도 글리프*—완료율, AI 사용 빈도, 의존 추세를 인코딩하여 학습자를 4개 행동 사분면으로 분류하는 복합 글리프; (b) *성과 절벽 감지기*—SHAP 기반 원인 설명과 함께 학습 전환 장벽을 자동 감지·정량화; (c) *궤적 정렬 뷰*—기준선 정규화, IQR 포락선, DTW 기반 클러스터링을 결합한 학급 간 비교.

3. **CodleViz 시스템**: 4단계 드릴다운, 9개 뷰, 연동 브러싱, 위험 학생 자동 감지, 학생 비교 모드, 시간 탐색용 세션 슬라이더, AI 보정 점수·XAI 인사이트·추천 설정 토글 등 고급 기능을 갖춘 연동형 다중 뷰 시스템.

4. **10명 도메인 전문가 대상 형성 평가** (플랫폼에서 실제 수업한 교육자 6명, 대학교수 및 교육 연구자를 포함한 외부 전문가 4명): 구조화 의사결정 과제(절벽 감지 정확도 70%, SHAP 요인 식별 70%, 위험 학생 식별 100%), SUS 사용성 65.8점, 뷰 유용성 최대 4.8/5.0, v0.5에서 v1.0으로 7개 시스템 개선을 포함한 반복적 정제를 통해 검증.
