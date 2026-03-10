"""
CodleViz — K-12 데이터 사이언스 교육 학습 분석 시스템
한국어 버전 (v0.3)
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


# ── Helper: 정보 카드 ──
def info_card(text, card_type="info"):
    st.markdown(f'<div class="{card_type}-card">{text}</div>', unsafe_allow_html=True)


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

    st.markdown("---")
    st.markdown(
        "<div style='text-align:center; opacity:0.6; font-size:0.75rem;'>"
        "49개 학교 · 709명 학생 · 3개 커리큘럼<br>"
        "CodleViz v0.3 · HPIC Lab, 고려대학교"
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
        "절벽 감지",
        "궤적 정렬",
    ])

    with tab1:
        info_card("각 학교(학급)의 평균 진도율을 비교합니다. 막대 색상은 커리큘럼을 나타냅니다.")
        filtered_summary = summary[summary["curriculum"].isin(selected_curricula)]
        fig = school_comparison_bar(filtered_summary)
        fig.update_layout(title=dict(text="학교별 평균 진도율 비교"))
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        info_card("5개 역량(DC 데이터이해, DA 분석, DV 시각화, DI 해석, CT 컴퓨팅사고)의 전체 평균을 비교합니다.")
        comp_df = load_competency_scores()
        filtered_classrooms = summary[summary["curriculum"].isin(selected_curricula)]["classroom_name"]
        comp_filtered = comp_df[comp_df["classroom_name"].isin(filtered_classrooms)]
        fig = competency_comparison_grouped(comp_filtered)
        fig.update_layout(title=dict(text="전체 역량 평균 비교"))
        st.plotly_chart(fig, use_container_width=True)

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
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        info_card("각 차시에서 학생들이 수행한 활동 유형(영상, 코딩, 퀴즈 등)의 비율 변화를 보여줍니다.")
        act_df = load_activity_types()
        for curr in selected_curricula:
            curr_data = act_df[act_df["curriculum"] == curr]
            if len(curr_data) > 0:
                fig = activity_type_stacked(curr_data)
                fig.update_layout(title=dict(text=f"활동 유형 분포 — {curr}"))
                st.plotly_chart(fig, use_container_width=True)

    with tab4:
        info_card(
            "<b>절벽 감지(Cliff Detector)</b>는 완료율이 급격히 하락하는 차시를 자동으로 탐지합니다. "
            "셀 색상이 진할수록 하락 심각도가 높습니다. "
            "특정 커리큘럼의 특정 차시에서 공통적으로 절벽이 발생하면, 해당 콘텐츠의 난이도 조정이 필요할 수 있습니다.",
            "warn"
        )

        session_df = load_session_progress()
        filtered_session = session_df[
            session_df["classroom_name"].isin(
                summary[summary["curriculum"].isin(selected_curricula)]["classroom_name"]
            )
        ]

        cliff_threshold = st.slider("절벽 감지 임계값 (%p)", 5, 30, 15, 5,
                                     help="이 값 이상 하락하면 '절벽'으로 감지합니다") / 100
        fig = cliff_heatmap(filtered_session, summary, threshold=cliff_threshold)
        fig.update_layout(title=dict(text="전체 학교 절벽 감지 히트맵"))
        st.plotly_chart(fig, use_container_width=True)

        # 절벽 통계
        st.markdown("### 절벽 발생 요약")
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
            c1.metric("감지된 총 절벽 수", f"{total_cliffs}건")
            c2.metric("가장 빈번한 절벽 차시", f"{worst_session}차시")
            c3.metric(f"{worst_session}차시 영향 학급",
                     f"{cliff_counts[worst_session]}/{n_classrooms}개")
        else:
            st.success("현재 임계값에서 감지된 절벽이 없습니다.")

    with tab5:
        info_card(
            "<b>궤적 정렬 뷰(Trajectory Alignment)</b>는 모든 학교의 학습 궤적을 1차시 기준으로 정규화하여 비교합니다. "
            "색상 띠는 커리큘럼별 25~75백분위 범위이며, 띠 아래의 학교는 같은 커리큘럼 내에서 상대적으로 저조한 성과를 보입니다.",
            "success"
        )

        session_df = load_session_progress()
        filtered_session = session_df[
            session_df["classroom_name"].isin(
                summary[summary["curriculum"].isin(selected_curricula)]["classroom_name"]
            )
        ]

        fig = trajectory_alignment(filtered_session, summary)
        fig.update_layout(title=dict(text="기준선 정규화 궤적 비교"))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 단계별 성과 요약")
        info_card("4개 학습 단계(이해→분석→코딩→종합)별 평균 완료율을 학교별로 비교합니다.")
        fig2 = trajectory_sparklines(filtered_session, summary)
        fig2.update_layout(title=dict(text="학교별 단계 성과"))
        st.plotly_chart(fig2, use_container_width=True)


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
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # 학습 여정
    st.markdown("### 학습 여정 타임라인")
    info_card(
        "15차시 완료율 추이입니다. 배경색은 학습 단계(이해/분석/코딩/종합)를 나타냅니다. "
        "<b>▼ 삼각형 마커</b>는 완료율이 급격히 하락한 '절벽' 지점입니다. "
        "빨간색=회복 안 됨, 초록색=이후 회복됨.",
        "warn"
    )
    for _, row in school_classrooms.iterrows():
        sess_data = get_session_for_classroom(row["classroom_name"])
        if len(sess_data) > 0:
            fig = session_timeline(sess_data, title=row["classroom_name"])
            st.plotly_chart(fig, use_container_width=True)


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
        "역량 레이더",
        "학습 여정",
        "학생 히트맵",
        "AI 의존도 분석",
    ])

    with tab1:
        info_card("이 학급의 5개 역량 달성도입니다.")
        comp_data = get_competency_for_classroom(selected_classroom)
        fig = competency_radar(comp_data, title="5대 역량 점수")
        st.plotly_chart(fig, use_container_width=True)

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
            "▼ 마커는 급격한 하락(절벽)을 나타냅니다.",
        )
        sess_data = get_session_for_classroom(selected_classroom)
        fig = session_timeline(sess_data, title="15차시 학습 여정")
        st.plotly_chart(fig, use_container_width=True)

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
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("이 학급의 히트맵 데이터가 없습니다.")

    with tab4:
        info_card(
            "<b>AI 의존도 분석</b>은 학생을 완료율과 코딩 활동 빈도 기준으로 4개 그룹으로 분류합니다.<br>"
            "• <b style='color:#10B981'>독립 학습자</b>: 높은 완료율 + 적은 활동 → 스스로 학습<br>"
            "• <b style='color:#EF4444'>AI 의존 위험</b>: 높은 완료율 + 많은 활동 → AI에 과도하게 의존 가능성<br>"
            "• <b style='color:#94A3B8'>이탈</b>: 낮은 완료율 + 적은 활동 → 학습 참여 저조<br>"
            "• <b style='color:#F59E0B'>어려움+도움 요청</b>: 낮은 완료율 + 많은 활동 → 노력하지만 어려움<br>"
            "마커 모양: ▲=활동 증가 추세, ▼=활동 감소 추세",
            "warn"
        )

        heat_data = get_heatmap_for_classroom(selected_classroom)
        if len(heat_data) > 0:
            fig = dependency_scatter(heat_data, title=f"AI 의존도 — {selected_classroom}")
            st.plotly_chart(fig, use_container_width=True)

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
                "독립 학습자": len(student_stats[(student_stats["avg_progress"] >= comp_med) & (student_stats["coding_activities"] < act_med)]),
                "AI 의존 위험": len(student_stats[(student_stats["avg_progress"] >= comp_med) & (student_stats["coding_activities"] >= act_med)]),
                "이탈": len(student_stats[(student_stats["avg_progress"] < comp_med) & (student_stats["coding_activities"] < act_med)]),
                "어려움+도움요청": len(student_stats[(student_stats["avg_progress"] < comp_med) & (student_stats["coding_activities"] >= act_med)]),
            }
            q_colors = ["#10B981", "#EF4444", "#94A3B8", "#F59E0B"]
            cols = st.columns(4)
            for i, (label, count) in enumerate(q_counts.items()):
                cols[i].metric(label, f"{count}명")
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
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("이 학급의 학생 데이터가 없습니다.")
