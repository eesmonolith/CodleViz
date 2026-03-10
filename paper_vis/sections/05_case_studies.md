# 5. Case Studies

## English

We demonstrate CodleViz's analytical capabilities through three case studies conducted with domain experts (T1, T3, R1). Each case study illustrates how the coordinated multi-view design enables insights that were previously inaccessible through conventional dashboards.

### 5.1 Case Study 1: Identifying Divergent School Trajectories

**Context:** R1, an education researcher at the Korea Foundation, needed to understand why some schools showed dramatically higher learning outcomes than others despite using identical curricula.

**Analysis with CodleViz:** Starting from the Overview level, R1 used the school comparison bar chart to identify that 경포고 (Gyeongpo High School, Ocean Debris curriculum) had an average progress of 83.6%, while 천안두정중 (Cheonan Dujeong Middle School, same curriculum) was at 28.9%—a nearly 3× gap.

Drilling down to the School level, R1 compared the competency radar charts side by side. 경포고 showed uniformly high scores across all five competencies (DC: 85.3%, DA: 87.6%, DV: 83.0%, DI: 78.9%, CT: 81.1%), while 천안두정중 showed a stark imbalance: DC at 67.5% but CT dropping to 28.9%.

The learning journey timeline revealed the critical divergence point: 천안두정중's completion rate dropped sharply at session 8 (the "coding cliff"), falling from ~60% in sessions 1–7 to below 20% in sessions 8–15. In contrast, 경포고 maintained above 65% throughout.

**Insight:** The performance gap is not uniform across the curriculum—it is concentrated at the transition from data analysis to Python programming (session 8). This suggests that middle school students may need additional scaffolding for the coding phase, a curriculum design insight that was invisible in aggregate completion statistics.

### 5.2 Case Study 2: Detecting AI Tutor Over-Reliance

**Context:** T2, a high school teacher, expressed concern that some students were using the AI tutor as a "crutch" rather than developing independent problem-solving skills.

**Analysis with CodleViz:** At the Classroom level, T2 examined the student heatmap for her class. She noticed that Student S07 showed perfect completion (green across all sessions) but had the highest AI tutor usage count in the class.

Drilling down to S07's Student view, the per-session breakdown revealed that S07 requested AI help an average of 4.2 times per coding activity, compared to the class average of 1.1. More critically, S07's AI usage *increased* over sessions 8–15 rather than decreasing, suggesting no development of independent debugging skills.

Comparing with S12, who had similar completion rates but only 0.6 AI requests per activity, T2 identified a clear distinction between **strategic AI users** (who gradually reduce reliance) and **dependent AI users** (who maintain or increase reliance).

**Insight:** Completion rates alone are misleading—a student can appear successful while developing dependency on AI tools. CodleViz's combination of completion heatmap and AI usage patterns reveals this hidden dimension of learning quality.

### 5.3 Case Study 3: Curriculum-Specific Competency Patterns

**Context:** T3, a teacher who had taught both Ocean Debris and Food Security curricula, wanted to understand whether different themes led to different competency development patterns.

**Analysis with CodleViz:** Using the Overview level's competency filter, T3 compared CT (Computational Thinking) scores across curricula. Ocean Debris schools averaged 48.1% on CT, while Food Security schools averaged 55.2%.

The activity type distribution view revealed a potential explanation: the Food Security curriculum allocated proportionally more Studio (coding) activities in sessions 4–7, introducing Python earlier than the Ocean Debris curriculum. This earlier exposure appeared to smooth the "coding cliff" transition at session 8.

At the session timeline level, Food Security classrooms showed a gradual increase in completion rate across sessions 8–11, while Ocean Debris classrooms showed a sharp dip at session 8 followed by partial recovery.

**Insight:** Curriculum theme affects not only content engagement but also competency development trajectories. Earlier introduction of coding activities appears to reduce the abruptness of the coding phase transition. This insight informed a curriculum revision recommendation.

