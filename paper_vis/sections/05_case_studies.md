# 5. Case Studies

## English

Three case studies demonstrate how CodleViz enables AI literacy measurement in practice, revealing patterns invisible to conventional completion-based dashboards. Each case study uses real data from the Codle platform and illustrates the system's four-level drill-down workflow.

### 5.1 Case Study 1: Identifying Divergent School Trajectories

**Context:** Understanding why schools with identical curricula produce dramatically different learning outcomes is a prerequisite for evidence-based curriculum revision. The Overview level of CodleViz enables this comparison at a glance.

**Analysis with CodleViz:** Starting from the Overview level, the school comparison bar chart revealed that School_01 (Ocean Debris curriculum, 20 students) had an average progress of 83.6%, while School_35 (same curriculum, 14 students) was at 28.3%---a nearly 3x gap despite using identical course material.

Drilling down to the School level, the competency radar charts showed the divergence in detail. School_01 had uniformly high scores across all five competencies (DC: 85.3%, DA: 87.6%, DV: 83.0%, DI: 78.9%, CT: 81.1%), while School_35 showed a stark imbalance: DC at 47.3% but DV dropping to 7.1% and CT to 16.7%.

The learning journey timeline revealed the critical divergence point. School_35's completion rate was reasonable in early sessions (S2: 59.5%, S3: 54.1%) but collapsed after session 6 (S7: 2.4%, S9: 9.8%, S10: 3.6%, S11: 6.1%)---a "cliff before the cliff." The Performance Cliff Detector confirmed this: sessions 1--10 averaged 30.8% completion while sessions 11--15 dropped further to 14.1%. In contrast, School_01 maintained above 77% throughout all 15 sessions.

Across all 49 schools, the cliff heatmap aggregation showed that 8 of 42 analyzable schools experienced drops exceeding 15 percentage points at the session 10-to-11 transition, confirming the "performance cliff" as a systematic pattern rather than an isolated incident.

**AI Literacy Measurement Insight:** The performance gap is not uniform across the curriculum---it concentrates at tier transitions where the nature of AI tool usage changes fundamentally. Schools where students struggled in Tier 2 (CODAP) also showed elevated AI tutor usage in those sessions, suggesting that early dependence on AI assistance may predict later disengagement when AI scaffolding becomes insufficient for the cognitive demands of Python programming. This multi-level pattern was invisible in aggregate completion statistics but immediately apparent through CodleViz's coordinated views.

### 5.2 Case Study 2: Detecting AI Tutor Over-Reliance

**Context:** When AI tutors are embedded in learning platforms, completion rates lose their validity as competency measures. Two students with identical scores may have fundamentally different levels of AI literacy---one building genuine competence, the other outsourcing thinking. Detecting this difference is the central challenge of behavioral AI literacy measurement.

**Analysis with CodleViz:** At the Classroom level for School_01 (Ocean Debris, 20 students), the AI Dependency Glyph scatter plot immediately revealed that 14 of 20 students fell in the "AI-Scaffolded" quadrant (high completion, high AI usage), while only 4 were "Independent" (high completion, low AI usage).

Drilling down, two students with nearly identical completion rates told strikingly different stories: Student S0486 (completion: 98.3%, 53 AI tutor requests) and Student S0480 (completion: 93.5%, only 6 requests)---a **9x difference** in AI reliance despite comparable outcomes. The per-session LLM usage breakdown revealed that S0486's AI requests were concentrated in session 7 (23 requests during CODAP data analysis) and session 8 (20 requests), suggesting heavy reliance during the analysis-to-coding transition. S0486's AI usage then declined sharply (trend: -15.5), indicating eventual adaptation. S0480 used the AI tutor only twice in session 8 and four times in session 13, showing consistent independence.

Across all 709 students, 493 (70%) used the AI tutor at least once, with a median of 9 requests per user. The AI Dependency classification revealed 62 students (8.7%) in the "AI-Dependent" quadrant (low completion despite high AI usage)---students for whom AI support was not translating into learning outcomes.

**AI Literacy Measurement Insight:** Completion rates mask fundamentally different AI usage strategies. The AI Dependency Glyph makes this hidden dimension visible and actionable: educators can identify the 62 AI-dependent students who need pedagogical intervention rather than more AI support. From an AI literacy perspective, the distinction between S0486 (high usage but decreasing trend---learning to use AI productively) and the 62 AI-dependent students (high usage, low completion---failing to learn with or without AI) represents precisely the behavioral nuance that survey-based AI literacy instruments cannot capture.

### 5.3 Case Study 3: Curriculum-Specific Competency Patterns

**Context:** When multiple curricula are deployed across different schools, understanding how curriculum design affects competency development is essential for evidence-based revision. The AI literacy question here is whether certain curriculum structures better support the development of independent competence versus AI-dependent completion.

