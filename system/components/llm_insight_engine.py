"""
CodleViz — LLM-Guided Visual Exploration Engine
자동 패턴 탐지 + LLM 기반 자연어 인사이트 생성 + 가이드 내비게이션
"""
import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from typing import Optional

# LLM은 선택적 의존성
try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

HAS_LLM = HAS_OPENAI or HAS_ANTHROPIC


@dataclass
class Insight:
    """자동 발견된 인사이트"""
    insight_id: str
    category: str          # "cliff", "ai_dependency", "competency_gap", "trajectory_divergence", "anomaly"
    severity: str          # "critical", "warning", "info"
    title: str             # 한글 제목
    summary: str           # 한글 설명
    evidence: dict         # 수치 근거
    related_view: str      # 관련 뷰 이름 (탭 연결용)
    related_filters: dict  # 해당 뷰로 이동할 때 적용할 필터
    suggestions: list      # 실행 방안
    llm_narrative: str = ""  # LLM이 생성한 자연어 해설


def detect_all_patterns(
    summary_df: pd.DataFrame,
    session_df: pd.DataFrame,
    competency_df: pd.DataFrame,
    heatmap_df: pd.DataFrame,
    activity_df: pd.DataFrame,
    cliff_threshold: float = 0.15,
) -> list[Insight]:
    """모든 패턴 탐지를 수행하고 Insight 리스트 반환"""
    insights = []
    insights.extend(_detect_coding_cliffs(session_df, summary_df, cliff_threshold))
    insights.extend(_detect_competency_gaps(competency_df, summary_df))
    insights.extend(_detect_trajectory_divergence(session_df, summary_df))
    insights.extend(_detect_at_risk_classrooms(summary_df))
    insights.extend(_detect_activity_anomalies(activity_df, summary_df))

    # severity 순 정렬
    severity_order = {"critical": 0, "warning": 1, "info": 2}
    insights.sort(key=lambda x: severity_order.get(x.severity, 3))

    return insights


# ═══════════════════════════════════════════════════════
# 패턴 1: 코딩 절벽 (Coding Cliff)
# ═══════════════════════════════════════════════════════

def _detect_coding_cliffs(
    session_df: pd.DataFrame,
    summary_df: pd.DataFrame,
    threshold: float = 0.15,
) -> list[Insight]:
    insights = []
    classrooms = session_df["classroom_name"].unique()

    # 차시별 하락 빈도 집계
    session_cliff_counts = {}
    cliff_details = []

    for classroom in classrooms:
        cls_data = session_df[session_df["classroom_name"] == classroom].sort_values("session")
        rates = cls_data["completion_rate"].values
        sessions = cls_data["session"].values

        for i in range(1, len(rates)):
            drop = rates[i] - rates[i - 1]
            if drop < -threshold:
                s = int(sessions[i])
                session_cliff_counts[s] = session_cliff_counts.get(s, 0) + 1
                severity = abs(drop) * rates[i - 1]
                cliff_details.append({
                    "classroom": classroom,
                    "session": s,
                    "drop": drop,
                    "severity": severity,
                    "prev_rate": rates[i - 1],
                    "curr_rate": rates[i],
                })

    if not cliff_details:
        return insights

    # 전체 요약 인사이트
    total_cliffs = len(cliff_details)
    n_classrooms = len(classrooms)
    worst_session = max(session_cliff_counts, key=session_cliff_counts.get)
    worst_count = session_cliff_counts[worst_session]
    pct = worst_count / n_classrooms * 100

    phase_map = {range(1, 4): "이해", range(4, 8): "분석", range(8, 12): "코딩", range(12, 16): "종합"}
    phase = next((v for k, v in phase_map.items() if worst_session in k), "")

    insights.append(Insight(
        insight_id="cliff_global",
        category="cliff",
        severity="critical" if pct > 30 else "warning",
        title=f"{worst_session}차시({phase} 단계)에서 {worst_count}개 학급 진도 하락",
        summary=(
            f"전체 {n_classrooms}개 학급 중 {worst_count}개({pct:.0f}%)가 "
            f"{worst_session}차시에서 완료율 급락을 경험했습니다. "
            f"총 {total_cliffs}건의 진도 하락이 감지되었습니다."
        ),
        evidence={
            "worst_session": worst_session,
            "cliff_count": worst_count,
            "total_cliffs": total_cliffs,
            "pct_affected": pct,
            "phase": phase,
        },
        related_view="진도 하락 탐지",
        related_filters={},
        suggestions=[
            f"{worst_session}차시 학습 콘텐츠 난이도 점검",
            f"{phase} 단계 진입 전 사전 점검 퀴즈 추가 고려",
            "하락 학급 교사 면담으로 원인 파악",
        ],
    ))

    # 가장 심한 개별 하락
    worst_cliff = max(cliff_details, key=lambda x: x["severity"])
    insights.append(Insight(
        insight_id=f"cliff_{worst_cliff['classroom']}_{worst_cliff['session']}",
        category="cliff",
        severity="critical",
        title=f"{worst_cliff['classroom']} — {worst_cliff['session']}차시에서 {worst_cliff['drop']*100:.1f}%p 급락",
        summary=(
            f"완료율이 {worst_cliff['prev_rate']*100:.1f}%에서 "
            f"{worst_cliff['curr_rate']*100:.1f}%로 급락했습니다."
        ),
        evidence=worst_cliff,
        related_view="학습 여정",
        related_filters={"classroom": worst_cliff["classroom"]},
        suggestions=[
            f"해당 학급 {worst_cliff['session']}차시 활동 내용 검토",
            "학생별 히트맵에서 어떤 학생이 영향 받았는지 확인",
        ],
    ))

    return insights


