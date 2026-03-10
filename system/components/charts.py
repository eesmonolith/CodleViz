"""CodleViz 시각화 컴포넌트"""
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

COMPETENCY_COLORS = {
    "DC": "#3B82F6", "DA": "#10B981", "DV": "#F59E0B",
    "DI": "#8B5CF6", "CT": "#EF4444",
}
COMPETENCY_NAMES = {
    "DC": "Data Comprehension", "DA": "Data Analysis",
    "DV": "Data Visualization", "DI": "Data Interpretation",
    "CT": "Computational Thinking",
}
CURRICULUM_COLORS = {
    "해양쓰레기": "#3B82F6", "기후변화": "#10B981", "식량안보": "#F59E0B",
}
LAYOUT_DEFAULTS = dict(
    font=dict(family="Inter, Pretendard, sans-serif", size=13, color="#1E293B"),
    paper_bgcolor="#FFFFFF",
    plot_bgcolor="#FFFFFF",
    margin=dict(l=60, r=20, t=50, b=40),
)


def competency_radar(df: pd.DataFrame, title: str = "") -> go.Figure:
    """5역량 레이더 차트 (학급별 평균 역량)"""
    competencies = ["DC", "DA", "DV", "DI", "CT"]
    values = []
    for c in competencies:
        row = df[df["competency"] == c]
        values.append(row["avg_progress"].values[0] * 100 if len(row) > 0 else 0)

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=[COMPETENCY_NAMES[c] for c in competencies] + [COMPETENCY_NAMES[competencies[0]]],
        fill="toself",
        fillcolor="rgba(37, 99, 235, 0.15)",
        line=dict(color="#2563EB", width=2.5),
        marker=dict(size=8, color="#2563EB"),
        name="Competency Score",
        hovertemplate="%{theta}: %{r:.1f}%<extra></extra>",
    ))

    fig.update_layout(
        font=LAYOUT_DEFAULTS["font"],
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        title=dict(text=title, x=0.5, font=dict(size=16)),
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], ticksuffix="%",
                           gridcolor="#F1F5F9", linecolor="#E2E8F0"),
            angularaxis=dict(gridcolor="#F1F5F9", linecolor="#E2E8F0"),
            bgcolor="#FFFFFF",
        ),
        showlegend=False,
        height=400,
    )
    return fig


def session_timeline(df: pd.DataFrame, title: str = "",
                     cliff_threshold: float = 0.15) -> go.Figure:
    """15세션 학습 여정 라인차트 + Cliff Detection 마커"""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["session"],
        y=df["completion_rate"] * 100,
        mode="lines+markers",
        name="Completion Rate",
        line=dict(color="#2563EB", width=2.5),
        marker=dict(size=7, color="#2563EB"),
        hovertemplate="Session %{x}: %{y:.1f}%<extra></extra>",
    ))

    # 단계별 배경 음영
    phases = [
        (1, 3, "#EFF6FF", "Understanding"),
        (4, 7, "#ECFDF5", "Analysis"),
        (8, 11, "#FEF2F2", "Coding"),
        (12, 15, "#F5F3FF", "Synthesis"),
    ]
    for start, end, color, label in phases:
        fig.add_vrect(x0=start - 0.5, x1=end + 0.5,
                      fillcolor=color, opacity=0.5, layer="below", line_width=0,
                      annotation_text=label, annotation_position="top left",
                      annotation_font_size=10, annotation_font_color="#94A3B8")

    # ── Cliff Detection ──
    rates = df.sort_values("session")["completion_rate"].values
    sessions = df.sort_values("session")["session"].values
    for i in range(1, len(rates)):
        drop = rates[i] - rates[i - 1]
        if drop < -cliff_threshold:
            severity = abs(drop) * rates[i - 1]
            # Recovery rate (next 3 sessions)
            if i + 3 < len(rates):
                recovery = (rates[i + 3] - rates[i]) / (rates[i - 1] - rates[i]) if (rates[i - 1] - rates[i]) > 0 else 0
                recovery = max(0, min(1, recovery))
            else:
                recovery = 0

            # Color: green=recovered, red=not recovered
            r_color = f"rgb({int(220 - 180 * recovery)}, {int(50 + 150 * recovery)}, {int(50 + 50 * recovery)})"
            marker_size = max(12, min(25, severity * 50))

            fig.add_trace(go.Scatter(
                x=[sessions[i]],
                y=[rates[i] * 100],
                mode="markers",
                marker=dict(
                    symbol="triangle-down",
                    size=marker_size,
                    color=r_color,
                    line=dict(color="#1E293B", width=1),
                ),
                name=f"Cliff S{int(sessions[i])}",
                hovertemplate=(
                    f"<b>Coding Cliff Detected</b><br>"
                    f"Session {int(sessions[i])}<br>"
                    f"Drop: {drop*100:.1f}%p<br>"
                    f"Severity: {severity:.2f}<br>"
                    f"Recovery: {recovery*100:.0f}%"
                    f"<extra></extra>"
                ),
                showlegend=False,
            ))

    fig.update_layout(
        font=LAYOUT_DEFAULTS["font"],
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        title=dict(text=title, x=0.5, font=dict(size=16)),
        xaxis=dict(title="Session", dtick=1, gridcolor="#F1F5F9"),
        yaxis=dict(title="Completion Rate (%)", range=[0, 105], gridcolor="#F1F5F9"),
        height=350,
        showlegend=False,
    )
    return fig


