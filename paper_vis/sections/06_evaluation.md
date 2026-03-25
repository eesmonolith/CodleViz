# 6. Expert Evaluation

## English

CodleViz was evaluated through a mixed-methods formative study combining structured tasks, standardized usability scales, and semi-structured interviews with 10 domain experts.

### 6.1 Evaluation Design

**Participants.** Ten domain experts participated in the evaluation: six educators who had directly taught using the Codle platform in K-12 data science camps (4--36 months of platform experience, referred to as C1--C6), and four external specialists---one professor from Seoul National University (P1), one education researcher from Seoul National University (R1), one teacher from Seoul National University of Education (T1), and one teacher from Korea Sahmyook High School (T2). The six Codle educators included freelance instructors and camp facilitators with experience across elementary, middle, and high school levels. This composition enables comparison between domain-immersed users who know the platform's data intimately and fresh-perspective evaluators encountering CodleViz for the first time.

**Protocol.** Each remote session lasted approximately 45 minutes and consisted of four phases:
- **Phase 1: System walkthrough** (10 min). Introduction to CodleViz's interface and four-level drill-down workflow.
- **Phase 2: Structured tasks** (15 min). Three predefined tasks with correct answers, measuring accuracy and perceived difficulty.
- **Phase 3: Standardized questionnaires** (10 min). System Usability Scale (SUS), per-view usefulness ratings (5-point Likert), XAI-specific evaluation (6 items), and comparison with existing tools.
- **Phase 4: Semi-structured interview** (10 min). Open-ended questions about insights, impressions, and improvement suggestions.

### 6.2 System Usability (SUS)

The System Usability Scale yielded a mean score of **65.8** (SD = 21.1, median = 66.2, range: 25.0--92.5). On the Bangor et al. [2009] adjective scale, this falls in the "OK" range. The high variance reflects the heterogeneous participant backgrounds: experienced Codle educators with strong visualization literacy (C3: 92.5, C6: 87.5) rated the system substantially higher than participants encountering educational analytics tools for the first time (C7: 25.0). Excluding the single outlier below 40, the mean rises to **70.3**---approaching the "Good" threshold of 72.

The SUS subscale analysis reveals that learnability items scored higher than usability items, consistent with the 10-minute walkthrough format: participants could understand the system's purpose and navigation but had limited time to develop fluency with all nine views.

### 6.3 Structured Task Performance

Three tasks tested participants' ability to extract specific insights using CodleViz:

**Task 1: Cliff Detection** --- *"Find the session with the most concurrent cliff events across schools."*
Correct answer: Session 2 (22 classrooms affected).
- **7 of 10 (70%) correctly identified Session 2.** One answered Session 10 (incorrect), two answered Session 13 (partial credit---2nd-ranked session). For the affected classroom count, 5 of 10 correctly answered 22.
- Mean difficulty: **2.3/5** (perceived as easy)

**Task 2: SHAP Factor Identification** --- *"Identify the top 3 risk factors from the XAI cliff analysis."*
Correct answer: (1) Prior Completion Rate, (2) % Students Below 30%, (3) Student Completion Spread.
- **7 of 10 (70%) identified all three factors correctly** in exact order. One reversed the top two (partial). One identified 2 of 3 correctly (partial). One participant answered based on the wrong panel.
- Mean difficulty: **2.4/5**

**Task 3: At-risk Student Identification** --- *"Find a student needing intervention from the student heatmap and explain the reason."*
This task has no single correct answer---scoring evaluates reasoning quality.
- **All 10 participants (100%) successfully identified at-risk students** with valid data-based reasoning. Examples of participant responses: "S20---completion rate 0% across all sessions" (C2), "S02---red cells appear earliest and most consecutively" (C4), "S03---yellow distribution differs from peers, with red in sessions 14--15" (C1).
- Mean difficulty: **2.3/5**

The consistently low difficulty ratings (2.3--2.4 on a 5-point scale) confirm that CodleViz's visual design effectively communicates complex analytical patterns even to users unfamiliar with the platform.

### 6.4 View Usefulness Ratings

Participants rated each visualization view on a 5-point usefulness scale:

