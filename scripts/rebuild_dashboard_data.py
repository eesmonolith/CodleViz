"""
CodleViz dashboard 데이터 재생성 스크립트
원본: MM/class csv/*.csv → CodleViz/data/dashboard/
3개 커리큘럼 포함: 해양쓰레기, 기후변화, 식량안보
"""
from __future__ import annotations

import pandas as pd
import numpy as np
import os
import re
from pathlib import Path
from typing import Optional

RAW_DIR = Path(__file__).resolve().parent.parent.parent / "MM" / "class csv"
OUT_DIR = Path(__file__).resolve().parent.parent / "data" / "dashboard"

CURRICULA = ["해양쓰레기", "기후변화", "식량안보"]
CURRICULA_PATTERN = "|".join(CURRICULA)

COMPETENCY_MAP = {
    1: "DC", 2: "DC", 3: "DC",
    4: "DA", 5: "DA", 6: "DA", 7: "DA",
    8: "CT", 9: "CT", 10: "CT",
    11: "DI", 12: "DI", 13: "DI", 14: "DV",
    15: "DI",
}


def extract_session(material_name: str) -> int | None:
    if pd.isna(material_name):
        return None
    m = re.search(r"(\d{1,2})(?:차시|\s)", str(material_name))
    if m:
        return int(m.group(1))
    m = re.search(r"\]\s*(\d{1,2})\s", str(material_name))
    if m:
        return int(m.group(1))
    return None


def load_raw_data() -> pd.DataFrame:
    """MM/class csv/ 의 모든 CSV를 합쳐서 3개 커리큘럼 학생 데이터 반환"""
    dfs = []
    for f in sorted(RAW_DIR.glob("*.csv")):
        print(f"  읽는 중: {f.name}")
        dfs.append(pd.read_csv(f, low_memory=False))
    all_df = pd.concat(dfs, ignore_index=True)
    print(f"  전체 행: {len(all_df):,}건")

    # 3개 커리큘럼 필터
    mask = all_df["classroom_name"].str.contains(CURRICULA_PATTERN, na=False)
    df = all_df[mask & (all_df["is_student"] == 1)].copy()
    print(f"  학생 이벤트 (3개 커리큘럼): {len(df):,}건")

    # 커리큘럼 추출
    def get_curriculum(name):
        name = str(name)
        for c in CURRICULA:
            if c in name:
                return c
        return "기타"

    df["curriculum"] = df["classroom_name"].apply(get_curriculum)

    # 학교명 추출 (커리큘럼 이름 제거)
    df["school"] = df["classroom_name"].str.replace(
        r"\s*(" + CURRICULA_PATTERN + r")$", "", regex=True
    )

    df["session"] = df["material_name"].apply(extract_session)
    df["competency"] = df["session"].map(COMPETENCY_MAP)

    return df


