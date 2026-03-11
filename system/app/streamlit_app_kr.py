"""
CodleViz — K-12 데이터 사이언스 교육 학습 분석 시스템
한국어 버전 (v0.4) — DR6/DR7/DR8 반영
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from system.utils.data_loader import (
    load_school_summary, load_competency_scores, load_session_progress,
    load_student_heatmap, load_activity_types, load_studio_progress,
    get_school_list, get_classroom_list, get_school_stats,
    get_competency_for_classroom, get_session_for_classroom,
    get_heatmap_for_classroom, COMPETENCY_COLORS, COMPETENCY_NAMES_KR,
    CURRICULUM_COLORS,
)
from system.components.charts import (
    competency_radar, session_timeline, student_heatmap,
    school_comparison_bar, competency_comparison_grouped,
    activity_type_stacked,
    dependency_scatter, cliff_heatmap, trajectory_alignment,
    trajectory_sparklines,
)

# ── Page Config ──
st.set_page_config(
    page_title="CodleViz — 학습 분석 대시보드",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ──
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

    html, body, [class*="css"] {
        font-family: 'Pretendard', 'Inter', -apple-system, sans-serif;
    }

    .block-container { padding-top: 1.5rem; max-width: 1400px; }

    h1 { color: #1E293B; font-weight: 700; font-size: 1.8rem !important; }
    h2 { color: #334155; font-weight: 600; font-size: 1.3rem !important; }
    h3 { color: #475569; font-weight: 600; font-size: 1.1rem !important; }

    /* KPI 카드 */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
        padding: 16px 20px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    div[data-testid="stMetric"] label {
        color: #64748B !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #1E293B !important;
        font-weight: 700 !important;
    }

    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: #F1F5F9;
        padding: 4px;
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: 500;
        font-size: 0.9rem;
    }
    .stTabs [aria-selected="true"] {
        background: white !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }

    /* 사이드바 */
    section[data-testid="stSidebar"] {
        background: #F8FAFC;
        border-right: 1px solid #E2E8F0;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] span {
        color: #1E293B !important;
    }
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stMultiSelect label,
    section[data-testid="stSidebar"] .stRadio label {
        color: #475569 !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* 정보 카드 */
    .info-card {
        background: #F0F9FF;
        border-left: 4px solid #2563EB;
        padding: 12px 16px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 16px;
        font-size: 0.9rem;
        color: #1E40AF;
        line-height: 1.5;
    }
    .warn-card {
        background: #FFFBEB;
        border-left: 4px solid #F59E0B;
        padding: 12px 16px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 16px;
        font-size: 0.9rem;
        color: #92400E;
        line-height: 1.5;
    }
    .success-card {
        background: #F0FDF4;
        border-left: 4px solid #10B981;
        padding: 12px 16px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 16px;
        font-size: 0.9rem;
        color: #065F46;
        line-height: 1.5;
    }

    /* 실행 방안 피드백 카드 (DR6) */
    .action-card {
        background: linear-gradient(135deg, #EFF6FF 0%, #F0F9FF 100%);
        border: 1px solid #BFDBFE;
        border-left: 4px solid #2563EB;
        padding: 14px 18px;
        border-radius: 0 10px 10px 0;
        margin: 10px 0;
        font-size: 0.88rem;
        color: #1E3A5F;
        line-height: 1.6;
    }
    .action-card b { color: #1E40AF; }
    .action-card ul { margin: 6px 0 2px 0; padding-left: 18px; }
    .action-card li { margin-bottom: 3px; }

    /* 윤리 공지 (DR8) */
    .ethics-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        padding: 10px 14px;
        border-radius: 8px;
        margin: 8px 0;
        font-size: 0.78rem;
        color: #64748B;
        line-height: 1.5;
    }

    /* 구분선 */
    hr { border-color: #E2E8F0 !important; margin: 1.5rem 0 !important; }

    /* 범례 뱃지 */
    .badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 6px;
    }
    .badge-blue { background: #DBEAFE; color: #1E40AF; }
    .badge-green { background: #D1FAE5; color: #065F46; }
    .badge-amber { background: #FEF3C7; color: #92400E; }
</style>
""", unsafe_allow_html=True)


# ── Helper ──
_PLOTLY_CONFIG = {"displayModeBar": False}