def student_heatmap(df: pd.DataFrame, title: str = "") -> go.Figure:
    """학생×세션 완료 히트맵"""
    pivot = df.pivot_table(
        index="profile_id", columns="session", values="avg_progress", aggfunc="mean"
    )
    pivot = pivot.sort_values(by=pivot.columns.tolist(), ascending=False)

    # 학생 익명 번호
    student_labels = [f"S{i+1:02d}" for i in range(len(pivot))]

    fig = go.Figure(data=go.Heatmap(
        z=pivot.values * 100,
        x=[f"S{int(c)}" for c in pivot.columns],
        y=student_labels,
        colorscale=[
            [0, "#FEE2E2"],     # Red-100 (0%)
            [0.5, "#FEF3C7"],   # Amber-100 (50%)
            [1, "#D1FAE5"],     # Green-100 (100%)
        ],
        colorbar=dict(title="%", ticksuffix="%"),
        hovertemplate="Student: %{y}<br>Session: %{x}<br>Progress: %{z:.1f}%<extra></extra>",
    ))

    fig.update_layout(
        font=LAYOUT_DEFAULTS["font"],
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        title=dict(text=title, x=0.5, font=dict(size=16)),
        xaxis=dict(title="Session", side="top"),
        yaxis=dict(title="Student", autorange="reversed"),
        height=max(300, len(pivot) * 22 + 100),
    )
    return fig


def school_comparison_bar(df: pd.DataFrame) -> go.Figure:
    """학교별 평균 진도 수평 막대 그래프"""
    df_sorted = df.sort_values("avg_progress", ascending=True)
    colors = [CURRICULUM_COLORS.get(c, "#94A3B8") for c in df_sorted["curriculum"]]

    fig = go.Figure(go.Bar(
        x=df_sorted["avg_progress"] * 100,
        y=df_sorted["classroom_name"],
        orientation="h",
        marker_color=colors,
        hovertemplate="%{y}<br>Progress: %{x:.1f}%<br>Students: %{customdata[0]}<extra></extra>",
        customdata=df_sorted[["n_students"]].values,
    ))

    fig.update_layout(
        font=LAYOUT_DEFAULTS["font"],
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        title=dict(text="School Comparison — Average Progress", x=0.5, font=dict(size=16)),
        xaxis=dict(title="Average Progress (%)", range=[0, 105], gridcolor="#F1F5F9"),
        yaxis=dict(title=""),
        height=max(400, len(df_sorted) * 28 + 100),
        margin=dict(l=250, r=20, t=50, b=40),
    )
    return fig


def competency_comparison_grouped(df: pd.DataFrame) -> go.Figure:
    """전체 학교 역량별 평균 비교 막대 그래프"""
    comp_avg = df.groupby("competency")["avg_progress"].mean().reset_index()
    comp_avg = comp_avg.sort_values("competency")

    fig = go.Figure(go.Bar(
        x=[COMPETENCY_NAMES.get(c, c) for c in comp_avg["competency"]],
        y=comp_avg["avg_progress"] * 100,
        marker_color=[COMPETENCY_COLORS.get(c, "#94A3B8") for c in comp_avg["competency"]],
        hovertemplate="%{x}: %{y:.1f}%<extra></extra>",
    ))

    fig.update_layout(
        font=LAYOUT_DEFAULTS["font"],
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        title=dict(text="Competency Scores — All Schools Average", x=0.5, font=dict(size=16)),
        yaxis=dict(title="Average Score (%)", range=[0, 100], gridcolor="#F1F5F9"),
        xaxis=dict(title=""),
        height=350,
    )
    return fig


