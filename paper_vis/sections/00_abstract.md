# Title & Abstract

## Title

**Beyond Completion Rates: Visual Analytics for Measuring AI Literacy with Explainable Diagnostics**

## English Abstract (for PCS submission)

Generative AI is rapidly permeating education, work, and daily life, yet we lack systematic methods for measuring how people actually use these tools. Do they build genuine competence, or silently outsource their thinking? Answering this question—assessing AI literacy—demands more than completion rates; it requires jointly analyzing tabular performance records, temporal skill trajectories, and textual logs of human-AI interaction. No prior work has integrated these heterogeneous data streams from a live generative-AI-embedded platform into a unified analytical environment. Existing dashboards, built around aggregate metrics, cannot distinguish a student who masters a concept independently from one who reaches the same score by copying AI-generated answers.

We present CodleViz, the first visual analytics system designed to measure AI literacy by combining nine coordinated views with SHAP-based explainable diagnostics. Built on data from an AI-integrated educational platform (709 students, 49 classrooms, 6,270 LLM tutor interaction logs collected over 15 sessions), CodleViz structures the analytical process as a four-level drill-down workflow (overview → school → classroom → student), enabling educators to move from pattern detection to root-cause reasoning to intervention decisions within a single environment. The system introduces three techniques: (1) an AI Dependency Glyph that encodes completion rate, AI usage frequency, and reliance trend to classify students into four behavioral quadrants, surfacing AI literacy differences invisible in completion data alone; (2) a Performance Cliff Detector that automatically identifies learning transition barriers in session-level temporal data and provides SHAP-based causal explanations; and (3) a Trajectory Alignment View for cross-classroom comparison through baseline normalization and IQR envelopes.

Three case studies demonstrate AI literacy measurement in practice: students with identical completion rates exhibit 9× differences in AI reliance, 8 of 42 classrooms show >15%p performance drops at skill transitions, and curriculum design measurably affects competency development (35.8%–61.9% variance). A formative evaluation with 10 domain experts (6 educators who taught on the platform, 4 external specialists) validated the system through structured decision tasks (70% accuracy on cliff detection, 70% on SHAP factor identification, 100% on at-risk student identification), a SUS usability score of 65.8, and per-view usefulness ratings up to 4.8/5.0. While grounded in education, the framework of jointly visualizing task performance and generative AI usage patterns establishes a foundation for measuring AI literacy across professional and everyday contexts.

## 한글 제목

**완료율을 넘어서: 설명 가능한 진단을 통한 AI 리터러시 측정을 위한 시각적 분석**

## 한글 Abstract

생성형 AI가 교육, 업무, 일상에 빠르게 스며들고 있지만, 사람들이 이 도구를 실제로 어떻게 활용하는지 체계적으로 측정하는 방법은 부재하다. 진정한 역량을 쌓는 것인지, 사고를 조용히 AI에 위임하는 것인지? 이 질문에 답하려면—즉 AI 리터러시를 평가하려면—완료율 이상이 필요하다: 테이블형 성과 기록, 시계열 역량 궤적, 인간-AI 상호작용 텍스트 로그를 통합 분석해야 한다. 생성형 AI가 내장된 실제 플랫폼에서 이러한 이질적 데이터 스트림을 통합 분석 환경으로 결합한 선행 연구는 없다. 집계 지표 기반의 기존 대시보드로는 개념을 독립적으로 숙달한 학생과 AI 생성 답변을 그대로 사용하여 동일 점수에 도달한 학생을 구별할 수 없다.

본 논문은 AI 리터러시를 측정하기 위해 9개 연동 뷰와 SHAP 기반 설명 가능 진단을 결합한 최초의 시각적 분석 시스템 CodleViz를 제안한다. AI 통합 교육 플랫폼의 데이터(709명 학생, 49개 학급, 15차시에 걸쳐 수집된 6,270건 LLM 튜터 상호작용 로그)를 기반으로 구축하였으며, 분석 과정을 4단계 드릴다운 워크플로우(전체→학교→학급→학생)로 구조화하여 교육자가 패턴 탐지에서 원인 추론, 개입 결정까지 단일 환경에서 수행할 수 있도록 한다. 3개 기법을 도입한다: (1) AI 의존도 글리프—완료율, AI 사용 빈도, 의존 추세를 인코딩하여 학생을 4개 행동 사분면으로 분류하고, 완료 데이터만으로는 보이지 않는 AI 리터러시 차이를 드러냄, (2) 성과 절벽 감지기—세션별 시계열 데이터에서 학습 전환 장벽을 자동 감지하고 SHAP 기반 원인 설명을 제공, (3) 궤적 정렬 뷰—기준선 정규화와 IQR 포락선을 통한 학급 간 비교를 지원.

3개 사례 연구가 실제 AI 리터러시 측정을 시연한다: 동일 완료율 학생 간 AI 의존도 9배 차이, 42개 학급 중 8개에서 역량 전환 시 15%p 이상 성과 하락, 커리큘럼 설계에 따른 역량 발달 차이(35.8%~61.9%). 10명 전문가 대상 형성 평가(플랫폼에서 실제 수업한 교육자 6명, 외부 전문가 4명)는 구조화 의사결정 과제(절벽 감지 정확도 70%, SHAP 요인 식별 70%, 위험 학생 식별 100%), SUS 사용성 65.8점, 뷰 유용성 최대 4.8/5.0으로 시스템을 검증하였다. 본 연구는 교육에 기반하지만, 과제 성과와 생성형 AI 사용 패턴을 통합 시각화하는 프레임워크는 전문 업무 및 일상적 맥락에서의 AI 리터러시 측정을 위한 토대를 제공한다.

---

## Paper Figure Mapping (NewVis 폴더)

| Fig # | 파일명 | 논문 위치 | 크기 |
|-------|--------|----------|------|
| Fig 1 | `Dashboard.png` | System Overview (§4.1) — Teaser | double |
| Fig 2 | `fig2_cliff_heatmap.svg` | Cliff Detector (§4.9) | double |
| Fig 3 | `fig3_trajectory.svg` | Trajectory Alignment (§4.10) | double |
| Fig 4a | `fig4a_ai_dependency.svg` | AI Dependency Scatter (§4.8) | single |
| Fig 4b | `fig4b_ai_usage_session.svg` | AI Usage by Session (§4.6) | single |
| Fig 5 | `fig5_student_heatmap.svg` | Student Heatmap (§4.5) | double |
| Fig 6 | `fig6_activity.svg` | Activity Distribution (§4.7) | double |
| Fig 7 | `fig7_shap_importance.svg` | SHAP Feature Importance (§4.9 XAI) | double |
| Fig 8 | `fig8_raw_vs_adjusted.svg` | Raw vs AI-Adjusted Competency (§4.11) | double |
| Fig 9 | `fig9_score_scatter.svg` | Individual Score Adjustment (§4.11) | single |
| Fig 10 | `fig10_sparklines.svg` | Phase Sparklines (§5.1) | double |
| — | `AI Dependency.png` | Dashboard detail: 4분면 도넛 | — |
| — | `AI Tutor Usage.png` | Dashboard detail: 세션별 LLM 사용 | — |
| — | `Competency Scores.png` | Dashboard detail: Raw/Adjusted 토글 | — |
| — | `Learning Journey.png` | Dashboard detail: DR6 Cliff Alert | — |
| — | `XAI : Cliff Risk Factors.png` | Dashboard detail: SHAP 바 차트 | — |
| — | `XAI : Cliff Explanation.png` | Dashboard detail: Session 7 SHAP 카드 | — |