def show_chart(fig):
    """Plotly 차트를 toolbar 없이 표시"""
    st.plotly_chart(fig, use_container_width=True, config=_PLOTLY_CONFIG)

def info_card(text, card_type="info"):
    st.markdown(f'<div class="{card_type}-card">{text}</div>', unsafe_allow_html=True)


def action_card(title, suggestions):
    """DR6: 실행 방안 피드백 카드"""
    items = "".join(f"<li>{s}</li>" for s in suggestions)
    st.markdown(
        f'<div class="action-card">'
        f'<b>{title}</b>'
        f'<ul>{items}</ul>'
        f'</div>',
        unsafe_allow_html=True,
    )


def ethics_notice():
    """DR8: 데이터 윤리 안내"""
    st.markdown(
        '<div class="ethics-card">'
        '본 대시보드의 모든 데이터는 익명화 처리되었습니다. '
        '학교명은 School_01~School_46, 학생 ID는 S0001~S0709로 변환되어 개인 식별이 불가합니다. '
        '데이터는 교수·학습 개선 목적으로만 활용되며, IRB 승인 하에 수집되었습니다.'
        '</div>',
        unsafe_allow_html=True,
    )


def generate_cliff_feedback(cliff_counts, worst_session):
    """DR6: 진도 하락에 대한 실행 방안 생성"""
    suggestions = []
    if worst_session <= 3:
        suggestions.append(f"{worst_session}차시(이해 단계): 사전 개념 점검 퀴즈 추가 또는 영상 보충 자료 배치")
        suggestions.append("학생 선수지식 수준 파악 후 수준별 학습자료 제공")
    elif worst_session <= 7:
        suggestions.append(f"{worst_session}차시(분석 단계): 데이터 분석 예시를 단계적으로 제시하는 스캐폴딩 적용")
        suggestions.append("분석 활동 전 짝 활동(페어 워크) 도입으로 협력적 문제 해결 유도")
    elif worst_session <= 11:
        suggestions.append(f"{worst_session}차시(코딩 단계): 코딩 기초 보충 활동 또는 블록 코딩→텍스트 코딩 점진적 전환")
        suggestions.append("페어 프로그래밍 도입으로 코딩 어려움 학생 지원")
        suggestions.append("AI 코딩 도우미 사용 가이드라인 제공")
    else:
        suggestions.append(f"{worst_session}차시(종합 단계): 프로젝트 중간 점검 체크리스트 도입")
        suggestions.append("최종 발표 전 초안 피드백 시간 확보")
    return suggestions


def generate_quadrant_feedback(q_counts):
    """DR6: 학습 유형별 실행 방안 생성"""
    suggestions = []
    if q_counts.get("참여 부족", 0) > 0:
        n = q_counts["참여 부족"]
        suggestions.append(f"참여 부족 학생 {n}명: 1:1 면담으로 학습 동기 파악, 흥미 기반 과제 제공")
    if q_counts.get("노력 중", 0) > 0:
        n = q_counts["노력 중"]
        suggestions.append(f"노력 중 학생 {n}명: 기초 보충 자료 제공, 또래 튜터링 매칭")
    if q_counts.get("과도한 도움 사용", 0) > 0:
        n = q_counts["과도한 도움 사용"]
        suggestions.append(f"AI 도움 과다 학생 {n}명: AI 사용 횟수 제한 또는 자기 설명 활동 추가")
    if q_counts.get("자기주도 학습", 0) > 0:
        n = q_counts["자기주도 학습"]
        suggestions.append(f"자기주도 학생 {n}명: 심화 과제 제공 또는 또래 튜터 역할 부여")
    return suggestions


def curriculum_badges():
    st.markdown(
        '<span class="badge badge-blue">해양쓰레기</span>'
        '<span class="badge badge-green">기후변화</span>'
        '<span class="badge badge-amber">식량안보</span>',
        unsafe_allow_html=True
    )