def activity_type_stacked(df: pd.DataFrame) -> go.Figure:
    """세션별 활동 유형 비율 스택 영역 차트"""
    activity_colors = {
        "PdfActivity": "#94A3B8",
        "VideoActivity": "#06B6D4",
        "StudioActivity": "#EF4444",
        "CodapActivity": "#10B981",
        "BoardActivity": "#8B5CF6",
        "SheetActivity": "#F59E0B",
        "QuizActivity": "#EC4899",
        "EmbeddedActivity": "#3B82F6",
        "EntryActivity": "#14B8A6",
    }

    total_per_session = df.groupby("session")["count"].sum()

    fig = go.Figure()
    for act_type in df["activitiable_type"].unique():
        act_data = df[df["activitiable_type"] == act_type]
        sessions = []
        ratios = []
        for s in sorted(df["session"].unique()):
            row = act_data[act_data["session"] == s]
            total = total_per_session.get(s, 1)
            sessions.append(int(s))
            ratios.append((row["count"].sum() / total * 100) if len(row) > 0 else 0)

        fig.add_trace(go.Scatter(
            x=sessions, y=ratios,
            mode="lines",
            name=act_type.replace("Activity", ""),
            stackgroup="one",
            line=dict(width=0),
            fillcolor=activity_colors.get(act_type, "#94A3B8"),
            hovertemplate="%{fullData.name}: %{y:.1f}%<extra></extra>",
        ))

    fig.update_layout(
        font=LAYOUT_DEFAULTS["font"],
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        title=dict(text="Activity Type Distribution by Session", x=0.5, font=dict(size=16)),
        xaxis=dict(title="Session", dtick=1),
        yaxis=dict(title="Proportion (%)", range=[0, 100]),
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
    )
    return fig


# ══════════════════════════════════════════════════════════════
# Novel Visualization 1: AI Dependency Glyph (Scatter View)
# ══════════════════════════════════════════════════════════════

