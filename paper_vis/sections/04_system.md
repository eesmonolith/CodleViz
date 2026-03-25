# 4. CodleViz System

## English

### 4.1 System Overview

CodleViz is a standalone D3.js visual analytics dashboard that analyzes data exported from the Codle platform. The system architecture follows a data-visualization-interaction pipeline: raw event logs from the Codle platform are preprocessed into aggregated views (school summary, competency scores, session progress, student-session matrices), which feed nine coordinated visualization views. Users navigate through four hierarchical levels---**Overview** (all schools), **School** (classrooms within a school), **Classroom** (students within a class), and **Student** (individual learning trajectory)---with consistent visual encoding and smooth transitions between levels (DR1).

Beyond standard visualization components, CodleViz introduces three novel visual analytics techniques specifically designed for AI-integrated educational data: (1) the **AI Dependency Glyph** for revealing hidden AI tutor reliance patterns, (2) the **Performance Cliff Detector** for automatically identifying learning transition barriers with SHAP-based causal explanations, and (3) the **Trajectory Alignment View** for cross-school comparative analysis.

The system also provides several advanced interaction features: **linked brushing** across all nine views, **search functionality** for locating specific schools, classrooms, or students, a **session slider** for temporal exploration, **student comparison mode** for side-by-side analysis, **at-risk student auto-detection** per classroom, and **settings toggles** for AI-adjusted scores, XAI insights, and pedagogical recommendations.

### 4.1.1 Multi-Level Drill-Down: Design Rationale

CodleViz organizes its analytical workflow into six distinct views, each designed for a specific stakeholder and decision context:

| View | Primary User | Decision Question |
|------|-------------|------------------|
| **Overview** | Program administrators | Which schools are falling behind? What are the system-wide patterns? |
| **School** | School coordinators | Are competencies balanced? At which sessions do students disengage? |
| **Classroom** | Classroom teachers | Which students in my class need attention? Who is over-relying on AI? |
| **Student** | Classroom teachers | How does this student use AI? How do they compare to peers? |
| **Analysis** | Researchers, administrators | What are the overall AI usage patterns? What drives performance drops? |
| **Curriculum** | Program administrators | Which of the three curricula is most effective, and why? |

This multi-level structure follows the Visual Information Seeking Mantra (Shneiderman, 1996): overview first, zoom and filter, then details on demand. The four-level drill-down (overview → school → classroom → student) enables educators to transition from identifying a problem ("8 schools show performance drops") to locating affected individuals ("Student S0486 in School_01 has 53 AI requests despite 98% completion") to reasoning about causes ("SHAP analysis attributes 38% of drop risk to prior completion rate") within a single coordinated environment.

The Curriculum Comparison view serves a distinct analytical need: program administrators evaluating the relative effectiveness of three thematic curricula (Marine Debris, Climate Change, Food Security) require side-by-side comparison across all five competency dimensions---a cross-cutting analysis that does not fit within the hierarchical drill-down.

### 4.2 View 1: School Comparison (DR1, DR5)

The school comparison view presents a horizontal bar chart of all classrooms ranked by average progress, color-coded by curriculum (Ocean Debris: blue, Climate Change: green, Food Security: amber). Each bar encodes the classroom name, average completion rate, and student count via hover tooltip. This view enables administrators to immediately identify high- and low-performing schools and compare across curricula.

**Design rationale:** A sorted horizontal bar chart was chosen over a geographic map as the primary comparison view because (1) exact value comparison is more important than spatial distribution at this stage, and (2) classroom names in Korean require sufficient horizontal space for readability. A geographic map is available as a supplementary view.

### 4.3 View 2: Competency Radar (DR2, DR5)

The competency radar chart displays the five core competencies (DC, DA, DV, DI, CT) on a pentagonal radar plot with consistent color encoding. At the school level, multiple radar charts are shown side-by-side for comparative analysis across classrooms. At the classroom level, a single detailed radar chart is complemented by a tabular breakdown of activity counts and student coverage per competency.

**Design rationale:** The radar chart naturally maps to the five non-hierarchical competency dimensions, enabling holistic assessment at a glance. Parallel coordinates were considered but the radar metaphor proved more intuitive for educators during prototype testing, likely because the "skill chart" metaphor is widely recognized.

### 4.4 View 3: Learning Journey Timeline (DR2)