# ── Sidebar ──
with st.sidebar:
    st.markdown("## 🎓 CodleViz")
    st.caption("K-12 AI·데이터 리터러시 학습 분석")
    st.markdown("---")

    view_level = st.radio(
        "분석 수준",
        ["전체 현황", "학교별", "학급별", "학생별"],
        index=0,
        help="4단계 드릴다운: 전체 → 학교 → 학급 → 학생"
    )

    st.markdown("---")

    summary = load_school_summary()
    curricula = sorted(summary["curriculum"].unique())
    selected_curricula = st.multiselect(
        "커리큘럼 필터", curricula, default=curricula,
        help="분석할 커리큘럼을 선택하세요"
    )

    if view_level in ["학교별", "학급별", "학생별"]:
        filtered = summary[summary["curriculum"].isin(selected_curricula)]
        schools = sorted(filtered["school"].unique())
        selected_school = st.selectbox("학교 선택", schools)

        if view_level in ["학급별", "학생별"]:
            classrooms = sorted(
                filtered[filtered["school"] == selected_school]["classroom_name"].tolist()
            )
            selected_classroom = st.selectbox("학급 선택", classrooms)

    # ── DR7: 교사 맞춤 설정 ──
    st.markdown("---")
    with st.expander("표시 설정", expanded=False):
        show_feedback = st.checkbox("실행 방안 피드백 표시", value=True,
                                     help="DR6: 시각화 옆에 실행 가능한 교수 전략을 표시합니다")
        show_text_summary = st.checkbox("텍스트 요약 표시", value=True,
                                         help="차트와 함께 핵심 수치를 텍스트로 요약합니다")
        display_density = st.radio("정보 밀도", ["기본", "상세"],
                                    help="상세 모드에서는 더 많은 통계와 피드백을 표시합니다")

    st.markdown("---")
    ethics_notice()
    st.markdown(
        "<div style='text-align:center; opacity:0.6; font-size:0.75rem; margin-top:8px;'>"
        "49개 학급 · 709명 학생 · 3개 커리큘럼<br>"
        "CodleViz v0.4 · HPIC Lab, 고려대학교"
        "</div>",
        unsafe_allow_html=True
    )


