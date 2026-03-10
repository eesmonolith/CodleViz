"""
CodleViz — Visual Analytics for K-12 Data Science Education
Main Streamlit Application (v0.2 — Novel Visualizations)
"""
import sys
from pathlib import Path

# Add project root to path
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
    # Novel visualizations
    dependency_scatter, cliff_heatmap, trajectory_alignment,
    trajectory_sparklines,
)

# ── Page Config ──────────────────────────────────────────
st.set_page_config(
    page_title="CodleViz — K-12 Learning Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stMetric { background: white; padding: 16px; border-radius: 12px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    .block-container { padding-top: 1rem; }
    h1, h2, h3 { color: #1E293B; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px; padding: 8px 16px;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────
with st.sidebar:
    st.title("🎓 CodleViz")
    st.caption("K-12 Data Science Learning Analytics")
    st.divider()

    # Level selector
    view_level = st.radio(
        "📊 Analysis Level",
        ["Overview", "School", "Classroom", "Student"],
        index=0,
    )

    st.divider()

    # Filters
    summary = load_school_summary()
    curricula = sorted(summary["curriculum"].unique())
    selected_curricula = st.multiselect(
        "📚 Curriculum", curricula, default=curricula
    )

    if view_level in ["School", "Classroom", "Student"]:
        filtered = summary[summary["curriculum"].isin(selected_curricula)]
        schools = sorted(filtered["school"].unique())
        selected_school = st.selectbox("🏫 School", schools)

        if view_level in ["Classroom", "Student"]:
            classrooms = sorted(
                filtered[filtered["school"] == selected_school]["classroom_name"].tolist()
            )
            selected_classroom = st.selectbox("📝 Classroom", classrooms)

    st.divider()
    st.caption("49 schools · 709 students · 3 curricula")
    st.caption("CodleViz v0.2 — HPIC Lab, Korea University")


# ── Main Content ─────────────────────────────────────────

if view_level == "Overview":
    # ─── Overview: 전체 사업 현황 ───
    st.title("📊 K-12 AI·Data Literacy Education Overview")

    stats = get_school_stats()

    # KPI Cards
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Schools", f"{stats['n_schools']}")
    col2.metric("Students", f"{stats['n_students']}")
    col3.metric("Classrooms", f"{stats['n_classrooms']}")
    col4.metric("Curricula", f"{stats['n_curricula']}")
    col5.metric("Avg Progress", f"{stats['avg_progress']*100:.1f}%")

    st.divider()

    # Tabs — 기존 3개 + Novel 2개
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "School Comparison",
        "Competency Analysis",
        "Activity Patterns",
        "🔺 Cliff Detector",
        "🔄 Trajectory Alignment",
    ])

    with tab1:
        filtered_summary = summary[summary["curriculum"].isin(selected_curricula)]
        fig = school_comparison_bar(filtered_summary)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        comp_df = load_competency_scores()
        filtered_classrooms = summary[summary["curriculum"].isin(selected_curricula)]["classroom_name"]
        comp_filtered = comp_df[comp_df["classroom_name"].isin(filtered_classrooms)]
        fig = competency_comparison_grouped(comp_filtered)
        st.plotly_chart(fig, use_container_width=True)

        # 역량별 학교 비교
        st.subheader("Competency by School")
        selected_comp = st.selectbox(
            "Select Competency",
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
            xaxis=dict(title=f"{selected_comp} Score (%)", range=[0, 100]),
            yaxis=dict(title=""),
            height=max(400, len(comp_school) * 25 + 100),
            margin=dict(l=250, r=20, t=30, b=40),
            font=dict(family="Inter, sans-serif", size=12),
            paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        )
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        act_df = load_activity_types()
        for curr in selected_curricula:
            curr_data = act_df[act_df["curriculum"] == curr]
            if len(curr_data) > 0:
                fig = activity_type_stacked(curr_data)
                fig.update_layout(title=dict(text=f"Activity Distribution — {curr}"))
                st.plotly_chart(fig, use_container_width=True)

    with tab4:
        # ── Novel Vis 2: Cliff Detector ──
        st.markdown("""
        **Coding Cliff Detector** automatically identifies sessions where completion rate
        drops sharply (>15%p). Cell color intensity = cliff severity.
        Darker = more severe drop from a higher baseline.
        """)

        session_df = load_session_progress()
        filtered_session = session_df[
            session_df["classroom_name"].isin(
                summary[summary["curriculum"].isin(selected_curricula)]["classroom_name"]
            )
        ]

        cliff_threshold = st.slider("Cliff Threshold (%p)", 5, 30, 15, 5) / 100
        fig = cliff_heatmap(filtered_session, summary, threshold=cliff_threshold)
        st.plotly_chart(fig, use_container_width=True)

        # 절벽 통계 요약
        st.subheader("Cliff Statistics")
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
            col1, col2, col3 = st.columns(3)
            total_cliffs = sum(cliff_counts.values())
            worst_session = max(cliff_counts, key=cliff_counts.get)
            col1.metric("Total Cliffs Detected", total_cliffs)
            col2.metric("Most Common Cliff Session", f"Session {worst_session}")
            col3.metric("Schools Affected at S{0}".format(worst_session),
                       f"{cliff_counts[worst_session]}/{len(filtered_session['classroom_name'].unique())}")
        else:
            st.info("No cliffs detected at current threshold.")

    with tab5:
        # ── Novel Vis 3: Trajectory Alignment ──
        st.markdown("""
        **Trajectory Alignment View** normalizes all school trajectories to Session 1 = 0%,
        showing relative growth. Shaded bands = 25-75th percentile range per curriculum.
        Schools below the band are underperforming relative to curriculum peers.
        """)

        session_df = load_session_progress()
        filtered_session = session_df[
            session_df["classroom_name"].isin(
                summary[summary["curriculum"].isin(selected_curricula)]["classroom_name"]
            )
        ]

        fig = trajectory_alignment(filtered_session, summary)
        st.plotly_chart(fig, use_container_width=True)

        # Phase Sparklines
        st.subheader("Phase Performance by School")
        fig2 = trajectory_sparklines(filtered_session, summary)
        st.plotly_chart(fig2, use_container_width=True)