The learning journey timeline visualizes session-by-session completion rates as a line chart with tier-coded background regions corresponding to the three-tier difficulty progression:
- Sessions 1--5 (blue): **Tier 1 -- Foundation** (Entry block coding)
- Sessions 6--10 (green): **Tier 2 -- Intermediate** (CODAP data analysis)
- Sessions 11--15 (red): **Tier 3 -- Advanced** (Python programming)

The tier coloring directly maps to the curriculum's scaffolded progression from visual programming to text-based coding, allowing educators to identify where students struggle during tier transitions (e.g., the common "performance cliff" at session 11 where many students drop in completion rate as they transition from code-free CODAP analysis to Python programming).

### 4.5 View 4: Student Heatmap (DR3)

The student-session heatmap provides a matrix view where rows represent anonymized students and columns represent sessions 1--15. Cell color encodes completion progress using a diverging colorscale (red to amber to green). Students are sorted by overall completion rate, naturally clustering high-performers at the top and struggling students at the bottom.

**Key interaction:** Clicking a student row transitions to the Student-level view, enabling drill-down to individual session details and activity breakdowns. **Student navigation buttons** allow sequential browsing through students without returning to the classroom view.

### 4.6 View 5: AI Usage Patterns (DR4)

This view visualizes LLM-powered AI tutor usage across sessions, students, and programming tiers. It shows the distribution of four AI interaction types---block-help (Entry block coding assistance), error-help (Python code error explanation), sheet-help (spreadsheet assistance), and sheet-filter (data filtering guidance)---over the 15-session curriculum. The tier-segmented display reveals how AI usage patterns evolve as students progress through increasing difficulty levels: from block coding scaffolding in Tier 1, through data analysis hints in Tier 2, to debugging support in Tier 3. At the classroom level, it reveals which students use AI tools most frequently and at which tier transitions AI reliance spikes.

### 4.7 View 6: Activity Type Distribution (DR2, DR5)

A stacked area chart shows the proportion of nine activity types across sessions, revealing the curriculum's multimodal structure. This view clearly illustrates the pedagogical progression from passive content consumption (PDF, Video) in early sessions to active coding (Studio, Entry) and synthesis (Board, Quiz) in later sessions.

### 4.8 Novel Visualization 1: AI Dependency Glyph (DR3, DR4)

A key challenge in AI-integrated education is distinguishing between productive AI use (strategic scaffolding) and counterproductive AI dependency (outsourcing thinking). Conventional metrics---completion rate and AI request count---are insufficient when examined independently, as students with identical completion scores can exhibit fundamentally different learning strategies.

The **AI Dependency Glyph** is a composite glyph that simultaneously encodes four dimensions of a student's learning behavior within a single visual mark:

**Glyph Design:**
- **Outer ring**: Completion rate, encoded as a circular progress arc (0--100%). Color follows the diverging scale (red to amber to green).
- **Inner circle**: AI tutor request frequency, encoded as circle radius. Larger radius = more AI requests.
- **Inner color**: AI reliance trend over sessions 11--15 (Tier 3, the Python programming phase). Green = decreasing reliance (healthy), Red = increasing reliance (dependency risk), Gray = no AI usage.
- **Directional arrow**: Small arrow inside the circle pointing up (increasing AI use) or down (decreasing AI use), providing a redundant encoding for colorblind accessibility.

**Glyph Quadrant Interpretation:**

| | Low AI Usage | High AI Usage |
|---|---|---|
| **High Completion** | **Independent Learner** (green ring, small circle) | **AI-Dependent** (green ring, large red circle) |
| **Low Completion** | **Disengaged** (red ring, small circle) | **Struggling + Seeking Help** (red ring, large green circle) |

The glyph is deployed in two contexts: (1) within the student heatmap as an overlay summary column, providing an at-a-glance dependency indicator for each student row, and (2) in a dedicated **Dependency Scatter View** where glyphs are positioned on a completion-rate x AI-frequency scatterplot, enabling educators to visually cluster students into the four behavioral quadrants.

**Design rationale:** Separate bar charts for completion and AI usage were considered, but prototype testing revealed that the cognitive cost of cross-referencing two separate views was too high for real-time classroom monitoring. The integrated glyph reduces this to a single visual comparison. The quadrant mapping emerged from the operational insight that educators need to see at a glance whether a student's high score reflects genuine mastery or AI-assisted completion.

### 4.9 Novel Visualization 2: Performance Cliff Detector (DR2, DR3)

