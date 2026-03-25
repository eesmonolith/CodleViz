# 7. Discussion

## English

### 7.1 AI Literacy Measurement through Behavioral Analytics

The central argument of this work is that AI literacy cannot be adequately measured through completion rates or self-report surveys alone. CodleViz demonstrates that behavioral analytics---jointly visualizing task performance and AI interaction patterns---can surface distinctions invisible to either approach in isolation.

**Completion rates mask divergent AI usage strategies.** Case Study 2 revealed a 9x difference in AI tutor reliance between students with nearly identical completion scores (98.3% vs. 93.5%). This finding is not an edge case: across all 709 students, 493 (70%) used the AI tutor, and 62 students (8.7%) fell in the "AI-Dependent" quadrant where high AI usage did not translate into learning outcomes. These behavioral patterns represent precisely the dimension of AI literacy that survey instruments cannot capture---not what students *know* about AI, but how they *behave* when given access to AI tools during authentic tasks.

**The "performance cliff" reveals where AI scaffolding fails.** The systematic performance drop at curriculum tier transitions (observed in 8 of 42 analyzable schools) marks the boundary where the nature of AI tool usage changes fundamentally. In Tier 2 (CODAP), students could use AI assistance for data filtering guidance. In Tier 3 (Python), the cognitive demands shift to algorithmic thinking, and AI tutor suggestions become less directly actionable. The cliff represents a moment where AI literacy---the ability to productively use AI tools for genuine learning---is tested most severely.

**Curriculum design measurably affects AI literacy development.** The 35.8%--61.9% variance in CT scores across curricula suggests that the timing and balance of hands-on coding activities influence whether students develop independent competence or become reliant on AI assistance. The Food Security curriculum's earlier introduction of coding activities appears to build AI literacy more effectively, reducing dependency during the Python programming phase.

### 7.2 Design Reflections

**The value of multi-level exploration.** The four-level drill-down was consistently identified as CodleViz's most distinctive feature in the evaluation. Existing LADs typically operate at either the institutional level (aggregate reports) or the individual level (student gradebooks), with limited support for the intermediate levels that educators most frequently need. The ability to seamlessly transition from "which schools are struggling" to "which students in those schools" to "what specific patterns characterize those students" enables a diagnostic workflow that is both top-down (identifying problems) and bottom-up (understanding causes).

**SHAP-based explanations: useful but incomplete.** The gap between "helps understand cliff causes" (4.1/5) and "consistent with teaching experience" (3.2/5) in the XAI evaluation is instructive. SHAP explanations identify statistical predictors of performance cliffs, but statistical prediction is not causal explanation. When "prior completion rate" appears as the top factor at every session, educators correctly note that this is tautological---low completion predicts low completion. Deeper causal factors (attendance, student motivation, classroom dynamics) are not captured in the available data. Future work should integrate richer contextual data to make SHAP explanations more pedagogically meaningful.

**Domain immersion as design methodology.** Rather than conducting formal design study interviews, the design requirements for CodleViz emerged from four years of platform operation by the first author. This approach---what Sedlmair et al. [2012] might classify as deep domain immersion through the *front-line analyst* role---has both strengths and limitations. The strength is ecological validity: the requirements reflect real operational pain points rather than hypothetical needs elicited in interview settings. The limitation is potential bias: a single researcher's operational experience may not capture the full diversity of educator needs. The formative evaluation with 10 domain experts partially addresses this limitation by validating the requirements with a broader set of stakeholders.

### 7.3 Limitations

**Single evaluation round.** The formative evaluation with 10 domain experts represents a single round of assessment. A second round with additional participants, conducted on v1.0 after iterative refinements, is planned to validate the improvements and broaden the participant pool. Longitudinal deployment studies measuring the impact of CodleViz on teaching practices and student outcomes would provide stronger evidence of the system's value.

**Data completeness.** Not all schools completed both pre-test and post-test assessments, limiting paired comparison analysis. Of the 49 schools, only 11 have sufficient paired data for statistical significance testing. Future deployments should enforce assessment completion protocols.

**Standalone system.** CodleViz operates as a standalone D3.js dashboard that analyzes data exported from the Codle platform, rather than being integrated directly into the platform. This means educators must export data and load it into a separate tool, adding friction to the analytical workflow. Integration into the Codle platform's native interface would reduce this barrier.