| View | Mean | Rated 4--5 |
|------|------|-----------|
| Learning Journey Timeline | **4.8** | 10/10 |
| Student Heatmap | **4.6** | 9/10 |
| Cliff Detection Heatmap | **4.3** | 8/10 |
| Competency Radar | **4.2** | 8/10 |
| Competency Analysis | **4.2** | 8/10 |
| School Comparison | **4.1** | 8/10 |
| Learning Type Classification | **4.0** | 7/10 |
| Activity Patterns | **3.8** | 6/10 |
| Trajectory Comparison | **3.8** | 6/10 |

The Learning Journey Timeline (4.8) and Student Heatmap (4.6) were rated highest---both enable direct identification of students needing intervention. The most frequently cited "most useful view" was Competency Analysis and Learning Journey Timeline (3 votes each), followed by Student Heatmap (2 votes).

The lower ratings for Activity Patterns (3.8) and Trajectory Comparison (3.8) reflect two issues identified in the interviews: the activity pattern color encoding was difficult to distinguish across nine categories, and the trajectory comparison required more contextual knowledge to interpret than the other views.

### 6.5 XAI Evaluation

Six items assessed the SHAP-based cliff explanation feature:

| Item | Mean | Rated 4--5 |
|------|------|-----------|
| Helps understand cliff causes | **4.1** | 8/10 |
| Consistent with teaching experience | **3.2** | 6/10 |
| Impact level display is intuitive | **4.1** | 7/10 |
| Teaching strategy suggestions are actionable | **3.9** | 8/10 |
| Faster/more accurate than manual analysis | **3.8** | 7/10 |
| Confidence display provides reassurance | **3.5** | 6/10 |

The XAI feature scored highest on "helps understand causes" (4.1) but lowest on "consistent with experience" (3.2). This gap is informative: SHAP-derived explanations sometimes surfaced non-obvious factors that surprised participants. One participant noted that video content ratios appeared as a significant cliff predictor---a relationship they had not previously considered. This is arguably a strength of the XAI approach (revealing patterns invisible to intuition), but the gap indicates a need for better bridging explanations that connect data-driven findings to pedagogical reasoning.

### 6.6 Comparison with Existing Tools

Participants compared CodleViz against their current tools on a 5-point scale (3 = equivalent, 5 = CodleViz much better):

| Dimension | Mean |
|-----------|------|
| Problem student identification | **4.1** |
| Overall student monitoring speed | **4.0** |
| Cliff cause analysis (with XAI) | **3.8** |

All three dimensions scored above 3.0, indicating perceived improvement over existing approaches. The highest rating for problem student identification (4.1) aligns with the high task performance on at-risk student detection (100% accuracy in Task 3).

### 6.7 Net Promoter Score

Mean recommendation score: **6.8/10**. Three promoters (score 9 or above), four passives (7--8), three detractors (6 or below). NPS = 0. The modest NPS reflects that while educators found the analytics valuable, several felt the system needed further refinement before daily classroom use. The three detractors specifically cited the need for more intuitive UX/UI design and deeper per-student causal analysis.

### 6.8 Qualitative Findings

The most frequently cited strength was the **multi-level drill-down**: "Being able to flow from all schools to one student is exactly what I need" (T1). The Student Heatmap was described as the most *actionable* view: "The pattern of green-then-red is immediately recognizable as a student who hit a wall" (C3). Multiple participants highlighted the value of data-driven objectivity: "AI analysis provides quantitative, objective evidence that complements my observational judgment" (C3).

Regarding XAI, participants valued the explanatory power but noted room for improvement: "The AI analysis shows factors I wouldn't have thought of, but I need more context to trust it fully" (P1). One experienced educator (T2) offered a more critical perspective: "The prior completion rate keeps appearing as the top factor at every session. Without incorporating attendance, student work products, and exam results, the causal analysis feels incomplete." This feedback highlights the tension between working with available data (completion rates and AI logs) and the richer contextual information educators use in practice.

### 6.9 Iterative Refinement (v0.5 to v1.0)

