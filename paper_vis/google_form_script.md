# Google Forms 생성 스크립트

## 사용법
1. [Google Apps Script](https://script.google.com) 접속
2. 새 프로젝트 생성
3. 아래 코드를 붙여넣기
4. `createCodleVizInterviewForm` 함수 실행
5. 생성된 Form URL이 로그에 출력됨 (Ctrl+Enter로 로그 확인)

---

## 코드

function createCodleVizInterviewForm() {
  var form = FormApp.create('[1차] CodleViz 디자인 인터뷰');
  form.setDescription(
    '연구 제목: CodleViz: A Visual Analytics System for Understanding Multimodal Learning Patterns in K-12 Data Science Education\n' +
    '연구 기관: 고려대학교 HPIC Lab\n' +
    '연구자: 엄은상\n\n' +
    '본 인터뷰는 K-12 데이터 사이언스 교육을 위한 시각적 분석 시스템의 디자인 요구사항을 도출하기 위한 연구 목적으로 수행됩니다.\n' +
    '수집된 데이터는 연구 목적으로만 사용되며, 개인 식별 정보는 익명 처리됩니다 (T1, T2 등으로 표기).\n' +
    '참여는 자발적이며 언제든 철회할 수 있습니다.\n\n' +
    '⏱ 예상 소요 시간: 약 30~40분\n' +
    '📌 CodleViz 시스템을 먼저 탐색한 후 응답해주세요.'
  );
  form.setIsQuiz(false);
  form.setCollectEmail(false);
  form.setAllowResponseEdits(true);
  form.setConfirmationMessage('참여해주셔서 감사합니다. 피드백을 반영하여 시스템을 개선한 후, 2차 평가에 다시 초대드리겠습니다.');

  // ══════════════════════════════════════════
  // 페이지 1 (첫 페이지): 연구 참여 동의
  // ══════════════════════════════════════════
  // 첫 페이지는 form.setDescription으로 이미 설명이 있으므로
  // SectionHeader만 추가 (첫 페이지에는 PageBreak 불필요)

  form.addSectionHeaderItem()
    .setTitle('Part 0: 연구 참여 동의')
    .setHelpText('아래 내용을 확인하시고 동의 여부를 선택해주세요.');

  form.addMultipleChoiceItem()
    .setTitle('연구 목적과 절차를 이해하였으며 자발적으로 참여에 동의합니다.')
    .setChoiceValues(['동의합니다', '동의하지 않습니다'])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('인터뷰 내용의 연구 활용(익명 처리)에 동의합니다.')
    .setChoiceValues(['동의합니다', '동의하지 않습니다'])
    .setRequired(true);

  // ══════════════════════════════════════════
  // 페이지 2: 참여자 배경 정보
  // ══════════════════════════════════════════
  form.addPageBreakItem()
    .setTitle('Part 1: 참여자 배경 정보')
    .setHelpText('참여자 기본 정보를 입력해주세요.');

  form.addTextItem()
    .setTitle('소속 기관/학교명')
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('역할')
    .setChoiceValues(['교사', '교육 연구자', '관리자', '기타'])
    .setRequired(true);

  form.addTextItem()
    .setTitle('교육 경력 (년)')
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('담당 학교급')
    .setChoiceValues(['초등학교', '중학교', '고등학교', '기타'])
    .setRequired(true);

  form.addTextItem()
    .setTitle('코들(Codle) 플랫폼 사용 경험 (개월)')
    .setHelpText('사용 경험이 없으면 0으로 입력해주세요.')
    .setRequired(true);

  form.addCheckboxItem()
    .setTitle('사용한 커리큘럼 (복수 선택 가능)')
    .setChoiceValues(['해양쓰레기', '기후변화', '식량안보', '사용 경험 없음'])
    .setRequired(true);

  form.addTextItem()
    .setTitle('담당 학생 수 (대략적으로)')
    .setRequired(false);

  form.addScaleItem()
    .setTitle('데이터 시각화 도구 사용 경험 수준')
    .setHelpText('1 = 전혀 없음, 5 = 전문가 수준')
    .setBounds(1, 5)
    .setLabels('전혀 없음', '전문가')
    .setRequired(true);

  // ══════════════════════════════════════════
  // 페이지 3: 현재 학습 데이터 관리 방식
  // ══════════════════════════════════════════
  form.addPageBreakItem()
    .setTitle('Part 2: 현재 학습 데이터 관리 방식')
    .setHelpText('현재 코들 캠프 또는 수업에서 학생 데이터를 어떻게 관리하고 계신지에 대한 질문입니다.');

  form.addParagraphTextItem()
    .setTitle('Q1. 코들 캠프 수업 중이나 수업 후에, 학생들의 학습 상황을 어떻게 파악하고 계십니까?')
    .setHelpText('사용하는 도구(엑셀, LMS, 직접 관찰 등)와 확인 빈도도 함께 적어주세요.')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('Q2. 학습 데이터를 볼 때, 가장 먼저 확인하고 싶은 정보는 무엇입니까?')
    .setHelpText('왜 그 정보가 가장 중요한지도 함께 적어주세요.')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('Q3. 현재 방식으로 학생 데이터를 파악할 때, 가장 큰 어려움이나 아쉬운 점은 무엇입니까?')
    .setHelpText('"이런 걸 볼 수 있으면 좋겠다"고 느낀 적이 있다면 함께 적어주세요.')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('Q4. 학습 데이터를 기반으로 교수 전략을 바꾸거나 특정 학생에게 개입한 경험이 있습니까?')
    .setHelpText('있다면 구체적으로 어떤 데이터가 결정적이었는지, 없다면 데이터가 부족해서 개입하지 못한 경험을 적어주세요.')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('Q5. 학생들이 AI 튜터를 어떻게 사용하는지 파악하고 계십니까?')
    .setHelpText('AI를 과도하게 의존하는 학생과 적절히 사용하는 학생을 어떻게 구별하시는지도 적어주세요.')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('Q6. 다른 학교나 학급과 비교 분석할 필요를 느낀 적이 있습니까?')
    .setHelpText('있다면 어떤 기준으로 비교하고 싶으셨는지 적어주세요. (성적, 참여도, 커리큘럼 등)')
    .setRequired(false);

  // ══════════════════════════════════════════
  // 페이지 4: CodleViz 시스템 탐색 안내
  // ══════════════════════════════════════════
  form.addPageBreakItem()
    .setTitle('Part 3: CodleViz 시스템 탐색 후 피드백')
    .setHelpText(
      '⚠️ 이 섹션을 작성하기 전에 CodleViz 시스템을 직접 탐색해주세요.\n\n' +
      '🔗 시스템 링크: [Streamlit Cloud URL을 여기에 입력]\n\n' +
      '시스템을 10~20분 정도 자유롭게 탐색한 후 아래 질문에 답해주세요.\n' +
      '탐색 시 Overview → School → Classroom → Student 순서로 둘러보시는 것을 추천합니다.'
    );

  // ── 뷰 ①②③: Overview 레벨 ──

  form.addSectionHeaderItem()
    .setTitle('3-1. Overview 레벨 뷰')
    .setHelpText('전체 학교를 조감하는 뷰들입니다.');

  // 뷰 1: 학교 비교
  form.addScaleItem()
    .setTitle('① 학교 비교 막대 그래프 — 이해하기 쉬운 정도')
    .setHelpText('전체 학교의 평균 진도를 비교하는 수평 막대 그래프입니다.')
    .setBounds(1, 5)
    .setLabels('매우 어려움', '매우 쉬움')
    .setRequired(true);

  form.addScaleItem()
    .setTitle('① 학교 비교 막대 그래프 — 유용한 정도')
    .setBounds(1, 5)
    .setLabels('전혀 유용하지 않음', '매우 유용함')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('① 학교 비교 막대 그래프 — 의견')
    .setHelpText('이 뷰가 유용할 것 같은 상황, 개선 제안 등을 자유롭게 적어주세요.')
    .setRequired(false);

  // 뷰 2: 역량 레이더
  form.addScaleItem()
    .setTitle('② 역량 레이더 차트 — 이해하기 쉬운 정도')
    .setHelpText('학급별 5개 역량(DC, DA, DV, DI, CT) 점수를 보여주는 레이더 차트입니다.')
    .setBounds(1, 5)
    .setLabels('매우 어려움', '매우 쉬움')
    .setRequired(true);

  form.addScaleItem()
    .setTitle('② 역량 레이더 차트 — 유용한 정도')
    .setBounds(1, 5)
    .setLabels('전혀 유용하지 않음', '매우 유용함')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('② 역량 레이더 차트 — 의견')
    .setRequired(false);

  // 뷰 3: 학습 여정 타임라인
  form.addScaleItem()
    .setTitle('③ 학습 여정 타임라인 — 이해하기 쉬운 정도')
    .setHelpText('15차시 완료율 추이 + 단계별 배경색 + 절벽 감지 마커(▼)가 포함된 라인 차트입니다.')
    .setBounds(1, 5)
    .setLabels('매우 어려움', '매우 쉬움')
    .setRequired(true);

  form.addScaleItem()
    .setTitle('③ 학습 여정 타임라인 — 유용한 정도')
    .setBounds(1, 5)
    .setLabels('전혀 유용하지 않음', '매우 유용함')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('③ 학습 여정 타임라인 — 의견')
    .setHelpText('특히 삼각형 절벽 마커(▼)에 대한 의견도 적어주세요.')
    .setRequired(false);

  // ══════════════════════════════════════════
  // 페이지 5: 뷰 ④⑤ — Classroom/Student 레벨
  // ══════════════════════════════════════════
  form.addPageBreakItem()
    .setTitle('3-2. Classroom / Student 레벨 뷰')
    .setHelpText('학급 및 학생 수준에서 세부 분석하는 뷰들입니다.');

  // 뷰 4: 학생 히트맵
  form.addScaleItem()
    .setTitle('④ 학생 히트맵 — 이해하기 쉬운 정도')
    .setHelpText('학생(행) × 세션(열) 매트릭스에서 빨강→초록 색상으로 완료도를 보여줍니다.')
    .setBounds(1, 5)
    .setLabels('매우 어려움', '매우 쉬움')
    .setRequired(true);

  form.addScaleItem()
    .setTitle('④ 학생 히트맵 — 유용한 정도')
    .setBounds(1, 5)
    .setLabels('전혀 유용하지 않음', '매우 유용함')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('④ 학생 히트맵 — 의견')
    .setRequired(false);

  // 뷰 5: AI 의존도 산점도
  form.addScaleItem()
    .setTitle('⑤ AI 의존도 산점도 — 이해하기 쉬운 정도')
    .setHelpText('학생을 완료율 × 코딩활동 빈도 기준 4사분면(독립/AI의존/이탈/어려움)으로 분류하는 산점도입니다.')
    .setBounds(1, 5)
    .setLabels('매우 어려움', '매우 쉬움')
    .setRequired(true);

  form.addScaleItem()
    .setTitle('⑤ AI 의존도 산점도 — 유용한 정도')
    .setBounds(1, 5)
    .setLabels('전혀 유용하지 않음', '매우 유용함')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('⑤ AI 의존도 산점도 — 의견')
    .setRequired(false);

  // ══════════════════════════════════════════
  // 페이지 6: 뷰 ⑥⑦ — 고급 분석 뷰
  // ══════════════════════════════════════════
  form.addPageBreakItem()
    .setTitle('3-3. 고급 분석 뷰')
    .setHelpText('학교 간 비교 및 패턴 탐지를 위한 고급 시각화입니다.');

  // 뷰 6: 절벽 감지 히트맵
  form.addScaleItem()
    .setTitle('⑥ 절벽 감지 히트맵 (Cliff Detector) — 이해하기 쉬운 정도')
    .setHelpText('전체 학교에서 어떤 차시에 급격한 완료율 하락이 발생하는지 보여주는 히트맵입니다.')
    .setBounds(1, 5)
    .setLabels('매우 어려움', '매우 쉬움')
    .setRequired(true);

  form.addScaleItem()
    .setTitle('⑥ 절벽 감지 히트맵 — 유용한 정도')
    .setBounds(1, 5)
    .setLabels('전혀 유용하지 않음', '매우 유용함')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('⑥ 절벽 감지 히트맵 — 의견')
    .setRequired(false);

  // 뷰 7: 궤적 정렬 뷰
  form.addScaleItem()
    .setTitle('⑦ 궤적 정렬 뷰 (Trajectory Alignment) — 이해하기 쉬운 정도')
    .setHelpText('모든 학교의 궤적을 1차시 기준 정규화하여 비교하고, 커리큘럼별 정상 범위(띠)를 보여줍니다.')
    .setBounds(1, 5)
    .setLabels('매우 어려움', '매우 쉬움')
    .setRequired(true);

  form.addScaleItem()
    .setTitle('⑦ 궤적 정렬 뷰 — 유용한 정도')
    .setBounds(1, 5)
    .setLabels('전혀 유용하지 않음', '매우 유용함')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('⑦ 궤적 정렬 뷰 — 의견')
    .setRequired(false);

  // ══════════════════════════════════════════
  // 페이지 7: 탐색 경험
  // ══════════════════════════════════════════
  form.addPageBreakItem()
    .setTitle('Part 4: 탐색 경험')
    .setHelpText('시스템을 자유롭게 탐색하면서 느낀 점을 적어주세요.');

  form.addParagraphTextItem()
    .setTitle('Q7. 시스템을 탐색하면서 이전에 몰랐던 것을 새로 알게 된 것이 있습니까?')
    .setHelpText('예: 특정 학교의 성과 차이, 특정 차시에서의 학생 이탈 패턴 등')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('Q8. 가장 유용하다고 느낀 기능이나 뷰는 무엇입니까? 그 이유는?')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('Q9. 혼란스럽거나 이해하기 어려웠던 부분이 있었습니까?')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('Q10. 이 시스템에 꼭 있었으면 하는데 현재 없는 기능이 있습니까?')
    .setRequired(false);

  // ══════════════════════════════════════════
  // 페이지 8: 디자인 요구사항 검증
  // ══════════════════════════════════════════
  form.addPageBreakItem()
    .setTitle('Part 5: 디자인 요구사항 검증')
    .setHelpText('저희가 사전에 정리한 요구사항에 대해 동의 정도를 평가해주세요.\n1 = 전혀 동의하지 않음, 5 = 매우 동의함');

  form.addScaleItem()
    .setTitle('DR1. 전국→학교→학급→학생 수준의 다단계 탐색이 필요하다')
    .setBounds(1, 5)
    .setLabels('전혀 동의하지 않음', '매우 동의함')
    .setRequired(true);

  form.addScaleItem()
    .setTitle('DR2. 다양한 활동(영상, 코딩, 퀴즈 등)과 역량을 통합적으로 볼 수 있어야 한다')
    .setBounds(1, 5)
    .setLabels('전혀 동의하지 않음', '매우 동의함')
    .setRequired(true);

  form.addScaleItem()
    .setTitle('DR3. 개입이 필요한 학생을 빠르게 찾을 수 있어야 한다')
    .setBounds(1, 5)
    .setLabels('전혀 동의하지 않음', '매우 동의함')
    .setRequired(true);

  form.addScaleItem()
    .setTitle('DR4. AI 튜터 사용 패턴을 볼 수 있어야 한다')
    .setBounds(1, 5)
    .setLabels('전혀 동의하지 않음', '매우 동의함')
    .setRequired(true);

  form.addScaleItem()
    .setTitle('DR5. 서로 다른 커리큘럼의 학습 효과를 비교할 수 있어야 한다')
    .setBounds(1, 5)
    .setLabels('전혀 동의하지 않음', '매우 동의함')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('위 5개 외에 추가해야 할 요구사항이 있다면 적어주세요.')
    .setRequired(false);

  form.addParagraphTextItem()
    .setTitle('위 5개 중 가장 중요한 것과 덜 중요한 것은? 그 이유는?')
    .setHelpText('예: "DR3이 가장 중요하다. 수업 중 즉각 개입이 필요하기 때문이다."')
    .setRequired(false);

  // ══════════════════════════════════════════
  // 페이지 9: 종합 의견
  // ══════════════════════════════════════════
  form.addPageBreakItem()
    .setTitle('Part 6: 종합 의견')
    .setHelpText('마지막으로 전체적인 의견을 남겨주세요.');

  form.addMultipleChoiceItem()
    .setTitle('이 시스템을 실제로 사용한다면, 어떤 시점에 사용하겠습니까?')
    .setChoiceValues([
      '수업 전 준비 단계',
      '수업 중 실시간 모니터링',
      '수업 후 리뷰',
      '캠프/학기 종료 후 보고',
      '기타'
    ])
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('CodleViz가 교수 전략이나 학생 지도에 어떤 변화를 가져올 수 있다고 생각하십니까?')
    .setRequired(false);

  form.addParagraphTextItem()
    .setTitle('기타 의견이나 제안 사항을 자유롭게 적어주세요.')
    .setRequired(false);

  // ── 완료 ──
  Logger.log('Form created successfully!');
  Logger.log('Form URL: ' + form.getEditUrl());
  Logger.log('Response URL: ' + form.getPublishedUrl());
  Logger.log('Response Spreadsheet: link it manually in Form settings');
}