The "performance cliff"---a sharp drop in completion rate at curriculum tier transitions, most commonly occurring at session 11 (the shift from CODAP data analysis to Python programming)---was the most consistently observed pattern across our data. This cliff arises at the boundary where students shift from a code-free interactive environment to text-based programming, representing a significant cognitive leap. Manually identifying this pattern for each school and classroom is tedious and prone to oversight. The **Performance Cliff Detector** is an automated visual analytics pipeline that detects, quantifies, and annotates learning transition barriers.

**Detection Algorithm:**
1. For each classroom's session completion time series $c = [c_1, c_2, ..., c_{15}]$, compute the first-order difference: $\Delta c_i = c_i - c_{i-1}$.
2. Identify "cliff points" where $\Delta c_i < -\theta$ (default threshold $\theta = 15\%p$). This threshold was calibrated through domain expertise to balance sensitivity and false positives.
3. Compute **cliff severity**: $S = |\Delta c_i| \times \frac{c_{i-1}}{100}$, which weights the drop magnitude by the prior completion level (a drop from 80% to 60% is more severe than from 30% to 10%).
4. Compute **recovery rate**: $R = \frac{c_{i+3} - c_i}{c_{i-1} - c_i}$, measuring how much of the lost completion is recovered within three sessions.

**Visual Encoding:**
- On the Learning Journey Timeline, detected cliff points are annotated with a **triangular cliff marker**. The marker size encodes cliff severity $S$, and the marker color encodes recovery rate $R$ (green = full recovery, red = no recovery).
- A **cliff summary strip** below the timeline shows all classrooms as rows, with cliff markers aligned to session columns, enabling cross-classroom cliff pattern comparison at a glance.
- Hovering over a cliff marker reveals a tooltip with: drop magnitude, severity score, recovery rate, and the specific activity types at the transition point.

**SHAP-based Causal Explanations:**
Each detected cliff is accompanied by a SHAP (SHapley Additive exPlanations) analysis that identifies the contributing factors. The system computes SHAP values for features including prior completion rate, percentage of students below 30%, student completion spread, activity type composition, and AI tutor usage rate. These factors are displayed as a ranked bar chart with impact labels (very high / high / moderate / low influence), enabling educators to understand not just *where* cliffs occur but *why*.

**Aggregated Cliff View (Overview level):**
At the Overview level, a **cliff heatmap** aggregates cliff occurrences across all 49 schools. Columns represent sessions 1--15, rows represent schools (grouped by curriculum), and cell intensity encodes cliff severity. This immediately reveals whether the performance cliff is universal or curriculum-specific, and at which exact session it occurs most frequently.

**Design rationale:** Initial prototypes simply highlighted session 11 with a static red background. Domain expertise indicated that not all schools experience the cliff at session 11---some experience it at earlier or later sessions depending on the curriculum. The automated detection allows the cliff to be identified wherever it occurs, regardless of curriculum structure. The severity + recovery dual encoding captures the insight that knowing a cliff exists is useful, but knowing whether students recover is what determines intervention strategy.

### 4.10 Novel Visualization 3: Trajectory Alignment View (DR1, DR5)

Comparing learning trajectories across schools is challenging because different schools start at different baseline levels and may have different class sizes. Simple overlay of line charts leads to visual clutter and makes it difficult to identify meaningful trajectory differences versus mere baseline differences.

The **Trajectory Alignment View** is a custom visualization designed for cross-school and cross-curriculum comparative analysis of learning trajectories.

**Design:**

**(a) Aligned Small Multiples with Baseline Normalization:**
Each school's 15-session completion trajectory is displayed as a small multiple line chart, but all trajectories are **baseline-normalized** to session 1 = 0%. This shows relative growth rather than absolute levels, making it possible to compare trajectory *shapes* independent of starting conditions. Schools are sorted by a composite metric (total growth + stability), and color-coded by curriculum.

**(b) Trajectory Envelope:**
For each curriculum, a **trajectory envelope** (shaded band between the 25th and 75th percentile trajectories) is computed and overlaid as a semi-transparent region. Individual school trajectories are drawn as lines within or outside this envelope. Schools falling below the envelope are automatically highlighted with a warning indicator, signaling underperformance relative to curriculum peers.

**(c) Phase-aligned Sparklines:**
Below each small multiple, a compact **sparkline strip** decomposes the trajectory into four phase segments (Understanding, Analysis, Coding, Synthesis). Each phase is rendered as a mini bar showing the average completion rate within that phase. This enables rapid phase-level comparison: an educator can scan across all schools and immediately identify which phase is the bottleneck for each school.

