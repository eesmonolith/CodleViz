# 4. CodleViz System

## English

### 4.1 System Overview

CodleViz is a coordinated multi-view visual analytics system that provides four-level drill-down exploration of K-12 data science learning data. The system architecture follows a data-visualization-interaction pipeline: raw event logs from the Codle platform are preprocessed into aggregated views (school summary, competency scores, session progress, student-session matrices), which feed nine coordinated visualization views. Users navigate through four hierarchical levels—**Overview** (all schools), **School** (classrooms within a school), **Classroom** (students within a class), and **Student** (individual learning trajectory)—with consistent visual encoding and smooth transitions between levels (DR1).

Beyond standard visualization components, CodleViz introduces three novel visual analytics techniques specifically designed for AI-integrated educational data: (1) the **Dependency Glyph** for revealing hidden AI tutor reliance patterns, (2) the **Cliff Detector** for automatically identifying pedagogical transition barriers, and (3) the **Trajectory Alignment View** for cross-school comparative analysis.

### 4.2 View 1: School Comparison (DR1, DR5)

The school comparison view presents a horizontal bar chart of all classrooms ranked by average progress, color-coded by curriculum (Ocean Debris: blue, Climate Change: green, Food Security: amber). Each bar encodes the classroom name, average completion rate, and student count via hover tooltip. This view enables administrators to immediately identify high- and low-performing schools and compare across curricula.

**Design rationale:** We chose a sorted horizontal bar chart over a geographic map as the primary comparison view because (1) exact value comparison is more important than spatial distribution at this stage, and (2) classroom names in Korean require sufficient horizontal space for readability. A geographic map is available as a supplementary view.

### 4.3 View 2: Competency Radar (DR2, DR5)

The competency radar chart displays the five core competencies (DC, DA, DV, DI, CT) on a pentagonal radar plot with consistent color encoding. At the school level, multiple radar charts are shown side-by-side for comparative analysis across classrooms. At the classroom level, a single detailed radar chart is complemented by a tabular breakdown of activity counts and student coverage per competency.

**Design rationale:** The radar chart naturally maps to the five non-hierarchical competency dimensions, enabling holistic assessment at a glance. We considered parallel coordinates but found that teachers strongly preferred the radar metaphor for its intuitiveness (*"It looks like a skill chart in a game—I immediately understand it"*, T5).

### 4.4 View 3: Learning Journey Timeline (DR2)

The learning journey timeline visualizes session-by-session completion rates as a line chart with phase-coded background regions:
- Sessions 1–3 (blue): Understanding phase
- Sessions 4–7 (green): Analysis phase
- Sessions 8–11 (red): Coding phase
- Sessions 12–15 (violet): Synthesis phase

The phase coloring directly maps to the curriculum's pedagogical structure, allowing teachers to identify where students struggle during phase transitions (e.g., the common "coding cliff" at session 8 where many students drop in completion rate).

### 4.5 View 4: Student Heatmap (DR3)

The student-session heatmap provides a matrix view where rows represent anonymized students and columns represent sessions 1–15. Cell color encodes completion progress using a diverging colorscale (red → amber → green). Students are sorted by overall completion rate, naturally clustering high-performers at the top and struggling students at the bottom.

**Key interaction:** Clicking a student row transitions to the Student-level view, enabling drill-down to individual session details and activity breakdowns.

### 4.6 View 5: AI Usage Patterns (DR4)

This view visualizes LLM-powered AI tutor usage across sessions and students. It shows the distribution of three AI interaction types (error-help, sheet-help, sheet-filter) over the 15-session curriculum. At the classroom level, it reveals which students use AI tools most frequently and at which points in the curriculum.

### 4.7 View 6: Activity Type Distribution (DR2, DR5)

A stacked area chart shows the proportion of nine activity types across sessions, revealing the curriculum's multimodal structure. This view clearly illustrates the pedagogical progression from passive content consumption (PDF, Video) in early sessions to active coding (Studio, Entry) and synthesis (Board, Quiz) in later sessions.

### 4.8 Novel Visualization 1: AI Dependency Glyph (DR3, DR4)

A key challenge in AI-integrated education is distinguishing between productive AI use (strategic scaffolding) and counterproductive AI dependency (outsourcing thinking). Conventional metrics—completion rate and AI request count—are insufficient when examined independently, as students with identical completion scores can exhibit fundamentally different learning strategies.

