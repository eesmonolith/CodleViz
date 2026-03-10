"""CodleViz 시각화 컴포넌트 (v0.3 — 가독성 개선)"""
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
    "DC": "Data\nComprehension", "DA": "Data\nAnalysis",
    "DV": "Data\nVisualization", "DI": "Data\nInterpretation",
    "CT": "Computational\nThinking",
}
COMPETENCY_NAMES_SHORT = {
    "DC": "DC", "DA": "DA", "DV": "DV", "DI": "DI", "CT": "CT",
}
CURRICULUM_COLORS = {
    "해양쓰레기": "#3B82F6", "기후변화": "#10B981", "식량안보": "#F59E0B",
}
LAYOUT_DEFAULTS = dict(
    font=dict(family="Pretendard, Inter, sans-serif", size=13, color="#1E293B"),
    paper_bgcolor="#FFFFFF",
    plot_bgcolor="#FFFFFF",
    margin=dict(l=60, r=20, t=50, b=40),
)

# 단계 정보 (공통)
PHASES = [
    (1, 3, "#EFF6FF", "이해"),
    (4, 7, "#ECFDF5", "분석"),
    (8, 11, "#FEF2F2", "코딩"),
    (12, 15, "#F5F3FF", "종합"),
]


def _truncate(text: str, max_len: int = 25) -> str:
    """긴 텍스트 잘라내기"""
    return text if len(text) <= max_len else text[:max_len-2] + "…"


def _add_phase_bg(fig, phases=None, y_pos=1.02):
    """차트에 단계 배경색 + 상단 라벨 추가 (겹침 방지)"""
    if phases is None:
        phases = PHASES
    for start, end, color, label in phases:
        fig.add_vrect(
            x0=start - 0.5, x1=end + 0.5,
            fillcolor=color, opacity=0.4, layer="below", line_width=0,
        )
        # 라벨을 차트 상단 바깥에 배치 (데이터와 겹치지 않음)
        fig.add_annotation(
            x=(start + end) / 2, y=y_pos,
            text=label, showarrow=False,
            font=dict(size=10, color="#94A3B8"),
            xref="x", yref="paper",
        )


def competency_radar(df: pd.DataFrame, title: str = "") -> go.Figure:
    """5역량 레이더 차트"""
    competencies = ["DC", "DA", "DV", "DI", "CT"]
    values = []
    for c in competencies:
        row = df[df["competency"] == c]
        values.append(row["avg_progress"].values[0] * 100 if len(row) > 0 else 0)

    # 짧은 라벨 사용 (겹침 방지)
    labels = [f"{c}\n{v:.0f}%" for c, v in zip(competencies, values)]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=labels + [labels[0]],
        fill="toself",
        fillcolor="rgba(37, 99, 235, 0.15)",
        line=dict(color="#2563EB", width=2.5),
        marker=dict(size=8, color="#2563EB"),
        name="Competency Score",
        hovertemplate="%{theta}: %{r:.1f}%<extra></extra>",
    ))

    fig.update_layout(
        font=dict(family="Pretendard, Inter, sans-serif", size=12, color="#1E293B"),
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        title=dict(text=_truncate(title, 30), x=0.5, font=dict(size=14)),
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], ticksuffix="%",
                           gridcolor="#F1F5F9", linecolor="#E2E8F0",
                           tickfont=dict(size=10)),
            angularaxis=dict(gridcolor="#F1F5F9", linecolor="#E2E8F0",
                            tickfont=dict(size=11)),
            bgcolor="#FFFFFF",
        ),
        showlegend=False,
        height=350,
        margin=dict(l=60, r=60, t=50, b=40),
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
        name="완료율",
        line=dict(color="#2563EB", width=2.5),
        marker=dict(size=7, color="#2563EB"),
        hovertemplate="%{x}차시: %{y:.1f}%<extra></extra>",
    ))

    # 단계 배경 (라벨은 차트 상단 바깥)
    _add_phase_bg(fig)

    # ── Cliff Detection ──
    rates = df.sort_values("session")["completion_rate"].values
    sessions = df.sort_values("session")["session"].values
    for i in range(1, len(rates)):
        drop = rates[i] - rates[i - 1]
        if drop < -cliff_threshold:
            severity = abs(drop) * rates[i - 1]
            if i + 3 < len(rates):
                recovery = (rates[i + 3] - rates[i]) / (rates[i - 1] - rates[i]) if (rates[i - 1] - rates[i]) > 0 else 0
                recovery = max(0, min(1, recovery))
            else:
                recovery = 0

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
                name=f"절벽 {int(sessions[i])}차시",
                hovertemplate=(
                    f"<b>절벽 감지</b><br>"
                    f"{int(sessions[i])}차시<br>"
                    f"하락: {drop*100:.1f}%p<br>"
                    f"심각도: {severity:.2f}<br>"
                    f"회복률: {recovery*100:.0f}%"
                    f"<extra></extra>"
                ),
                showlegend=False,
            ))

    fig.update_layout(
        font=LAYOUT_DEFAULTS["font"],
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        title=dict(text=_truncate(title, 35), x=0.5, font=dict(size=14)),
        xaxis=dict(title="", dtick=1, gridcolor="#F1F5F9", tickfont=dict(size=11)),
        yaxis=dict(title="완료율 (%)", range=[0, 110], gridcolor="#F1F5F9"),
        height=380,
        showlegend=False,
        margin=dict(l=60, r=20, t=65, b=30),
    )
    return fig


