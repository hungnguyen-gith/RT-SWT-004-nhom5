#!/usr/bin/env python3
"""
calculate_iaa.py — Tinh Inter-Annotator Agreement (IAA) cho ground truth
Du an: Evaluating GPT-4o mini Zero-Shot for Unit Test Generation (Nhom 5)

Vai tro: DG (Data & Ground Truth)
Khop voi proposal.md SS5.4 / SS7.1 Threat 2:
    - Metric chinh: Cohen's Kappa (2 annotators)
    - Nguong bat buoc: Kappa >= 0.7 truoc khi dung ground truth
    - Neu Kappa < 0.7 va co annotator thu 3 (tiebreaker) -> tinh them Fleiss' Kappa

CACH DUNG
---------
    python calculate_iaa.py data/pilot_ground_truth.csv
    python calculate_iaa.py data/full_ground_truth.csv --threshold 0.7
    python calculate_iaa.py data/pilot_ground_truth.csv --weighted linear   # neu label la thang do (vd 1-5)

INPUT FORMAT (CSV, wide format)
--------------------------------
    function_id,annotator_1,annotator_2,annotator_3
    java_001,valid,valid,
    java_002,invalid,valid,invalid
    py_001,valid,valid,

    - Cot dau tien: id cua function/test (bat ky ten cot nao, script se tu nhan dien cot dau)
    - Cac cot con lai: moi cot la nhan cua 1 annotator
    - annotator_3 co the de trong neu chua co tiebreaker (pilot thuong chi co 2 nguoi)
    - Nhan (label) co the la text ("valid"/"invalid") hoac so (thang Likert)

OUTPUT
------
    - In report ra terminal: Cohen's Kappa (tung cap), % agreement, Fleiss' Kappa (neu >=3 annotator)
    - Bao PASS/FAIL theo nguong du an (mac dinh 0.7)
    - Luu report vao results/iaa_report_<ten_file>.txt
"""

import argparse
import itertools
import os
import sys

import numpy as np
import pandas as pd
from sklearn.metrics import cohen_kappa_score

# ---------------------------------------------------------------------------
# Diễn giải mức độ đồng thuận (Landis & Koch, 1977) — dùng để đọc kết quả
# ---------------------------------------------------------------------------
LANDIS_KOCH = [
    (0.00, "Poor (khong dong thuan)"),
    (0.20, "Slight"),
    (0.40, "Fair"),
    (0.60, "Moderate"),
    (0.80, "Substantial"),
    (1.01, "Almost Perfect"),
]


def interpret_kappa(k: float) -> str:
    for upper, label in LANDIS_KOCH:
        if k < upper:
            return label
    return "Almost Perfect"


def percent_agreement(a: pd.Series, b: pd.Series) -> float:
    mask = a.notna() & b.notna()
    if mask.sum() == 0:
        return float("nan")
    return float((a[mask] == b[mask]).mean())


def fleiss_kappa(rating_matrix: np.ndarray) -> float:
    """
    Fleiss' Kappa cho >=3 annotators, nhan dang phan loai.
    rating_matrix: shape (n_items, n_categories) — moi o la so annotator gan category do cho item.
    """
    n_items, n_categories = rating_matrix.shape
    n_raters = rating_matrix.sum(axis=1)
    if not np.allclose(n_raters, n_raters[0]):
        raise ValueError("Fleiss' Kappa can moi item co cung so annotator gan nhan (khong missing).")
    n = n_raters[0]

    # P_i: muc do dong thuan tren tung item
    P_i = (np.sum(rating_matrix ** 2, axis=1) - n) / (n * (n - 1))
    P_bar = P_i.mean()

    # p_j: ty le trung binh moi category duoc chon tren toan bo
    p_j = rating_matrix.sum(axis=0) / (n_items * n)
    P_bar_e = np.sum(p_j ** 2)

    if P_bar_e == 1:
        return 1.0
    return (P_bar - P_bar_e) / (1 - P_bar_e)


def build_rating_matrix(df: pd.DataFrame, rater_cols: list) -> tuple:
    """Chuyen wide-format labels sang ma tran dem (item x category) cho Fleiss' Kappa."""
    categories = sorted(pd.unique(df[rater_cols].values.ravel()))
    categories = [c for c in categories if pd.notna(c)]
    cat_index = {c: i for i, c in enumerate(categories)}

    matrix = np.zeros((len(df), len(categories)), dtype=int)
    for row_idx, (_, row) in enumerate(df.iterrows()):
        for col in rater_cols:
            val = row[col]
            if pd.notna(val):
                matrix[row_idx, cat_index[val]] += 1
    return matrix, categories


# Cot metadata cua function (KHONG phai annotator) — gop ca 2 schema da gap trong du an:
# schema 1 (crawl + Lizard): func_id, source_repo, file, nloc, params, start_line, end_line, raw_source_path
# schema 2 (functions_input.csv): function_id, cc_band, cc_value, source_code
METADATA_COLS = {
    "func_id", "function_id", "language", "source_repo", "file", "func_name",
    "cc", "cc_band", "cc_value", "nloc", "params", "start_line", "end_line",
    "raw_source_path", "source_code",
}
# Cot phu tro, khong phai raw annotation cua 1 nguoi cu the
NON_RATER_COLS = {"final_label", "notes"}


def detect_rater_cols(df: pd.DataFrame) -> list:
    """Tu dong nhan dien cot annotator: khong phai metadata, khong phai final_label/notes,
    va co it nhat 1 gia tri (khong rong hoan toan)."""
    candidates = [c for c in df.columns if c not in METADATA_COLS and c not in NON_RATER_COLS]
    return [c for c in candidates if df[c].notna().any()]