def dependency_scatter(heatmap_df: pd.DataFrame, all_students_df: pd.DataFrame = None,
                       title: str = "AI Dependency Analysis") -> go.Figure:
    """AI 의존도 산점도 — 완료율 × 코딩활동 빈도로 4사분면 분류

    all_students_df가 없으면 heatmap_df의 n_activities를 proxy로 사용
    """
    # 학생별 집계
    student_stats = heatmap_df.groupby("profile_id").agg(
        avg_progress=("avg_progress", "mean"),
        total_activities=("n_activities", "sum"),
        n_sessions=("session", "nunique"),
    ).reset_index()

    # 코딩 단계(8~15차시) 활동 빈도 = AI 활용 proxy
    coding_phase = heatmap_df[heatmap_df["session"] >= 8]
    if len(coding_phase) > 0:
        coding_stats = coding_phase.groupby("profile_id").agg(
            coding_activities=("n_activities", "sum"),
        ).reset_index()
        student_stats = student_stats.merge(coding_stats, on="profile_id", how="left")
        student_stats["coding_activities"] = student_stats["coding_activities"].fillna(0)
    else:
        student_stats["coding_activities"] = 0

    # 초기(1~7) vs 후기(8~15) 활동 비율 = 의존도 추세 proxy
    early = heatmap_df[heatmap_df["session"] <= 7].groupby("profile_id")["n_activities"].mean()
    late = heatmap_df[heatmap_df["session"] > 7].groupby("profile_id")["n_activities"].mean()
    trend = (late - early).reset_index()
    trend.columns = ["profile_id", "activity_trend"]
    student_stats = student_stats.merge(trend, on="profile_id", how="left")
    student_stats["activity_trend"] = student_stats["activity_trend"].fillna(0)

    # 사분면 분류
    completion_median = student_stats["avg_progress"].median()
    activity_median = student_stats["coding_activities"].median()

    def classify(row):
        high_comp = row["avg_progress"] >= completion_median
        high_act = row["coding_activities"] >= activity_median
        if high_comp and not high_act:
            return "Independent Learner"
        elif high_comp and high_act:
            return "AI-Dependent Risk"
        elif not high_comp and not high_act:
            return "Disengaged"
        else:
            return "Struggling + Seeking Help"

    student_stats["quadrant"] = student_stats.apply(classify, axis=1)

    quadrant_colors = {
        "Independent Learner": "#10B981",
        "AI-Dependent Risk": "#EF4444",
        "Disengaged": "#94A3B8",
        "Struggling + Seeking Help": "#F59E0B",
    }

    # 의존도 추세를 마커 크기로
    trend_abs = student_stats["activity_trend"].abs()
    marker_sizes = 8 + (trend_abs / (trend_abs.max() + 1e-6)) * 20

    # 추세 방향을 마커 심볼로
    symbols = ["triangle-up" if t > 0 else "triangle-down" if t < 0 else "circle"
               for t in student_stats["activity_trend"]]

    fig = go.Figure()

    for quad, color in quadrant_colors.items():
        mask = student_stats["quadrant"] == quad
        subset = student_stats[mask]
        if len(subset) == 0:
            continue

        fig.add_trace(go.Scatter(
            x=subset["coding_activities"],
            y=subset["avg_progress"] * 100,
            mode="markers",
            name=quad,
            marker=dict(
                size=marker_sizes[mask].tolist(),
                color=color,
                opacity=0.8,
                line=dict(color="#1E293B", width=1),
                symbol=[symbols[i] for i in subset.index],
            ),
            hovertemplate=(
                "<b>%{text}</b><br>"
                "Completion: %{y:.1f}%<br>"
                "Coding Activities: %{x}<br>"
                "Trend: %{customdata[0]:+.1f}<br>"
                "Quadrant: %{customdata[1]}"
                "<extra></extra>"
            ),
            text=[f"Student {i+1:02d}" for i in range(len(subset))],
            customdata=list(zip(
                subset["activity_trend"].round(1).tolist(),
                subset["quadrant"].tolist(),
            )),
        ))

    # 사분면 구분선
    fig.add_hline(y=completion_median * 100, line_dash="dash",
                  line_color="#CBD5E1", line_width=1)
    fig.add_vline(x=activity_median, line_dash="dash",
                  line_color="#CBD5E1", line_width=1)

    # 사분면 라벨
    x_range = student_stats["coding_activities"].max()
    fig.add_annotation(x=x_range * 0.15, y=95, text="Independent", showarrow=False,
                       font=dict(color="#10B981", size=11, family="Inter"))
    fig.add_annotation(x=x_range * 0.85, y=95, text="AI-Dependent", showarrow=False,
                       font=dict(color="#EF4444", size=11, family="Inter"))
    fig.add_annotation(x=x_range * 0.15, y=5, text="Disengaged", showarrow=False,
                       font=dict(color="#94A3B8", size=11, family="Inter"))
    fig.add_annotation(x=x_range * 0.85, y=5, text="Struggling", showarrow=False,
                       font=dict(color="#F59E0B", size=11, family="Inter"))

    fig.update_layout(
        font=LAYOUT_DEFAULTS["font"],
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        title=dict(text=title, x=0.5, font=dict(size=16)),
        xaxis=dict(title="Coding Phase Activities (Sessions 8-15)", gridcolor="#F1F5F9"),
        yaxis=dict(title="Average Completion (%)", range=[0, 105], gridcolor="#F1F5F9"),
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
    )
    return fig


# ══════════════════════════════════════════════════════════════
# Novel Visualization 2: Cliff Detector Heatmap
# ══════════════════════════════════════════════════════════════