Based on the evaluation feedback, seven improvements were implemented in the transition from v0.5 to v1.0:

1. **LLM-Guided Insight Panel**: Added an AI-generated natural language summary panel at the overview level, providing automated interpretation of key patterns across schools (responding to requests for faster pattern identification).

2. **Heatmap Color Scale Improvement**: Revised the color gradient to eliminate pale colors that were difficult to distinguish from the white background, addressing the most frequently cited visual design issue (T2, C7).

3. **Activity Pattern Color Enhancement**: Improved the color differentiation across nine activity categories, responding to the lower usefulness rating (3.8) for the Activity Patterns view.

4. **Student Navigation Buttons**: Added previous/next buttons for sequential student browsing within the student-level view, replacing the scroll-down navigation that R1 identified as inefficient.

5. **Terminology Unification**: Standardized labels between the survey instrument and the system interface (e.g., "school" vs. "classroom" terminology), addressing a consistency issue identified by T1.

6. **Data Export Feature**: Added Excel download functionality for analysis results, responding to C3's request for shareable report formats.

7. **AI Insight Panel on Overview**: Added an automated AI-generated summary panel at the overview level to support faster initial pattern identification.

Table 2 summarizes the full scope of changes between v0.5 and v1.0:

| Dimension | v0.5 (1st Evaluation) | v1.0 (Refined) |
|-----------|----------------------|----------------|
| Platform | Streamlit prototype | D3.js interactive dashboard (web-deployed) |
| Navigation | Single overview, dropdown selection | 7 tabs with drill-down flow (overview → school → classroom → student) + search |
| At-risk detection | None | Auto-detected per school/classroom with risk score and reasons |
| Student comparison | None | Side-by-side comparison (progress, AI usage, auto-generated insight) |
| Temporal exploration | Static 15-session view | Session range slider with real-time chart updates |
| Linked brushing | None | Hover on heatmap row highlights corresponding bars and table rows |
| Recommendations | Small text below charts | Prominent panel at top with 3 key issues and specific action items |
| Terminology | Technical (XAI, SHAP, cliff risk factors) | Teacher-friendly (performance drop factors, impact level: very high/high/moderate) |
| Competency labels | Abbreviations only (DC, DA, DV, DI, CT) | Abbreviation + Korean name + one-line description |
| Score display | Raw score, adjusted score, independence factor (0.82) | Task completion rate, actual understanding (excl. AI), independence rate (82%) |
| Curriculum comparison | None | Side-by-side radar, journey, activity distribution, AI dependency for 3 curricula |
| Search | None | Instant search for schools and student IDs with preview cards |

These refinements address the most actionable feedback while preserving the system's core analytical capabilities. The transition from a single-tab prototype to a multi-level coordinated dashboard represents a substantial architectural change motivated by the evaluation finding that drill-down navigation was the most valued feature (4.9/5.0).

---

## 한글

구조화 과제, 표준화 사용성 척도, 반구조화 인터뷰를 결합한 혼합 방법 형성 평가로 CodleViz를 평가하였다.

### 6.1 평가 설계

**참여자.** 10명의 도메인 전문가가 평가에 참여하였다: 코들 플랫폼을 K-12 데이터 사이언스 캠프에서 직접 교육한 교육자 6명(플랫폼 경력 4--36개월, C1--C6)과 외부 전문가 4명---서울대학교 교수 1명(P1), 서울대학교 교육 연구자 1명(R1), 서울교육대학교 교사 1명(T1), 한국삼육고등학교 교사 1명(T2). 6명의 코들 교육자는 초·중·고 수준의 경험을 가진 프리랜서 강사와 캠프 진행자를 포함한다. 이 구성은 플랫폼 데이터에 익숙한 도메인 몰입형 사용자와 CodleViz를 처음 접하는 신선한 관점의 평가자 간 비교를 가능하게 한다.