# ═══════════════════════════════════════════════════════
# 패턴 2: 역량 격차
# ═══════════════════════════════════════════════════════

def _detect_competency_gaps(
    competency_df: pd.DataFrame,
    summary_df: pd.DataFrame,
) -> list[Insight]:
    insights = []

    comp_avg = competency_df.groupby("competency")["avg_progress"].mean()
    if len(comp_avg) < 2:
        return insights

    best = comp_avg.idxmax()
    worst = comp_avg.idxmin()
    gap = (comp_avg[best] - comp_avg[worst]) * 100

    COMP_NAMES = {"DC": "데이터 이해", "DA": "데이터 분석", "DV": "데이터 시각화",
                  "DI": "데이터 해석", "CT": "컴퓨팅 사고"}

    if gap > 15:
        insights.append(Insight(
            insight_id="comp_gap",
            category="competency_gap",
            severity="warning" if gap > 20 else "info",
            title=f"역량 격차 {gap:.1f}%p — {COMP_NAMES.get(worst, worst)} 보강 필요",
            summary=(
                f"가장 높은 역량 {COMP_NAMES.get(best, best)}({comp_avg[best]*100:.1f}%)와 "
                f"가장 낮은 역량 {COMP_NAMES.get(worst, worst)}({comp_avg[worst]*100:.1f}%) 간 "
                f"격차가 {gap:.1f}%p입니다."
            ),
            evidence={
                "best_competency": best,
                "worst_competency": worst,
                "gap": gap,
                "all_scores": comp_avg.to_dict(),
            },
            related_view="역량 분석",
            related_filters={},
            suggestions=[
                f"{COMP_NAMES.get(worst, worst)} 역량 강화를 위한 추가 활동 배치",
                "역량 간 균형을 위한 커리큘럼 조정 검토",
            ],
        ))

    # 커리큘럼별 역량 차이
    curriculum_map = dict(zip(summary_df["classroom_name"], summary_df["curriculum"]))
    competency_df_with_curr = competency_df.copy()
    competency_df_with_curr["curriculum"] = competency_df_with_curr["classroom_name"].map(curriculum_map)

    for comp in comp_avg.index:
        curr_scores = competency_df_with_curr[
            competency_df_with_curr["competency"] == comp
        ].groupby("curriculum")["avg_progress"].mean()

        if len(curr_scores) > 1:
            curr_gap = (curr_scores.max() - curr_scores.min()) * 100
            if curr_gap > 20:
                best_curr = curr_scores.idxmax()
                worst_curr = curr_scores.idxmin()
                insights.append(Insight(
                    insight_id=f"comp_curr_{comp}",
                    category="competency_gap",
                    severity="info",
                    title=f"{COMP_NAMES.get(comp, comp)} — 커리큘럼별 격차 {curr_gap:.1f}%p",
                    summary=(
                        f"{best_curr}({curr_scores[best_curr]*100:.1f}%) vs "
                        f"{worst_curr}({curr_scores[worst_curr]*100:.1f}%)"
                    ),
                    evidence={
                        "competency": comp,
                        "best_curriculum": best_curr,
                        "worst_curriculum": worst_curr,
                        "gap": curr_gap,
                    },
                    related_view="역량 분석",
                    related_filters={"competency": comp},
                    suggestions=[
                        f"{worst_curr} 커리큘럼의 {COMP_NAMES.get(comp, comp)} 관련 활동 강화",
                    ],
                ))

    return insights


# ═══════════════════════════════════════════════════════
# 패턴 3: 학습 궤적 이탈
# ═══════════════════════════════════════════════════════