# ══════════════════════════════════════════════════════
# 전체 현황
# ══════════════════════════════════════════════════════
if view_level == "전체 현황":
    st.title("K-12 AI·데이터 리터러시 교육 현황")
    curriculum_badges()
    st.markdown("")

    stats = get_school_stats()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("참여 학교", f"{stats['n_schools']}개")
    c2.metric("참여 학생", f"{stats['n_students']}명")
    c3.metric("학급 수", f"{stats['n_classrooms']}개")
    c4.metric("커리큘럼", f"{stats['n_curricula']}종")
    c5.metric("평균 진도율", f"{stats['avg_progress']*100:.1f}%")

    st.markdown("---")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "학교 비교",
        "역량 분석",
        "활동 패턴",
        "진도 하락 탐지",
        "학습 흐름 비교",
    ])

    with tab1:
        info_card("각 학교(학급)의 평균 진도율을 비교합니다. 막대 색상은 커리큘럼을 나타냅니다.")
        filtered_summary = summary[summary["curriculum"].isin(selected_curricula)]
        fig = school_comparison_bar(filtered_summary)
        fig.update_layout(title=dict(text="학교별 평균 진도율 비교"))
        show_chart(fig)

        # DR6+DR7: 텍스트 요약 + 실행 방안
        if show_text_summary:
            top3 = filtered_summary.nlargest(3, "avg_progress")
            bot3 = filtered_summary.nsmallest(3, "avg_progress")
            avg_all = filtered_summary["avg_progress"].mean() * 100
            info_card(
                f"<b>요약</b>: 전체 평균 진도율 <b>{avg_all:.1f}%</b> | "
                f"최고: {top3.iloc[0]['classroom_name']} ({top3.iloc[0]['avg_progress']*100:.1f}%) | "
                f"최저: {bot3.iloc[0]['classroom_name']} ({bot3.iloc[0]['avg_progress']*100:.1f}%)"
            )
        if show_feedback:
            low_progress = filtered_summary[filtered_summary["avg_progress"] < 0.3]
            if len(low_progress) > 0:
                action_card(
                    f"진도율 30% 미만 학급 {len(low_progress)}개 발견",
                    [
                        "해당 학급 교사와 진도 지연 원인 파악 면담 권장",
                        "수업 시간 내 활동 완료 가능 여부 점검 (시간 부족 vs 난이도 문제)",
                        "보충 학습 시간 확보 또는 활동 수 조정 검토",
                    ]
                )

    with tab2:
        info_card("5개 역량(DC 데이터이해, DA 분석, DV 시각화, DI 해석, CT 컴퓨팅사고)의 전체 평균을 비교합니다.")
        comp_df = load_competency_scores()
        filtered_classrooms = summary[summary["curriculum"].isin(selected_curricula)]["classroom_name"]
        comp_filtered = comp_df[comp_df["classroom_name"].isin(filtered_classrooms)]
        fig = competency_comparison_grouped(comp_filtered)
        fig.update_layout(title=dict(text="전체 역량 평균 비교"))
        show_chart(fig)

        # DR6: 역량별 텍스트 요약 + 피드백
        if show_text_summary:
            comp_avg = comp_filtered.groupby("competency")["avg_progress"].mean()
            best_comp = comp_avg.idxmax()
            worst_comp = comp_avg.idxmin()
            gap = (comp_avg.max() - comp_avg.min()) * 100
            info_card(
                f"<b>요약</b>: 가장 높은 역량 <b>{COMPETENCY_NAMES_KR[best_comp]}</b> "
                f"({comp_avg[best_comp]*100:.1f}%) | "
                f"가장 낮은 역량 <b>{COMPETENCY_NAMES_KR[worst_comp]}</b> "
                f"({comp_avg[worst_comp]*100:.1f}%) | "
                f"역량 간 격차 {gap:.1f}%p"
            )
        if show_feedback:
            comp_avg = comp_filtered.groupby("competency")["avg_progress"].mean()
            weak_comps = comp_avg[comp_avg < 0.4]
            if len(weak_comps) > 0:
                comp_suggestions = []
                for c in weak_comps.index:
                    if c == "CT":
                        comp_suggestions.append(f"{COMPETENCY_NAMES_KR[c]}: 언플러그드 활동 → 블록 코딩 → 텍스트 코딩 단계적 전환 권장")
                    elif c == "DV":
                        comp_suggestions.append(f"{COMPETENCY_NAMES_KR[c]}: 시각화 예시 갤러리 제공, 차트 유형 선택 가이드 추가")
                    elif c == "DI":
                        comp_suggestions.append(f"{COMPETENCY_NAMES_KR[c]}: 데이터 해석 프레임워크(주장-근거-추론) 워크시트 활용")
                    elif c == "DA":
                        comp_suggestions.append(f"{COMPETENCY_NAMES_KR[c]}: CODAP 활용 실습 시간 확대, 분석 절차 체크리스트 제공")
                    else:
                        comp_suggestions.append(f"{COMPETENCY_NAMES_KR[c]}: 개념 이해를 위한 영상/퀴즈 보충 자료 배치")
                action_card(f"40% 미만 역량 {len(weak_comps)}개 — 보강 방안", comp_suggestions)

        st.markdown("### 역량별 학교 비교")
        selected_comp = st.selectbox(
            "역량 선택",
            list(COMPETENCY_NAMES_KR.keys()),
            format_func=lambda x: f"{x} — {COMPETENCY_NAMES_KR[x]}"
        )
        comp_school = comp_filtered[comp_filtered["competency"] == selected_comp].copy()
        comp_school = comp_school.sort_values("avg_progress", ascending=True)

        fig2 = go.Figure(go.Bar(
            x=comp_school["avg_progress"] * 100,
            y=comp_school["classroom_name"],
            orientation="h",
            marker_color=COMPETENCY_COLORS[selected_comp],
        ))
        fig2.update_layout(
            xaxis=dict(title=f"{COMPETENCY_NAMES_KR[selected_comp]} 점수 (%)", range=[0, 100]),
            yaxis=dict(title=""),
            height=max(400, len(comp_school) * 25 + 100),
            margin=dict(l=250, r=20, t=30, b=40),
            font=dict(family="Pretendard, Inter, sans-serif", size=12),
            paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        )
        show_chart(fig2)

    with tab3:
        info_card("각 차시에서 학생들이 수행한 활동 유형(영상, 코딩, 퀴즈 등)의 비율 변화를 보여줍니다.")
        act_df = load_activity_types()
        for curr in selected_curricula:
            curr_data = act_df[act_df["curriculum"] == curr]
            if len(curr_data) > 0:
                fig = activity_type_stacked(curr_data)
                fig.update_layout(title=dict(text=f"활동 유형 분포 — {curr}"))
                show_chart(fig)

    with tab4:
        info_card(
            "<b>진도 하락 탐지</b>: 학생들의 완료율이 갑자기 떨어지는 차시를 자동으로 찾아줍니다. "
            "색이 진할수록 많이 떨어진 것입니다. "
            "여러 학급에서 같은 차시에 하락이 나타나면, 그 차시의 학습 내용이 어렵거나 개선이 필요할 수 있습니다.",
            "warn"
        )

        session_df = load_session_progress()
        filtered_session = session_df[
            session_df["classroom_name"].isin(
                summary[summary["curriculum"].isin(selected_curricula)]["classroom_name"]
            )
        ]

        cliff_threshold = st.slider("하락 기준 (%p)", 5, 30, 15, 5,
                                     help="이 값 이상 떨어지면 '하락'으로 표시합니다") / 100
        fig = cliff_heatmap(filtered_session, summary, threshold=cliff_threshold)
        fig.update_layout(title=dict(text="학교별 진도 하락 현황"))
        show_chart(fig)

        # 하락 통계
        st.markdown("### 하락 발생 요약")
        cliff_counts = {}
        for classroom in filtered_session["classroom_name"].unique():
            cls_data = filtered_session[
                filtered_session["classroom_name"] == classroom
            ].sort_values("session")
            rates = cls_data["completion_rate"].values
            for i in range(1, len(rates)):
                if rates[i] - rates[i-1] < -cliff_threshold:
                    session_num = int(cls_data["session"].values[i])
                    cliff_counts[session_num] = cliff_counts.get(session_num, 0) + 1

        if cliff_counts:
            c1, c2, c3 = st.columns(3)
            total_cliffs = sum(cliff_counts.values())
            worst_session = max(cliff_counts, key=cliff_counts.get)
            n_classrooms = len(filtered_session['classroom_name'].unique())
            c1.metric("하락 발생 횟수", f"{total_cliffs}건")
            c2.metric("하락이 가장 많은 차시", f"{worst_session}차시")
            c3.metric(f"{worst_session}차시 해당 학급",
                     f"{cliff_counts[worst_session]}/{n_classrooms}개")

            # DR6: 진도 하락 실행 방안
            if show_feedback:
                suggestions = generate_cliff_feedback(cliff_counts, worst_session)
                pct = cliff_counts[worst_session] / n_classrooms * 100
                suggestions.insert(0,
                    f"{worst_session}차시에서 {cliff_counts[worst_session]}개 학급({pct:.0f}%)이 하락 — 해당 차시 학습 콘텐츠 검토 필요")
                action_card("교수 전략 제안", suggestions)

            # DR7: 상세 모드 — 차시별 하락 빈도 표
            if display_density == "상세":
                st.markdown("### 차시별 하락 빈도")
                import pandas as pd
                cliff_df = pd.DataFrame(
                    sorted(cliff_counts.items()),
                    columns=["차시", "하락 학급 수"]
                )
                cliff_df["비율"] = (cliff_df["하락 학급 수"] / n_classrooms * 100).round(1).astype(str) + "%"
                st.dataframe(cliff_df, hide_index=True, use_container_width=True)
        else:
            st.success("현재 기준에서 급격한 하락이 발견되지 않았습니다.")

    with tab5:
        info_card(
            "<b>학습 흐름 비교</b>: 모든 학교의 진도 변화를 1차시 기준으로 맞춰서 비교합니다. "
            "색상 띠는 커리큘럼별 평균 범위이며, 띠 아래에 있는 학교는 같은 커리큘럼 내에서 상대적으로 진도가 느린 편입니다.",
            "success"
        )

        session_df = load_session_progress()
        filtered_session = session_df[
            session_df["classroom_name"].isin(
                summary[summary["curriculum"].isin(selected_curricula)]["classroom_name"]
            )
        ]

        fig = trajectory_alignment(filtered_session, summary)
        fig.update_layout(title=dict(text="학교별 학습 흐름 비교"))
        show_chart(fig)

        st.markdown("### 단계별 성과 요약")
        info_card("4개 학습 단계(이해→분석→코딩→종합)별로 학교마다 평균 완료율이 어떻게 다른지 비교합니다.")
        fig2 = trajectory_sparklines(filtered_session, summary)
        fig2.update_layout(title=dict(text="학교별 단계 성과"))
        show_chart(fig2)