**Scalability.** The current implementation processes data in batch mode from CSV exports. For real-time classroom monitoring (the most requested feature in the evaluation), a streaming data pipeline would be required.

**Generalizability.** The system was developed in the specific context of South Korean K-12 data science education. The design requirements, competency framework, and curriculum structure may not directly transfer to other educational contexts. However, the core analytical framework---jointly visualizing task performance and generative AI usage patterns---is domain-independent and could be adapted to any context where AI tools are embedded in authentic tasks: professional training platforms, coding bootcamps, or corporate learning management systems.

### 7.4 Broader Implications: AI Literacy Beyond Education

While CodleViz is grounded in K-12 education, the underlying framework has implications beyond this specific domain. As generative AI tools become embedded in professional work (coding assistants, writing tools, data analysis copilots), the question of AI literacy---whether users build genuine competence or develop dependency---becomes relevant across all domains. The approach demonstrated here, jointly analyzing task performance and AI interaction logs, could be applied to:

1. **Professional training**: Measuring whether software engineers develop debugging skills or become dependent on AI code completion tools.
2. **Medical education**: Assessing whether clinical trainees develop diagnostic reasoning or rely on AI decision support systems.
3. **Creative work**: Understanding whether designers use AI tools to augment creativity or substitute for original thinking.

The key insight is that AI literacy measurement requires *behavioral* data from authentic tasks, not self-reported attitudes. CodleViz establishes a methodological precedent for this approach, demonstrating that visual analytics can make the hidden dimension of AI dependency visible and actionable.

---

## 한글

### 7.1 행동 분석을 통한 AI 리터러시 측정

본 연구의 핵심 주장은 AI 리터러시가 완료율이나 자기보고 설문만으로는 적절히 측정될 수 없다는 것이다. CodleViz는 행동 분석---과제 성과와 AI 상호작용 패턴의 통합 시각화---이 어느 한 접근법만으로는 보이지 않는 구분을 드러낼 수 있음을 보여준다.

**완료율은 상이한 AI 사용 전략을 가린다.** 사례 연구 2는 거의 동일한 완료율(98.3% vs. 93.5%)을 가진 학생 간 AI 튜터 의존도에서 9배 차이를 드러냈다. 이것은 예외적 사례가 아니다: 전체 709명 중 493명(70%)이 AI 튜터를 사용하였으며, 62명(8.7%)이 높은 AI 사용이 학습 성과로 연결되지 않는 "AI 의존" 사분면에 위치하였다. 이러한 행동 패턴은 설문 도구가 포착할 수 없는 AI 리터러시의 차원---학생이 AI에 대해 *아는* 것이 아니라 실제 과제에서 AI 도구에 접근할 때 *어떻게 행동하는지*---을 정확히 대표한다.

**"성과 절벽"은 AI 스캐폴딩이 실패하는 지점을 드러낸다.** 커리큘럼 단계 전환에서의 체계적 성과 하락(분석 가능한 42개 학교 중 8개에서 관찰)은 AI 도구 사용의 본질이 근본적으로 변하는 경계를 표시한다. 절벽은 AI 리터러시---진정한 학습을 위해 AI 도구를 생산적으로 사용하는 능력---가 가장 심하게 시험받는 순간을 대표한다.

**커리큘럼 설계가 AI 리터러시 발달에 측정 가능한 영향을 미친다.** 커리큘럼 간 CT 점수의 35.8%--61.9% 분산은 실습 코딩 활동의 시기와 균형이 학생이 독립적 역량을 개발하는지, AI 지원에 의존하게 되는지에 영향을 미침을 시사한다.

### 7.2 디자인 성찰

**다단계 탐색의 가치.** 4단계 드릴다운이 평가에서 CodleViz의 가장 차별적 기능으로 일관되게 식별되었다. 기존 LAD는 기관 수준이나 개인 수준에서 작동하며, 교사와 관리자가 가장 빈번히 필요로 하는 중간 수준에 대한 지원이 제한적이다.

**SHAP 기반 설명: 유용하나 불완전.** XAI 평가에서 "원인 이해 도움"(4.1/5)과 "경험 일치"(3.2/5) 간 격차는 시사적이다. SHAP 설명은 성과 절벽의 통계적 예측인자를 식별하나, 통계적 예측이 인과적 설명은 아니다. "이전 차시 완료율"이 매 차시 최상위 요인으로 나타날 때, 교육자들은 이것이 동어반복적임을 정확히 지적한다. 더 깊은 인과 요인(출석, 동기, 학급 역학)은 가용 데이터에 포착되지 않는다. 향후 연구에서 더 풍부한 맥락 데이터를 통합하여 SHAP 설명의 교수학적 의미를 높여야 한다.