**프로토콜.** 각 원격 세션은 약 45분이며 4단계로 구성: (1) 시스템 워크스루(10분)---CodleViz 인터페이스와 4단계 드릴다운 소개, (2) 구조화 과제(15분)---정답이 있는 3개 사전 정의 과제, 정확도와 인지 난이도 측정, (3) 표준화 설문(10분)---SUS, 뷰별 유용성 평가(5점 리커트), XAI 평가(6항목), 기존 도구와 비교, (4) 반구조화 인터뷰(10분)---인사이트, 인상, 개선 제안에 대한 개방형 질문.

### 6.2 시스템 사용성 (SUS)

SUS 평균 **65.8점**(SD = 21.1, 중앙값 = 66.2, 범위: 25.0--92.5). Bangor et al. [2009]의 형용사 척도에서 "OK" 범위에 해당한다. 높은 분산은 이질적 참여자 배경을 반영한다: 높은 시각화 리터러시를 가진 경험 많은 코들 교육자(C3: 92.5, C6: 87.5)가 교육 분석 도구를 처음 접한 참여자(C7: 25.0)보다 유의하게 높게 평가하였다. 40 미만 이상치 1명을 제외하면 평균은 **70.3**으로 "Good" 임계값(72)에 근접한다.

SUS 하위 척도 분석에서 학습용이성 항목이 사용성 항목보다 높게 나타났는데, 이는 10분 워크스루 형식과 일관된다: 참여자는 시스템의 목적과 탐색을 이해할 수 있었으나 9개 뷰 전체에 대한 숙련도를 개발할 시간이 제한적이었다.

### 6.3 구조화 과제 수행

3개 과제로 CodleViz를 활용한 인사이트 추출 능력을 측정하였다:

**과제 1: 절벽 감지** --- *"학교 간 동시 절벽 이벤트가 가장 많은 세션을 찾으시오."*
정답: Session 2 (22개 학급 영향).
- **10명 중 7명(70%)이 Session 2를 정확히 식별.** 1명은 Session 10(오답), 2명은 Session 13(부분 정답---2위 세션). 영향 학급 수는 10명 중 5명이 22개로 정확히 답변.
- 평균 난이도: **2.3/5** (쉬움)

**과제 2: SHAP 요인 식별** --- *"XAI 절벽 분석에서 상위 3개 위험 요인을 식별하시오."*
정답: (1) 이전 차시 완료율, (2) 30% 미만 학생 비율, (3) 학생 간 완료율 편차.
- **10명 중 7명(70%)이 3개 요인을 정확한 순서로 식별.** 1명은 상위 2개 순서 역전(부분), 1명은 3개 중 2개 정확(부분), 1명은 잘못된 패널에서 답변.
- 평균 난이도: **2.4/5**

**과제 3: 위험 학생 식별** --- *"학생 히트맵에서 개입이 필요한 학생을 찾고 이유를 설명하시오."*
단일 정답이 없는 과제---추론 품질로 평가.
- **10명 전원(100%)이 유효한 데이터 기반 추론으로 위험 학생을 식별.** 참여자 응답 예: "S20---전 세션 완료율 0%"(C2), "S02---빨간 셀이 가장 일찍, 가장 연속적으로 나타남"(C4), "S03---노란 분포가 동료와 다르고 14--15세션에서 빨강"(C1).
- 평균 난이도: **2.3/5**

일관적으로 낮은 난이도 평가(2.3--2.4)는 CodleViz의 시각적 설계가 플랫폼에 익숙하지 않은 사용자에게도 복잡한 분석 패턴을 효과적으로 전달함을 확인한다.

### 6.4 뷰 유용성 평가

참여자가 각 시각화 뷰를 5점 유용성 척도로 평가:

| 뷰 | 평균 | 4--5점 비율 |
|------|------|-----------|
| 학습 여정 타임라인 | **4.8** | 10/10 |
| 학생 히트맵 | **4.6** | 9/10 |
| 절벽 감지 히트맵 | **4.3** | 8/10 |
| 역량 레이더 | **4.2** | 8/10 |
| 역량 분석 | **4.2** | 8/10 |
| 학교 비교 | **4.1** | 8/10 |
| 학습 유형 분류 | **4.0** | 7/10 |
| 활동 패턴 | **3.8** | 6/10 |
| 궤적 비교 | **3.8** | 6/10 |