We introduce the **Dependency Glyph**, a composite glyph that simultaneously encodes four dimensions of a student's learning behavior within a single visual mark:

**Glyph Design:**
- **Outer ring**: Completion rate, encoded as a circular progress arc (0–100%). Color follows the diverging scale (red → amber → green).
- **Inner circle**: AI tutor request frequency, encoded as circle radius. Larger radius = more AI requests.
- **Inner color**: AI reliance trend over sessions 8–15 (the coding phase). Green = decreasing reliance (healthy), Red = increasing reliance (dependency risk), Gray = no AI usage.
- **Directional arrow**: Small arrow inside the circle pointing up (↑ increasing AI use) or down (↓ decreasing AI use), providing a redundant encoding for colorblind accessibility.

**Glyph Quadrant Interpretation:**

| | Low AI Usage | High AI Usage |
|---|---|---|
| **High Completion** | **Independent Learner** (green ring, small circle) | **AI-Dependent** (green ring, large red circle) |
| **Low Completion** | **Disengaged** (red ring, small circle) | **Struggling + Seeking Help** (red ring, large green circle) |

The glyph is deployed in two contexts: (1) within the student heatmap as an overlay summary column, providing an at-a-glance dependency indicator for each student row, and (2) in a dedicated **Dependency Scatter View** where glyphs are positioned on a completion-rate × AI-frequency scatterplot, enabling teachers to visually cluster students into the four behavioral quadrants.

**Design rationale:** We considered separate bar charts for completion and AI usage, but pilot testing with teachers (T1, T3) revealed that the cognitive cost of cross-referencing two separate views was too high for real-time classroom monitoring. The integrated glyph reduces this to a single visual comparison. The quadrant mapping emerged from teacher feedback: *"I need to see at a glance whether a student's green score is real or AI-assisted"* (T2).

### 4.9 Novel Visualization 2: Coding Cliff Detector (DR2, DR3)

The "coding cliff"—a sharp drop in completion rate at the transition from data analysis to Python programming (typically session 8)—was the most consistently observed pattern across our case studies. However, manually identifying this pattern for each school and classroom is tedious and prone to oversight. We introduce the **Cliff Detector**, an automated visual analytics pipeline that detects, quantifies, and annotates pedagogical transition barriers.

**Detection Algorithm:**
1. For each classroom's session completion time series $c = [c_1, c_2, ..., c_{15}]$, compute the first-order difference: $\Delta c_i = c_i - c_{i-1}$.
2. Identify "cliff points" where $\Delta c_i < -\theta$ (default threshold $\theta = 15\%p$). This threshold was calibrated through domain expert feedback to balance sensitivity and false positives.
3. Compute **cliff severity**: $S = |\Delta c_i| \times \frac{c_{i-1}}{100}$, which weights the drop magnitude by the prior completion level (a drop from 80% to 60% is more severe than from 30% to 10%).
4. Compute **recovery rate**: $R = \frac{c_{i+3} - c_i}{c_{i-1} - c_i}$, measuring how much of the lost completion is recovered within three sessions.

**Visual Encoding:**
- On the Learning Journey Timeline, detected cliff points are annotated with a **triangular cliff marker** (▼). The marker size encodes cliff severity $S$, and the marker color encodes recovery rate $R$ (green = full recovery, red = no recovery).
- A **cliff summary strip** below the timeline shows all classrooms as rows, with cliff markers aligned to session columns, enabling cross-classroom cliff pattern comparison at a glance.
- Hovering over a cliff marker reveals a tooltip with: drop magnitude, severity score, recovery rate, and the specific activity types at the transition point.

**Aggregated Cliff View (Overview level):**
At the Overview level, a **cliff heatmap** aggregates cliff occurrences across all 49 schools. Columns represent sessions 1–15, rows represent schools (grouped by curriculum), and cell intensity encodes cliff severity. This immediately reveals whether the coding cliff is universal or curriculum-specific, and at which exact session it occurs most frequently.

**Design rationale:** Initial prototypes simply highlighted session 8 with a static red background. Expert feedback (R1) indicated that not all schools experience the cliff at session 8—some experience it at session 7 or 9 depending on the curriculum. The automated detection allows the cliff to be identified wherever it occurs, regardless of curriculum structure. The severity + recovery dual encoding was requested by T3: *"Knowing there's a cliff is useful, but knowing whether students recover is what determines my intervention strategy."*

### 4.10 Novel Visualization 3: Trajectory Alignment View (DR1, DR5)