def build_school_summary(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for school_class in df["classroom_name"].unique():
        s = df[df["classroom_name"] == school_class]
        school = s["school"].iloc[0]
        curriculum = s["curriculum"].iloc[0]
        n_students = s["profile_id"].nunique() if "profile_id" in s.columns else s["user_id"].nunique()

        uid_col = "profile_id" if "profile_id" in s.columns else "user_id"

        pre_ids = set()
        post_ids = set()
        if "activity_name" in s.columns:
            pre_mask = s["activity_name"].str.contains("사전", na=False) & (s["progress"] == 1.0)
            pre_ids = set(s[pre_mask][uid_col])
            post_mask = s["activity_name"].str.contains("사후", na=False) & (s["progress"] == 1.0)
            post_ids = set(s[post_mask][uid_col])

        paired = len(pre_ids & post_ids)

        sess_data = s[s["session"].notna()]
        avg_progress = sess_data["progress"].mean() if len(sess_data) > 0 else 0
        sessions_covered = sess_data["session"].nunique()

        rows.append({
            "classroom_name": school_class,
            "school": school,
            "curriculum": curriculum,
            "n_students": n_students,
            "n_pre": len(pre_ids),
            "n_post": len(post_ids),
            "n_paired": paired,
            "avg_progress": avg_progress,
            "sessions_covered": sessions_covered,
        })

    return pd.DataFrame(rows).sort_values("n_paired", ascending=False)


def build_session_progress(df: pd.DataFrame) -> pd.DataFrame:
    sess = df[df["session"].notna() & (df["session"] >= 1) & (df["session"] <= 15)]
    uid_col = "profile_id" if "profile_id" in df.columns else "user_id"
    result = (
        sess.groupby(["classroom_name", "session"])
        .agg(
            avg_progress=("progress", "mean"),
            n_activities=("progress", "count"),
            n_completed=("progress", lambda x: (x == 1.0).sum()),
            n_students=(uid_col, "nunique"),
        )
        .reset_index()
    )
    result["completion_rate"] = result["n_completed"] / result["n_activities"]
    return result


def build_competency_scores(df: pd.DataFrame) -> pd.DataFrame:
    sess = df[df["competency"].notna()]
    uid_col = "profile_id" if "profile_id" in df.columns else "user_id"
    result = (
        sess.groupby(["classroom_name", "competency"])
        .agg(
            avg_progress=("progress", "mean"),
            n_activities=("progress", "count"),
            n_students=(uid_col, "nunique"),
        )
        .reset_index()
    )
    return result


def build_student_heatmap(df: pd.DataFrame) -> pd.DataFrame:
    sess = df[df["session"].notna() & (df["session"] >= 1) & (df["session"] <= 15)]
    uid_col = "profile_id" if "profile_id" in df.columns else "user_id"
    result = (
        sess.groupby(["classroom_name", uid_col, "session"])
        .agg(avg_progress=("progress", "mean"), n_activities=("progress", "count"))
        .reset_index()
    )
    if uid_col != "profile_id":
        result = result.rename(columns={uid_col: "profile_id"})
    return result


def build_activity_type_by_session(df: pd.DataFrame) -> pd.DataFrame:
    sess = df[df["session"].notna()]
    if "activitiable_type" not in sess.columns:
        # event_type을 대신 사용
        type_col = "event_type" if "event_type" in sess.columns else None
        if type_col is None:
            return pd.DataFrame(columns=["curriculum", "session", "activitiable_type", "count"])
        result = (
            sess.groupby(["curriculum", "session", type_col])
            .size()
            .reset_index(name="count")
        )
        result = result.rename(columns={type_col: "activitiable_type"})
    else:
        result = (
            sess.groupby(["curriculum", "session", "activitiable_type"])
            .size()
            .reset_index(name="count")
        )
    return result


def build_studio_progress(df: pd.DataFrame) -> pd.DataFrame:
    type_col = "activitiable_type" if "activitiable_type" in df.columns else "event_type"
    studio_val = "StudioActivity" if "activitiable_type" in df.columns else "studio"
    uid_col = "profile_id" if "profile_id" in df.columns else "user_id"

    studio = df[(df[type_col] == studio_val) & df["session"].notna()]
    if len(studio) == 0:
        return pd.DataFrame(columns=["classroom_name", "session", "avg_progress", "n_activities", "n_students"])

    result = (
        studio.groupby(["classroom_name", "session"])
        .agg(
            avg_progress=("progress", "mean"),
            n_activities=("progress", "count"),
            n_students=(uid_col, "nunique"),
        )
        .reset_index()
    )
    return result


def anonymize(df: pd.DataFrame) -> pd.DataFrame:
    """학교명과 학생 ID를 익명화"""
    # 학교명 익명화: 고유 학교명 → School_01, School_02, ...
    unique_schools = sorted(df["school"].unique())
    school_map = {name: f"School_{i+1:02d}" for i, name in enumerate(unique_schools)}
    df["school"] = df["school"].map(school_map)

    # classroom_name 익명화: "장기중학교 해양쓰레기" → "School_01 해양쓰레기"
    def anon_classroom(name):
        name = str(name)
        for orig, anon in school_map.items():
            if orig in name:
                return name.replace(orig, anon)
        return name

    df["classroom_name"] = df["classroom_name"].apply(anon_classroom)

    # profile_id 익명화: 순차 ID
    uid_col = "profile_id" if "profile_id" in df.columns else "user_id"
    unique_ids = sorted(df[uid_col].unique())
    id_map = {orig: f"S{i+1:04d}" for i, orig in enumerate(unique_ids)}
    df[uid_col] = df[uid_col].map(id_map)

    print(f"  익명화 완료: {len(school_map)}개 학교, {len(id_map)}명 학생")
    return df


def main():
    print("=== CodleViz Dashboard 데이터 재생성 ===\n")
    print("원본 데이터 로딩...")
    df = load_raw_data()

    uid_col = "profile_id" if "profile_id" in df.columns else "user_id"
    print(f"\n  학교: {df['classroom_name'].nunique()}개")
    print(f"  학생: {df[uid_col].nunique()}명")
    print(f"  커리큘럼: {df['curriculum'].unique().tolist()}")
    for c in CURRICULA:
        n = len(df[df["curriculum"] == c])
        nc = df[df["curriculum"] == c]["classroom_name"].nunique()
        print(f"    {c}: {n:,}건, {nc}개 학급")

    print("\n익명화 처리...")
    df = anonymize(df)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print("\n학교별 요약...")
    school_summary = build_school_summary(df)
    school_summary.to_csv(OUT_DIR / "school_summary.csv", index=False)
    print(f"  → {len(school_summary)}개 학급")

    print("차시별 완료율...")
    session_progress = build_session_progress(df)
    session_progress.to_csv(OUT_DIR / "session_progress.csv", index=False)

    print("역량별 점수...")
    competency_scores = build_competency_scores(df)
    competency_scores.to_csv(OUT_DIR / "competency_scores.csv", index=False)

    print("학생 히트맵...")
    student_heatmap = build_student_heatmap(df)
    student_heatmap.to_csv(OUT_DIR / "student_heatmap.csv", index=False)

    print("활동 유형 분포...")
    activity_types = build_activity_type_by_session(df)
    activity_types.to_csv(OUT_DIR / "activity_types.csv", index=False)

    print("Studio 진행률...")
    studio_progress = build_studio_progress(df)
    studio_progress.to_csv(OUT_DIR / "studio_progress.csv", index=False)

    print("원본 데이터 저장...")
    df.to_csv(OUT_DIR / "all_students.csv", index=False)

    print(f"\n완료! 출력: {OUT_DIR}")
    print(f"커리큘럼별 학급 수:")
    for c in CURRICULA:
        n = len(school_summary[school_summary["curriculum"] == c])
        print(f"  {c}: {n}개")


if __name__ == "__main__":
    main()