def cliff_heatmap(session_df: pd.DataFrame, summary_df: pd.DataFrame,
                  threshold: float = 0.15,
                  title: str = "Coding Cliff Detection — All Schools") -> go.Figure:
    """전체 학교의 절벽 발생 히트맵

    행=학교(커리큘럼별 그룹), 열=세션, 셀=절벽 심각도
    """
    classrooms = session_df["classroom_name"].unique()
    sessions = sorted(session_df["session"].unique())

    cliff_matrix = []
    labels = []
    curriculum_labels = []

    # 커리큘럼별 정렬
    classroom_curriculum = {}
    for _, row in summary_df.iterrows():
        classroom_curriculum[row["classroom_name"]] = row["curriculum"]

    sorted_classrooms = sorted(classrooms,
                               key=lambda c: (classroom_curriculum.get(c, ""), c))

    for classroom in sorted_classrooms:
        cls_data = session_df[session_df["classroom_name"] == classroom].sort_values("session")
        rates = cls_data["completion_rate"].values

        row_severity = []
        for s_idx in range(len(sessions)):
            if s_idx == 0 or s_idx >= len(rates):
                row_severity.append(0)
                continue

            drop = rates[s_idx] - rates[s_idx - 1]
            if drop < -threshold:
                severity = abs(drop) * rates[s_idx - 1]
                row_severity.append(round(severity, 3))
            else:
                row_severity.append(0)

        cliff_matrix.append(row_severity)
        labels.append(classroom)
        curriculum_labels.append(classroom_curriculum.get(classroom, ""))

    cliff_array = np.array(cliff_matrix)

    # 커리큘럼 구분선 위치
    curr_boundaries = []
    prev_curr = curriculum_labels[0] if curriculum_labels else ""
    for i, c in enumerate(curriculum_labels):
        if c != prev_curr:
            curr_boundaries.append(i)
            prev_curr = c

    fig = go.Figure(data=go.Heatmap(
        z=cliff_array,
        x=[f"S{int(s)}" for s in sessions],
        y=labels,
        colorscale=[
            [0, "#FFFFFF"],
            [0.3, "#FEF3C7"],
            [0.6, "#FBBF24"],
            [1, "#DC2626"],
        ],
        colorbar=dict(title="Severity"),
        hovertemplate=(
            "School: %{y}<br>"
            "Session: %{x}<br>"
            "Cliff Severity: %{z:.3f}"
            "<extra></extra>"
        ),
    ))

    # 커리큘럼 구분선
    for b in curr_boundaries:
        fig.add_hline(y=b - 0.5, line_color="#1E293B", line_width=2)

    fig.update_layout(
        font=LAYOUT_DEFAULTS["font"],
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        title=dict(text=title, x=0.5, font=dict(size=16)),
        xaxis=dict(title="Session", side="top"),
        yaxis=dict(title="", autorange="reversed"),
        height=max(400, len(labels) * 22 + 120),
        margin=dict(l=280, r=20, t=80, b=40),
    )
    return fig


# ══════════════════════════════════════════════════════════════
# Novel Visualization 3: Trajectory Alignment View
# ══════════════════════════════════════════════════════════════

def trajectory_alignment(session_df: pd.DataFrame, summary_df: pd.DataFrame,
                         title: str = "Trajectory Alignment — Baseline Normalized") -> go.Figure:
    """기준선 정규화 궤적 비교 + 커리큘럼별 포락선"""

    classrooms = session_df["classroom_name"].unique()
    sessions = sorted(session_df["session"].unique())

    # 커리큘럼 매핑
    classroom_curriculum = {}
    for _, row in summary_df.iterrows():
        classroom_curriculum[row["classroom_name"]] = row["curriculum"]

    # 각 학급의 정규화 궤적 계산
    trajectories = {}  # curriculum -> list of normalized trajectories
    for classroom in classrooms:
        cls_data = session_df[session_df["classroom_name"] == classroom].sort_values("session")
        rates = cls_data["completion_rate"].values

        if len(rates) < 2:
            continue

        # 1차시 기준 정규화
        baseline = rates[0]
        normalized = (rates - baseline) * 100  # %p 단위

        curr = classroom_curriculum.get(classroom, "Unknown")
        if curr not in trajectories:
            trajectories[curr] = []
        trajectories[curr].append({
            "classroom": classroom,
            "sessions": cls_data["session"].values,
            "normalized": normalized,
            "raw": rates * 100,
        })

    fig = go.Figure()

    for curr, color in CURRICULUM_COLORS.items():
        if curr not in trajectories:
            continue

        trajs = trajectories[curr]

        # 포락선 계산 (25~75 백분위)
        all_normalized = np.array([t["normalized"] for t in trajs])
        if len(all_normalized) > 1:
            p25 = np.percentile(all_normalized, 25, axis=0)
            p75 = np.percentile(all_normalized, 75, axis=0)
            median_traj = np.median(all_normalized, axis=0)
            sess_list = trajs[0]["sessions"].tolist()

            # 포락선 (band)
            fig.add_trace(go.Scatter(
                x=sess_list + sess_list[::-1],
                y=p75.tolist() + p25[::-1].tolist(),
                fill="toself",
                fillcolor=color.replace(")", ", 0.12)").replace("rgb", "rgba") if "rgb" in color
                          else f"rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.12)",
                line=dict(color="rgba(0,0,0,0)"),
                name=f"{curr} (25-75%)",
                showlegend=True,
                hoverinfo="skip",
            ))

            # 중앙값 라인
            fig.add_trace(go.Scatter(
                x=sess_list,
                y=median_traj.tolist(),
                mode="lines",
                name=f"{curr} median",
                line=dict(color=color, width=3, dash="solid"),
                hovertemplate=f"{curr} median<br>Session %{{x}}: %{{y:+.1f}}%p<extra></extra>",
            ))

        # 개별 학교 라인 (얇게)
        for traj in trajs:
            fig.add_trace(go.Scatter(
                x=traj["sessions"].tolist(),
                y=traj["normalized"].tolist(),
                mode="lines",
                name=traj["classroom"],
                line=dict(color=color, width=1, dash="dot"),
                opacity=0.4,
                showlegend=False,
                hovertemplate=(
                    f"<b>{traj['classroom']}</b><br>"
                    f"Session %{{x}}<br>"
                    f"Change: %{{y:+.1f}}%p"
                    f"<extra></extra>"
                ),
            ))

    # 기준선 (0)
    fig.add_hline(y=0, line_color="#CBD5E1", line_width=1, line_dash="dash")

    # 단계 구분
    phases = [
        (1, 3, "#EFF6FF", "Understanding"),
        (4, 7, "#ECFDF5", "Analysis"),
        (8, 11, "#FEF2F2", "Coding"),
        (12, 15, "#F5F3FF", "Synthesis"),
    ]
    for start, end, color_bg, label in phases:
        fig.add_vrect(x0=start - 0.5, x1=end + 0.5,
                      fillcolor=color_bg, opacity=0.3, layer="below", line_width=0,
                      annotation_text=label, annotation_position="top left",
                      annotation_font_size=9, annotation_font_color="#94A3B8")

    fig.update_layout(
        font=LAYOUT_DEFAULTS["font"],
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        title=dict(text=title, x=0.5, font=dict(size=16)),
        xaxis=dict(title="Session", dtick=1, gridcolor="#F1F5F9"),
        yaxis=dict(title="Change from Baseline (%p)", gridcolor="#F1F5F9",
                   zeroline=True, zerolinecolor="#94A3B8"),
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
    )
    return fig


