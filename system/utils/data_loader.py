"""CodleViz 데이터 로더 — K-12 코들 학습 데이터"""
import pandas as pd
import numpy as np
from pathlib import Path
from functools import lru_cache

DATA_DIR = Path(__file__).parent.parent.parent / "data" / "dashboard"

# 역량 컬러 매핑
COMPETENCY_COLORS = {
    "DC": "#3B82F6",  # 데이터 이해 (Blue)
    "DA": "#10B981",  # 데이터 분석 (Green)
    "DV": "#F59E0B",  # 데이터 시각화 (Amber)
    "DI": "#8B5CF6",  # 데이터 해석 (Violet)
    "CT": "#EF4444",  # 컴퓨팅 사고 (Red)
}

COMPETENCY_NAMES_KR = {
    "DC": "데이터 이해",
    "DA": "데이터 분석",
    "DV": "데이터 시각화",
    "DI": "데이터 해석",
    "CT": "컴퓨팅 사고",
}

COMPETENCY_NAMES_EN = {
    "DC": "Data Comprehension",
    "DA": "Data Analysis",
    "DV": "Data Visualization",
    "DI": "Data Interpretation",
    "CT": "Computational Thinking",
}

CURRICULUM_COLORS = {
    "해양쓰레기": "#3B82F6",
    "기후변화": "#10B981",
    "식량안보": "#F59E0B",
}


@lru_cache(maxsize=1)
def load_school_summary() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "school_summary.csv")


@lru_cache(maxsize=1)
def load_competency_scores() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "competency_scores.csv")


@lru_cache(maxsize=1)
def load_session_progress() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "session_progress.csv")


@lru_cache(maxsize=1)
def load_student_heatmap() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "student_heatmap.csv")


@lru_cache(maxsize=1)
def load_all_students() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "all_students.csv")


@lru_cache(maxsize=1)
def load_activity_types() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "activity_types.csv")


@lru_cache(maxsize=1)
def load_studio_progress() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "studio_progress.csv")


def get_school_list() -> list[str]:
    df = load_school_summary()
    return sorted(df["school"].unique().tolist())


def get_classroom_list(school: str = None) -> list[str]:
    df = load_school_summary()
    if school:
        df = df[df["school"] == school]
    return sorted(df["classroom_name"].tolist())


def get_curriculum_list() -> list[str]:
    df = load_school_summary()
    return sorted(df["curriculum"].unique().tolist())


def get_school_stats() -> dict:
    """전체 사업 요약 통계"""
    summary = load_school_summary()
    return {
        "n_schools": summary["school"].nunique(),
        "n_classrooms": len(summary),
        "n_students": summary["n_students"].sum(),
        "n_paired": summary["n_paired"].sum(),
        "n_curricula": summary["curriculum"].nunique(),
        "avg_progress": summary["avg_progress"].mean(),
        "curricula": summary["curriculum"].unique().tolist(),
    }


def get_competency_for_classroom(classroom_name: str) -> pd.DataFrame:
    """특정 학급의 역량별 점수"""
    df = load_competency_scores()
    return df[df["classroom_name"] == classroom_name].copy()


def get_session_for_classroom(classroom_name: str) -> pd.DataFrame:
    """특정 학급의 세션별 진도"""
    df = load_session_progress()
    return df[df["classroom_name"] == classroom_name].copy()


def get_heatmap_for_classroom(classroom_name: str) -> pd.DataFrame:
    """특정 학급의 학생별 히트맵 데이터"""
    df = load_student_heatmap()
    return df[df["classroom_name"] == classroom_name].copy()
