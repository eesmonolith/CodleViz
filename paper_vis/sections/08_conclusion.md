# 8. Conclusion

## English

Completion rates are the dominant metric in educational technology, yet they systematically fail when AI tools are embedded in learning platforms. Two students with identical scores can exhibit a 9x difference in AI reliance---a distinction invisible to conventional dashboards but critical for understanding whether learners are building genuine competence or outsourcing their thinking.

CodleViz addresses this measurement gap with four contributions. First, it is the first visual analytics system to integrate generative AI usage logs with task performance data for behavioral AI literacy measurement, combining tabular, temporal, and textual data streams from a live AI-embedded platform into a unified analytical environment. Second, three novel visual analytics techniques---the AI Dependency Glyph, the Performance Cliff Detector with SHAP-based causal explanations, and the Trajectory Alignment View---address specific analytical gaps that no existing learning analytics dashboard provides. Third, the CodleViz system implements these techniques within a coordinated multi-view dashboard with four-level drill-down, nine views, and advanced features including linked brushing, at-risk student auto-detection, student comparison mode, and configurable XAI settings---validated with real data from 709 students across 49 classrooms. Fourth, a formative evaluation with 10 domain experts (6 educators who taught on the platform, 4 external specialists) confirmed the system's analytical value through structured decision tasks (70% cliff detection accuracy, 70% SHAP factor identification, 100% at-risk student identification), per-view usefulness ratings up to 4.8/5.0, and iterative refinement from v0.5 to v1.0.

Three case studies ground these contributions in practice: students with identical completion rates exhibit 9x differences in AI reliance, 8 of 42 classrooms show performance cliffs exceeding 15 percentage points at skill transitions, and curriculum design measurably affects competency development (35.8%--61.9% variance in Computational Thinking scores alone).

Looking ahead, three directions guide future work. First, a second evaluation round on v1.0 with additional participants will validate the iterative improvements and broaden the evidence base. Second, integrating real-time data streaming and predictive models for at-risk student identification would transform CodleViz from a retrospective analytical tool into a live classroom monitoring system. Third, longitudinal deployment studies measuring the impact on teaching practices and student outcomes would provide stronger evidence of the system's practical value.

While grounded in K-12 education, the framework of jointly visualizing task performance and generative AI usage patterns establishes a foundation for measuring AI literacy across professional and everyday contexts. As AI tools become embedded in software development, medical training, creative work, and daily decision-making, the question CodleViz addresses---whether people build genuine competence or develop dependency---will only grow in importance.

---

## 한글

완료율은 교육 기술의 지배적 지표이나, AI 도구가 학습 플랫폼에 내장되면 체계적으로 실패한다. 동일 점수의 두 학생이 AI 의존도에서 9배 차이를 보일 수 있다---기존 대시보드에서는 보이지 않지만 학습자가 진정한 역량을 쌓는지, 사고를 외주화하는지 이해하는 데 핵심적인 구별이다.

CodleViz는 4개 기여로 이 측정 공백을 해소한다. 첫째, 행동적 AI 리터러시 측정을 위해 생성형 AI 사용 로그와 과제 성과 데이터를 통합한 최초의 시각적 분석 시스템으로, 실제 AI 내장 플랫폼의 테이블형, 시계열, 텍스트 데이터 스트림을 통합 분석 환경으로 결합한다. 둘째, 3개 새로운 시각적 분석 기법---AI 의존도 글리프, SHAP 기반 원인 설명을 갖춘 성과 절벽 감지기, 궤적 정렬 뷰---이 기존 학습 분석 대시보드가 제공하지 않는 특정 분석적 공백을 해소한다. 셋째, CodleViz 시스템은 이러한 기법을 4단계 드릴다운, 9개 뷰, 연동 브러싱·위험 학생 자동 감지·학생 비교 모드·설정 가능한 XAI 설정 등 고급 기능을 갖춘 연동형 다중 뷰 대시보드로 구현하며---49개 학급 709명 학생의 실제 데이터로 검증되었다. 넷째, 10명 도메인 전문가(플랫폼에서 실제 수업한 교육자 6명, 외부 전문가 4명) 대상 형성 평가가 구조화 의사결정 과제(절벽 감지 정확도 70%, SHAP 요인 식별 70%, 위험 학생 식별 100%), 뷰 유용성 최대 4.8/5.0, v0.5에서 v1.0으로의 반복적 정제를 통해 시스템의 분석적 가치를 확인하였다.

3개 사례 연구가 이러한 기여를 실제로 뒷받침한다: 동일 완료율 학생 간 AI 의존도 9배 차이, 42개 학급 중 8개에서 역량 전환 시 15%p 이상 성과 절벽, 커리큘럼 설계에 따른 역량 발달 차이(컴퓨팅 사고 점수만으로 35.8%--61.9% 분산).

향후 세 방향이 후속 연구를 안내한다. 첫째, 추가 참여자로 v1.0에 대한 2차 평가 라운드를 수행하여 반복적 개선을 검증하고 증거 기반을 확대한다. 둘째, 실시간 데이터 스트리밍과 위험 학생 식별 예측 모델을 통합하여 CodleViz를 회고적 분석 도구에서 실시간 교실 모니터링 시스템으로 전환한다. 셋째, 교수 실천과 학생 성과에 대한 영향을 측정하는 종단 배포 연구가 시스템의 실용적 가치의 더 강한 증거를 제공할 것이다.

본 연구는 K-12 교육에 기반하지만, 과제 성과와 생성형 AI 사용 패턴을 통합 시각화하는 프레임워크는 전문 업무 및 일상적 맥락에서의 AI 리터러시 측정을 위한 토대를 제공한다. AI 도구가 소프트웨어 개발, 의학 교육, 창작 작업, 일상적 의사결정에 내장됨에 따라, CodleViz가 다루는 질문---사람들이 진정한 역량을 쌓는지, 의존을 개발하는지---의 중요성은 더욱 커질 것이다.