elif view_level == "School":
    # ─── School Level ───
    st.title(f"🏫 {selected_school}")

    school_classrooms = summary[
        (summary["school"] == selected_school) &
        (summary["curriculum"].isin(selected_curricula))
    ]

    # KPI
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Classrooms", len(school_classrooms))
    col2.metric("Students", school_classrooms["n_students"].sum())
    col3.metric("Paired (Pre+Post)", school_classrooms["n_paired"].sum())
    col4.metric("Avg Progress", f"{school_classrooms['avg_progress'].mean()*100:.1f}%")

    st.divider()

    # 각 학급 역량 레이더 차트
    cols = st.columns(min(3, len(school_classrooms)))
    for i, (_, row) in enumerate(school_classrooms.iterrows()):
        comp_data = get_competency_for_classroom(row["classroom_name"])
        with cols[i % len(cols)]:
            fig = competency_radar(comp_data, title=row["classroom_name"])
            st.plotly_chart(fig, use_container_width=True)

    # 세션별 진도 (with cliff markers)
    st.subheader("📈 Learning Journey by Session (with Cliff Detection)")
    for _, row in school_classrooms.iterrows():
        sess_data = get_session_for_classroom(row["classroom_name"])
        if len(sess_data) > 0:
            fig = session_timeline(sess_data, title=row["classroom_name"])
            st.plotly_chart(fig, use_container_width=True)


