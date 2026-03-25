/**
 * CodleViz 전문가 평가 설문지 (v4) — 신규 전문가 대상
 * A/B그룹 구분 없이, 교수/연구자/현직교사 등 전문가 대상
 *
 * 사용법:
 * 1. https://script.google.com/ 에서 새 프로젝트 생성
 * 2. 이 코드를 붙여넣기
 * 3. createCodleVizSurveyV4() 함수 실행
 * 4. 로그에서 Google Form URL 확인
 */

function createCodleVizSurveyV4() {
  var form = FormApp.create('CodleViz 전문가 평가 설문지');
  form.setDescription(
    'CodleViz — AI 리터러시 측정을 위한 학습 분석 대시보드\n\n' +
    '체험 URL: https://eesmonolith.github.io/CodleViz/dashboard_kr.html\n\n' +
    '설문 전에 위 URL에서 대시보드를 5~10분 정도 자유롭게 탐색해주세요.\n' +
    '예상 소요 시간: 약 15~20분\n\n' +
    '연구 기관: 고려대학교 HPIC Lab\n' +
    '연구자: 엄은상'
  );
  form.setIsQuiz(false);
  form.setCollectEmail(false);
  form.setAllowResponseEdits(true);
  form.setProgressBar(true);

  // ══════════════════════════════════════════
  // 섹션 1: 동의 + 배경 정보
  // ══════════════════════════════════════════
  form.addPageBreakItem().setTitle('섹션 1: 참여 동의 및 배경 정보');

  form.addMultipleChoiceItem()
    .setTitle('본 설문은 CodleViz 학습 분석 대시보드의 평가를 위한 연구 목적으로 수행됩니다. 수집된 데이터는 연구 목적으로만 사용되며, 개인 식별 정보는 익명 처리됩니다. 참여에 동의하십니까?')
    .setChoiceValues(['동의합니다'])
    .setRequired(true);

  form.addTextItem().setTitle('소속 기관/학교명').setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('역할')
    .setChoiceValues([
      '정규 교사 (초등)',
      '정규 교사 (중등)',
      '정규 교사 (고등)',
      '대학교 교수',
      '교육 연구자',
      '교육 행정/사업 담당자',
      '코들 캠프 강사',
      '기타'
    ])
    .setRequired(true);

  form.addTextItem()
    .setTitle('교육 경력 (년)')
    .setHelpText('예: 5')
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('AI/데이터 교육 경험')
    .setChoiceValues(['없음', '1년 미만', '1~3년', '3~5년', '5년 이상'])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('코들 플랫폼 사용 경험')
    .setChoiceValues(['없음 (처음 봅니다)', '들어본 적은 있음', '6개월 미만', '6개월~1년', '1년 이상'])
    .setRequired(true);

  form.addTextItem()
    .setTitle('담당 학생 수')
    .setHelpText('현재 담당하고 있는 학생 수')
    .setRequired(true);

  form.addScaleItem()
    .setTitle('데이터 시각화 도구(엑셀 차트, 대시보드 등) 사용 경험')
    .setBounds(1, 5)
    .setLabels('전혀 사용 안 함', '매일 사용')
    .setRequired(true);

  // ══════════════════════════════════════════
  // 섹션 2: 시스템 체험 안내
  // ══════════════════════════════════════════
  form.addPageBreakItem().setTitle('섹션 2: 시스템 체험')
    .setHelpText(
      '아래 링크에서 CodleViz 대시보드를 체험해주세요.\n\n' +
      'https://eesmonolith.github.io/CodleViz/dashboard_kr.html\n\n' +
      'CodleViz는 AI 튜터가 내장된 코딩 교육 플랫폼(코들)의 학습 데이터를 분석하는 대시보드입니다.\n' +
      '49개 학교, 709명 학생의 실제 데이터가 들어 있습니다.\n\n' +
      '주요 기능:\n' +
      '• 전체 현황 — 학교 성과 순위, 교수 전략 추천, 시간 슬라이더\n' +
      '• 학교별/학급별 — 역량 레이더, 학습 여정, 위험 학생 자동 감지\n' +
      '• 학생별 — 개인 진도, AI 사용 패턴, 다른 학생과 비교\n' +
      '• 분석 — AI 활용 유형 분류, 진도 하락 원인 AI 분석\n' +
      '• 커리큘럼 비교 — 3개 커리큘럼 성과 비교\n' +
      '• 검색 — 학교명/학생 ID 즉시 검색\n\n' +
      '5~10분 자유 탐색 후 다음으로 진행해주세요.'
    );

  // ══════════════════════════════════════════
  // 섹션 3: 탐색 과제 (4개)
  // ══════════════════════════════════════════
  form.addPageBreakItem().setTitle('섹션 3: 탐색 과제')
    .setHelpText('아래 4개 과제를 대시보드에서 직접 수행하고 답변해주세요.');

  // Task 1
  form.addSectionHeaderItem()
    .setTitle('과제 1: 학교 분석')
    .setHelpText('사이드바 "학교별" → School_01 선택');

  form.addTextItem()
    .setTitle('School_01의 학생 수는?')
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('School_01의 역량 레이더에서 가장 높은 역량은?')
    .setChoiceValues(['DC (데이터 수집)', 'DA (데이터 분석)', 'DV (데이터 시각화)', 'DI (데이터 해석)', 'CT (컴퓨팅 사고)'])
    .setRequired(true);

  form.addScaleItem().setTitle('과제 1 난이도').setBounds(1, 5).setLabels('매우 쉬움', '매우 어려움').setRequired(true);

  // Task 2
  form.addSectionHeaderItem()
    .setTitle('과제 2: 위험 학생 찾기')
    .setHelpText('사이드바 "학급별" → 아무 학교/학급 선택 → "주의가 필요한 학생" 패널 확인');

  form.addTextItem().setTitle('선택한 학급 이름은?').setRequired(true);
  form.addTextItem().setTitle('위험 학생이 몇 명인가요?').setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('위험 학생 1명을 클릭하세요. 해당 학생의 AI 활용 유형은?')
    .setChoiceValues(['자립형', 'AI 활용형', 'AI 의존형', '이탈형'])
    .setRequired(true);

  form.addScaleItem().setTitle('과제 2 난이도').setBounds(1, 5).setLabels('매우 쉬움', '매우 어려움').setRequired(true);

  // Task 3
  form.addSectionHeaderItem()
    .setTitle('과제 3: 진도 하락 원인 확인')
    .setHelpText('사이드바 "전체 현황" → 아래로 스크롤 → "AI 분석: 진도 하락 원인" 차트');

  form.addTextItem().setTitle('진도 하락에 가장 큰 영향을 미치는 요인은?').setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('이 분석 결과가 교육 현장의 경험과 일치하나요?')
    .setChoiceValues(['매우 일치한다', '대체로 일치한다', '보통이다', '다소 다르다', '전혀 다르다'])
    .setRequired(true);

  form.addScaleItem().setTitle('과제 3 난이도').setBounds(1, 5).setLabels('매우 쉬움', '매우 어려움').setRequired(true);

  // Task 4
  form.addSectionHeaderItem()
    .setTitle('과제 4: 학생 비교')
    .setHelpText('사이드바 "학생별" → 아무 학생 선택 → "다른 학생과 비교" 버튼');

  form.addTextItem().setTitle('비교한 두 학생의 ID는? (예: S0479 vs S0480)').setRequired(true);
  form.addParagraphTextItem().setTitle('두 학생을 비교하면서 새롭게 알게 된 점이 있다면?').setRequired(false);
  form.addScaleItem().setTitle('과제 4 난이도').setBounds(1, 5).setLabels('매우 쉬움', '매우 어려움').setRequired(true);

  // ══════════════════════════════════════════
  // 섹션 4: SUS
  // ══════════════════════════════════════════
  form.addPageBreakItem().setTitle('섹션 4: 시스템 사용성 (SUS)')
    .setHelpText('1 = 전혀 동의하지 않음 ~ 5 = 매우 동의함');

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
    form.addScaleItem().setTitle(item).setBounds(1, 5).setLabels('전혀 동의하지 않음', '매우 동의함').setRequired(true);
  });

  // ══════════════════════════════════════════
  // 섹션 5: 기능별 평가
  // ══════════════════════════════════════════
  form.addPageBreakItem().setTitle('섹션 5: 주요 기능 평가')
    .setHelpText('1 = 전혀 동의하지 않음 ~ 5 = 매우 동의함');

  form.addSectionHeaderItem().setTitle('탐색 및 네비게이션');
  form.addScaleItem().setTitle('학교→학급→학생 단계별 드릴다운이 자연스럽다').setBounds(1,5).setLabels('전혀 동의하지 않음','매우 동의함').setRequired(true);
  form.addScaleItem().setTitle('검색으로 원하는 학교/학생을 빠르게 찾을 수 있다').setBounds(1,5).setLabels('전혀 동의하지 않음','매우 동의함').setRequired(true);
  form.addScaleItem().setTitle('시간 슬라이더(차시 범위)가 분석에 도움이 된다').setBounds(1,5).setLabels('전혀 동의하지 않음','매우 동의함').setRequired(true);

  form.addSectionHeaderItem().setTitle('위험 학생 감지');
  form.addScaleItem().setTitle('"주의가 필요한 학생" 자동 표시가 유용하다').setBounds(1,5).setLabels('전혀 동의하지 않음','매우 동의함').setRequired(true);
  form.addScaleItem().setTitle('위험 이유(AI 의존형, 최근 급락 등)가 이해하기 쉽다').setBounds(1,5).setLabels('전혀 동의하지 않음','매우 동의함').setRequired(true);
  form.addScaleItem().setTitle('이 기능 없이 위험 학생을 발견하기 어려웠을 것이다').setBounds(1,5).setLabels('전혀 동의하지 않음','매우 동의함').setRequired(true);

  form.addSectionHeaderItem().setTitle('AI 리터러시 분석');
  form.addScaleItem().setTitle('"과제 완료율"과 "실제 이해도(AI 도움 제외)" 비교가 유용하다').setBounds(1,5).setLabels('전혀 동의하지 않음','매우 동의함').setRequired(true);
  form.addScaleItem().setTitle('4가지 AI 활용 유형 분류(자립/활용/의존/이탈)가 직관적이다').setBounds(1,5).setLabels('전혀 동의하지 않음','매우 동의함').setRequired(true);
  form.addScaleItem().setTitle('학생 비교로 AI 활용 차이를 이해할 수 있다').setBounds(1,5).setLabels('전혀 동의하지 않음','매우 동의함').setRequired(true);

  form.addSectionHeaderItem().setTitle('AI 진도 분석 및 추천');
  form.addScaleItem().setTitle('AI가 분석한 진도 하락 원인이 이해하기 쉽다').setBounds(1,5).setLabels('전혀 동의하지 않음','매우 동의함').setRequired(true);
  form.addScaleItem().setTitle('교수 전략 추천이 구체적이고 실행 가능하다').setBounds(1,5).setLabels('전혀 동의하지 않음','매우 동의함').setRequired(true);

  form.addSectionHeaderItem().setTitle('커리큘럼 비교');
  form.addScaleItem().setTitle('3개 커리큘럼 비교가 사업 운영/교육 설계에 도움이 된다').setBounds(1,5).setLabels('전혀 동의하지 않음','매우 동의함').setRequired(true);

  // ══════════════════════════════════════════
  // 섹션 6: 기존 도구 비교
  // ══════════════════════════════════════════
  form.addPageBreakItem().setTitle('섹션 6: 기존 도구/방법과 비교')
    .setHelpText('현재 사용하시는 도구나 방법과 비교해주세요.\n1 = 기존이 훨씬 나음, 3 = 동등, 5 = CodleViz가 훨씬 나음');

  form.addScaleItem().setTitle('학생 현황 파악 속도').setBounds(1,5).setLabels('기존이 훨씬 나음','CodleViz가 훨씬 나음').setRequired(true);
  form.addScaleItem().setTitle('문제 학생 식별').setBounds(1,5).setLabels('기존이 훨씬 나음','CodleViz가 훨씬 나음').setRequired(true);
  form.addScaleItem().setTitle('AI 활용 현황 파악').setBounds(1,5).setLabels('기존이 훨씬 나음','CodleViz가 훨씬 나음').setRequired(true);
  form.addScaleItem().setTitle('진도 하락 원인 분석').setBounds(1,5).setLabels('기존이 훨씬 나음','CodleViz가 훨씬 나음').setRequired(true);

  // ══════════════════════════════════════════
  // 섹션 7: 종합 평가
  // ══════════════════════════════════════════
  form.addPageBreakItem().setTitle('섹션 7: 종합 평가');

  form.addScaleItem()
    .setTitle('CodleViz를 동료 교사/교육자에게 추천하시겠습니까?')
    .setBounds(0, 10)
    .setLabels('전혀 추천하지 않음', '매우 강력히 추천')
    .setRequired(true);

  form.addParagraphTextItem().setTitle('추천/비추천 이유').setRequired(true);
  form.addParagraphTextItem().setTitle('가장 인상적이었던 기능은?').setRequired(true);

  form.addParagraphTextItem()
    .setTitle('이 대시보드가 실제 수업/업무에서 어떻게 활용될 수 있을까요?')
    .setHelpText('구체적인 활용 시나리오를 적어주시면 연구에 큰 도움이 됩니다.')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('개선이 필요한 부분이 있다면? (최대 3개)')
    .setRequired(false);

  form.addParagraphTextItem().setTitle('기타 의견').setRequired(false);

  // ══════════════════════════════════════════
  // 완료
  // ══════════════════════════════════════════
  form.setConfirmationMessage(
    '설문에 참여해주셔서 감사합니다!\n\n' +
    '소중한 의견을 연구에 반영하겠습니다.\n' +
    '문의: 엄은상 (고려대학교 HPIC Lab)'
  );

  Logger.log('설문지 생성 완료!');
  Logger.log('편집 URL: ' + form.getEditUrl());
  Logger.log('배포 URL: ' + form.getPublishedUrl());

  return form;
}