학습 여정 타임라인(4.8)과 학생 히트맵(4.6)이 가장 높은 평가---둘 다 개입이 필요한 학생을 직접 식별할 수 있는 뷰이다. 가장 많이 꼽힌 "가장 유용한 뷰"는 역량 분석과 학습 여정 타임라인(각 3표), 학생 히트맵(2표)이었다.

활동 패턴(3.8)과 궤적 비교(3.8)의 낮은 평가는 인터뷰에서 식별된 두 가지 문제를 반영한다: 활동 패턴의 색상 인코딩이 9개 범주 간 구별이 어려웠고, 궤적 비교는 다른 뷰보다 해석에 더 많은 맥락적 지식을 필요로 하였다.

### 6.5 XAI 평가

6개 항목으로 SHAP 기반 절벽 설명 기능을 평가:

| 항목 | 평균 | 4--5점 비율 |
|------|------|-----------|
| 절벽 원인 이해에 도움 | **4.1** | 8/10 |
| 교수 경험과 일치 | **3.2** | 6/10 |
| 영향력 수준 표시가 직관적 | **4.1** | 7/10 |
| 교수 전략 제안이 실행 가능 | **3.9** | 8/10 |
| 수동 분석보다 빠르고 정확 | **3.8** | 7/10 |
| 신뢰도 표시가 안심감 제공 | **3.5** | 6/10 |

"원인 이해 도움"(4.1)에서 가장 높고 "경험과 일치"(3.2)에서 가장 낮았다. 이 격차는 SHAP 기반 설명이 때때로 직관에 보이지 않던 비자명 요인을 드러낸 것으로, XAI 접근의 강점(직관에 보이지 않는 패턴 발견)이나 데이터 기반 발견과 교수학적 추론을 연결하는 더 나은 연결 설명이 필요함을 시사한다.

### 6.6 기존 도구와 비교

참여자가 현재 도구 대비 CodleViz를 5점 척도로 비교 (3 = 동등, 5 = CodleViz가 훨씬 우수):

| 차원 | 평균 |
|-----------|------|
| 문제 학생 식별 | **4.1** |
| 전체 학생 모니터링 속도 | **4.0** |
| 절벽 원인 분석 (XAI 포함) | **3.8** |

세 차원 모두 3.0 이상으로 기존 접근 대비 개선이 인지되었다. 문제 학생 식별(4.1)의 최고 평가는 과제 3의 높은 성과(100% 정확도)와 일치한다.

### 6.7 Net Promoter Score

평균 추천 점수: **6.8/10**. 추천자 3명(9점 이상), 수동자 4명(7--8점), 비추천자 3명(6점 이하). NPS = 0. 다소 낮은 NPS는 교육자들이 분석 기능의 가치는 인정하면서도 일상 교실 사용 전 추가 완성도가 필요하다고 느낀 것을 반영한다. 3명의 비추천자는 특히 더 직관적인 UX/UI 설계와 학생별 심층 원인 분석의 필요성을 지적하였다.

### 6.8 정성적 결과

가장 많이 언급된 강점은 **다단계 드릴다운**: "모든 학교에서 한 학생까지 흐르듯 볼 수 있는 게 정확히 제가 필요한 거예요"(T1). 학생 히트맵은 가장 *실행 가능한* 뷰로 평가: "초록-빨강 패턴은 벽에 부딪힌 학생이라는 걸 바로 알 수 있어요"(C3). 다수의 참여자가 데이터 기반 객관성의 가치를 강조: "AI 분석이 제 관찰적 판단을 보완하는 정량적, 객관적 증거를 제공합니다"(C3).

XAI에 대해 참여자들은 설명력을 높이 평가하면서도 개선 여지를 지적: "AI 분석이 생각지 못한 요인을 보여주지만, 완전히 신뢰하려면 더 많은 맥락이 필요해요"(P1). 경험 많은 교육자(T2)는 더 비판적 관점을 제시: "이전 차시 완료율이 매 차시 최상위 요인으로 계속 나타납니다. 출결, 학생 결과물, 시험 결과를 통합하지 않으면 원인 분석이 불완전하게 느껴집니다." 이 피드백은 가용 데이터(완료율과 AI 로그)로 작업하는 것과 교육자가 실제로 사용하는 더 풍부한 맥락 정보 간의 긴장을 부각한다.