# ══════════════════════════════════════════════════════
# 학교별
# ══════════════════════════════════════════════════════
elif view_level == "학교별":
    st.title(f"🏫 {selected_school}")

    school_classrooms = summary[
        (summary["school"] == selected_school) &
        (summary["curriculum"].isin(selected_curricula))
    ]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("학급 수", f"{len(school_classrooms)}개")
    c2.metric("학생 수", f"{int(school_classrooms['n_students'].sum())}명")
    c3.metric("사전·사후 매칭", f"{int(school_classrooms['n_paired'].sum())}명")
    c4.metric("평균 진도율", f"{school_classrooms['avg_progress'].mean()*100:.1f}%")

    st.markdown("---")

    # 역량 레이더
    st.markdown("### 학급별 역량 프로필")
    info_card("각 학급의 5개 역량 점수를 레이더 차트로 표시합니다. 차트가 넓을수록 해당 역량의 달성도가 높습니다.")

    cols = st.columns(min(3, len(school_classrooms)))
    for i, (_, row) in enumerate(school_classrooms.iterrows()):
        comp_data = get_competency_for_classroom(row["classroom_name"])
        with cols[i % len(cols)]:
            fig = competency_radar(comp_data, title=row["classroom_name"])
            show_chart(fig)

    st.markdown("---")

    # DR6: 학교 수준 피드백
    if show_feedback:
        avg_progress = school_classrooms['avg_progress'].mean()
        if avg_progress < 0.4:
            action_card(
                f"{selected_school} 전체 진도율 {avg_progress*100:.1f}% — 개선 필요",
                [
                    "학교 차원의 보충 학습 시간 확보 논의",
                    "교사 간 수업 사례 공유 워크숍 제안",
                    "커리큘럼 난이도 대비 수업 시수 적정성 검토",
                ]
            )

    # 학습 여정
    st.markdown("### 학습 여정 타임라인")
    info_card(
        "15차시 완료율 추이입니다. 배경색은 학습 단계(이해/분석/코딩/종합)를 나타냅니다. "
        "<b>▼ 삼각형 마커</b>는 완료율이 크게 떨어진 구간입니다. "
        "빨간색=이후에도 회복 안 됨, 초록색=이후 회복됨.",
        "warn"
    )
    for _, row in school_classrooms.iterrows():
        sess_data = get_session_for_classroom(row["classroom_name"])
        if len(sess_data) > 0:
            fig = session_timeline(sess_data, title=row["classroom_name"])
            show_chart(fig)