**Analysis with CodleViz:** Using the Overview level's competency filter, the Trajectory Alignment View with baseline normalization revealed striking differences across the three curricula. Food Security schools averaged 61.9% on CT (Computational Thinking), compared to Ocean Debris at 44.3% and Climate Change at only 35.8%.

This gap was consistent across all five competencies. Food Security outperformed the others on every measure: DC (67.1% vs. 54.9% vs. 46.3%), DA (62.8% vs. 51.0% vs. 34.3%), DV (46.6% vs. 27.0% vs. 19.6%), DI (43.4% vs. 33.3% vs. 31.1%), and CT (61.9% vs. 44.3% vs. 35.8%). Climate Change consistently showed the lowest scores.

The activity type distribution view revealed a potential explanation: the Food Security curriculum incorporated a more balanced mix of activity types across sessions, with coding activities (Studio and Entry) appearing earlier and more frequently in Tier 2 (sessions 6--10). Climate Change relied more heavily on PDF and Video activities during the same phase, providing less hands-on preparation for the Tier 3 coding transition.

At the session timeline level, Food Security classrooms showed more gradual completion rate changes across sessions 11--15, while Climate Change classrooms showed the steepest drops, with the lowest overall recovery.

**AI Literacy Measurement Insight:** Curriculum design---specifically the timing and balance of activity types---has a measurable impact on competency development trajectories (35.8%--61.9% variance in CT alone). Earlier, more distributed introduction of coding activities appears to reduce the abruptness of the Tier 2-to-3 transition. From an AI literacy perspective, the Food Security curriculum's earlier hands-on activities may better prepare students for independent problem-solving, reducing the need for AI assistance during the Python programming phase. This finding informed a specific curriculum revision recommendation: blending lightweight Python exercises into Tier 2 sessions for the Ocean Debris and Climate Change curricula.

---

## 한글

3개 사례 연구를 통해 CodleViz가 실제로 AI 리터러시 측정을 어떻게 가능하게 하는지 시연하며, 기존 완료율 기반 대시보드에서는 보이지 않는 패턴을 드러낸다. 각 사례 연구는 코들 플랫폼의 실제 데이터를 사용하며 시스템의 4단계 드릴다운 워크플로우를 보여준다.

### 5.1 사례 연구 1: 학교 간 궤적 격차 발견

**맥락:** 동일 커리큘럼을 사용하면서도 극적으로 다른 학습 성과를 보이는 학교 간 차이를 이해하는 것은 증거 기반 커리큘럼 개정의 전제 조건이다.

**CodleViz 분석:** 개요 수준에서 학교 비교 막대 그래프를 통해 School_01(해양쓰레기, 20명, 평균 진도 83.6%)과 School_35(동일 커리큘럼, 14명, 28.3%) 간 약 3배 격차를 확인하였다.

학교 수준으로 드릴다운하여 역량 레이더 차트를 비교한 결과, School_01은 모든 역량에서 균일하게 높은 점수(DC: 85.3%, DA: 87.6%, DV: 83.0%, DI: 78.9%, CT: 81.1%)를 보인 반면, School_35는 DC 47.3%에서 DV 7.1%, CT 16.7%로 급감하는 불균형을 보였다.

학습 여정 타임라인은 핵심 분기점을 드러냈다. School_35의 완료율은 초기 세션에서는 양호했으나(S2: 59.5%, S3: 54.1%), 6차시 이후 붕괴하여(S7: 2.4%, S9: 9.8%, S10: 3.6%, S11: 6.1%) "절벽 전의 절벽" 패턴을 보였다. 1--10차시 평균 30.8%에서 11--15차시 14.1%로 추가 하락하였고, School_01은 전 15차시에 걸쳐 77% 이상을 유지하였다.

전체 49개 학교에 걸쳐 절벽 히트맵 집계는 분석 가능한 42개 학교 중 8개가 10→11차시 전환에서 15%p 이상의 하락을 경험하였음을 보여, "성과 절벽"이 고립된 사건이 아닌 체계적 패턴임을 확인하였다.

**AI 리터러시 측정 인사이트:** 성과 격차는 커리큘럼 전반에 걸쳐 균일하지 않고, AI 도구 사용의 본질이 근본적으로 변하는 단계 전환에 집중된다. 2단계(CODAP)에서 어려움을 겪은 학교는 해당 세션에서 AI 튜터 사용도 증가하여, AI 지원에 대한 초기 의존이 파이썬 프로그래밍의 인지적 요구에 AI 스캐폴딩이 불충분해질 때 이탈을 예측할 수 있음을 시사한다. 이 다단계 패턴은 집계 통계에서는 보이지 않았으나 CodleViz의 연동 뷰를 통해 즉시 드러났다.

### 5.2 사례 연구 2: AI 튜터 과의존 감지