def _detect_trajectory_divergence(
    session_df: pd.DataFrame,
    summary_df: pd.DataFrame,
) -> list[Insight]:
    insights = []

    curriculum_map = dict(zip(summary_df["classroom_name"], summary_df["curriculum"]))

    # 커리큘럼별 궤적 그룹화
    curr_trajectories = {}
    for classroom in session_df["classroom_name"].unique():
        cls_data = session_df[session_df["classroom_name"] == classroom].sort_values("session")
        rates = cls_data["completion_rate"].values
        curr = curriculum_map.get(classroom, "Unknown")
        if curr not in curr_trajectories:
            curr_trajectories[curr] = {}
        curr_trajectories[curr][classroom] = rates

    for curr, trajs in curr_trajectories.items():
        if len(trajs) < 3:
            continue

        all_rates = list(trajs.values())
        min_len = min(len(r) for r in all_rates)
        all_rates_arr = np.array([r[:min_len] for r in all_rates])

        final_avg = np.mean([r[-1] for r in all_rates])
        final_std = np.std([r[-1] for r in all_rates])

        # 궤적이 크게 벗어난 학급
        for classroom, rates in trajs.items():
            final = rates[-1] if len(rates) > 0 else 0
            if final < final_avg - 1.5 * final_std and final_std > 0.05:
                insights.append(Insight(
                    insight_id=f"traj_{classroom}",
                    category="trajectory_divergence",
                    severity="warning",
                    title=f"{classroom} — {curr} 평균 대비 진도 이탈",
                    summary=(
                        f"최종 완료율 {final*100:.1f}%로, "
                        f"{curr} 평균({final_avg*100:.1f}%)보다 "
                        f"{(final_avg - final)*100:.1f}%p 낮습니다."
                    ),
                    evidence={
                        "classroom": classroom,
                        "curriculum": curr,
                        "final_rate": final,
                        "curr_avg": final_avg,
                        "gap": final_avg - final,
                    },
                    related_view="학습 흐름 비교",
                    related_filters={"classroom": classroom},
                    suggestions=[
                        f"{classroom} 교사 면담으로 진도 지연 원인 파악",
                        "보충 학습 시간 확보 또는 활동 수 조정 검토",
                    ],
                ))

    return insights


# ═══════════════════════════════════════════════════════
# 패턴 4: 위험 학급 식별
# ═══════════════════════════════════════════════════════

def _detect_at_risk_classrooms(summary_df: pd.DataFrame) -> list[Insight]:
    insights = []

    low_progress = summary_df[summary_df["avg_progress"] < 0.3]
    if len(low_progress) > 0:
        names = low_progress["classroom_name"].tolist()
        insights.append(Insight(
            insight_id="at_risk_classrooms",
            category="anomaly",
            severity="critical",
            title=f"진도율 30% 미만 학급 {len(low_progress)}개 발견",
            summary=f"즉각 개입이 필요한 학급: {', '.join(names[:5])}{'...' if len(names) > 5 else ''}",
            evidence={
                "classrooms": names,
                "count": len(low_progress),
                "avg_progress": low_progress["avg_progress"].mean(),
            },
            related_view="학교 비교",
            related_filters={},
            suggestions=[
                "해당 학급 교사와 진도 지연 원인 파악 면담",
                "수업 시간 내 활동 완료 가능 여부 점검",
                "보충 학습 시간 확보 또는 활동 수 조정",
            ],
        ))

    return insights


# ═══════════════════════════════════════════════════════
# 패턴 5: 활동 패턴 이상 감지
# ═══════════════════════════════════════════════════════

def _detect_activity_anomalies(
    activity_df: pd.DataFrame,
    summary_df: pd.DataFrame,
) -> list[Insight]:
    insights = []

    # 커리큘럼별 코딩 활동 비율 차이
    if "activitiable_type" not in activity_df.columns:
        return insights

    curriculum_map = dict(zip(summary_df["classroom_name"], summary_df["curriculum"]))
    activity_df_with_curr = activity_df.copy()
    if "classroom_name" in activity_df_with_curr.columns:
        activity_df_with_curr["curriculum"] = activity_df_with_curr["classroom_name"].map(curriculum_map)
    elif "curriculum" not in activity_df_with_curr.columns:
        return insights

    if "curriculum" in activity_df_with_curr.columns:
        for curr in activity_df_with_curr["curriculum"].dropna().unique():
            curr_data = activity_df_with_curr[activity_df_with_curr["curriculum"] == curr]
            coding = curr_data[curr_data["activitiable_type"] == "StudioActivity"]["count"].sum()
            total = curr_data["count"].sum()
            if total > 0:
                coding_pct = coding / total * 100
                if coding_pct < 10:
                    insights.append(Insight(
                        insight_id=f"activity_low_coding_{curr}",
                        category="anomaly",
                        severity="info",
                        title=f"{curr} — 코딩 활동 비율 낮음 ({coding_pct:.1f}%)",
                        summary=f"전체 활동 중 코딩(Studio) 비율이 {coding_pct:.1f}%로 낮습니다.",
                        evidence={"curriculum": curr, "coding_pct": coding_pct},
                        related_view="활동 패턴",
                        related_filters={"curriculum": curr},
                        suggestions=["코딩 활동 시간 추가 배정 검토"],
                    ))

    return insights