def trajectory_sparklines(session_df: pd.DataFrame, summary_df: pd.DataFrame,
                          title: str = "Phase Performance Summary") -> go.Figure:
    """학교별 4단계 스파크라인 요약"""
    phase_ranges = {
        "Understanding\n(1-3)": (1, 3),
        "Analysis\n(4-7)": (4, 7),
        "Coding\n(8-11)": (8, 11),
        "Synthesis\n(12-15)": (12, 15),
    }
    phase_colors = ["#3B82F6", "#10B981", "#EF4444", "#8B5CF6"]

    classroom_curriculum = {}
    for _, row in summary_df.iterrows():
        classroom_curriculum[row["classroom_name"]] = row["curriculum"]

    classrooms = sorted(session_df["classroom_name"].unique(),
                        key=lambda c: (classroom_curriculum.get(c, ""), c))

    phase_data = {phase: [] for phase in phase_ranges}

    for classroom in classrooms:
        cls_data = session_df[session_df["classroom_name"] == classroom]
        for phase_name, (start, end) in phase_ranges.items():
            phase_sessions = cls_data[
                (cls_data["session"] >= start) & (cls_data["session"] <= end)
            ]
            avg = phase_sessions["completion_rate"].mean() * 100 if len(phase_sessions) > 0 else 0
            phase_data[phase_name].append(avg)

    fig = go.Figure()

    for i, (phase_name, values) in enumerate(phase_data.items()):
        fig.add_trace(go.Bar(
            y=classrooms,
            x=values,
            orientation="h",
            name=phase_name.replace("\n", " "),
            marker_color=phase_colors[i],
            opacity=0.85,
            hovertemplate="%{y}<br>" + phase_name.replace("\n", " ") + ": %{x:.1f}%<extra></extra>",
        ))

    fig.update_layout(
        font=LAYOUT_DEFAULTS["font"],
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        title=dict(text=title, x=0.5, font=dict(size=16)),
        barmode="group",
        xaxis=dict(title="Completion Rate (%)", range=[0, 105], gridcolor="#F1F5F9"),
        yaxis=dict(title="", autorange="reversed"),
        height=max(500, len(classrooms) * 25 + 150),
        margin=dict(l=280, r=20, t=60, b=60),
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
    )
    return fig