**(d) Trajectory Similarity Clustering:**
Using Dynamic Time Warping (DTW) distance, school trajectories are clustered into groups of similar learning patterns. The resulting dendrogram is displayed alongside the small multiples, and linked brushing allows users to select a cluster to highlight all schools with similar trajectories. This reveals hidden groupings---for example, schools that experience the performance cliff but recover versus schools that experience the cliff and never recover.

**Design rationale:** A single overlaid line chart was considered but proved unreadable with 49 schools. Small multiples preserve individual trajectory detail while enabling comparison through aligned spatial position. The baseline normalization was critical---without it, users consistently confused "high starting level" with "better trajectory," making erroneous comparative judgments. DTW clustering was added to enable identification of schools with similar behavioral patterns. The trajectory envelope concept was adapted from weather forecast visualization (ensemble plots), mapping the notion of "normal range" to educational trajectory analysis.

### 4.11 Design Iteration: AI-Adjusted Competency Score (DR4)

A critical observation from the platform data was that **completion-based competency scores can be systematically inflated by AI tutor dependency**. Students with high completion rates but heavy AI usage may not have developed the competencies their scores suggest. This observation, grounded in four years of platform operation and confirmed by the literature on automation complacency [Prather et al., 2023], motivated a key system feature: integrating LLM tutor logs into competency measurement.

**AI-Adjusted Competency Score.** An independence-weighted competency score penalizes completion rates proportional to AI tutor reliance:

$$\text{AdjustedScore}_i = \text{RawCompletion}_i \times \frac{1}{1 + \alpha \cdot \text{LLMRate}_i}$$

where $\text{LLMRate}_i = \frac{\text{LLM requests by student } i}{\text{Total activities by student } i}$, and $\alpha = 0.5$ is the penalty weight calibrated to produce meaningful but not excessive adjustments.

**Impact.** Across 709 students, the adjustment reveals hidden disparities:
- **30 students** experience penalties exceeding 10 percentage points, all with heavy AI usage (22--87 LLM requests)
- The most dramatic case: Student S0158 drops from 95.8% (raw) to 65.3% (adjusted), a **-30.5%p penalty**, reflecting 87 AI tutor requests
- Competency-level impact varies: DA and CT (the competencies most associated with coding activities where AI help is available) show the largest adjustments (-2.4%p and -2.3%p respectively), while DC (primarily reading/comprehension activities where AI help is less relevant) shows minimal impact (-0.5%p)
- Curriculum-level: Food Security shows the largest adjustment (-2.8%p), consistent with its higher overall AI usage

**Visual Integration.** The competency radar chart offers a toggle between "Raw" and "AI-Adjusted" views. When AI-Adjusted mode is active, the radar polygon contracts for students with high AI dependency, making the difference immediately visible. The student heatmap also supports a toggle, re-coloring cells based on adjusted scores---revealing "hidden reds" (students whose green cells turn amber or red after adjustment).

**Design rationale.** Binary penalties (discounting any activity where AI was used) were considered but deemed too harsh: occasional strategic use of AI to understand an error message is qualitatively different from systematic reliance on AI for every coding task. The smooth, rate-based penalty preserves the distinction between occasional strategic use and systematic dependency.

### 4.12 Coordinated Interactions

All nine views (six standard + three novel) are coordinated through:
- **Filtering**: Sidebar controls for curriculum, school, and session range selection propagate across all views
- **Drill-down**: Four-level hierarchy (Overview, School, Classroom, Student) with consistent visual transitions
- **Linked brushing**: Selecting a competency in the radar chart highlights corresponding sessions in the timeline; selecting a cluster in the Trajectory Alignment View highlights corresponding schools in the School Comparison; selecting a quadrant in the Dependency Scatter highlights corresponding students in the heatmap
- **Search**: Text-based search for schools, classrooms, or individual students with auto-complete
- **Session slider**: Temporal exploration control enabling educators to focus on specific session ranges
- **Student comparison**: Side-by-side comparison of two students' complete profiles (heatmap, AI usage, competency radar)
- **At-risk auto-detection**: Per-classroom automatic identification of students meeting at-risk criteria (low completion, high AI dependency, or sudden disengagement)
- **Settings toggles**: Three configurable modes---AI-adjusted scores (on/off), XAI insights (on/off), and pedagogical recommendations (on/off)---allowing educators to control information density
- **Details-on-demand**: Hover tooltips provide exact values without cluttering the visual display
- **Cliff-linked highlighting**: Clicking a cliff marker in the Performance Cliff Detector highlights the corresponding students who dropped at that session in the Student Heatmap, enabling immediate drill-down from pattern to individuals