def student_heatmap(df: pd.DataFrame, title: str = "") -> go.Figure:
    """학생x세션 완료 히트맵"""
    pivot = df.pivot_table(
        index="profile_id", columns="session", values="avg_progress", aggfunc="mean"
    )
    pivot = pivot.sort_values(by=pivot.columns.tolist(), ascending=False)

    student_labels = [f"S{i+1:02d}" for i in range(len(pivot))]

    fig = go.Figure(data=go.Heatmap(
        z=pivot.values * 100,
        x=[f"{int(c)}차시" for c in pivot.columns],
        y=student_labels,
        colorscale=[
            [0, "#FEE2E2"],
            [0.5, "#FEF3C7"],
            [1, "#D1FAE5"],
        ],
        colorbar=dict(title="%", ticksuffix="%", len=0.8),
        hovertemplate="%{y} · %{x}: %{z:.1f}%<extra></extra>",
    ))

    fig.update_layout(
        font=LAYOUT_DEFAULTS["font"],
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        title=dict(text=title, x=0.5, font=dict(size=14)),
        xaxis=dict(title="", side="top", tickfont=dict(size=10)),
        yaxis=dict(title="", autorange="reversed", tickfont=dict(size=10)),
        height=max(300, len(pivot) * 22 + 100),
        margin=dict(l=50, r=20, t=80, b=20),
    )
    return fig


def school_comparison_bar(df: pd.DataFrame) -> go.Figure:
    """학교별 평균 진도 수평 막대 그래프"""
    df_sorted = df.sort_values("avg_progress", ascending=True)
    colors = [CURRICULUM_COLORS.get(c, "#94A3B8") for c in df_sorted["curriculum"]]
    # 라벨 잘라내기
    labels = [_truncate(name, 28) for name in df_sorted["classroom_name"]]

    fig = go.Figure(go.Bar(
        x=df_sorted["avg_progress"] * 100,
        y=labels,
        orientation="h",
        marker_color=colors,
        hovertemplate="%{y}<br>진도: %{x:.1f}%<br>학생 수: %{customdata[0]}<extra></extra>",
        customdata=df_sorted[["n_students"]].values,
    ))

    fig.update_layout(
        font=LAYOUT_DEFAULTS["font"],
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        title=dict(text="학교별 평균 진도율 비교", x=0.5, font=dict(size=14)),
        xaxis=dict(title="평균 진도율 (%)", range=[0, 105], gridcolor="#F1F5F9"),
        yaxis=dict(title="", tickfont=dict(size=11)),
        height=max(400, len(df_sorted) * 26 + 100),
        margin=dict(l=220, r=20, t=50, b=40),
    )
    return fig