### 6.9 반복적 정제 (v0.5에서 v1.0으로)

평가 피드백에 기반하여 v0.5에서 v1.0으로의 전환에서 7개 개선이 구현되었다:

1. **LLM 가이드 인사이트 패널**: 개요 수준에 AI 생성 자연어 요약 패널을 추가하여 학교 간 핵심 패턴의 자동 해석을 제공 (더 빠른 패턴 식별 요청에 대응).

2. **히트맵 색상 스케일 개선**: 흰 배경과 구별이 어려운 연한 색상을 제거하도록 색상 그라데이션을 수정 (가장 많이 지적된 시각적 설계 문제 해결, T2, C7).

3. **활동 패턴 색상 강화**: 9개 활동 범주 간 색상 차별화를 개선 (활동 패턴 뷰의 낮은 유용성 평가(3.8)에 대응).

4. **학생 탐색 버튼**: 학생 수준 뷰에서 이전/다음 버튼을 추가하여 순차 탐색 지원 (R1이 비효율적이라고 지적한 스크롤 탐색 대체).

5. **용어 통일**: 설문 도구와 시스템 인터페이스 간 라벨 표준화 (예: "학교" vs. "학급" 용어, T1이 식별한 일관성 문제 해결).

6. **데이터 내보내기 기능**: 분석 결과의 Excel 다운로드 기능 추가 (공유 가능한 보고서 형식에 대한 C3의 요청 대응).

7. **개요 AI 인사이트 패널**: 개요 수준에 자동 AI 생성 요약 패널을 추가하여 더 빠른 초기 패턴 식별 지원.

표 2는 v0.5와 v1.0 간의 전체 변경 범위를 요약한다:

| 차원 | v0.5 (1차 평가) | v1.0 (개선) |
|------|----------------|-------------|
| 플랫폼 | Streamlit 프로토타입 | D3.js 인터랙티브 대시보드 (웹 배포) |
| 탐색 | 단일 전체 현황, 드롭다운 선택 | 7개 탭 + 드릴다운 흐름 (전체→학교→학급→학생) + 검색 |
| 위험 학생 감지 | 없음 | 학교별/학급별 자동 감지 (위험도 점수 + 이유 표시) |
| 학생 비교 | 없음 | 나란히 비교 (진도, AI 사용 패턴, 자동 인사이트) |
| 시간 탐색 | 정적 15차시 뷰 | 차시 범위 슬라이더 + 차트 실시간 업데이트 |
| 연동 하이라이팅 | 없음 | 히트맵 행 호버 → 바 차트, 테이블 행 연동 |
| 교수 전략 추천 | 차트 아래 작은 텍스트 | 맨 위 큰 패널 (3개 핵심 이슈 + 구체적 행동 추천) |
| 용어 | 기술 용어 (XAI, SHAP, 절벽 위험 요인) | 교사 친화적 (진도 하락 원인, 영향력 매우 큼/큼/보통) |
| 역량 라벨 | 약칭만 (DC, DA, DV, DI, CT) | 약칭 + 한글명 + 한 줄 설명 |
| 점수 표시 | 원점수, 보정점수, 자립도 (0.82) | 과제 완료율, 실제 이해도(AI 도움 제외), 혼자 한 비율 (82%) |
| 커리큘럼 비교 | 없음 | 3개 커리큘럼 레이더, 학습여정, 활동분포, AI의존도 나란히 비교 |
| 검색 | 없음 | 학교명/학생ID 즉시 검색 + 미리보기 카드 |

이러한 정제는 시스템의 핵심 분석 기능을 보존하면서 가장 실행 가능한 피드백을 해소한다. 단일 탭 프로토타입에서 다단계 연동 대시보드로의 전환은 드릴다운 탐색이 가장 높이 평가된 기능(4.9/5.0)이라는 평가 결과에 의해 동기 부여된 실질적 아키텍처 변경이다.