---

## 한글

### 4.1 시스템 개요

CodleViz는 코들 플랫폼에서 내보낸 데이터를 분석하는 독립형 D3.js 시각적 분석 대시보드이다. 코들 플랫폼의 원시 이벤트 로그를 전처리하여 집계된 뷰(학교 요약, 역량 점수, 세션 진도, 학생-세션 매트릭스)로 변환하고, 이를 9개의 연동 시각화 뷰에 공급한다. 사용자는 **개요**(전체 학교), **학교**(학교 내 학급), **학급**(학급 내 학생), **학생**(개별 학습 궤적)의 4개 계층 수준을 탐색한다 (DR1).

표준 시각화 구성요소 외에, CodleViz는 AI 통합 교육 데이터를 위해 특별히 설계된 3개의 새로운 시각적 분석 기법을 도입한다: (1) 숨겨진 AI 튜터 의존 패턴을 드러내는 **AI 의존도 글리프(AI Dependency Glyph)**, (2) SHAP 기반 원인 설명과 함께 학습 전환 장벽을 자동 식별하는 **성과 절벽 감지기(Performance Cliff Detector)**, (3) 학교 간 비교 분석을 위한 **궤적 정렬 뷰(Trajectory Alignment View)**.

시스템은 또한 여러 고급 인터랙션 기능을 제공한다: 9개 뷰 전체에 걸친 **연동 브러싱**, 학교·학급·학생 검색을 위한 **검색 기능**, 시간 탐색을 위한 **세션 슬라이더**, 나란히 분석을 위한 **학생 비교 모드**, 학급별 **위험 학생 자동 감지**, AI 보정 점수·XAI 인사이트·교수학적 추천을 위한 **설정 토글**.

### 4.1.1 다단계 드릴다운: 설계 근거

CodleViz는 분석 워크플로우를 6개의 뷰로 구성하며, 각 뷰는 특정 이해관계자와 의사결정 맥락을 위해 설계되었다:

| 뷰 | 주요 사용자 | 의사결정 질문 |
|------|-----------|------------|
| **전체 현황** | 사업 담당자, 관리자 | 49개 학교 중 어디가 뒤처지는가? 전체적으로 어떤 문제가 있는가? |
| **학교별** | 관리자, 학교 담당자 | 이 학교의 5개 역량은 균형 잡혀 있는가? 어느 차시에서 이탈하는가? |
| **학급별** | 담당 교사 | 내 학급에서 주의가 필요한 학생은 누구인가? AI에 과의존하는 학생은? |
| **학생별** | 담당 교사 | 이 학생은 AI를 어떻게 쓰는가? 다른 학생과 비교하면 어떤가? |
| **분석** | 연구자, 관리자 | 전체적으로 AI를 어떤 유형으로 활용하는가? 진도 하락의 원인은? |
| **커리큘럼 비교** | 사업 담당자 | 3개 커리큘럼 중 어떤 것이 가장 효과적이며 왜 그런가? |

이 다단계 구조는 Visual Information Seeking Mantra(Shneiderman, 1996)를 따른다: 먼저 개요, 줌과 필터, 그리고 요청 시 세부 정보. 4단계 드릴다운(전체→학교→학급→학생)을 통해 교육자가 문제 식별("8개 학교에서 진도 급락")에서 해당 개인 특정("School_01의 S0486은 98% 완료율에 AI 53회 사용")으로, 그리고 원인 추론("SHAP 분석은 하락 위험의 38%를 직전 차시 완료율에 귀속")으로 단일 연동 환경 내에서 전환할 수 있다.

커리큘럼 비교 뷰는 별도의 분석적 필요를 충족한다: 3개 주제별 커리큘럼의 상대적 효과를 평가하는 사업 담당자는 5개 역량 차원에 걸친 나란히 비교를 필요로 하며, 이는 계층적 드릴다운에 맞지 않는 횡단적 분석이다.

### 4.2 뷰 1: 학교 비교 (DR1, DR5)

