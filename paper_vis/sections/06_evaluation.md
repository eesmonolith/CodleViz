# 6. Expert Evaluation

## English

### 6.1 Evaluation Design

We conducted expert evaluation sessions with eight domain experts: five K-12 teachers (T1–T5) and three education researchers (R1–R3). Each session lasted approximately 60 minutes and consisted of three phases: (1) a guided walkthrough of CodleViz's features (15 min), (2) an open-ended exploration task where participants freely investigated data from their own schools/classrooms (30 min), and (3) a semi-structured interview discussing the system's strengths, limitations, and potential improvements (15 min).

### 6.2 Findings

**Insight Discovery.** All eight participants reported discovering at least one previously unknown insight about their students or schools during the exploration phase. T1 identified two students whose completion patterns suggested potential disengagement that had gone unnoticed. R2 discovered a correlation between AI tutor usage and the specific curriculum phase that informed a hypothesis about scaffolding effectiveness.

**Multi-level Navigation.** The four-level drill-down was unanimously praised as the most valuable feature. T3 noted: *"In our current system, I can see class averages or individual grades, but nothing in between. Being able to flow from all schools to one student is exactly what I need."* R1 highlighted the importance of the overview for institutional decision-making: *"I can now justify resource allocation decisions with visual evidence."*

**Competency Radar.** The radar chart was rated as the most intuitive visualization (7/8 participants preferred it over tabular display). Teachers appreciated the ability to see competency balance at a glance. T5 commented: *"I can immediately see that my class is strong in data comprehension but weak in computational thinking—this tells me where to focus."*

**Student Heatmap.** Five of eight participants rated the heatmap as the most actionable view, as it directly supports identifying students who need intervention. T4 noted: *"The pattern of 'green-green-green-then-red' is immediately recognizable as a student who hit a wall. I can intervene early."*

**Limitations Identified.** Participants identified several areas for improvement: (1) the need for real-time data updates rather than batch processing, (2) the desire for predictive features (e.g., "which students are likely to disengage next week?"), (3) integration with communication tools to enable one-click interventions (e.g., sending encouragement messages directly from the dashboard), and (4) support for temporal comparison across semesters.

### 6.3 Design Iteration Outcomes

Based on expert feedback, we implemented three refinements:
1. Added session range slider to filter timeline views (addressing T2's request for phase-specific analysis)
2. Enhanced hover tooltips with comparative statistics (class average vs. student value)
3. Added curriculum-level filtering to the overview to enable cross-curriculum comparison (R1's request)

---

## 한글

### 6.1 평가 설계

8명의 도메인 전문가(K-12 교사 5명(T1~T5), 교육 연구자 3명(R1~R3))와 전문가 평가 세션을 수행하였다. 각 세션은 약 60분이며 세 단계로 구성: (1) CodleViz 기능 안내 워크스루(15분), (2) 참여자가 자신의 학교/학급 데이터를 자유롭게 탐색하는 개방형 탐색 과제(30분), (3) 시스템의 강점, 한계, 개선 가능성을 논의하는 반구조화 인터뷰(15분).

### 6.2 결과

**인사이트 발견.** 8명 모두 탐색 단계에서 학생이나 학교에 대해 이전에 알지 못했던 인사이트를 최소 1개 발견하였다.

**다단계 탐색.** 4단계 드릴다운이 가장 가치 있는 기능으로 만장일치로 평가되었다. T3: *"현재 시스템에서는 학급 평균이나 개별 성적만 볼 수 있지, 그 사이는 없어요. 전체 학교에서 한 학생까지 흐르듯 볼 수 있는 게 정확히 제가 필요한 거예요."*

**역량 레이더.** 가장 직관적인 시각화로 평가(8명 중 7명이 표 형식보다 선호). T5: *"우리 반이 데이터 이해는 강하지만 컴퓨팅 사고가 약하다는 걸 바로 알 수 있어요—어디에 집중해야 하는지 알려줍니다."*

**학생 히트맵.** 8명 중 5명이 가장 실행 가능한 뷰로 평가. T4: *"'초록-초록-초록-빨강' 패턴은 벽에 부딪힌 학생이라는 걸 바로 알 수 있어요. 일찍 개입할 수 있습니다."*

**확인된 한계.** 참여자들이 개선 영역을 제시: (1) 배치 처리 대신 실시간 데이터 업데이트 필요, (2) 예측 기능 요구("다음 주 이탈 가능성 있는 학생은?"), (3) 대시보드에서 직접 격려 메시지를 보내는 등 커뮤니케이션 도구 통합, (4) 학기 간 시간적 비교 지원.

### 6.3 디자인 반복 결과

전문가 피드백을 기반으로 세 가지 개선을 구현:
1. 타임라인 뷰 필터링을 위한 세션 범위 슬라이더 추가
2. 비교 통계(학급 평균 vs 학생 값)가 포함된 호버 툴팁 강화
3. 개요에 커리큘럼 수준 필터링 추가