Comparing learning trajectories across schools is challenging because different schools start at different baseline levels and may have different class sizes. Simple overlay of line charts leads to visual clutter and makes it difficult to identify meaningful trajectory differences versus mere baseline differences.

We introduce the **Trajectory Alignment View**, a custom visualization designed for cross-school and cross-curriculum comparative analysis of learning trajectories.

**Design:**

**(a) Aligned Small Multiples with Baseline Normalization:**
Each school's 15-session completion trajectory is displayed as a small multiple line chart, but all trajectories are **baseline-normalized** to session 1 = 0%. This shows relative growth rather than absolute levels, making it possible to compare trajectory *shapes* independent of starting conditions. Schools are sorted by a composite metric (total growth + stability), and color-coded by curriculum.

**(b) Trajectory Envelope:**
For each curriculum, a **trajectory envelope** (shaded band between the 25th and 75th percentile trajectories) is computed and overlaid as a semi-transparent region. Individual school trajectories are drawn as lines within or outside this envelope. Schools falling below the envelope are automatically highlighted with a warning indicator, signaling underperformance relative to curriculum peers.

**(c) Phase-aligned Sparklines:**
Below each small multiple, a compact **sparkline strip** decomposes the trajectory into four phase segments (Understanding, Analysis, Coding, Synthesis). Each phase is rendered as a mini bar showing the average completion rate within that phase. This enables rapid phase-level comparison: a teacher can scan across all schools and immediately identify which phase is the bottleneck for each school.

**(d) Trajectory Similarity Clustering:**
Using Dynamic Time Warping (DTW) distance, school trajectories are clustered into groups of similar learning patterns. The resulting dendrogram is displayed alongside the small multiples, and linked brushing allows users to select a cluster to highlight all schools with similar trajectories. This reveals hidden groupings—for example, schools that experience the coding cliff but recover (cluster A) versus schools that experience the cliff and never recover (cluster B).

**Design rationale:** We considered a single overlaid line chart but found it unreadable with 49 schools. Small multiples preserve individual trajectory detail while enabling comparison through aligned spatial position. The baseline normalization was critical—without it, pilot users (R1, R2) consistently confused "high starting level" with "better trajectory," making erroneous comparative judgments. DTW clustering was added after R1 remarked: *"I want to find schools that behave similarly so I can understand what makes them different from the rest."* The trajectory envelope concept was adapted from weather forecast visualization (ensemble plots), mapping the notion of "normal range" to educational trajectory analysis.

### 4.11 Coordinated Interactions

All nine views (six standard + three novel) are coordinated through:
- **Filtering**: Sidebar controls for curriculum, school, and session range selection propagate across all views
- **Drill-down**: Four-level hierarchy (Overview → School → Classroom → Student) with consistent visual transitions
- **Brushing**: Selecting a competency in the radar chart highlights corresponding sessions in the timeline; selecting a cluster in the Trajectory Alignment View highlights corresponding schools in the School Comparison; selecting a quadrant in the Dependency Scatter highlights corresponding students in the heatmap
- **Details-on-demand**: Hover tooltips provide exact values without cluttering the visual display
- **Cliff-linked highlighting**: Clicking a cliff marker in the Cliff Detector highlights the corresponding students who dropped at that session in the Student Heatmap, enabling immediate drill-down from pattern to individuals

---

## 한글

### 4.1 시스템 개요

CodleViz는 K-12 데이터 사이언스 학습 데이터의 4단계 드릴다운 탐색을 제공하는 연동형 다중 뷰 시각적 분석 시스템이다. 코들 플랫폼의 원시 이벤트 로그를 전처리하여 집계된 뷰(학교 요약, 역량 점수, 세션 진도, 학생-세션 매트릭스)로 변환하고, 이를 9개의 연동 시각화 뷰에 공급한다. 사용자는 **개요**(전체 학교), **학교**(학교 내 학급), **학급**(학급 내 학생), **학생**(개별 학습 궤적)의 4개 계층 수준을 탐색한다 (DR1).

표준 시각화 구성요소 외에, CodleViz는 AI 통합 교육 데이터를 위해 특별히 설계된 3개의 새로운 시각적 분석 기법을 도입한다: (1) 숨겨진 AI 튜터 의존 패턴을 드러내는 **의존도 글리프(Dependency Glyph)**, (2) 교수학적 전환 장벽을 자동 식별하는 **절벽 감지기(Cliff Detector)**, (3) 학교 간 비교 분석을 위한 **궤적 정렬 뷰(Trajectory Alignment View)**.

