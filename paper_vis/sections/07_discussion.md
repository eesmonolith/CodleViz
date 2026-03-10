# 7. Discussion

## English

### 7.1 Design Reflections

**The "Coding Cliff" as a universal pattern.** Across multiple case studies and evaluation sessions, the sharp drop in completion rate at session 8—the transition from data analysis to Python programming—emerged as the most consistently observed pattern. This "coding cliff" was visible in nearly every school using the Ocean Debris curriculum and to a lesser extent in the Food Security curriculum. CodleViz's learning journey timeline made this pattern immediately apparent, whereas conventional grade-based systems only revealed it retrospectively through final assessment scores. This finding has direct implications for curriculum design: introducing lightweight coding activities earlier (sessions 4–7) appears to reduce the cliff's severity, as evidenced by cross-curriculum comparison.

**AI tutor usage as a hidden dimension of learning.** Our case studies revealed that completion rates can mask fundamentally different learning strategies. Students with identical progress scores can exhibit vastly different AI tutor reliance patterns. This finding aligns with the broader concern in AI-assisted education about the distinction between productive AI use (strategic scaffolding) and counterproductive AI dependency (outsourcing thinking). CodleViz makes this distinction visible through the juxtaposition of completion heatmaps and AI usage patterns—a combination that no existing LAD provides.

**The value of multi-level exploration.** The four-level drill-down was consistently identified as CodleViz's most distinctive and valuable feature. Existing LADs typically operate at either the institutional level (aggregate reports) or the individual level (student gradebooks), with little support for the intermediate levels that teachers and administrators most frequently need. The ability to seamlessly transition from "which schools are struggling" to "which students in those schools" to "what specific patterns characterize those students" enables a diagnostic workflow that is both top-down (identifying problems) and bottom-up (understanding causes).

### 7.2 Limitations

**Data completeness.** Not all schools completed both pre-test and post-test assessments, limiting paired comparison analysis. Of the 49 schools, only 11 have sufficient paired data for statistical significance testing. Future deployments should enforce assessment completion protocols.

**Scalability.** CodleViz currently processes data in batch mode from CSV exports. For real-time classroom monitoring (as identified in expert evaluation), a streaming data pipeline would be required. The current Streamlit-based implementation may face performance limitations with significantly larger datasets.

**Generalizability.** Our design study was conducted in the specific context of South Korean K-12 data science education. The design requirements, competency framework, and curriculum structure may not directly transfer to other educational contexts. However, the four-level drill-down paradigm and the coordinated multi-view approach are domain-independent architectural choices that could be adapted to other educational settings.

**Evaluation scope.** Our expert evaluation included eight domain experts from the Codle ecosystem. A broader evaluation with teachers from other platforms and educational contexts would strengthen the generalizability claims. Additionally, a longitudinal deployment study measuring the impact of CodleViz on teaching practices and student outcomes would provide stronger evidence of the system's value.

### 7.3 Implications for Education Technology

CodleViz demonstrates that as learning platforms incorporate increasingly diverse activity types and AI-powered tools, the visualization needs of educators evolve correspondingly. Simple completion dashboards are no longer sufficient—educators need tools that reveal the *how* and *why* of learning, not just the *what*. This has implications for:

1. **Platform design**: Learning platforms should expose rich event-level data through APIs to enable third-party visual analytics tools.
2. **AI transparency**: As AI tutors become ubiquitous, visualization of AI usage patterns should be a standard feature of educational dashboards.
3. **Curriculum analytics**: Visual analytics can serve as a feedback loop for curriculum design, revealing which pedagogical transitions are most challenging and where intervention is most needed.

---

## 한글

### 7.1 디자인 성찰

**"코딩 절벽"의 보편적 패턴.** 다수의 사례 연구와 평가 세션에서 8차시(데이터 분석에서 파이썬 프로그래밍으로의 전환)에서의 급격한 완료율 하락이 가장 일관되게 관찰된 패턴으로 나타났다. CodleViz의 학습 여정 타임라인은 이 패턴을 즉시 드러냈으나, 기존 성적 기반 시스템은 최종 평가 점수를 통해 사후적으로만 이를 보여주었다. 이 발견은 커리큘럼 설계에 직접적 시사점을 갖는다: 경량 코딩 활동을 더 일찍(4~7차시) 도입하면 절벽의 심각성이 줄어드는 것으로 보인다.

**AI 튜터 활용: 학습의 숨겨진 차원.** 사례 연구들은 완료율이 근본적으로 다른 학습 전략을 가릴 수 있음을 보여주었다. 동일한 진도 점수를 가진 학생이 매우 다른 AI 튜터 의존 패턴을 보일 수 있다. CodleViz는 완료 히트맵과 AI 활용 패턴의 병치를 통해 이 구분을 가시화한다—기존 LAD가 제공하지 않는 조합이다.

**다단계 탐색의 가치.** 4단계 드릴다운이 CodleViz의 가장 차별적이고 가치 있는 기능으로 일관되게 식별되었다. 기존 LAD는 기관 수준(집계 보고서)이나 개인 수준(학생 성적표)에서 작동하며, 교사와 관리자가 가장 빈번히 필요로 하는 중간 수준에 대한 지원이 부족하다.

### 7.2 한계

**데이터 완전성.** 모든 학교가 사전/사후 평가를 모두 완료하지 않아 대응 비교 분석이 제한된다. 49개 학교 중 11개만 통계적 유의성 검정에 충분한 대응 데이터를 보유하고 있다.

**확장성.** CodleViz는 현재 CSV 내보내기에서 배치 모드로 데이터를 처리한다. 실시간 교실 모니터링을 위해서는 스트리밍 데이터 파이프라인이 필요하다.

**일반화 가능성.** 디자인 스터디는 한국 K-12 데이터 사이언스 교육의 특정 맥락에서 수행되었다. 그러나 4단계 드릴다운 패러다임과 연동 다중 뷰 접근법은 도메인 독립적 아키텍처 선택으로, 다른 교육 환경에 적응 가능하다.

### 7.3 교육 기술에 대한 시사점

CodleViz는 학습 플랫폼이 점점 더 다양한 활동 유형과 AI 도구를 통합함에 따라 교육자의 시각화 요구도 그에 맞게 진화함을 보여준다. 단순 완료 대시보드는 더 이상 충분하지 않다—교육자는 학습의 *무엇*뿐 아니라 *어떻게*와 *왜*를 드러내는 도구가 필요하다.