**디자인 방법론으로서의 도메인 몰입.** CodleViz의 디자인 요구사항은 공식적 디자인 스터디 인터뷰가 아닌 제1저자의 4년간 플랫폼 운영으로부터 도출되었다. 이 접근법의 강점은 생태학적 타당성이다: 요구사항이 인터뷰 환경에서 도출된 가설적 요구가 아닌 실제 운영적 문제점을 반영한다. 한계는 잠재적 편향이다: 단일 연구자의 운영 경험이 교육자 요구의 전체 다양성을 포착하지 못할 수 있다. 10명 도메인 전문가 대상 형성 평가가 더 넓은 이해관계자 집단으로 요구사항을 검증함으로써 이 한계를 부분적으로 해소한다.

### 7.3 한계

**단일 평가 라운드.** 10명 도메인 전문가 대상 형성 평가는 단일 평가 라운드를 대표한다. 반복적 정제 후 v1.0에 대해 추가 참여자로 2차 라운드를 수행하여 개선 사항을 검증하고 참여자 풀을 확대할 계획이다. CodleViz가 교수 실천과 학생 성과에 미치는 영향을 측정하는 종단 배포 연구가 시스템 가치의 더 강한 증거를 제공할 것이다.

**데이터 완전성.** 모든 학교가 사전/사후 평가를 모두 완료하지 않아 대응 비교 분석이 제한된다. 49개 학교 중 11개만 통계적 유의성 검정에 충분한 대응 데이터를 보유하고 있다.

**독립형 시스템.** CodleViz는 코들 플랫폼에 직접 통합되지 않고, 플랫폼에서 내보낸 데이터를 분석하는 독립형 D3.js 대시보드로 작동한다. 교육자가 데이터를 내보내고 별도 도구에 로드해야 하므로 분석 워크플로우에 마찰이 추가된다.

**확장성.** 현재 구현은 CSV 내보내기에서 배치 모드로 데이터를 처리한다. 실시간 교실 모니터링(평가에서 가장 많이 요청된 기능)을 위해서는 스트리밍 데이터 파이프라인이 필요하다.

**일반화 가능성.** 시스템은 한국 K-12 데이터 사이언스 교육의 특정 맥락에서 개발되었다. 그러나 핵심 분석 프레임워크---과제 성과와 생성형 AI 사용 패턴의 통합 시각화---는 도메인 독립적이며, AI 도구가 실제 과제에 내장된 모든 맥락에 적응 가능하다: 전문 교육 플랫폼, 코딩 부트캠프, 기업 학습관리 시스템 등.

### 7.4 더 넓은 시사점: 교육을 넘어선 AI 리터러시

CodleViz는 K-12 교육에 기반하지만, 기저의 프레임워크는 이 특정 도메인을 넘어서는 시사점을 갖는다. 생성형 AI 도구가 전문 업무(코딩 어시스턴트, 작문 도구, 데이터 분석 코파일럿)에 내장됨에 따라, AI 리터러시 문제---사용자가 진정한 역량을 쌓는지, 의존을 개발하는지---는 모든 도메인에서 적합해진다. 여기서 시연된 접근법은 다음에 적용될 수 있다:

1. **전문 교육**: 소프트웨어 엔지니어가 디버깅 역량을 개발하는지, AI 코드 완성 도구에 의존하게 되는지 측정.
2. **의학 교육**: 임상 수련생이 진단 추론을 개발하는지, AI 의사결정 지원 시스템에 의존하는지 평가.
3. **창작 작업**: 디자이너가 AI 도구를 창의성 증강에 사용하는지, 독창적 사고의 대체물로 사용하는지 이해.

핵심 통찰은 AI 리터러시 측정이 자기보고된 태도가 아닌 실제 과제의 *행동* 데이터를 필요로 한다는 것이다. CodleViz는 이 접근법의 방법론적 선례를 수립하여, 시각적 분석이 AI 의존도의 숨겨진 차원을 가시적이고 실행 가능하게 만들 수 있음을 보여준다.