# ══════════════════════════════════════════════════════
# 학급별
# ══════════════════════════════════════════════════════
elif view_level == "학급별":
    st.title(f"📝 {selected_classroom}")

    classroom_info = summary[summary["classroom_name"] == selected_classroom].iloc[0]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("학생 수", f"{int(classroom_info['n_students'])}명")
    c2.metric("사전 검사", f"{int(classroom_info['n_pre'])}명")
    c3.metric("사후 검사", f"{int(classroom_info['n_post'])}명")
    c4.metric("평균 진도율", f"{classroom_info['avg_progress']*100:.1f}%")

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs([
        "역량 달성도",
        "차시별 진도",
        "학생별 현황",
        "학습 유형 분류",
    ])

    with tab1:
        info_card("이 학급의 5개 역량 달성도입니다.")
        comp_data = get_competency_for_classroom(selected_classroom)
        fig = competency_radar(comp_data, title="5대 역량 점수")
        show_chart(fig)

        st.dataframe(
            comp_data[["competency", "avg_progress", "n_activities", "n_students"]]
            .assign(avg_progress=lambda x: (x["avg_progress"] * 100).round(1))
            .rename(columns={
                "competency": "역량",
                "avg_progress": "점수 (%)",
                "n_activities": "활동 수",
                "n_students": "학생 수",
            }),
            hide_index=True,
            use_container_width=True,
        )

    with tab2:
        info_card(
            "15차시에 걸친 학습 진행 추이입니다. "
            "▼ 마커는 완료율이 크게 떨어진 구간입니다.",
        )
        sess_data = get_session_for_classroom(selected_classroom)
        fig = session_timeline(sess_data, title="15차시 학습 여정")
        show_chart(fig)

    with tab3:
        info_card(
            "학생(행) × 차시(열) 매트릭스입니다. "
            "색상: <span style='color:#EF4444'>빨강</span>=낮은 완료율, "
            "<span style='color:#F59E0B'>노랑</span>=중간, "
            "<span style='color:#10B981'>초록</span>=높은 완료율. "
            "개입이 필요한 학생을 빠르게 찾을 수 있습니다."
        )
        heat_data = get_heatmap_for_classroom(selected_classroom)
        if len(heat_data) > 0:
            fig = student_heatmap(heat_data, title="학생별 차시 진도")
            show_chart(fig)

            # DR6: 위험 학생 식별 + 피드백
            if show_text_summary or show_feedback:
                student_avgs = heat_data.groupby("profile_id")["avg_progress"].mean()
                at_risk = student_avgs[student_avgs < 0.3]
                if show_text_summary:
                    info_card(
                        f"<b>요약</b>: 학생 {len(student_avgs)}명 중 "
                        f"진도율 30% 미만 <b>{len(at_risk)}명</b> | "
                        f"전체 평균 {student_avgs.mean()*100:.1f}%"
                    )
                if show_feedback and len(at_risk) > 0:
                    action_card(
                        f"위험 학생 {len(at_risk)}명 조기 개입 필요",
                        [
                            "히트맵에서 빨간색이 연속되는 학생 우선 면담",
                            "특정 차시부터 급락한 경우 해당 차시 활동 난이도 확인",
                            "출결·참여 이슈와 학업 어려움 구분하여 대응",
                        ]
                    )
        else:
            st.info("이 학급의 히트맵 데이터가 없습니다.")

    with tab4:
        info_card(
            "<b>학습 유형 분류</b>: 완료율과 코딩 활동량을 기준으로 학생을 4개 유형으로 나눕니다.<br>"
            "• <b style='color:#10B981'>자기주도 학습</b>: 완료율 높음 + 활동 적음 → 스스로 잘 해냄<br>"
            "• <b style='color:#EF4444'>과도한 도움 사용</b>: 완료율 높음 + 활동 많음 → AI 도움에 많이 의존<br>"
            "• <b style='color:#94A3B8'>참여 부족</b>: 완료율 낮음 + 활동 적음 → 학습에 잘 참여하지 않음<br>"
            "• <b style='color:#F59E0B'>노력 중</b>: 완료율 낮음 + 활동 많음 → 열심히 하지만 어려움을 겪는 중<br>"
            "마커 모양: ▲=활동이 점점 늘어남, ▼=활동이 점점 줄어듦",
            "warn"
        )

        heat_data = get_heatmap_for_classroom(selected_classroom)
        if len(heat_data) > 0:
            fig = dependency_scatter(heat_data, title=f"학습 유형 분류 — {selected_classroom}")
            show_chart(fig)

            # 사분면 통계
            st.markdown("### 그룹별 학생 수")
            student_stats = heat_data.groupby("profile_id").agg(
                avg_progress=("avg_progress", "mean"),
            ).reset_index()

            coding_phase = heat_data[heat_data["session"] >= 8]
            if len(coding_phase) > 0:
                coding_stats = coding_phase.groupby("profile_id")["n_activities"].sum().reset_index()
                coding_stats.columns = ["profile_id", "coding_activities"]
                student_stats = student_stats.merge(coding_stats, on="profile_id", how="left")
                student_stats["coding_activities"] = student_stats["coding_activities"].fillna(0)
            else:
                student_stats["coding_activities"] = 0

            comp_med = student_stats["avg_progress"].median()
            act_med = student_stats["coding_activities"].median()

            q_counts = {
                "자기주도 학습": len(student_stats[(student_stats["avg_progress"] >= comp_med) & (student_stats["coding_activities"] < act_med)]),
                "과도한 도움 사용": len(student_stats[(student_stats["avg_progress"] >= comp_med) & (student_stats["coding_activities"] >= act_med)]),
                "참여 부족": len(student_stats[(student_stats["avg_progress"] < comp_med) & (student_stats["coding_activities"] < act_med)]),
                "노력 중": len(student_stats[(student_stats["avg_progress"] < comp_med) & (student_stats["coding_activities"] >= act_med)]),
            }
            q_colors = ["#10B981", "#EF4444", "#94A3B8", "#F59E0B"]
            cols = st.columns(4)
            for i, (label, count) in enumerate(q_counts.items()):
                cols[i].metric(label, f"{count}명")

            # DR6: 유형별 실행 방안 피드백
            if show_feedback:
                fb_suggestions = generate_quadrant_feedback(q_counts)
                if fb_suggestions:
                    action_card(f"{selected_classroom} — 유형별 교수 전략", fb_suggestions)
        else:
            st.info("이 학급의 학생 데이터가 없습니다.")


