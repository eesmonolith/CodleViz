"""
CodleViz XAI Engine — SHAP-based Cliff Explanation
===================================================
Trains an XGBoost model to predict progress-drop ("cliff") events,
then uses SHAP to explain *why* each cliff occurred.

Pipeline:
  1. extract_cliff_features()  → classroom×session feature matrix
  2. train_cliff_model()       → XGBoost + SHAP values
  3. get_cliff_explanation()   → top-k factors for a specific cliff
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional

try:
    import xgboost as xgb
    import shap
    HAS_XAI = True
except ImportError:
    HAS_XAI = False


# ── Feature column definitions ──────────────────────────

FEATURE_COLS = [
    "session_num",
    "phase",
    "is_phase_transition",
    "prev_completion",
    "prior_trend",
    "n_activities",
    "n_students",
    "coding_ratio",
    "passive_ratio",
    "pct_StudioActivity",
    "pct_VideoActivity",
    "pct_PdfActivity",
    "pct_QuizActivity",
    "pct_CodapActivity",
    "pct_BoardActivity",
    "pct_SheetActivity",
    "completion_std",
    "completion_min",
    "pct_below_30",
]

FEATURE_NAMES_EN = {
    "session_num": "Session Number",
    "phase": "Learning Phase",
    "is_phase_transition": "Phase Transition",
    "prev_completion": "Prior Completion Rate",
    "prior_trend": "Prior 3-Session Trend",
    "n_activities": "Activity Count",
    "n_students": "Student Count",
    "coding_ratio": "Coding Activity Ratio",
    "passive_ratio": "Passive Content Ratio (PDF+Video)",
    "pct_StudioActivity": "Studio (Coding) %",
    "pct_VideoActivity": "Video %",
    "pct_PdfActivity": "PDF %",
    "pct_QuizActivity": "Quiz %",
    "pct_CodapActivity": "CODAP %",
    "pct_BoardActivity": "Board %",
    "pct_SheetActivity": "Sheet %",
    "completion_std": "Student Completion Spread",
    "completion_min": "Lowest Student Completion",
    "pct_below_30": "% Students Below 30%",
}

FEATURE_NAMES_KR = {
    "session_num": "차시 번호",
    "phase": "학습 단계",
    "is_phase_transition": "단계 전환 여부",
    "prev_completion": "이전 차시 완료율",
    "prior_trend": "이전 3차시 추세",
    "n_activities": "활동 수",
    "n_students": "학생 수",
    "coding_ratio": "코딩 활동 비율",
    "passive_ratio": "수동 콘텐츠 비율 (PDF+영상)",
    "pct_StudioActivity": "코딩(Studio) 비율",
    "pct_VideoActivity": "영상 비율",
    "pct_PdfActivity": "PDF 비율",
    "pct_QuizActivity": "퀴즈 비율",
    "pct_CodapActivity": "CODAP 비율",
    "pct_BoardActivity": "게시판 비율",
    "pct_SheetActivity": "시트 비율",
    "completion_std": "학생 간 완료율 편차",
    "completion_min": "최저 학생 완료율",
    "pct_below_30": "30% 미만 학생 비율",
}


# ── 1. Feature Extraction ───────────────────────────────

def _session_to_phase(s: float) -> int:
    if s <= 3:
        return 1
    elif s <= 7:
        return 2
    elif s <= 11:
        return 3
    return 4


def extract_cliff_features(
    all_students_df: pd.DataFrame,
    session_progress_df: pd.DataFrame,
    student_heatmap_df: pd.DataFrame,
) -> pd.DataFrame:
    """Build feature matrix: one row per (classroom, session-transition)."""

    records: list[dict] = []

    for classroom in session_progress_df["classroom_name"].unique():
        # Session-level progress
        cls_sess = (
            session_progress_df[session_progress_df["classroom_name"] == classroom]
            .sort_values("session")
        )
        rates = cls_sess["completion_rate"].values
        sessions = cls_sess["session"].values

        # Student-level activity breakdown
        cls_all = (
            all_students_df[all_students_df["classroom_name"] == classroom]
            if all_students_df is not None else None
        )
        cls_heat = student_heatmap_df[
            student_heatmap_df["classroom_name"] == classroom
        ]

        for i in range(1, len(rates)):
            sess = sessions[i]
            prev_sess = sessions[i - 1]
            drop = rates[i] - rates[i - 1]

            feat: dict = {
                "classroom_name": classroom,
                "session": sess,
                "drop": drop,
                "cliff_label": int(drop < -0.15),
            }

            # --- numeric features ---
            feat["session_num"] = sess
            feat["phase"] = _session_to_phase(sess)
            feat["is_phase_transition"] = int(
                _session_to_phase(sess) != _session_to_phase(prev_sess)
            )
            feat["prev_completion"] = rates[i - 1]

            # Prior 3-session trend (slope)
            if i >= 3:
                window = rates[i - 3 : i]
                feat["prior_trend"] = float(
                    np.polyfit(range(len(window)), window, 1)[0]
                )
            else:
                feat["prior_trend"] = 0.0

            # Session row stats
            sess_row = cls_sess[cls_sess["session"] == sess]
            if len(sess_row) > 0:
                feat["n_activities"] = int(sess_row["n_activities"].values[0])
                feat["n_students"] = int(sess_row["n_students"].values[0])
            else:
                feat["n_activities"] = 0
                feat["n_students"] = 0

            # --- Activity type composition ---
            act_types = [
                "StudioActivity", "VideoActivity", "PdfActivity",
                "QuizActivity", "CodapActivity", "BoardActivity",
                "SheetActivity", "EmbeddedActivity",
            ]
            if cls_all is not None:
                sa = cls_all[cls_all["session"] == sess]
                total = len(sa)
                if total > 0:
                    vc = sa["activitiable_type"].value_counts()
                    for at in act_types:
                        feat[f"pct_{at}"] = vc.get(at, 0) / total
                    coding_n = vc.get("StudioActivity", 0) + vc.get("CodapActivity", 0)
                    passive_n = vc.get("PdfActivity", 0) + vc.get("VideoActivity", 0)
                    feat["coding_ratio"] = coding_n / total
                    feat["passive_ratio"] = passive_n / total
                else:
                    for at in act_types:
                        feat[f"pct_{at}"] = 0.0
                    feat["coding_ratio"] = 0.0
                    feat["passive_ratio"] = 0.0
            else:
                for at in act_types:
                    feat[f"pct_{at}"] = 0.0
                feat["coding_ratio"] = 0.0
                feat["passive_ratio"] = 0.0

            # --- Student-level dispersion ---
            sh = cls_heat[cls_heat["session"] == sess]
            if len(sh) > 1:
                feat["completion_std"] = float(sh["avg_progress"].std())
                feat["completion_min"] = float(sh["avg_progress"].min())
                feat["pct_below_30"] = float((sh["avg_progress"] < 0.3).mean())
            else:
                feat["completion_std"] = 0.0
                feat["completion_min"] = 0.0
                feat["pct_below_30"] = 0.0

            records.append(feat)

    return pd.DataFrame(records)


# ── 2. Model Training ───────────────────────────────────

def train_cliff_model(
    features_df: pd.DataFrame,
    threshold: float = 0.15,
) -> dict:
    """
    Train XGBoost and compute SHAP values.

    Returns dict with keys:
        model, explainer, shap_values, X, feature_cols, features_df
    Returns {"error": msg} if training is impossible.
    """
    if not HAS_XAI:
        return {"error": "xgboost/shap not installed"}

    df = features_df.copy()
    available = [c for c in FEATURE_COLS if c in df.columns]
    X = df[available].fillna(0).astype(float)
    y = (df["drop"] < -threshold).astype(int)

    if y.sum() < 3 or (1 - y).sum() < 3:
        return {"error": f"Too few cliff events ({y.sum()}) for training"}

    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1,
        min_child_weight=3,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        eval_metric="logloss",
        verbosity=0,
    )
    model.fit(X, y)

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)

    df["cliff_prob"] = model.predict_proba(X)[:, 1]

    return {
        "model": model,
        "explainer": explainer,
        "shap_values": shap_values,
        "X": X,
        "feature_cols": available,
        "features_df": df,
    }


# ── 3. Per-cliff Explanation ────────────────────────────

def get_cliff_explanation(
    result: dict,
    classroom: str,
    session: float,
    lang: str = "en",
    top_k: int = 6,
) -> List[Dict]:
    """
    Return top-k SHAP factors for a specific classroom×session cliff.

    Each item: {feature, feature_key, value, shap_value, direction}
    """
    if "error" in result:
        return []

    df = result["features_df"]
    sv = result["shap_values"]
    X = result["X"]
    cols = result["feature_cols"]
    names = FEATURE_NAMES_EN if lang == "en" else FEATURE_NAMES_KR

    mask = (df["classroom_name"] == classroom) & (df["session"] == session)
    idx_list = df.index[mask]
    if len(idx_list) == 0:
        return []

    # Position within the array (not DataFrame index)
    pos = df.index.get_loc(idx_list[0])
    if isinstance(pos, slice):
        pos = pos.start

    row_shap = sv[pos]
    row_vals = X.iloc[pos]

    top_idx = np.argsort(np.abs(row_shap))[::-1][:top_k]

    explanations = []
    for i in top_idx:
        col = cols[i]
        s = float(row_shap[i])
        explanations.append({
            "feature": names.get(col, col),
            "feature_key": col,
            "value": float(row_vals.iloc[i]),
            "shap_value": s,
            "direction": "risk" if s > 0 else "protective",
        })
    return explanations


# ── 4. Global feature importance ────────────────────────

def get_global_importance(result: dict, lang: str = "en", top_k: int = 8) -> List[Dict]:
    """Return globally most important features (mean |SHAP|)."""
    if "error" in result:
        return []

    sv = result["shap_values"]
    cols = result["feature_cols"]
    names = FEATURE_NAMES_EN if lang == "en" else FEATURE_NAMES_KR

    mean_abs = np.abs(sv).mean(axis=0)
    top_idx = np.argsort(mean_abs)[::-1][:top_k]

    return [
        {"feature": names.get(cols[i], cols[i]),
         "feature_key": cols[i],
         "importance": float(mean_abs[i])}
        for i in top_idx
    ]


# ── 5. Model performance summary ────────────────────────

def get_model_summary(result: dict) -> dict:
    """Return accuracy, AUC, and cliff count."""
    if "error" in result:
        return {"error": result["error"]}

    from sklearn.metrics import accuracy_score, roc_auc_score

    df = result["features_df"]
    model = result["model"]
    X = result["X"]
    y_true = (df["drop"] < -0.15).astype(int)
    y_pred = model.predict(X)
    y_prob = model.predict_proba(X)[:, 1]

    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "auc": float(roc_auc_score(y_true, y_prob)),
        "n_samples": len(y_true),
        "n_cliffs": int(y_true.sum()),
        "n_features": len(result["feature_cols"]),
    }