def competency_comparison_grouped(df: pd.DataFrame) -> go.Figure:
    """전체 학교 역량별 평균 비교 막대 그래프"""
    comp_avg = df.groupby("competency")["avg_progress"].mean().reset_index()
    comp_avg = comp_avg.sort_values("competency")

    fig = go.Figure(go.Bar(
        x=comp_avg["competency"],
        y=comp_avg["avg_progress"] * 100,
        marker_color=[COMPETENCY_COLORS.get(c, "#94A3B8") for c in comp_avg["competency"]],
        text=[f"{v*100:.1f}%" for v in comp_avg["avg_progress"]],
        textposition="outside",
        hovertemplate="%{x}: %{y:.1f}%<extra></extra>",
    ))

    fig.update_layout(
        font=LAYOUT_DEFAULTS["font"],
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        title=dict(text="전체 역량 평균 비교", x=0.5, font=dict(size=14)),
        yaxis=dict(title="평균 점수 (%)", range=[0, 110], gridcolor="#F1F5F9"),
        xaxis=dict(title=""),
        height=380,
        margin=dict(l=60, r=20, t=50, b=40),
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
    activity_names_kr = {
        "PdfActivity": "PDF",
        "VideoActivity": "영상",
        "StudioActivity": "코딩",
        "CodapActivity": "CODAP",
        "BoardActivity": "게시판",
        "SheetActivity": "시트",
        "QuizActivity": "퀴즈",
        "EmbeddedActivity": "임베드",
        "EntryActivity": "엔트리",
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

        display_name = activity_names_kr.get(act_type, act_type.replace("Activity", ""))
        fig.add_trace(go.Scatter(
            x=sessions, y=ratios,
            mode="lines",
            name=display_name,
            stackgroup="one",
            line=dict(width=0),
            fillcolor=activity_colors.get(act_type, "#94A3B8"),
            hovertemplate=f"{display_name}: %{{y:.1f}}%<extra></extra>",
        ))

    fig.update_layout(
        font=LAYOUT_DEFAULTS["font"],
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        title=dict(text="차시별 활동 유형 분포", x=0.5, font=dict(size=14)),
        xaxis=dict(title="", dtick=1, tickfont=dict(size=11)),
        yaxis=dict(title="비율 (%)", range=[0, 100]),
        height=480,
        legend=dict(
            orientation="h", yanchor="top", y=-0.18, xanchor="center", x=0.5,
            font=dict(size=10), tracegroupgap=5,
        ),
        margin=dict(l=60, r=20, t=50, b=140),
    )
    return fig


# ══════════════════════════════════════════════════════════════
# Novel Visualization 1: AI Dependency Scatter
# ══════════════════════════════════════════════════════════════

def dependency_scatter(heatmap_df: pd.DataFrame, all_students_df: pd.DataFrame = None,
                       title: str = "AI 의존도 분석") -> go.Figure:
    """AI 의존도 산점도 — 완료율 x 코딩활동 빈도로 4사분면 분류"""
    student_stats = heatmap_df.groupby("profile_id").agg(
        avg_progress=("avg_progress", "mean"),
        total_activities=("n_activities", "sum"),
        n_sessions=("session", "nunique"),
    ).reset_index()

    coding_phase = heatmap_df[heatmap_df["session"] >= 8]
    if len(coding_phase) > 0:
        coding_stats = coding_phase.groupby("profile_id").agg(
            coding_activities=("n_activities", "sum"),
        ).reset_index()
        student_stats = student_stats.merge(coding_stats, on="profile_id", how="left")
        student_stats["coding_activities"] = student_stats["coding_activities"].fillna(0)
    else:
        student_stats["coding_activities"] = 0

    early = heatmap_df[heatmap_df["session"] <= 7].groupby("profile_id")["n_activities"].mean()
    late = heatmap_df[heatmap_df["session"] > 7].groupby("profile_id")["n_activities"].mean()
    trend = (late - early).reset_index()
    trend.columns = ["profile_id", "activity_trend"]
    student_stats = student_stats.merge(trend, on="profile_id", how="left")
    student_stats["activity_trend"] = student_stats["activity_trend"].fillna(0)

    completion_median = student_stats["avg_progress"].median()
    activity_median = student_stats["coding_activities"].median()

    def classify(row):
        high_comp = row["avg_progress"] >= completion_median
        high_act = row["coding_activities"] >= activity_median
        if high_comp and not high_act:
            return "독립 학습자"
        elif high_comp and high_act:
            return "AI 의존 위험"
        elif not high_comp and not high_act:
            return "이탈"
        else:
            return "어려움+도움요청"

    student_stats["quadrant"] = student_stats.apply(classify, axis=1)

    quadrant_colors = {
        "독립 학습자": "#10B981",
        "AI 의존 위험": "#EF4444",
        "이탈": "#94A3B8",
        "어려움+도움요청": "#F59E0B",
    }

    trend_abs = student_stats["activity_trend"].abs()
    marker_sizes = 8 + (trend_abs / (trend_abs.max() + 1e-6)) * 20

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
                "완료율: %{y:.1f}%<br>"
                "코딩 활동: %{x}<br>"
                "추세: %{customdata[0]:+.1f}<br>"
                "분류: %{customdata[1]}"
                "<extra></extra>"
            ),
            text=[f"학생 {i+1:02d}" for i in range(len(subset))],
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

    # 사분면 라벨 — 반투명 배경으로 겹침 방지
    x_max = student_stats["coding_activities"].max()
    x_min = student_stats["coding_activities"].min()
    x_pad = (x_max - x_min) * 0.05 if x_max > x_min else 5

    annotations = [
        (x_min + x_pad, 102, "독립 학습자", "#10B981"),
        (x_max - x_pad, 102, "AI 의존 위험", "#EF4444"),
        (x_min + x_pad, 3, "이탈", "#94A3B8"),
        (x_max - x_pad, 3, "어려움+도움요청", "#F59E0B"),
    ]
    for ax, ay, atext, acolor in annotations:
        fig.add_annotation(
            x=ax, y=ay, text=atext, showarrow=False,
            font=dict(color=acolor, size=11, family="Pretendard, Inter"),
            bgcolor="rgba(255,255,255,0.8)",
            borderpad=3,
            xanchor="left" if ax < activity_median else "right",
        )

    fig.update_layout(
        font=LAYOUT_DEFAULTS["font"],
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        title=dict(text=_truncate(title, 35), x=0.5, font=dict(size=14)),
        xaxis=dict(title="코딩 단계 활동 수 (8-15차시)", gridcolor="#F1F5F9",
                   title_standoff=10),
        yaxis=dict(title="평균 완료율 (%)", range=[-2, 108], gridcolor="#F1F5F9"),
        height=520,
        legend=dict(
            orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5,
            font=dict(size=10),
        ),
        margin=dict(l=60, r=20, t=50, b=100),
    )
    return fig


# ══════════════════════════════════════════════════════════════
# Novel Visualization 2: Cliff Detector Heatmap
# ══════════════════════════════════════════════════════════════

def cliff_heatmap(session_df: pd.DataFrame, summary_df: pd.DataFrame,
                  threshold: float = 0.15,
                  title: str = "전체 학교 절벽 감지") -> go.Figure:
    """전체 학교의 절벽 발생 히트맵"""
    classrooms = session_df["classroom_name"].unique()
    sessions = sorted(session_df["session"].unique())

    cliff_matrix = []
    labels = []
    curriculum_labels = []

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
        labels.append(_truncate(classroom, 25))
        curriculum_labels.append(classroom_curriculum.get(classroom, ""))

    cliff_array = np.array(cliff_matrix)

    curr_boundaries = []
    prev_curr = curriculum_labels[0] if curriculum_labels else ""
    for i, c in enumerate(curriculum_labels):
        if c != prev_curr:
            curr_boundaries.append(i)
            prev_curr = c

    fig = go.Figure(data=go.Heatmap(
        z=cliff_array,
        x=[f"{int(s)}차시" for s in sessions],
        y=labels,
        colorscale=[
            [0, "#FFFFFF"],
            [0.3, "#FEF3C7"],
            [0.6, "#FBBF24"],
            [1, "#DC2626"],
        ],
        colorbar=dict(title="심각도", len=0.8),
        hovertemplate="%{y}<br>%{x}<br>심각도: %{z:.3f}<extra></extra>",
    ))

    for b in curr_boundaries:
        fig.add_hline(y=b - 0.5, line_color="#1E293B", line_width=2)

    fig.update_layout(
        font=LAYOUT_DEFAULTS["font"],
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        title=dict(text=title, x=0.5, font=dict(size=14)),
        xaxis=dict(title="", side="top", tickfont=dict(size=10)),
        yaxis=dict(title="", autorange="reversed", tickfont=dict(size=9)),
        height=max(400, len(labels) * 22 + 140),
        margin=dict(l=200, r=20, t=80, b=20),
    )
    return fig


# ══════════════════════════════════════════════════════════════
# Novel Visualization 3: Trajectory Alignment View
# ══════════════════════════════════════════════════════════════

def trajectory_alignment(session_df: pd.DataFrame, summary_df: pd.DataFrame,
                         title: str = "기준선 정규화 궤적 비교") -> go.Figure:
    """기준선 정규화 궤적 비교 + 커리큘럼별 포락선"""
    classrooms = session_df["classroom_name"].unique()
    sessions = sorted(session_df["session"].unique())

    classroom_curriculum = {}
    for _, row in summary_df.iterrows():
        classroom_curriculum[row["classroom_name"]] = row["curriculum"]

    trajectories = {}
    for classroom in classrooms:
        cls_data = session_df[session_df["classroom_name"] == classroom].sort_values("session")
        rates = cls_data["completion_rate"].values

        if len(rates) < 2:
            continue

        baseline = rates[0]
        normalized = (rates - baseline) * 100

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
        all_normalized = np.array([t["normalized"] for t in trajs])

        if len(all_normalized) > 1:
            p25 = np.percentile(all_normalized, 25, axis=0)
            p75 = np.percentile(all_normalized, 75, axis=0)
            median_traj = np.median(all_normalized, axis=0)
            sess_list = trajs[0]["sessions"].tolist()

            # 포락선 (band)
            hex_color = color.lstrip("#")
            r, g, b = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
            fill_rgba = f"rgba({r}, {g}, {b}, 0.12)"

            fig.add_trace(go.Scatter(
                x=sess_list + sess_list[::-1],
                y=p75.tolist() + p25[::-1].tolist(),
                fill="toself",
                fillcolor=fill_rgba,
                line=dict(color="rgba(0,0,0,0)"),
                name=f"{curr} (25-75%)",
                showlegend=True,
                hoverinfo="skip",
            ))

            fig.add_trace(go.Scatter(
                x=sess_list,
                y=median_traj.tolist(),
                mode="lines",
                name=f"{curr} 중앙값",
                line=dict(color=color, width=3),
                hovertemplate=f"{curr} 중앙값<br>%{{x}}차시: %{{y:+.1f}}%p<extra></extra>",
            ))

        for traj in trajs:
            fig.add_trace(go.Scatter(
                x=traj["sessions"].tolist(),
                y=traj["normalized"].tolist(),
                mode="lines",
                name=traj["classroom"],
                line=dict(color=color, width=1, dash="dot"),
                opacity=0.35,
                showlegend=False,
                hovertemplate=(
                    f"<b>{_truncate(traj['classroom'], 20)}</b><br>"
                    f"%{{x}}차시: %{{y:+.1f}}%p"
                    f"<extra></extra>"
                ),
            ))

    fig.add_hline(y=0, line_color="#CBD5E1", line_width=1, line_dash="dash")

    _add_phase_bg(fig, y_pos=1.03)

    fig.update_layout(
        font=LAYOUT_DEFAULTS["font"],
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        title=dict(text=title, x=0.5, font=dict(size=14)),
        xaxis=dict(title="", dtick=1, gridcolor="#F1F5F9", tickfont=dict(size=11)),
        yaxis=dict(title="기준선 대비 변화 (%p)", gridcolor="#F1F5F9",
                   zeroline=True, zerolinecolor="#94A3B8"),
        height=520,
        legend=dict(
            orientation="h", yanchor="top", y=-0.08, xanchor="center", x=0.5,
            font=dict(size=10),
        ),
        margin=dict(l=60, r=20, t=70, b=100),
    )
    return fig


def trajectory_sparklines(session_df: pd.DataFrame, summary_df: pd.DataFrame,
                          title: str = "학교별 단계 성과") -> go.Figure:
    """학교별 4단계 스파크라인 요약"""
    phase_ranges = {
        "이해(1-3)": (1, 3),
        "분석(4-7)": (4, 7),
        "코딩(8-11)": (8, 11),
        "종합(12-15)": (12, 15),
    }
    phase_colors = ["#3B82F6", "#10B981", "#EF4444", "#8B5CF6"]

    classroom_curriculum = {}
    for _, row in summary_df.iterrows():
        classroom_curriculum[row["classroom_name"]] = row["curriculum"]

    classrooms = sorted(session_df["classroom_name"].unique(),
                        key=lambda c: (classroom_curriculum.get(c, ""), c))

    # 라벨 잘라내기
    labels = [_truncate(c, 25) for c in classrooms]

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
            y=labels,
            x=values,
            orientation="h",
            name=phase_name,
            marker_color=phase_colors[i],
            opacity=0.85,
            hovertemplate="%{y}<br>" + phase_name + ": %{x:.1f}%<extra></extra>",
        ))

    fig.update_layout(
        font=LAYOUT_DEFAULTS["font"],
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        title=dict(text=title, x=0.5, font=dict(size=14)),
        barmode="group",
        xaxis=dict(title="", range=[0, 105], gridcolor="#F1F5F9", ticksuffix="%"),
        yaxis=dict(title="", autorange="reversed", tickfont=dict(size=9)),
        height=max(500, len(classrooms) * 25 + 180),
        margin=dict(l=200, r=20, t=50, b=90),
        legend=dict(
            orientation="h", yanchor="top", y=-0.06, xanchor="center", x=0.5,
            font=dict(size=10),
        ),
    )
    return fig
