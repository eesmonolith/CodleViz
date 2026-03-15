/**
 * CodleViz 전문가 평가 설문지 (v0.5 XAI) — 30분 축소 버전
 * Google Forms 자동 생성 스크립트
 *
 * 사용법:
 * 1. https://script.google.com/ 에서 새 프로젝트 생성
 * 2. 이 코드를 붙여넣기
 * 3. createCodleVizSurvey() 함수 실행 (▶️)
 * 4. 로그에서 Google Form URL 확인
 */

function createCodleVizSurvey() {
  var form = FormApp.create('CodleViz 전문가 평가 설문지');
  form.setDescription(
    'CodleViz — K-12 AI·데이터 리터러시 교육을 위한 학습 분석 시각화 시스템\n\n' +
    '📌 체험 URL: https://codleviz-7tuevfclyvhjpvtfk863sq.streamlit.app/\n\n' +
    '설문 전에 위 URL에서 시스템을 10~15분 정도 자유롭게 체험해주세요.\n' +
    '예상 소요 시간: 약 25~30분\n\n' +
    '연구 기관: 고려대학교 HPIC Lab\n' +
    '연구자: 엄은상'
  );
  form.setIsQuiz(false);
  form.setCollectEmail(false);
  form.setAllowResponseEdits(true);
  form.setProgressBar(true);

  // ══════════════════════════════════════════
  // Part 1: 동의 + 배경 정보 (~3분)
  // ══════════════════════════════════════════
  form.addPageBreakItem().setTitle('Part 1: 참여 동의 및 배경 정보');

  form.addMultipleChoiceItem()
    .setTitle('본 설문은 연구 목적으로 수행되며 개인정보는 익명 처리됩니다. 참여에 동의하십니까?')
    .setChoiceValues(['동의합니다', '동의하지 않습니다'])
    .setRequired(true);

  form.addTextItem().setTitle('소속 기관/학교명').setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('역할')
    .setChoiceValues(['교사', '교육 연구자', '관리자', '기타'])
    .setRequired(true);

  form.addTextItem().setTitle('교육 경력 (년)').setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('담당 학교급')
    .setChoiceValues(['초등', '중등', '고등', '기타'])
    .setRequired(true);

  form.addTextItem()
    .setTitle('코들 플랫폼 사용 경험 (개월)')
    .setHelpText('없으면 0')
    .setRequired(true);

  form.addTextItem().setTitle('담당 학생 수').setRequired(true);

  form.addScaleItem()
    .setTitle('데이터 시각화 도구 사용 경험 수준')
    .setBounds(1, 5)
    .setLabels('경험 없음', '전문가')
    .setRequired(true);

  // ══════════════════════════════════════════
  // Part 2: 시스템 사용성 (SUS) (~3분)
  // ══════════════════════════════════════════
  form.addPageBreakItem().setTitle('Part 2: 시스템 사용성 평가')
    .setHelpText('CodleViz를 체험한 후 답변해주세요.\n1 = 전혀 동의하지 않음 ~ 5 = 매우 동의함');

  var susItems = [
    '이 시스템을 자주 사용하고 싶다',
    '이 시스템이 불필요하게 복잡하다고 느꼈다',
    '이 시스템이 사용하기 쉽다고 느꼈다',
    '이 시스템을 사용하려면 기술 지원이 필요할 것 같다',
    '이 시스템의 다양한 기능이 잘 통합되어 있다고 느꼈다',
    '이 시스템에 일관성이 없는 부분이 많다고 느꼈다',
    '대부분의 사람들이 이 시스템을 빠르게 배울 수 있을 것이다',
    '이 시스템을 사용하는 것이 매우 번거롭다고 느꼈다',
    '이 시스템을 사용하면서 자신감을 느꼈다',
    '이 시스템을 사용하기 전에 많은 것을 배워야 했다'
  ];

  susItems.forEach(function(item) {
    form.addScaleItem()
      .setTitle(item)
      .setBounds(1, 5)
      .setLabels('전혀 동의하지 않음', '매우 동의함')
      .setRequired(true);
  });

  // ══════════════════════════════════════════
  // Part 3: 시각화 종합 평가 (~5분)
  // ══════════════════════════════════════════
  form.addPageBreakItem().setTitle('Part 3: 시각화 뷰 종합 평가')
    .setHelpText(
      '📌 플랫폼 사이드바에서 분석 수준(전체 현황/학교별/학급별/학생별)을 전환하며 각 탭을 확인해주세요.\n\n' +
      '1 = 매우 낮음 ~ 5 = 매우 높음'
    );

  // 뷰별 1문항씩 (유용성만)
  var viewItems = [
    ['「전체 현황 > 학교 비교」 — 학교별 진도율 막대 그래프', '학교 간 성과를 비교하는 데 유용한가?'],
    ['「전체 현황 > 역량 분석」 — 5개 역량별 비교 그래프', '역량의 균형/불균형을 파악하는 데 유용한가?'],
    ['「전체 현황 > 활동 패턴」 — 차시별 활동 유형 스택 차트', '커리큘럼의 활동 구성을 이해하는 데 유용한가?'],
    ['「전체 현황 > 진도 하락 탐지」 — 하락 히트맵 + 실행 방안', '학습 이탈 패턴을 식별하는 데 유용한가?'],
    ['「전체 현황 > 학습 흐름 비교」 — 학교별 궤적 비교', '학교 간 학습 흐름을 비교하는 데 유용한가?'],
    ['「학교별 > 역량 레이더」 — 학급별 5역량 레이더 차트', '학급별 역량 프로필을 비교하는 데 유용한가?'],
    ['「학교별 > 학습 여정 타임라인」 — 15차시 완료율 추이', '차시별 완료율 추이와 하락 지점을 파악하는 데 유용한가?'],
    ['「학급별 > 학생별 현황」 — 학생×차시 히트맵', '개입이 필요한 학생을 즉시 식별하는 데 유용한가?'],
    ['「학급별 > 학습 유형 분류」 — 4유형 산점도', '학생 유형별 맞춤 지도 전략을 수립하는 데 유용한가?']
  ];

  viewItems.forEach(function(v) {
    form.addScaleItem()
      .setTitle(v[0])
      .setHelpText(v[1])
      .setBounds(1, 5)
      .setLabels('매우 낮음', '매우 높음')
      .setRequired(true);
  });

  form.addMultipleChoiceItem()
    .setTitle('가장 유용했던 뷰는?')
    .setChoiceValues([
      '학교 비교', '역량 분석', '활동 패턴', '진도 하락 탐지',
      '학습 흐름 비교', '역량 레이더', '학습 여정 타임라인',
      '학생별 현황 히트맵', '학습 유형 분류'
    ])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('가장 이해하기 어려웠던 뷰는?')
    .setChoiceValues([
      '학교 비교', '역량 분석', '활동 패턴', '진도 하락 탐지',
      '학습 흐름 비교', '역량 레이더', '학습 여정 타임라인',
      '학생별 현황 히트맵', '학습 유형 분류', '없음 (모두 이해하기 쉬웠음)'
    ])
    .setRequired(true);

  // ══════════════════════════════════════════
  // Part 4: AI 원인 분석 평가 (~5분) ⭐ 핵심
  // ══════════════════════════════════════════
  form.addPageBreakItem().setTitle('Part 4: AI 원인 분석 평가 ⭐')
    .setHelpText(
      '📌 사이드바: 전체 현황 → 진도 하락 탐지 탭 → "표시 설정" > "AI 원인 분석 표시" 체크박스 켜기\n\n' +
      'AI가 진도 하락 원인을 자동 분석하고, 영향 요인 순위와 교수 전략을 추천하는 기능입니다.\n' +
      '1 = 전혀 동의하지 않음 ~ 5 = 매우 동의함'
    );

  var xaiItems = [
    'AI 원인 분석이 진도 하락의 원인을 이해하는 데 도움이 된다',
    'AI가 제시한 원인이 교육 현장의 실제 경험과 부합한다',
    '영향력 수준 표시(매우 큰/큰/보통/약한 영향)가 직관적이다',
    'AI가 추천하는 교수 전략이 구체적이고 실행 가능하다',
    'AI 원인 분석이 없을 때보다 하락 원인을 더 빠르고 정확하게 파악할 수 있다',
    'AI 분석 결과의 신뢰도(정확도) 표시가 안심감을 준다'
  ];

  xaiItems.forEach(function(item) {
    form.addScaleItem()
      .setTitle(item)
      .setBounds(1, 5)
      .setLabels('전혀 동의하지 않음', '매우 동의함')
      .setRequired(true);
  });

  form.addCheckboxItem()
    .setTitle('AI 원인 분석에서 가장 유용했던 정보는? (복수 선택)')
    .setChoiceValues([
      '진도 하락에 가장 큰 영향을 주는 요인 순위 (전역 분석)',
      '특정 학급/차시의 개별 원인 분석',
      '영향력 수준 표시 (매우 큰/큰/보통/약한 영향)',
      'AI가 추천하는 교수 전략',
      '분석 신뢰도(정확도) 표시'
    ])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('AI 원인 분석이 없었다면, 진도 하락 원인 파악에 얼마나 더 오래 걸렸을 것 같습니까?')
    .setChoiceValues([
      '거의 차이 없음',
      '1.5배 정도 더 오래',
      '2~3배 더 오래',
      '5배 이상 더 오래',
      'AI 없이는 원인 파악이 어려웠을 것'
    ])
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('AI 분석 결과 중 "이건 새로운 발견이다"라고 느낀 부분이 있습니까?')
    .setRequired(false);

  // ══════════════════════════════════════════
  // Part 5: 탐색 과제 (~8분)
  // ══════════════════════════════════════════
  form.addPageBreakItem().setTitle('Part 5: 탐색 과제')
    .setHelpText('아래 3개 과제를 수행하고 결과를 기록해주세요.');

  // Task 1: 진도 하락 패턴
  form.addSectionHeaderItem()
    .setTitle('과제 1: 진도 하락 패턴 찾기')
    .setHelpText('사이드바: 전체 현황 → 상단 탭: 진도 하락 탐지\n\n히트맵에서 가장 많은 학교가 동시에 하락하는 차시를 찾으세요.');

  form.addTextItem().setTitle('가장 하락이 집중된 차시').setRequired(true);
  form.addTextItem().setTitle('영향받은 학교 수').setRequired(true);
  form.addScaleItem().setTitle('과제 1 난이도').setBounds(1,5).setLabels('매우 쉬움','매우 어려움').setRequired(true);

  // Task 2: AI 원인 분석 활용
  form.addSectionHeaderItem()
    .setTitle('과제 2: AI 원인 분석 활용 ⭐')
    .setHelpText(
      '"표시 설정" > "AI 원인 분석 표시" 체크박스를 켜세요.\n\n' +
      '1. "진도 하락에 가장 큰 영향을 주는 요인" 상위 3개를 확인\n' +
      '2. 학급/차시 하나를 선택하여 개별 원인 분석 확인\n' +
      '3. "AI가 추천하는 교수 전략" 읽기'
    );

  form.addTextItem().setTitle('상위 영향 요인 1위').setRequired(true);
  form.addTextItem().setTitle('상위 영향 요인 2위').setRequired(true);
  form.addTextItem().setTitle('상위 영향 요인 3위').setRequired(true);
  form.addTextItem().setTitle('선택한 학급/차시 (예: ○○학급 / 5차시)').setRequired(true);
  form.addTextItem().setTitle('해당 학급의 가장 큰 하락 원인').setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('AI 분석 결과가 본인의 직관/경험과 일치하는가?')
    .setChoiceValues(['매우 일치', '대체로 일치', '보통', '다소 불일치', '전혀 불일치'])
    .setRequired(true);

  form.addScaleItem().setTitle('과제 2 난이도').setBounds(1,5).setLabels('매우 쉬움','매우 어려움').setRequired(true);

  // Task 3: 개입 학생 식별
  form.addSectionHeaderItem()
    .setTitle('과제 3: 개입 대상 학생 식별')
    .setHelpText('사이드바: 학급별 → 학교/학급 선택 → 상단 탭: 학생별 현황\n\n히트맵에서 개입이 필요한 학생 1명을 찾고 이유를 설명하세요.');

  form.addParagraphTextItem()
    .setTitle('식별한 학생과 개입 필요 이유')
    .setRequired(true);

  form.addScaleItem().setTitle('과제 3 난이도').setBounds(1,5).setLabels('매우 쉬움','매우 어려움').setRequired(true);

  // ══════════════════════════════════════════
  // Part 6: 종합 의견 (~5분)
  // ══════════════════════════════════════════
  form.addPageBreakItem().setTitle('Part 6: 종합 의견');

  // 기존 도구 대비 (3개만)
  form.addSectionHeaderItem()
    .setTitle('기존 도구 대비 비교')
    .setHelpText('1 = 기존이 훨씬 나음, 3 = 동등, 5 = CodleViz가 훨씬 나음');

  form.addScaleItem().setTitle('학생 전체 현황 파악 속도').setBounds(1,5).setLabels('기존이 훨씬 나음','CodleViz가 훨씬 나음').setRequired(true);
  form.addScaleItem().setTitle('문제 학생 식별 능력').setBounds(1,5).setLabels('기존이 훨씬 나음','CodleViz가 훨씬 나음').setRequired(true);
  form.addScaleItem().setTitle('진도 하락 원인 파악 (AI 원인 분석)').setBounds(1,5).setLabels('기존이 훨씬 나음','CodleViz가 훨씬 나음').setRequired(true);

  // 개방형 핵심 질문
  form.addParagraphTextItem()
    .setTitle('CodleViz를 사용하면서 가장 인상적이었던 점은?')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('AI 원인 분석이 기존에 교사가 직접 판단하는 것과 비교하여 어떤 점이 다릅니까?')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('실제 수업 현장에서 CodleViz를 정기적으로 사용할 의향이 있습니까? 그 이유는?')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('개선이 필요한 부분이 있다면? (최대 3개)')
    .setRequired(false);

  // NPS
  form.addScaleItem()
    .setTitle('다른 교사/교육자에게 CodleViz를 추천하시겠습니까?')
    .setBounds(0, 10)
    .setLabels('전혀 추천하지 않음', '매우 강력히 추천')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('추천/비추천 이유')
    .setRequired(false);

  form.addParagraphTextItem()
    .setTitle('기타 의견')
    .setRequired(false);

  // ══════════════════════════════════════════
  // 완료
  // ══════════════════════════════════════════
  form.setConfirmationMessage(
    '설문에 참여해주셔서 감사합니다! 🙏\n\n' +
    '피드백을 반영하여 시스템을 개선하겠습니다.\n' +
    '문의: 엄은상 (고려대학교 HPIC Lab)'
  );

  Logger.log('✅ 설문지 생성 완료!');
  Logger.log('📋 편집 URL: ' + form.getEditUrl());
  Logger.log('📤 배포 URL: ' + form.getPublishedUrl());

  return form;
}
