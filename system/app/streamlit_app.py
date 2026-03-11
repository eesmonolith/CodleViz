"""
CodleViz — Visual Analytics for K-12 Data Science Education
English Version (v0.4) — DR6/DR7/DR8
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

# Competency English names
COMPETENCY_NAMES_EN = {
    "DC": "Data Comprehension",
    "DA": "Data Analysis",
    "DV": "Data Visualization",
    "DI": "Data Interpretation",
    "CT": "Computational Thinking",
}

CURRICULUM_NAMES_EN = {
    "해양쓰레기": "Marine Debris",
    "기후변화": "Climate Change",
    "식량안보": "Food Security",
}

def _cur_en(name):
    """Translate curriculum name to English"""
    return CURRICULUM_NAMES_EN.get(name, name)

# ── Page Config ──
st.set_page_config(
    page_title="CodleViz — Learning Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ──
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, sans-serif;
    }

    .block-container { padding-top: 1.5rem; max-width: 1400px; }

    h1 { color: #1E293B; font-weight: 700; font-size: 1.8rem !important; }
    h2 { color: #334155; font-weight: 600; font-size: 1.3rem !important; }
    h3 { color: #475569; font-weight: 600; font-size: 1.1rem !important; }

    /* KPI Cards */
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

    /* Tab Style */
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

    /* Sidebar */
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

    /* Info Cards */
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

    /* Actionable Feedback Card (DR6) */
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

    /* Ethics Notice (DR8) */
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

    /* Divider */
    hr { border-color: #E2E8F0 !important; margin: 1.5rem 0 !important; }

    /* Badges */
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
    """Display Plotly chart without toolbar"""
    st.plotly_chart(fig, use_container_width=True, config=_PLOTLY_CONFIG)

def info_card(text, card_type="info"):
    st.markdown(f'<div class="{card_type}-card">{text}</div>', unsafe_allow_html=True)


def action_card(title, suggestions):
    """DR6: Actionable feedback card"""
    items = "".join(f"<li>{s}</li>" for s in suggestions)
    st.markdown(
        f'<div class="action-card">'
        f'<b>{title}</b>'
        f'<ul>{items}</ul>'
        f'</div>',
        unsafe_allow_html=True,
    )


def ethics_notice():
    """DR8: Data ethics notice"""
    st.markdown(
        '<div class="ethics-card">'
        'All data in this dashboard has been anonymized. '
        'School names are mapped to School_01~School_46 and student IDs to S0001~S0709, '
        'preventing individual identification. '
        'Data is used solely for improving teaching and learning.'
        '</div>',
        unsafe_allow_html=True,
    )


def generate_cliff_feedback(cliff_counts, worst_session):
    """DR6: Generate actionable feedback for progress drops"""
    suggestions = []
    if worst_session <= 3:
        suggestions.append(f"Session {worst_session} (Comprehension phase): Add prerequisite knowledge quizzes or supplementary video materials")
        suggestions.append("Assess prior knowledge levels and provide differentiated learning materials")
    elif worst_session <= 7:
        suggestions.append(f"Session {worst_session} (Analysis phase): Apply scaffolded data analysis examples with step-by-step guidance")
        suggestions.append("Introduce pair work before analysis activities to promote collaborative problem-solving")
    elif worst_session <= 11:
        suggestions.append(f"Session {worst_session} (Coding phase): Provide coding fundamentals review or gradual transition from block to text coding")
        suggestions.append("Introduce pair programming to support struggling coders")
        suggestions.append("Provide AI coding assistant usage guidelines")
    else:
        suggestions.append(f"Session {worst_session} (Synthesis phase): Introduce mid-project checkpoint checklists")
        suggestions.append("Allocate draft feedback time before final presentations")
    return suggestions


def generate_quadrant_feedback(q_counts):
    """DR6: Generate feedback for each learning type"""
    suggestions = []
    if q_counts.get("Disengaged", 0) > 0:
        n = q_counts["Disengaged"]
        suggestions.append(f"Disengaged students ({n}): Conduct 1:1 interviews to identify motivation barriers; provide interest-based tasks")
    if q_counts.get("Struggling", 0) > 0:
        n = q_counts["Struggling"]
        suggestions.append(f"Struggling students ({n}): Provide foundational supplementary materials; match with peer tutors")
    if q_counts.get("AI-Dependent", 0) > 0:
        n = q_counts["AI-Dependent"]
        suggestions.append(f"AI-dependent students ({n}): Limit AI usage frequency or add self-explanation activities")
    if q_counts.get("Independent", 0) > 0:
        n = q_counts["Independent"]
        suggestions.append(f"Independent learners ({n}): Provide advanced challenges or assign peer tutor roles")
    return suggestions


def curriculum_badges():
    st.markdown(
        '<span class="badge badge-blue">Marine Debris</span>'
        '<span class="badge badge-green">Climate Change</span>'
        '<span class="badge badge-amber">Food Security</span>',
        unsafe_allow_html=True
    )


# ── Sidebar ──
with st.sidebar:
    st.markdown("## CodleViz")
    st.caption("K-12 AI & Data Literacy Learning Analytics")
    st.markdown("---")

    view_level = st.radio(
        "Analysis Level",
        ["Overview", "School", "Classroom", "Student"],
        index=0,
        help="4-level drill-down: Overview > School > Classroom > Student"
    )

    st.markdown("---")

    summary = load_school_summary()
    curricula = sorted(summary["curriculum"].unique())
    selected_curricula = st.multiselect(
        "Curriculum Filter", curricula, default=curricula,
        format_func=_cur_en,
        help="Select curricula to analyze"
    )

    if view_level in ["School", "Classroom", "Student"]:
        filtered = summary[summary["curriculum"].isin(selected_curricula)]
        schools = sorted(filtered["school"].unique())
        selected_school = st.selectbox("Select School", schools)

        if view_level in ["Classroom", "Student"]:
            classrooms = sorted(
                filtered[filtered["school"] == selected_school]["classroom_name"].tolist()
            )
            selected_classroom = st.selectbox("Select Classroom", classrooms)

    # ── DR7: Display Settings ──
    st.markdown("---")
    with st.expander("Display Settings", expanded=False):
        show_feedback = st.checkbox("Show Actionable Feedback", value=True,
                                     help="DR6: Display actionable teaching strategies alongside visualizations")
        show_text_summary = st.checkbox("Show Text Summaries", value=True,
                                         help="Display key statistics as text alongside charts")
        display_density = st.radio("Information Density", ["Standard", "Detailed"],
                                    help="Detailed mode shows additional statistics and feedback")

    st.markdown("---")
    ethics_notice()
    st.markdown(
        "<div style='text-align:center; opacity:0.6; font-size:0.75rem; margin-top:8px;'>"
        "49 classrooms · 709 students · 3 curricula<br>"
        "CodleViz v0.4 · HPIC Lab, Korea University"
        "</div>",
        unsafe_allow_html=True
    )


# ══════════════════════════════════════════════════════
# Overview
# ══════════════════════════════════════════════════════
if view_level == "Overview":
    st.title("K-12 AI & Data Literacy Education Overview")
    curriculum_badges()
    st.markdown("")

    stats = get_school_stats()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Schools", f"{stats['n_schools']}")
    c2.metric("Students", f"{stats['n_students']}")
    c3.metric("Classrooms", f"{stats['n_classrooms']}")
    c4.metric("Curricula", f"{stats['n_curricula']}")
    c5.metric("Avg Progress", f"{stats['avg_progress']*100:.1f}%")

    st.markdown("---")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "School Comparison",
        "Competency Analysis",
        "Activity Patterns",
        "Progress Drop Detection",
        "Trajectory Comparison",
    ])

    with tab1:
        info_card("Compares average progress rates across all schools (classrooms). Bar colors indicate curriculum.")
        filtered_summary = summary[summary["curriculum"].isin(selected_curricula)]
        fig = school_comparison_bar(filtered_summary)
        fig.update_layout(title=dict(text="School Progress Rate Comparison"))
        show_chart(fig)

        # DR6+DR7: Text summary + actionable feedback
        if show_text_summary:
            top3 = filtered_summary.nlargest(3, "avg_progress")
            bot3 = filtered_summary.nsmallest(3, "avg_progress")
            avg_all = filtered_summary["avg_progress"].mean() * 100
            info_card(
                f"<b>Summary</b>: Overall average progress <b>{avg_all:.1f}%</b> | "
                f"Highest: {top3.iloc[0]['classroom_name']} ({top3.iloc[0]['avg_progress']*100:.1f}%) | "
                f"Lowest: {bot3.iloc[0]['classroom_name']} ({bot3.iloc[0]['avg_progress']*100:.1f}%)"
            )
        if show_feedback:
            low_progress = filtered_summary[filtered_summary["avg_progress"] < 0.3]
            if len(low_progress) > 0:
                action_card(
                    f"{len(low_progress)} classroom(s) below 30% progress detected",
                    [
                        "Schedule meetings with teachers to identify causes of progress delays",
                        "Check whether in-class activity completion is feasible (time vs. difficulty)",
                        "Consider supplementary learning time or reducing activity count",
                    ]
                )

    with tab2:
        info_card("Compares overall averages of 5 competencies: DC (Data Comprehension), DA (Analysis), DV (Visualization), DI (Interpretation), CT (Computational Thinking).")
        comp_df = load_competency_scores()
        filtered_classrooms = summary[summary["curriculum"].isin(selected_curricula)]["classroom_name"]
        comp_filtered = comp_df[comp_df["classroom_name"].isin(filtered_classrooms)]
        fig = competency_comparison_grouped(comp_filtered)
        fig.update_layout(title=dict(text="Overall Competency Average Comparison"))
        show_chart(fig)

        # DR6: Competency text summary + feedback
        if show_text_summary:
            comp_avg = comp_filtered.groupby("competency")["avg_progress"].mean()
            best_comp = comp_avg.idxmax()
            worst_comp = comp_avg.idxmin()
            gap = (comp_avg.max() - comp_avg.min()) * 100
            info_card(
                f"<b>Summary</b>: Strongest competency <b>{COMPETENCY_NAMES_EN[best_comp]}</b> "
                f"({comp_avg[best_comp]*100:.1f}%) | "
                f"Weakest competency <b>{COMPETENCY_NAMES_EN[worst_comp]}</b> "
                f"({comp_avg[worst_comp]*100:.1f}%) | "
                f"Gap: {gap:.1f}%p"
            )
        if show_feedback:
            comp_avg = comp_filtered.groupby("competency")["avg_progress"].mean()
            weak_comps = comp_avg[comp_avg < 0.4]
            if len(weak_comps) > 0:
                comp_suggestions = []
                for c in weak_comps.index:
                    if c == "CT":
                        comp_suggestions.append(f"{COMPETENCY_NAMES_EN[c]}: Recommend gradual transition from unplugged activities to block coding to text coding")
                    elif c == "DV":
                        comp_suggestions.append(f"{COMPETENCY_NAMES_EN[c]}: Provide visualization example galleries and chart type selection guides")
                    elif c == "DI":
                        comp_suggestions.append(f"{COMPETENCY_NAMES_EN[c]}: Use data interpretation frameworks (claim-evidence-reasoning) worksheets")
                    elif c == "DA":
                        comp_suggestions.append(f"{COMPETENCY_NAMES_EN[c]}: Increase CODAP hands-on practice time; provide analysis procedure checklists")
                    else:
                        comp_suggestions.append(f"{COMPETENCY_NAMES_EN[c]}: Deploy supplementary video/quiz materials for concept understanding")
                action_card(f"{len(weak_comps)} competency(ies) below 40% — Suggested Interventions", comp_suggestions)

        st.markdown("### Competency by School")
        selected_comp = st.selectbox(
            "Select Competency",
            list(COMPETENCY_NAMES_EN.keys()),
            format_func=lambda x: f"{x} — {COMPETENCY_NAMES_EN[x]}"
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
            xaxis=dict(title=f"{COMPETENCY_NAMES_EN[selected_comp]} Score (%)", range=[0, 100]),
            yaxis=dict(title=""),
            height=max(400, len(comp_school) * 25 + 100),
            margin=dict(l=250, r=20, t=30, b=40),
            font=dict(family="Inter, sans-serif", size=12),
            paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        )
        show_chart(fig2)

    with tab3:
        info_card("Shows how the proportion of activity types (video, coding, quiz, etc.) changes across sessions.")
        act_df = load_activity_types()
        for curr in selected_curricula:
            curr_data = act_df[act_df["curriculum"] == curr]
            if len(curr_data) > 0:
                fig = activity_type_stacked(curr_data)
                fig.update_layout(title=dict(text=f"Activity Type Distribution — {_cur_en(curr)}"))
                show_chart(fig)

    with tab4:
        info_card(
            "<b>Progress Drop Detection</b>: Automatically identifies sessions where completion rates drop sharply. "
            "Darker colors indicate more severe drops. "
            "If the same session shows drops across multiple classrooms, that session's content may need revision.",
            "warn"
        )

        session_df = load_session_progress()
        filtered_session = session_df[
            session_df["classroom_name"].isin(
                summary[summary["curriculum"].isin(selected_curricula)]["classroom_name"]
            )
        ]

        cliff_threshold = st.slider("Drop Threshold (%p)", 5, 30, 15, 5,
                                     help="Drops exceeding this value are flagged") / 100
        fig = cliff_heatmap(filtered_session, summary, threshold=cliff_threshold)
        fig.update_layout(title=dict(text="Progress Drop Heatmap by School"))
        show_chart(fig)

        # Drop statistics
        st.markdown("### Drop Summary")
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
            c1.metric("Total Drops", f"{total_cliffs}")
            c2.metric("Most Frequent Drop Session", f"Session {worst_session}")
            c3.metric(f"Classrooms at Session {worst_session}",
                     f"{cliff_counts[worst_session]}/{n_classrooms}")

            # DR6: Progress drop actionable feedback
            if show_feedback:
                suggestions = generate_cliff_feedback(cliff_counts, worst_session)
                pct = cliff_counts[worst_session] / n_classrooms * 100
                suggestions.insert(0,
                    f"Session {worst_session}: {cliff_counts[worst_session]} classrooms ({pct:.0f}%) affected — review session content")
                action_card("Teaching Strategy Suggestions", suggestions)

            # DR7: Detailed mode — drop frequency table
            if display_density == "Detailed":
                st.markdown("### Drop Frequency by Session")
                cliff_df = pd.DataFrame(
                    sorted(cliff_counts.items()),
                    columns=["Session", "Classrooms Affected"]
                )
                cliff_df["Ratio"] = (cliff_df["Classrooms Affected"] / n_classrooms * 100).round(1).astype(str) + "%"
                st.dataframe(cliff_df, hide_index=True, use_container_width=True)
        else:
            st.success("No significant drops detected at the current threshold.")

    with tab5:
        info_card(
            "<b>Trajectory Comparison</b>: Normalizes all school trajectories to Session 1 as baseline. "
            "Shaded bands show the 25th-75th percentile range per curriculum. "
            "Schools below the band are underperforming relative to curriculum peers.",
            "success"
        )

        session_df = load_session_progress()
        filtered_session = session_df[
            session_df["classroom_name"].isin(
                summary[summary["curriculum"].isin(selected_curricula)]["classroom_name"]
            )
        ]

        fig = trajectory_alignment(filtered_session, summary)
        fig.update_layout(title=dict(text="School Trajectory Comparison"))
        show_chart(fig)

        st.markdown("### Phase Performance Summary")
        info_card("Compares average completion rates across 4 learning phases (Comprehension > Analysis > Coding > Synthesis) for each school.")
        fig2 = trajectory_sparklines(filtered_session, summary)
        fig2.update_layout(title=dict(text="Phase Performance by School"))
        show_chart(fig2)


# ══════════════════════════════════════════════════════
# School Level
# ══════════════════════════════════════════════════════
elif view_level == "School":
    st.title(f"{selected_school}")

    school_classrooms = summary[
        (summary["school"] == selected_school) &
        (summary["curriculum"].isin(selected_curricula))
    ]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Classrooms", f"{len(school_classrooms)}")
    c2.metric("Students", f"{int(school_classrooms['n_students'].sum())}")
    c3.metric("Pre-Post Paired", f"{int(school_classrooms['n_paired'].sum())}")
    c4.metric("Avg Progress", f"{school_classrooms['avg_progress'].mean()*100:.1f}%")

    st.markdown("---")

    # Competency Radar
    st.markdown("### Classroom Competency Profiles")
    info_card("Radar charts show the 5 competency scores for each classroom. Wider charts indicate higher achievement.")

    cols = st.columns(min(3, len(school_classrooms)))
    for i, (_, row) in enumerate(school_classrooms.iterrows()):
        comp_data = get_competency_for_classroom(row["classroom_name"])
        with cols[i % len(cols)]:
            fig = competency_radar(comp_data, title=row["classroom_name"])
            show_chart(fig)

    st.markdown("---")

    # DR6: School-level feedback
    if show_feedback:
        avg_progress = school_classrooms['avg_progress'].mean()
        if avg_progress < 0.4:
            action_card(
                f"{selected_school} overall progress {avg_progress*100:.1f}% — Improvement needed",
                [
                    "Discuss supplementary learning time allocation at school level",
                    "Propose cross-teacher lesson sharing workshops",
                    "Review curriculum difficulty relative to allocated class hours",
                ]
            )

    # Learning Journey
    st.markdown("### Learning Journey Timeline")
    info_card(
        "Completion rate trends across 15 sessions. Background colors indicate learning phases (Comprehension/Analysis/Coding/Synthesis). "
        "<b>Down-triangle markers</b> indicate sharp drops. "
        "Red = no recovery afterwards, Green = recovered.",
        "warn"
    )
    for _, row in school_classrooms.iterrows():
        sess_data = get_session_for_classroom(row["classroom_name"])
        if len(sess_data) > 0:
            fig = session_timeline(sess_data, title=row["classroom_name"])
            show_chart(fig)


# ══════════════════════════════════════════════════════
# Classroom Level
# ══════════════════════════════════════════════════════
elif view_level == "Classroom":
    st.title(f"{selected_classroom}")

    classroom_info = summary[summary["classroom_name"] == selected_classroom].iloc[0]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Students", f"{int(classroom_info['n_students'])}")
    c2.metric("Pre-test", f"{int(classroom_info['n_pre'])}")
    c3.metric("Post-test", f"{int(classroom_info['n_post'])}")
    c4.metric("Avg Progress", f"{classroom_info['avg_progress']*100:.1f}%")

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs([
        "Competency Achievement",
        "Session Progress",
        "Student Overview",
        "Learning Type Classification",
    ])

    with tab1:
        info_card("Competency achievement scores for this classroom.")
        comp_data = get_competency_for_classroom(selected_classroom)
        fig = competency_radar(comp_data, title="5 Competency Scores")
        show_chart(fig)

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
        info_card(
            "Learning progress across 15 sessions. "
            "Down-triangle markers indicate sessions with sharp completion rate drops.",
        )
        sess_data = get_session_for_classroom(selected_classroom)
        fig = session_timeline(sess_data, title="15-Session Learning Journey")
        show_chart(fig)

    with tab3:
        info_card(
            "Student (row) x Session (column) matrix. "
            "Colors: <span style='color:#EF4444'>Red</span> = low completion, "
            "<span style='color:#F59E0B'>Yellow</span> = medium, "
            "<span style='color:#10B981'>Green</span> = high completion. "
            "Quickly identify students who need intervention."
        )
        heat_data = get_heatmap_for_classroom(selected_classroom)
        if len(heat_data) > 0:
            fig = student_heatmap(heat_data, title="Student Session Progress")
            show_chart(fig)

            # DR6: At-risk student identification + feedback
            if show_text_summary or show_feedback:
                student_avgs = heat_data.groupby("profile_id")["avg_progress"].mean()
                at_risk = student_avgs[student_avgs < 0.3]
                if show_text_summary:
                    info_card(
                        f"<b>Summary</b>: {len(student_avgs)} students total | "
                        f"Below 30% progress: <b>{len(at_risk)}</b> | "
                        f"Class average: {student_avgs.mean()*100:.1f}%"
                    )
                if show_feedback and len(at_risk) > 0:
                    action_card(
                        f"{len(at_risk)} at-risk student(s) — Early intervention needed",
                        [
                            "Prioritize interviews with students showing consecutive red cells in the heatmap",
                            "If a sharp drop starts at a specific session, review that session's activity difficulty",
                            "Distinguish between attendance issues and academic difficulties in response strategy",
                        ]
                    )
        else:
            st.info("No heatmap data available for this classroom.")

    with tab4:
        info_card(
            "<b>Learning Type Classification</b>: Students are classified into 4 types based on completion rate and coding activity volume.<br>"
            "- <b style='color:#10B981'>Independent Learner</b>: High completion + low activity = self-directed success<br>"
            "- <b style='color:#EF4444'>AI-Dependent</b>: High completion + high activity = possible over-reliance on AI<br>"
            "- <b style='color:#94A3B8'>Disengaged</b>: Low completion + low activity = low participation<br>"
            "- <b style='color:#F59E0B'>Struggling</b>: Low completion + high activity = working hard but facing difficulties<br>"
            "Marker shape: triangle-up = increasing activity trend, triangle-down = decreasing trend",
            "warn"
        )

        heat_data = get_heatmap_for_classroom(selected_classroom)
        if len(heat_data) > 0:
            fig = dependency_scatter(heat_data, title=f"Learning Type Classification — {selected_classroom}")
            show_chart(fig)

            # Quadrant statistics
            st.markdown("### Students by Group")
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
                "Independent": len(student_stats[(student_stats["avg_progress"] >= comp_med) & (student_stats["coding_activities"] < act_med)]),
                "AI-Dependent": len(student_stats[(student_stats["avg_progress"] >= comp_med) & (student_stats["coding_activities"] >= act_med)]),
                "Disengaged": len(student_stats[(student_stats["avg_progress"] < comp_med) & (student_stats["coding_activities"] < act_med)]),
                "Struggling": len(student_stats[(student_stats["avg_progress"] < comp_med) & (student_stats["coding_activities"] >= act_med)]),
            }
            cols = st.columns(4)
            for i, (label, count) in enumerate(q_counts.items()):
                cols[i].metric(label, f"{count}")

            # DR6: Type-specific actionable feedback
            if show_feedback:
                fb_suggestions = generate_quadrant_feedback(q_counts)
                if fb_suggestions:
                    action_card(f"{selected_classroom} — Teaching Strategies by Type", fb_suggestions)
        else:
            st.info("No student data available for this classroom.")


# ══════════════════════════════════════════════════════
# Student Level
# ══════════════════════════════════════════════════════
elif view_level == "Student":
    heat_data = get_heatmap_for_classroom(selected_classroom)
    if len(heat_data) > 0:
        students = sorted(heat_data["profile_id"].unique())
        selected_student = st.sidebar.selectbox(
            "Select Student",
            students,
            format_func=lambda x: f"Student {students.index(x)+1:02d}"
        )

        student_idx = students.index(selected_student) + 1
        st.title(f"Student {student_idx:02d}")
        st.caption(f"{selected_classroom}")

        student_data = heat_data[heat_data["profile_id"] == selected_student]

        # Summary statistics
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Avg Progress", f"{student_data['avg_progress'].mean()*100:.1f}%")
        c2.metric("Sessions Active", f"{len(student_data)}/15")
        c3.metric("Total Activities", f"{int(student_data['n_activities'].sum())}")

        coding_data = student_data[student_data["session"] >= 8]
        early_data = student_data[student_data["session"] < 8]
        coding_intensity = coding_data["n_activities"].mean() if len(coding_data) > 0 else 0
        early_intensity = early_data["n_activities"].mean() if len(early_data) > 0 else 0
        trend = coding_intensity - early_intensity
        c4.metric("Activity Trend (Coding Phase)",
                 f"{trend:+.1f}",
                 delta=f"{'Increasing' if trend > 0 else 'Decreasing'}")

        # DR6: Student-level feedback
        if show_feedback:
            avg_prog = student_data['avg_progress'].mean()
            n_sessions = len(student_data)
            student_suggestions = []
            if avg_prog < 0.3:
                student_suggestions.append("Very low progress — conduct 1:1 interview to identify learning difficulties")
                student_suggestions.append("Provide foundational supplementary materials and match with peer tutor")
            elif avg_prog < 0.5:
                student_suggestions.append("Moderate progress — provide additional support for challenging sessions")
            if n_sessions < 10:
                student_suggestions.append(f"Only {n_sessions}/15 sessions attended — check attendance records")
            if trend < -2:
                student_suggestions.append("Sharp activity decrease in coding phase — adjust coding difficulty or add scaffolding")
            elif trend > 5:
                student_suggestions.append("Sharp activity increase in coding phase — check AI assistance dependency")
            if student_suggestions:
                action_card(f"Student {student_idx:02d} — Teaching Strategy", student_suggestions)

        st.markdown("---")

        info_card(
            "Session-by-session completion rate. Background colors indicate learning phases: "
            "<span style='color:#3B82F6'>Comprehension (1-3)</span> > "
            "<span style='color:#10B981'>Analysis (4-7)</span> > "
            "<span style='color:#EF4444'>Coding (8-11)</span> > "
            "<span style='color:#8B5CF6'>Synthesis (12-15)</span>"
        )

        # Session progress bar chart
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=[f"S{int(s)}" for s in student_data["session"]],
            y=student_data["avg_progress"] * 100,
            marker_color=["#10B981" if p >= 0.7 else "#F59E0B" if p >= 0.3 else "#EF4444"
                         for p in student_data["avg_progress"]],
            hovertemplate="Session %{x}: %{y:.1f}%<extra></extra>",
        ))

        # Phase backgrounds
        phases = [(0.5, 3.5, "#EFF6FF"), (3.5, 7.5, "#ECFDF5"),
                  (7.5, 11.5, "#FEF2F2"), (11.5, 15.5, "#F5F3FF")]
        for x0, x1, color in phases:
            fig.add_vrect(x0=x0 - 1, x1=x1 - 1, fillcolor=color,
                          opacity=0.3, layer="below", line_width=0)

        fig.update_layout(
            title=dict(text="Session Completion Rate", x=0.5),
            yaxis=dict(title="Completion (%)", range=[0, 105]),
            xaxis=dict(title="Session"),
            height=350,
            font=dict(family="Inter, sans-serif", size=13),
            paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        )
        show_chart(fig)

    else:
        st.info("No student data available for this classroom.")