### 4.2 뷰 1: 학교 비교 (DR1, DR5)

학교 비교 뷰는 평균 진도 순으로 정렬된 모든 학급의 수평 막대 그래프를 제시하며, 커리큘럼별로 색상 코딩된다. 관리자가 고성과/저성과 학교를 즉시 식별하고 커리큘럼 간 비교를 할 수 있다.

**디자인 근거:** 지리적 지도 대신 정렬된 수평 막대 그래프를 주요 비교 뷰로 선택하였는데, (1) 이 단계에서는 정확한 값 비교가 공간적 분포보다 중요하고, (2) 한국어 학급명이 가독성을 위해 충분한 수평 공간을 필요로 하기 때문이다.

### 4.3 뷰 2: 역량 레이더 (DR2, DR5)

역량 레이더 차트는 5개 핵심 역량(DC, DA, DV, DI, CT)을 일관된 색상 인코딩으로 오각형 레이더 도표에 표시한다. 학교 수준에서는 학급 간 비교 분석을 위해 여러 레이더 차트가 나란히 표시된다.

**디자인 근거:** 레이더 차트는 비계층적인 5개 역량 차원에 자연스럽게 매핑되어 한눈에 전체적 평가를 가능하게 한다. *"게임의 스킬 차트처럼 보여서 바로 이해가 됩니다"* (T5)

### 4.4 뷰 3: 학습 여정 타임라인 (DR2)

학습 여정 타임라인은 세션별 완료율을 단계 코딩된 배경 영역이 있는 라인 차트로 시각화한다:
- 1–3차시(파랑): 이해 단계
- 4–7차시(초록): 분석 단계
- 8–11차시(빨강): 코딩 단계
- 12–15차시(보라): 종합 단계

단계 색상은 커리큘럼의 교수학적 구조에 직접 매핑되어, 교사가 단계 전환 시 학생이 어려움을 겪는 지점을 식별할 수 있다.

### 4.5 뷰 4: 학생 히트맵 (DR3)

학생-세션 히트맵은 행이 익명화된 학생, 열이 1~15차시인 매트릭스 뷰를 제공한다. 셀 색상은 발산 색상 스케일(빨강→주황→초록)로 완료 진도를 인코딩한다. 학생은 전체 완료율 순으로 정렬되어 상위 학생이 위에, 어려움을 겪는 학생이 아래에 자연스럽게 군집된다.

### 4.6 뷰 5: AI 활용 패턴 (DR4)

LLM 기반 AI 튜터 활용을 세션 및 학생별로 시각화한다. 15차시 커리큘럼에 걸쳐 3가지 AI 상호작용 유형(에러 도움, 시트 도움, 시트 필터)의 분포를 보여준다.

### 4.7 뷰 6: 활동 유형 분포 (DR2, DR5)

스택 영역 차트는 9가지 활동 유형의 비율을 세션별로 보여주어 커리큘럼의 멀티모달 구조를 드러낸다.

### 4.8 새로운 시각화 1: AI 의존도 글리프 (DR3, DR4)

AI 통합 교육에서 핵심 과제는 생산적 AI 활용(전략적 스캐폴딩)과 비생산적 AI 의존(사고 외주화)을 구별하는 것이다. 기존 지표인 완료율과 AI 요청 횟수는 개별적으로 검토할 때 불충분하다.

**의존도 글리프(Dependency Glyph)**는 학생의 학습 행동 4차원을 단일 시각적 마크에 동시 인코딩하는 복합 글리프이다:

**글리프 설계:**
- **외부 링**: 완료율. 원형 진행 호(0~100%)로 인코딩. 발산 색상 스케일(빨강→주황→초록) 적용.
- **내부 원**: AI 튜터 요청 빈도. 원 반지름으로 인코딩. 큰 반지름 = 더 많은 AI 요청.
- **내부 색상**: 8~15차시(코딩 단계)에서의 AI 의존도 추세. 초록 = 의존도 감소(건강), 빨강 = 의존도 증가(의존 위험), 회색 = AI 미사용.
- **방향 화살표**: 색맹 접근성을 위한 이중 인코딩.

**글리프 사분면 해석:**

| | 낮은 AI 사용 | 높은 AI 사용 |
|---|---|---|
| **높은 완료율** | **자립 학습자** | **AI 의존** |
| **낮은 완료율** | **이탈** | **어려움+도움 탐색** |