**맥락:** AI 튜터가 학습 플랫폼에 내장되면 완료율은 역량 측정 지표로서의 타당성을 상실한다. 동일 점수의 두 학생이 근본적으로 다른 수준의 AI 리터러시를 가질 수 있다---하나는 진정한 역량을 쌓고, 다른 하나는 사고를 외주화한다. 이 차이를 감지하는 것이 행동적 AI 리터러시 측정의 핵심 과제이다.

**CodleViz 분석:** School_01(해양쓰레기, 20명) 학급 수준에서 AI 의존도 글리프 산점도를 검토한 결과, 20명 중 14명이 "AI-Scaffolded" 사분면(높은 완료율, 높은 AI 사용)에, 4명만 "Independent"(높은 완료율, 낮은 AI 사용)에 위치하였다.

드릴다운하여 거의 동일한 완료율을 가진 두 학생을 비교: S0486(완료율 98.3%, AI 53회 요청)과 S0480(완료율 93.5%, 6회 요청)---유사한 성과에도 **9배 차이**의 AI 의존도를 보였다. 세션별 LLM 사용 분석에서 S0486의 AI 요청은 7차시(23회, CODAP 데이터 분석)와 8차시(20회)에 집중되어, 분석→코딩 전환 구간에서의 높은 의존도를 시사하였다. 이후 급격히 감소(추세: -15.5)하여 적응을 보였다. 반면 S0480은 8차시 2회, 13차시 4회만 사용하여 일관된 독립성을 보였다.

전체 709명 중 493명(70%)이 AI 튜터를 1회 이상 사용하였으며(중앙값: 사용자당 9회), AI 의존도 분류에서 62명(8.7%)이 "AI-Dependent" 사분면(높은 AI 사용에도 낮은 완료율)에 위치---AI 지원이 학습 성과로 연결되지 않는 학생들이었다.

**AI 리터러시 측정 인사이트:** 완료율은 근본적으로 다른 AI 사용 전략을 가린다. AI 의존도 글리프는 이 숨겨진 차원을 가시화하여 실행 가능한 정보로 전환한다. AI 리터러시 관점에서, S0486(높은 사용이나 감소 추세---AI를 생산적으로 사용하는 법을 학습)과 62명의 AI 의존 학생(높은 사용, 낮은 완료율---AI 유무와 관계없이 학습 실패) 간의 구별은 정확히 설문 기반 AI 리터러시 도구가 포착할 수 없는 행동적 뉘앙스를 대표한다.

### 5.3 사례 연구 3: 커리큘럼별 역량 발달 패턴

**맥락:** 복수 커리큘럼이 서로 다른 학교에 배포될 때, 커리큘럼 설계가 역량 발달에 미치는 영향을 이해하는 것은 증거 기반 개정에 필수적이다. 여기서의 AI 리터러시 질문은 특정 커리큘럼 구조가 독립적 역량 개발을 AI 의존적 완료보다 더 잘 지원하는지이다.

**CodleViz 분석:** 개요 수준의 역량 필터와 궤적 정렬 뷰(기준선 정규화 적용)를 사용하여 3개 커리큘럼 간 뚜렷한 차이가 드러났다: 식량안보 평균 CT 61.9%, 해양쓰레기 44.3%, 기후변화 35.8%.

이 격차는 5개 역량 전체에서 일관되었다. 식량안보가 모든 역량에서 우위: DC(67.1% vs. 54.9% vs. 46.3%), DA(62.8% vs. 51.0% vs. 34.3%), DV(46.6% vs. 27.0% vs. 19.6%), DI(43.4% vs. 33.3% vs. 31.1%), CT(61.9% vs. 44.3% vs. 35.8%). 기후변화가 일관되게 최저 점수를 보였다.

활동 유형 분포 뷰는 잠재적 설명을 제시: 식량안보 커리큘럼이 세션 전반에 걸쳐 더 균형 잡힌 활동 유형 조합을 편성하여 코딩 활동(Studio, Entry)이 2단계(6--10차시)에 더 일찍, 더 빈번히 등장하였다. 반면 기후변화는 동일 단계에서 PDF와 Video 활동에 더 의존하여 3단계 코딩 전환에 대한 실습 준비가 부족하였다.

**AI 리터러시 측정 인사이트:** 커리큘럼 설계---특히 활동 유형의 시기와 균형---가 역량 발달 궤적에 측정 가능한 영향을 미친다(CT만으로 35.8%--61.9% 분산). AI 리터러시 관점에서, 식량안보 커리큘럼의 조기 실습 활동이 독립적 문제해결을 더 잘 준비시켜 파이썬 프로그래밍 단계에서 AI 지원 필요성을 줄이는 것으로 보인다. 이 발견은 해양쓰레기·기후변화 커리큘럼의 2단계에 경량 파이썬 연습을 혼합하는 구체적 커리큘럼 개정 권고로 이어졌다.