def run_report(path: str, threshold: float, weighted: str | None) -> str:
    df = pd.read_csv(path)
    id_col = "func_id" if "func_id" in df.columns else ("function_id" if "function_id" in df.columns else df.columns[0])
    rater_cols = detect_rater_cols(df)

    if len(rater_cols) == 0:
        raise ValueError(
            f"Khong tim thay cot annotator nao co du lieu trong {os.path.basename(path)}.\n"
            f"  -> File nay chua duoc gan nhan (annotator_dg / annotator_rw con rong).\n"
            f"  -> DG + RW can dien nhan doc lap truoc, sau do chay lai script nay."
        )
    if len(rater_cols) < 2:
        raise ValueError(f"Can it nhat 2 annotator co du lieu de tinh IAA. Tim thay: {rater_cols}")

    lines = []
    lines.append("=" * 70)
    lines.append(f"IAA REPORT — {os.path.basename(path)}")
    lines.append(f"So items: {len(df)} | Annotators: {rater_cols}")
    lines.append(f"Nguong du an (proposal SS5.4): Kappa >= {threshold}")
    lines.append("=" * 70)

    # --- Cohen's Kappa cho tung cap annotator ---
    lines.append("\n[1] Cohen's Kappa (pairwise)")
    pair_kappas = []
    for a, b in itertools.combinations(rater_cols, 2):
        mask = df[a].notna() & df[b].notna()
        if mask.sum() == 0:
            continue
        kw = {"weights": weighted} if weighted else {}
        k = cohen_kappa_score(df.loc[mask, a], df.loc[mask, b], **kw)
        agree = percent_agreement(df[a], df[b])
        pair_kappas.append(k)
        status = "PASS" if k >= threshold else "FAIL"
        lines.append(
            f"  {a} vs {b}: Kappa = {k:.3f} ({interpret_kappa(k)}) | "
            f"%% agreement = {agree:.1%} | [{status}]"
        )

    primary_kappa = pair_kappas[0] if pair_kappas else float("nan")

    # --- Fleiss' Kappa neu >= 3 annotator va khong missing ---
    if len(rater_cols) >= 3:
        full_mask = df[rater_cols].notna().all(axis=1)
        if full_mask.sum() > 0:
            matrix, categories = build_rating_matrix(df.loc[full_mask], rater_cols)
            fk = fleiss_kappa(matrix)
            lines.append(f"\n[2] Fleiss' Kappa ({len(rater_cols)} annotators, n={full_mask.sum()} items day du)")
            lines.append(f"  Categories: {categories}")
            status = "PASS" if fk >= threshold else "FAIL"
            lines.append(f"  Fleiss' Kappa = {fk:.3f} ({interpret_kappa(fk)}) | [{status}]")

    # --- Ket luan + hanh dong tiep theo (khop quy trinh proposal SS7.1 / Threat 2) ---
    lines.append("\n[3] Ket luan")
    if primary_kappa >= threshold:
        lines.append(f"  ✅ PASS — Kappa = {primary_kappa:.3f} >= {threshold}. Dung ground truth nay de chay tiep pipeline.")
    else:
        lines.append(f"  ❌ FAIL — Kappa = {primary_kappa:.3f} < {threshold}.")
        lines.append("  Theo proposal SS7.1 Threat 2: dung lai, lam ro guideline gan nhan,")
        lines.append("  gan lai cac item conflicting truoc khi chay LLM. Neu van khong dat,")
        lines.append("  them annotator thu 3 lam tiebreaker roi tinh lai Fleiss' Kappa.")
        # Chi ra cac item bi conflict de gan lai nhanh
        if len(rater_cols) == 2:
            a, b = rater_cols
            conflicts = df[(df[a].notna()) & (df[b].notna()) & (df[a] != df[b])]
            if len(conflicts):
                lines.append(f"\n  Cac item conflicting ({len(conflicts)}/{len(df)}):")
                lines.append("  " + conflicts[[id_col, a, b]].to_string(index=False).replace("\n", "\n  "))

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Tinh IAA (Cohen's Kappa / Fleiss' Kappa) cho ground truth annotation.")
    parser.add_argument("csv_path", help="Duong dan file CSV (vd: data/pilot_ground_truth.csv)")
    parser.add_argument("--threshold", type=float, default=0.7, help="Nguong Kappa (mac dinh 0.7, theo proposal SS5.4)")
    parser.add_argument(
        "--weighted",
        choices=["linear", "quadratic"],
        default=None,
        help="Dung weighted kappa neu nhan la thang do thu tu (vd Likert 1-5). Bo trong neu nhan la categorical (valid/invalid).",
    )
    parser.add_argument("--out", default=None, help="Duong dan luu report (mac dinh: results/iaa_report_<ten_file>.txt)")
    args = parser.parse_args()

    if not os.path.exists(args.csv_path):
        print(f"Khong tim thay file: {args.csv_path}", file=sys.stderr)
        sys.exit(1)

    try:
        report = run_report(args.csv_path, args.threshold, args.weighted)
    except ValueError as e:
        print(f"\n⚠️  {e}\n", file=sys.stderr)
        sys.exit(1)
    print(report)

    out_path = args.out or os.path.join(
        "results", f"iaa_report_{os.path.splitext(os.path.basename(args.csv_path))[0]}.txt"
    )
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\n[Da luu report vao {out_path}]")


if __name__ == "__main__":
    main()