# ═══════════════════════════════════════════════════════
# LLM 내러티브 생성
# ═══════════════════════════════════════════════════════

def generate_llm_narrative(
    insights: list[Insight],
    api_key: Optional[str] = None,
    model: str = "gpt-4o-mini",
    provider: str = "openai",
) -> list[Insight]:
    """LLM으로 인사이트에 대한 자연어 해설 생성 (선택적)"""
    if not api_key:
        # LLM 없이 규칙 기반 내러티브 생성
        for ins in insights:
            ins.llm_narrative = _rule_based_narrative(ins)
        return insights

    # LLM API 호출
    prompt = _build_narrative_prompt(insights)

    try:
        if provider == "openai" and HAS_OPENAI:
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": (
                        "당신은 K-12 교육 데이터 분석 전문가입니다. "
                        "학습 데이터에서 발견된 패턴을 교사가 이해하기 쉬운 한국어로 설명해주세요. "
                        "각 인사이트에 대해 2-3문장으로 핵심을 전달하고, 구체적인 교수 전략을 제안하세요."
                    )},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=2000,
            )
            narratives = response.choices[0].message.content
        elif provider == "anthropic" and HAS_ANTHROPIC:
            client = anthropic.Anthropic(api_key=api_key)
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}],
                system=(
                    "당신은 K-12 교육 데이터 분석 전문가입니다. "
                    "학습 데이터에서 발견된 패턴을 교사가 이해하기 쉬운 한국어로 설명해주세요."
                ),
            )
            narratives = response.content[0].text
        else:
            for ins in insights:
                ins.llm_narrative = _rule_based_narrative(ins)
            return insights

        # 파싱: 간단히 번호로 매칭
        narrative_parts = narratives.split("\n\n")
        for i, ins in enumerate(insights):
            if i < len(narrative_parts):
                ins.llm_narrative = narrative_parts[i].strip()
            else:
                ins.llm_narrative = _rule_based_narrative(ins)

    except Exception:
        for ins in insights:
            ins.llm_narrative = _rule_based_narrative(ins)

    return insights


def _build_narrative_prompt(insights: list[Insight]) -> str:
    parts = ["아래 학습 데이터 인사이트 각각에 대해 교사를 위한 2-3문장 해설을 작성해주세요.\n"]
    for i, ins in enumerate(insights[:10]):
        parts.append(
            f"{i+1}. [{ins.category}] {ins.title}\n"
            f"   근거: {ins.summary}\n"
            f"   수치: {ins.evidence}\n"
        )
    return "\n".join(parts)


def _rule_based_narrative(ins: Insight) -> str:
    """LLM 없이 규칙 기반 내러티브 생성"""
    if ins.category == "cliff":
        if "worst_session" in ins.evidence:
            phase = ins.evidence.get("phase", "")
            return (
                f"⚠️ {ins.evidence.get('worst_session')}차시({phase} 단계)는 "
                f"가장 많은 학급이 어려움을 겪는 구간입니다. "
                f"이 차시의 학습 내용과 난이도를 점검하고, "
                f"필요 시 사전 준비 활동을 추가하는 것을 권장합니다."
            )
        else:
            return f"⚠️ {ins.title}. 해당 구간의 학습 활동 재설계를 검토하세요."

    elif ins.category == "competency_gap":
        return (
            f"📊 {ins.summary} "
            f"낮은 역량의 관련 활동을 보강하거나, "
            f"해당 역량에 집중하는 보충 차시를 마련하는 것을 고려하세요."
        )

    elif ins.category == "trajectory_divergence":
        return (
            f"📉 {ins.summary} "
            f"교사 면담을 통해 수업 운영 환경이나 학생 특성에 따른 원인을 파악하고, "
            f"맞춤형 지원 방안을 마련하세요."
        )

    elif ins.category == "anomaly":
        return f"🔍 {ins.summary}"

    return ins.summary


# ═══════════════════════════════════════════════════════
# 인사이트 요약 통계
# ═══════════════════════════════════════════════════════

def get_insight_summary(insights: list[Insight]) -> dict:
    """인사이트 요약 통계"""
    return {
        "total": len(insights),
        "critical": sum(1 for i in insights if i.severity == "critical"),
        "warning": sum(1 for i in insights if i.severity == "warning"),
        "info": sum(1 for i in insights if i.severity == "info"),
        "categories": list(set(i.category for i in insights)),
    }