elif view_level == "Classroom":
    # ─── Classroom Level ───
    st.title(f"📝 {selected_classroom}")

    classroom_info = summary[summary["classroom_name"] == selected_classroom].iloc[0]
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Students", int(classroom_info["n_students"]))
    col2.metric("Pre-test", int(classroom_info["n_pre"]))
    col3.metric("Post-test", int(classroom_info["n_post"]))
    col4.metric("Avg Progress", f"{classroom_info['avg_progress']*100:.1f}%")

    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs([
        "Competency Radar",
        "Learning Journey",
        "Student Heatmap",
        "🎯 AI Dependency Analysis",
    ])

    with tab1:
        comp_data = get_competency_for_classroom(selected_classroom)
        fig = competency_radar(comp_data, title="5 Competency Scores")
        st.plotly_chart(fig, use_container_width=True)

        # 역량별 상세 테이블
        st.dataframe(
            comp_data[["competency", "avg_progress", "n_activities", "n_students"]]
            .assign(avg_progress=lambda x: (x["avg_progress"] * 100).round(1))
            .rename(columns={
                "competency": "Competency",
                "avg_progress": "Score (%)",
                "n_activities": "Activities",
                "n_students": "Students",
            }),
            hide_index=True,
            use_container_width=True,
        )

    with tab2:
        sess_data = get_session_for_classroom(selected_classroom)
        fig = session_timeline(sess_data, title="15-Session Learning Journey")
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        heat_data = get_heatmap_for_classroom(selected_classroom)
        if len(heat_data) > 0:
            fig = student_heatmap(heat_data, title="Student × Session Progress")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No heatmap data available for this classroom.")

    with tab4:
        # ── Novel Vis 1: AI Dependency Glyph/Scatter ──
        st.markdown("""
        **AI Dependency Analysis** classifies students into four quadrants based on
        completion rate and coding-phase activity intensity.

        - **Independent Learner** (🟢): High completion, low activity count
        - **AI-Dependent Risk** (🔴): High completion, high activity count (possible over-reliance)
        - **Disengaged** (⬜): Low completion, low activity
        - **Struggling + Seeking Help** (🟡): Low completion, high activity

        Marker shape: ▲ = increasing activity trend, ▼ = decreasing trend.
        Marker size = trend magnitude.
        """)

        heat_data = get_heatmap_for_classroom(selected_classroom)
        if len(heat_data) > 0:
            fig = dependency_scatter(heat_data, title=f"AI Dependency — {selected_classroom}")
            st.plotly_chart(fig, use_container_width=True)

            # 사분면 통계
            st.subheader("Quadrant Summary")
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
                "🟢 Independent": len(student_stats[(student_stats["avg_progress"] >= comp_med) & (student_stats["coding_activities"] < act_med)]),
                "🔴 AI-Dependent": len(student_stats[(student_stats["avg_progress"] >= comp_med) & (student_stats["coding_activities"] >= act_med)]),
                "⬜ Disengaged": len(student_stats[(student_stats["avg_progress"] < comp_med) & (student_stats["coding_activities"] < act_med)]),
                "🟡 Struggling": len(student_stats[(student_stats["avg_progress"] < comp_med) & (student_stats["coding_activities"] >= act_med)]),
            }
            cols = st.columns(4)
            for i, (label, count) in enumerate(q_counts.items()):
                cols[i].metric(label, f"{count} students")
        else:
            st.info("No student data available for this classroom.")


elif view_level == "Student":
    # ─── Student Level ───
    heat_data = get_heatmap_for_classroom(selected_classroom)
    if len(heat_data) > 0:
        students = sorted(heat_data["profile_id"].unique())
        selected_student = st.sidebar.selectbox(
            "👤 Student",
            students,
            format_func=lambda x: f"Student {students.index(x)+1:02d}"
        )

        st.title(f"👤 Student {students.index(selected_student)+1:02d}")
        st.caption(f"{selected_classroom}")

        student_data = heat_data[heat_data["profile_id"] == selected_student]

        # 학생 개인 세션별 진도
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=[f"S{int(s)}" for s in student_data["session"]],
            y=student_data["avg_progress"] * 100,
            marker_color=["#10B981" if p >= 0.7 else "#F59E0B" if p >= 0.3 else "#EF4444"
                         for p in student_data["avg_progress"]],
            hovertemplate="Session %{x}: %{y:.1f}%<extra></extra>",
        ))

        # 단계 배경
        phases = [(0.5, 3.5, "#EFF6FF"), (3.5, 7.5, "#ECFDF5"),
                  (7.5, 11.5, "#FEF2F2"), (11.5, 15.5, "#F5F3FF")]
        for x0, x1, color in phases:
            fig.add_vrect(x0=x0 - 1, x1=x1 - 1, fillcolor=color,
                          opacity=0.3, layer="below", line_width=0)

        fig.update_layout(
            title=dict(text="Session Progress", x=0.5),
            yaxis=dict(title="Progress (%)", range=[0, 105]),
            xaxis=dict(title="Session"),
            height=350,
            font=dict(family="Inter, sans-serif", size=13),
            paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        )
        st.plotly_chart(fig, use_container_width=True)

        # 요약 통계
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Avg Progress", f"{student_data['avg_progress'].mean()*100:.1f}%")
        col2.metric("Sessions Active", f"{len(student_data)}/15")
        col3.metric("Total Activities", int(student_data["n_activities"].sum()))

        # 코딩 단계 활동 강도
        coding_data = student_data[student_data["session"] >= 8]
        early_data = student_data[student_data["session"] < 8]
        coding_intensity = coding_data["n_activities"].mean() if len(coding_data) > 0 else 0
        early_intensity = early_data["n_activities"].mean() if len(early_data) > 0 else 0
        trend = coding_intensity - early_intensity
        col4.metric("Activity Trend (Coding Phase)",
                   f"{trend:+.1f}",
                   delta=f"{'Increasing' if trend > 0 else 'Decreasing'}")

    else:
        st.info("No student data available for this classroom.")