---

## 한글

도메인 전문가(T1, T3, R1)와 함께 수행한 3개 사례 연구를 통해 CodleViz의 분석 역량을 시연한다.

### 5.1 사례 연구 1: 학교 간 궤적 격차 발견

**맥락:** 한국과학창의재단의 교육 연구자 R1은 동일 커리큘럼을 사용함에도 일부 학교의 학습 성과가 극적으로 높은 이유를 파악해야 했다.

**CodleViz 분석:** 개요 수준에서 학교 비교 막대 그래프를 통해 경포고(해양쓰레기, 평균 진도 83.6%)와 천안두정중(동일 커리큘럼, 28.9%) 간 약 3배 격차를 확인하였다.

학교 수준으로 드릴다운하여 역량 레이더 차트를 비교한 결과, 경포고는 모든 역량에서 균일하게 높은 점수를 보인 반면, 천안두정중은 DC 67.5%에서 CT 28.9%로 급감하는 불균형을 보였다.

학습 여정 타임라인은 핵심 분기점을 드러냈다: 천안두정중의 완료율이 8차시("코딩 절벽")에서 급락하여 1~7차시의 ~60%에서 8~15차시의 20% 이하로 떨어졌다.

**인사이트:** 성과 격차는 커리큘럼 전반에 걸쳐 균일하지 않고, 데이터 분석에서 파이썬 프로그래밍으로의 전환(8차시)에 집중된다. 중학생에게 코딩 단계에 대한 추가 스캐폴딩이 필요할 수 있다는 커리큘럼 설계 인사이트로, 집계 통계에서는 보이지 않았던 것이다.

### 5.2 사례 연구 2: AI 튜터 과의존 감지

**맥락:** 고등학교 교사 T2는 일부 학생이 독립적 문제해결 능력을 기르지 않고 AI 튜터를 "지팡이"로 사용하는 것을 우려하였다.

**CodleViz 분석:** 학급 수준에서 학생 히트맵을 검토한 결과, 학생 S07이 모든 세션에서 완벽한 완료(전체 초록)를 보이면서도 학급 내 가장 높은 AI 튜터 활용 횟수를 기록하였다. S07은 코딩 활동당 평균 4.2회 AI 도움을 요청하였고(학급 평균 1.1회), 8~15차시에서 AI 사용이 감소하지 않고 *증가*하여 독립적 디버깅 능력의 미발달을 시사하였다.

**인사이트:** 완료율만으로는 오해를 초래할 수 있다—학생이 성공적으로 보이면서도 AI 도구에 대한 의존성을 키울 수 있다. CodleViz의 완료 히트맵과 AI 활용 패턴의 조합이 이 학습 품질의 숨겨진 차원을 드러낸다.

### 5.3 사례 연구 3: 커리큘럼별 역량 발달 패턴

**맥락:** 해양쓰레기와 식량안보 커리큘럼을 모두 가르친 교사 T3는 서로 다른 주제가 역량 발달 패턴의 차이로 이어지는지 알고 싶었다.

**CodleViz 분석:** 개요 수준의 역량 필터를 사용하여 커리큘럼 간 CT 점수를 비교한 결과, 해양쓰레기 학교 평균 48.1%, 식량안보 학교 평균 55.2%였다.

활동 유형 분포 뷰는 식량안보 커리큘럼이 4~7차시에 스튜디오(코딩) 활동을 비례적으로 더 많이 배치하여 파이썬을 더 일찍 도입하고 있음을 보여주었다. 이 조기 노출이 8차시의 "코딩 절벽" 전환을 완화하는 것으로 보였다.

**인사이트:** 커리큘럼 주제는 콘텐츠 참여뿐 아니라 역량 발달 궤적에도 영향을 미친다. 코딩 활동의 조기 도입이 코딩 단계 전환의 급격함을 줄이는 것으로 보이며, 이 인사이트가 커리큘럼 개정 권고에 반영되었다.