학교 비교 뷰는 평균 진도 순으로 정렬된 모든 학급의 수평 막대 그래프를 제시하며, 커리큘럼별로 색상 코딩된다. 관리자가 고성과/저성과 학교를 즉시 식별하고 커리큘럼 간 비교를 할 수 있다.

**디자인 근거:** 지리적 지도 대신 정렬된 수평 막대 그래프를 주요 비교 뷰로 선택하였는데, (1) 이 단계에서는 정확한 값 비교가 공간적 분포보다 중요하고, (2) 한국어 학급명이 가독성을 위해 충분한 수평 공간을 필요로 하기 때문이다.

### 4.3 뷰 2: 역량 레이더 (DR2, DR5)

역량 레이더 차트는 5개 핵심 역량(DC, DA, DV, DI, CT)을 일관된 색상 인코딩으로 오각형 레이더 도표에 표시한다. 학교 수준에서는 학급 간 비교 분석을 위해 여러 레이더 차트가 나란히 표시된다.

**디자인 근거:** 레이더 차트는 비계층적인 5개 역량 차원에 자연스럽게 매핑되어 한눈에 전체적 평가를 가능하게 한다. 평행 좌표가 고려되었으나 프로토타입 테스트에서 레이더 은유가 교육자에게 더 직관적인 것으로 확인되었다.

### 4.4 뷰 3: 학습 여정 타임라인 (DR2)

학습 여정 타임라인은 세션별 완료율을 3단계 난이도 체계에 대응하는 단계 코딩된 배경 영역이 있는 라인 차트로 시각화한다:
- 1--5차시(파랑): **1단계 -- 기초** (엔트리 블록코딩)
- 6--10차시(초록): **2단계 -- 중급** (CODAP 데이터 분석)
- 11--15차시(빨강): **3단계 -- 심화** (파이썬 프로그래밍)

단계 색상은 시각적 프로그래밍에서 텍스트 기반 코딩으로의 스캐폴딩 진행에 직접 매핑되어, 교육자가 단계 전환 시 학생이 어려움을 겪는 지점을 식별할 수 있다(예: 코드 없는 CODAP 분석에서 파이썬 프로그래밍으로 전환하는 11차시의 "성과 절벽").

### 4.5 뷰 4: 학생 히트맵 (DR3)

학생-세션 히트맵은 행이 익명화된 학생, 열이 1--15차시인 매트릭스 뷰를 제공한다. 셀 색상은 발산 색상 스케일(빨강→주황→초록)로 완료 진도를 인코딩한다. 학생은 전체 완료율 순으로 정렬되어 상위 학생이 위에, 어려움을 겪는 학생이 아래에 자연스럽게 군집된다.

**핵심 인터랙션:** 학생 행을 클릭하면 학생 수준 뷰로 전환된다. **학생 탐색 버튼**으로 학급 뷰로 돌아가지 않고 학생 간 순차 탐색이 가능하다.

### 4.6 뷰 5: AI 활용 패턴 (DR4)

LLM 기반 AI 튜터 활용을 세션, 학생, 프로그래밍 단계별로 시각화한다. 15차시 커리큘럼에 걸쳐 4가지 AI 상호작용 유형---블록 도움, 에러 도움, 시트 도움, 시트 필터---의 분포를 보여준다. 단계별 분할 표시를 통해 학생이 난이도가 높아짐에 따라 AI 활용 패턴이 어떻게 변화하는지 드러낸다.

### 4.7 뷰 6: 활동 유형 분포 (DR2, DR5)

스택 영역 차트는 9가지 활동 유형의 비율을 세션별로 보여주어 커리큘럼의 멀티모달 구조를 드러낸다.

### 4.8 새로운 시각화 1: AI 의존도 글리프 (DR3, DR4)

AI 통합 교육에서 핵심 과제는 생산적 AI 활용(전략적 스캐폴딩)과 비생산적 AI 의존(사고 외주화)을 구별하는 것이다. 기존 지표인 완료율과 AI 요청 횟수는 개별적으로 검토할 때 불충분하다.

**AI 의존도 글리프(AI Dependency Glyph)**는 학생의 학습 행동 4차원을 단일 시각적 마크에 동시 인코딩하는 복합 글리프이다:

**글리프 설계:**
- **외부 링**: 완료율. 원형 진행 호(0--100%)로 인코딩. 발산 색상 스케일 적용.
- **내부 원**: AI 튜터 요청 빈도. 원 반지름으로 인코딩.
- **내부 색상**: 11--15차시(3단계)에서의 AI 의존도 추세. 초록 = 의존도 감소, 빨강 = 의존도 증가, 회색 = AI 미사용.
- **방향 화살표**: 색맹 접근성을 위한 이중 인코딩.

