# CLAUDE.md — CodleViz (VIS + UIST 2026)

## Project Goal

K-12 데이터 사이언스 교육 플랫폼(코들)의 **멀티모달 학습 데이터 시각화 시스템** 논문 2편 동시 제출

| 학회 | 마감 | 논문 각도 |
|------|------|----------|
| **IEEE VIS 2026** | Abstract Mar 21 / Paper Mar 31 | Visual Analytics + Insight Discovery |
| **ACM UIST 2026** | Abstract Mar 24 / Paper Mar 31 | Real-time Interactive Dashboard System |

---

## System: CodleViz

### 핵심 아이디어
49개 K-12 학교, 709명 학생의 멀티모달 학습 데이터(코드+행동+역량)를
**4-level drill-down**(전체→학교→학급→학생)으로 탐색하는 Visual Analytics 시스템

### 데이터
- **소스**: `/Users/eom-eunsang/Desktop/HPIC March/Project_LLMKT/MM/dashboard/data/`
- **원본**: `/Users/eom-eunsang/Desktop/HPIC March/Project_LLMKT/MM/data/Query.2026.*.csv`

| 파일 | 내용 |
|------|------|
| `all_students.csv` | 전체 학생-활동 데이터 (21MB) |
| `school_summary.csv` | 학교별 요약 (49개 학교) |
| `competency_scores.csv` | 역량별 점수 (DC/DA/DV/DI/CT) |
| `session_progress.csv` | 세션별 진도 |
| `student_heatmap.csv` | 학생×세션 완료 매트릭스 |
| `studio_progress.csv` | 코딩 활동 진도 |
| `activity_types.csv` | 활동 유형 분포 |

### 시각화 뷰 (6개)
1. **School Comparison Map** — 49개 학교 지도 + 성장률
2. **Competency Radar** — 5역량 사전/사후 레이더 차트
3. **Learning Journey Timeline** — 15세션 역량 추이 라인차트
4. **Student Heatmap** — 학생×세션 완료 히트맵
5. **AI Usage Pattern** — LLM 활용 추이
6. **Activity Flow** — 활동 유형 전환 Sankey

### 인터랙션
- Coordinated views (브러싱, 필터링, 드릴다운)
- 학교→학급→학생 drill-down
- 사전/사후 비교 토글
- 세션 범위 슬라이더

---

## 논문 차별화

### VIS: Design Study 방법론
- Sedlmair et al. (2012) Design Study 프레임워크
- Domain expert (교사 5명 + 교육연구자 3명) 참여
- Design Requirements (DR1~DR5) 도출
- Insight-based evaluation + case studies 3개

### UIST: System Paper
- 코들 플랫폼에 내장된 실시간 교사 대시보드
- Participatory Design (교사 참여 설계)
- Real-time WebSocket 데이터 파이프라인
- Teacher usability study (SUS, NASA-TLX)

---

## Tech Stack

- **Frontend**: Streamlit (프로토타입) → D3.js/React (최종)
- **Charts**: Plotly, Altair
- **Data**: Pandas, NumPy
- **Stats**: SciPy (paired t-test, Cohen's d)
- **Map**: Folium
- **Paper**: LaTeX (TVCG format / ACM format)

---

## 컬러 시스템

```
역량별:
  DC(데이터 이해): #3B82F6
  DA(데이터 분석): #10B981
  DV(데이터 시각화): #F59E0B
  DI(데이터 해석): #8B5CF6
  CT(컴퓨팅 사고): #EF4444

브랜드:
  Primary: #2563EB
  Success: #10B981
  Warning: #F59E0B
  Danger: #EF4444
  BG: #F8FAFC
  Text: #1E293B
```

---

## Project Structure

```
CodleViz/
├── .claude/CLAUDE.md         # 이 파일
├── system/
│   ├── app/
│   │   └── streamlit_app.py  # 메인 Streamlit 앱
│   ├── components/           # 시각화 컴포넌트
│   └── utils/                # 데이터 로딩/전처리
├── data/                     # 심볼릭 링크 or 복사본
├── figures/                  # 논문용 figure
├── paper_vis/                # VIS 논문 LaTeX
├── paper_uist/               # UIST 논문 LaTeX
├── VIS/                      # VIS 관련 자료
└── UIST/                     # UIST 관련 자료
```

---

## Deadlines

```
3/10 (TODAY)  프로젝트 시작, 프로토타입 착수
3/14          프로토타입 v1 완성
3/17          VIS case study 분석
3/21          VIS abstract 제출
3/24          UIST abstract 제출
3/28          양쪽 논문 초안 완성
3/31          VIS + UIST full paper 제출
```