# ══════════════════════════════════════════════════════
# 학생별
# ══════════════════════════════════════════════════════
elif view_level == "학생별":
    heat_data = get_heatmap_for_classroom(selected_classroom)
    if len(heat_data) > 0:
        students = sorted(heat_data["profile_id"].unique())
        selected_student = st.sidebar.selectbox(
            "학생 선택",
            students,
            format_func=lambda x: f"학생 {students.index(x)+1:02d}"
        )

        student_idx = students.index(selected_student) + 1
        st.title(f"👤 학생 {student_idx:02d}")
        st.caption(f"{selected_classroom}")

        student_data = heat_data[heat_data["profile_id"] == selected_student]

        # 요약 통계
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("평균 진도율", f"{student_data['avg_progress'].mean()*100:.1f}%")
        c2.metric("참여 차시", f"{len(student_data)}/15")
        c3.metric("총 활동 수", f"{int(student_data['n_activities'].sum())}개")

        coding_data = student_data[student_data["session"] >= 8]
        early_data = student_data[student_data["session"] < 8]
        coding_intensity = coding_data["n_activities"].mean() if len(coding_data) > 0 else 0
        early_intensity = early_data["n_activities"].mean() if len(early_data) > 0 else 0
        trend = coding_intensity - early_intensity
        c4.metric("활동 추세 (코딩 단계)",
                 f"{trend:+.1f}",
                 delta=f"{'증가' if trend > 0 else '감소'}")

        # DR6: 학생 수준 피드백
        if show_feedback:
            avg_prog = student_data['avg_progress'].mean()
            n_sessions = len(student_data)
            student_suggestions = []
            if avg_prog < 0.3:
                student_suggestions.append("진도율이 매우 낮습니다 — 1:1 면담을 통해 학습 어려움 원인 파악 필요")
                student_suggestions.append("기초 보충 자료 제공 및 또래 튜터링 매칭 권장")
            elif avg_prog < 0.5:
                student_suggestions.append("중간 수준 진도 — 어려운 차시에 대한 추가 지원 제공 권장")
            if n_sessions < 10:
                student_suggestions.append(f"참여 차시가 {n_sessions}/15로 낮습니다 — 출결 현황 확인 필요")
            if trend < -2:
                student_suggestions.append("코딩 단계에서 활동량이 급감 — 코딩 난이도 조정 또는 스캐폴딩 필요")
            elif trend > 5:
                student_suggestions.append("코딩 단계에서 활동량 급증 — AI 도움 의존도 확인 필요")
            if student_suggestions:
                action_card(f"학생 {student_idx:02d} 교수 전략", student_suggestions)

        st.markdown("---")

        info_card(
            "차시별 완료율입니다. 배경색은 학습 단계를 나타냅니다: "
            "<span style='color:#3B82F6'>이해(1-3)</span> → "
            "<span style='color:#10B981'>분석(4-7)</span> → "
            "<span style='color:#EF4444'>코딩(8-11)</span> → "
            "<span style='color:#8B5CF6'>종합(12-15)</span>"
        )

        # 차시별 진도 바 차트
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=[f"{int(s)}차시" for s in student_data["session"]],
            y=student_data["avg_progress"] * 100,
            marker_color=["#10B981" if p >= 0.7 else "#F59E0B" if p >= 0.3 else "#EF4444"
                         for p in student_data["avg_progress"]],
            hovertemplate="%{x}: %{y:.1f}%<extra></extra>",
        ))

        # 단계 배경
        phases = [(0.5, 3.5, "#EFF6FF"), (3.5, 7.5, "#ECFDF5"),
                  (7.5, 11.5, "#FEF2F2"), (11.5, 15.5, "#F5F3FF")]
        for x0, x1, color in phases:
            fig.add_vrect(x0=x0 - 1, x1=x1 - 1, fillcolor=color,
                          opacity=0.3, layer="below", line_width=0)

        fig.update_layout(
            title=dict(text="차시별 완료율", x=0.5),
            yaxis=dict(title="완료율 (%)", range=[0, 105]),
            xaxis=dict(title="차시"),
            height=350,
            font=dict(family="Pretendard, Inter, sans-serif", size=13),
            paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        )
        show_chart(fig)

    else:
        st.info("이 학급의 학생 데이터가 없습니다.")