**글리프 사분면 해석:**

| | 낮은 AI 사용 | 높은 AI 사용 |
|---|---|---|
| **높은 완료율** | **자립 학습자** | **AI 의존** |
| **낮은 완료율** | **이탈** | **어려움+도움 탐색** |

글리프는 학생 히트맵의 요약 열과 **의존도 산점도 뷰**에 배치되어, 교육자가 학생들을 4개 행동 사분면으로 시각적으로 군집화할 수 있다.

**디자인 근거:** 완료율과 AI 사용에 대한 별도 막대 차트가 고려되었으나, 프로토타입 테스트에서 두 뷰를 교차 참조하는 인지적 비용이 실시간 교실 모니터링에는 너무 높은 것으로 확인되었다. 통합 글리프가 이를 단일 시각적 비교로 축소한다.

### 4.9 새로운 시각화 2: 성과 절벽 감지기 (DR2, DR3)

"성과 절벽"---커리큘럼 단계 전환 시 급격한 완료율 하락, 가장 흔히 11차시(CODAP 데이터 분석에서 파이썬 프로그래밍으로의 전환)에서 발생---은 데이터에서 가장 일관되게 관찰된 패턴이다. 이 절벽은 코드 없는 인터랙티브 환경에서 텍스트 기반 프로그래밍으로의 인지적 도약이 발생하는 경계에서 나타난다. **성과 절벽 감지기(Performance Cliff Detector)**는 학습 전환 장벽을 자동 감지, 정량화, 주석 처리하는 시각적 분석 파이프라인이다.

**감지 알고리즘:**
1. 각 학급의 세션 완료율 시계열에 대해 1차 차분 계산
2. 임계값(기본 15%p) 이하의 "절벽 지점" 식별
3. **절벽 심각도** 계산: $S = |\Delta c_i| \times \frac{c_{i-1}}{100}$
4. **회복률** 계산: $R = \frac{c_{i+3} - c_i}{c_{i-1} - c_i}$

**SHAP 기반 원인 설명:**
각 감지된 절벽에 SHAP 분석이 동반되어 기여 요인을 식별한다. 이전 차시 완료율, 30% 미만 학생 비율, 학생 간 완료율 편차, 활동 유형 구성, AI 튜터 사용률 등의 특성에 대한 SHAP 값을 계산하고, 영향력 라벨(매우 큰/큰/보통/약한 영향)이 달린 순위 막대 차트로 표시한다.

**시각적 인코딩:**
- 학습 여정 타임라인에 삼각형 절벽 마커 주석. 크기 = 심각도, 색상 = 회복률.
- 타임라인 하단의 **절벽 요약 스트립**으로 학급 간 패턴 비교.
- 개요 수준의 **절벽 히트맵**으로 49개 학교의 절벽 발생 집계.

**디자인 근거:** 초기 프로토타입은 11차시에 정적 빨간 배경을 표시했을 뿐이다. 도메인 전문성에 기반하여, 모든 학교가 11차시에서 절벽을 경험하지 않으며 커리큘럼에 따라 더 이르거나 늦은 차시에서 발생할 수 있음을 확인하였다. 자동 감지로 커리큘럼 구조에 관계없이 절벽이 발생하는 곳을 식별할 수 있다.

### 4.10 새로운 시각화 3: 궤적 정렬 뷰 (DR1, DR5)

학교 간 학습 궤적 비교는 기준선 수준과 학급 크기가 달라 어렵다. **궤적 정렬 뷰(Trajectory Alignment View)**는 학교 간/커리큘럼 간 학습 궤적의 비교 분석을 위한 맞춤 시각화이다.

**설계:**

**(a) 기준선 정규화 스몰 멀티플:** 각 학교의 15차시 궤적을 1차시 = 0%로 정규화하여 절대 수준이 아닌 상대 성장을 표시.

**(b) 궤적 포락선:** 커리큘럼별 25--75 백분위 궤적 대역을 반투명 영역으로 표시. 포락선 아래 학교는 경고 표시.

**(c) 단계별 스파크라인:** 각 스몰 멀티플 아래 4단계(이해/분석/코딩/종합) 평균 완료율 미니 막대.