글리프는 학생 히트맵의 요약 열과 **의존도 산점도 뷰**에 배치되어, 교사가 학생들을 4개 행동 사분면으로 시각적으로 군집화할 수 있다.

**디자인 근거:** T2: *"학생의 초록 점수가 진짜인지 AI 도움으로 만들어진 건지 한눈에 봐야 합니다."*

### 4.9 새로운 시각화 2: 코딩 절벽 감지기 (DR2, DR3)

"코딩 절벽"—데이터 분석에서 파이썬 프로그래밍으로의 전환(주로 8차시)에서의 급격한 완료율 하락—은 사례 연구에서 가장 일관되게 관찰된 패턴이다. 그러나 이 패턴을 각 학교와 학급별로 수동 식별하는 것은 번거롭다. **절벽 감지기(Cliff Detector)**는 교수학적 전환 장벽을 자동 감지, 정량화, 주석 처리하는 시각적 분석 파이프라인이다.

**감지 알고리즘:**
1. 각 학급의 세션 완료율 시계열 $c = [c_1, ..., c_{15}]$에 대해 1차 차분 $\Delta c_i = c_i - c_{i-1}$ 계산
2. $\Delta c_i < -\theta$ (기본 임계값 $\theta = 15\%p$)인 "절벽 지점" 식별
3. **절벽 심각도** 계산: $S = |\Delta c_i| \times \frac{c_{i-1}}{100}$
4. **회복률** 계산: $R = \frac{c_{i+3} - c_i}{c_{i-1} - c_i}$

**시각적 인코딩:**
- 학습 여정 타임라인에 삼각형 절벽 마커(▼) 주석. 크기 = 심각도, 색상 = 회복률.
- 타임라인 하단의 **절벽 요약 스트립**으로 학급 간 패턴 비교.
- 개요 수준의 **절벽 히트맵**으로 49개 학교의 절벽 발생 집계.

**디자인 근거:** T3: *"절벽이 있다는 건 유용하지만, 학생들이 회복하는지가 제 개입 전략을 결정합니다."*

### 4.10 새로운 시각화 3: 궤적 정렬 뷰 (DR1, DR5)

학교 간 학습 궤적 비교는 기준선 수준과 학급 크기가 달라 어렵다. **궤적 정렬 뷰(Trajectory Alignment View)**는 학교 간/커리큘럼 간 학습 궤적의 비교 분석을 위한 맞춤 시각화이다.

**설계:**

**(a) 기준선 정규화 스몰 멀티플:** 각 학교의 15차시 궤적을 1차시 = 0%로 정규화하여 절대 수준이 아닌 상대 성장을 표시.

**(b) 궤적 포락선:** 커리큘럼별 25~75 백분위 궤적 대역을 반투명 영역으로 표시. 포락선 아래 학교는 경고 표시.

**(c) 단계별 스파크라인:** 각 스몰 멀티플 아래 4단계(이해/분석/코딩/종합) 평균 완료율 미니 막대.

**(d) 궤적 유사도 클러스터링:** DTW(Dynamic Time Warping) 거리를 사용한 궤적 클러스터링. 덴드로그램과 연동 브러싱으로 유사 패턴 학교 그룹 식별.

**디자인 근거:** R1: *"비슷하게 행동하는 학교를 찾아서 나머지와 무엇이 다른지 이해하고 싶습니다."* 궤적 포락선 개념은 기상 예보 시각화(앙상블 플롯)에서 차용.

### 4.11 연동 인터랙션

9개 뷰(표준 6개 + 새로운 3개)는 다음을 통해 연동된다:
- **필터링**: 커리큘럼, 학교, 세션 범위 선택이 모든 뷰에 전파
- **드릴다운**: 4단계 계층(개요→학교→학급→학생)의 일관된 시각적 전환
- **브러싱**: 레이더 차트의 역량 선택 → 타임라인 세션 하이라이트; 궤적 정렬 뷰의 클러스터 선택 → 학교 비교 하이라이트; 의존도 산점도의 사분면 선택 → 히트맵 학생 하이라이트
- **세부사항 요청**: 호버 툴팁이 정확한 값 제공
- **절벽 연동 하이라이팅**: 절벽 마커 클릭 → 해당 세션에서 이탈한 학생을 히트맵에서 하이라이트, 패턴에서 개인으로의 즉시 드릴다운 지원
