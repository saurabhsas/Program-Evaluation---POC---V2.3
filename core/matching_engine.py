import pandas as pd
import numpy as np


def prepare_pairs(g1, g2):

    g1 = g1[["MEMBER_UCI", "MATCH_SCORE", "LOB", "MEMBER_ID"]].drop_duplicates()
    g2 = g2[["MEMBER_UCI", "MATCH_SCORE", "LOB", "MEMBER_ID"]].drop_duplicates()

    g1["MATCH_SCORE"] = pd.to_numeric(g1["MATCH_SCORE"], errors="coerce")
    g2["MATCH_SCORE"] = pd.to_numeric(g2["MATCH_SCORE"], errors="coerce")

    g1 = g1.dropna(subset=["MATCH_SCORE"])
    g2 = g2.dropna(subset=["MATCH_SCORE"])

    g1["key"] = 1
    g2["key"] = 1

    pairs = g1.merge(g2, on="key", suffixes=("_G1", "_G2")).drop("key", axis=1)

    pairs["diff"] = np.abs(pairs["MATCH_SCORE_G1"] - pairs["MATCH_SCORE_G2"])

    pairs = pairs[pairs["LOB_G1"] == pairs["LOB_G2"]]

    return pairs.sort_values("diff")


def match_with_caliper(pairs, used_g1, used_g2, caliper):

    matches = []

    for _, row in pairs.iterrows():

        if caliper is not None and row["diff"] > caliper:
            continue

        g1 = row["MEMBER_UCI_G1"]
        g2 = row["MEMBER_UCI_G2"]

        if g1 not in used_g1 and g2 not in used_g2:

            matches.append({
                "G1_MEMBER_ID": str(row["MEMBER_ID_G1"]),
                "G2_MEMBER_ID": str(row["MEMBER_ID_G2"]),
                "diff": row["diff"],
                "caliper_used": str(caliper) if caliper else "no_caliper"
            })

            used_g1.add(g1)
            used_g2.add(g2)

    return matches


def multi_caliper_matching(g1, g2):

    pairs = prepare_pairs(g1, g2)

    used_g1 = set()
    used_g2 = set()
    all_matches = []

    calipers = [1e-5, 1e-4, 1e-3, 0.02, None]

    for cal in calipers:
        new = match_with_caliper(pairs, used_g1, used_g2, cal)
        all_matches.extend(new)
        print(f"Caliper {cal}: {len(new)} matches")

    return pd.DataFrame(all_matches)