**(d) 궤적 유사도 클러스터링:** DTW(Dynamic Time Warping) 거리를 사용한 궤적 클러스터링. 덴드로그램과 연동 브러싱으로 유사 패턴 학교 그룹 식별.

**디자인 근거:** 49개 학교의 단일 중첩 라인 차트는 판독 불가능하였다. 스몰 멀티플은 정렬된 공간 위치를 통한 비교를 가능하게 하면서 개별 궤적의 세부 사항을 보존한다. 기준선 정규화가 핵심이었다---이것 없이는 사용자가 "높은 시작 수준"과 "더 나은 궤적"을 일관되게 혼동하였다. 궤적 포락선 개념은 기상 예보 시각화(앙상블 플롯)에서 차용.

### 4.11 디자인 반복: AI-보정 역량 점수 (DR4)

플랫폼 데이터에서의 핵심 관찰은 **완료율 기반 역량 점수가 AI 튜터 의존도에 의해 체계적으로 부풀려질 수 있다**는 점이다. 높은 완료율이지만 많은 AI 사용을 보이는 학생은 점수가 시사하는 역량을 실제로 개발하지 못했을 수 있다. 이 관찰은 4년간의 플랫폼 운영에 기반하며 자동화 안주에 관한 문헌 [Prather et al., 2023]으로 확인되어, 핵심 시스템 기능---LLM 튜터 로그의 역량 측정 통합---을 촉발하였다.

**AI-보정 역량 점수.** AI 튜터 의존도에 비례하여 완료율을 보정하는 독립성 가중 역량 점수를 정의한다:

$$\text{AdjustedScore}_i = \text{RawCompletion}_i \times \frac{1}{1 + \alpha \cdot \text{LLMRate}_i}$$

$\alpha = 0.5$는 의미 있으면서도 과도하지 않은 보정을 생성하도록 설정된 페널티 가중치이다.

**영향.** 709명 학생에 걸쳐:
- **30명**이 10%p 이상의 보정을 경험 (모두 22--87회 AI 요청)
- 가장 극적: S0158이 95.8%(원시) → 65.3%(보정)으로 **-30.5%p 하락** (87회 AI 요청)
- 역량별: DA와 CT가 가장 큰 보정(각 -2.4%p, -2.3%p), DC는 최소 영향(-0.5%p)

**시각적 통합.** 역량 레이더 차트가 "원시"/"AI-보정" 뷰 토글을 제공. AI-보정 모드에서 AI 의존 학생의 레이더 다각형이 수축하여 차이가 즉시 가시화됨. 학생 히트맵도 보정 점수 기반 재색상화를 지원---"숨겨진 빨강"을 드러냄.

**디자인 근거.** 이진 페널티(AI가 사용된 모든 활동 감점)가 고려되었으나 지나치게 가혹한 것으로 판단: 에러 메시지를 이해하기 위한 간헐적 전략적 AI 사용은 모든 코딩 과제에 대한 체계적 의존과 질적으로 다르다. 부드러운 비율 기반 페널티가 이 구별을 보존한다.

### 4.12 연동 인터랙션

9개 뷰(표준 6개 + 새로운 3개)는 다음을 통해 연동된다:
- **필터링**: 커리큘럼, 학교, 세션 범위 선택이 모든 뷰에 전파
- **드릴다운**: 4단계 계층의 일관된 시각적 전환
- **연동 브러싱**: 레이더 차트의 역량 선택 → 타임라인 세션 하이라이트; 궤적 정렬 뷰의 클러스터 선택 → 학교 비교 하이라이트; 의존도 산점도의 사분면 선택 → 히트맵 학생 하이라이트
- **검색**: 학교, 학급, 개별 학생에 대한 텍스트 기반 검색 및 자동 완성
- **세션 슬라이더**: 특정 세션 범위에 집중하는 시간 탐색 제어
- **학생 비교**: 두 학생의 전체 프로필(히트맵, AI 사용, 역량 레이더) 나란히 비교
- **위험 학생 자동 감지**: 학급별 위험 기준(낮은 완료율, 높은 AI 의존도, 갑작스러운 이탈) 충족 학생 자동 식별
- **설정 토글**: AI 보정 점수, XAI 인사이트, 교수학적 추천의 3가지 설정 모드로 정보 밀도 제어
- **세부사항 요청**: 호버 툴팁이 정확한 값 제공
- **절벽 연동 하이라이팅**: 절벽 마커 클릭 → 해당 세션에서 이탈한 학생을 히트맵에서 하이라이트
