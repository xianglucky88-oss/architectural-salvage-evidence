from __future__ import annotations

from .contract import Row, apply_rows, choice, index_rows, integer, read_rows, text


def transform(row: Row) -> Row:
    """将可相接且侧面做法相同的左右格栅配对，不重复使用构件。"""
    groups = {}
    for piece, item in index_rows(read_rows(row, "grilles"), "piece").items():
        key = (text(item, "connector"), integer(item, "joint_mm"), text(item, "finish"))
        sides = groups.setdefault(key, {"left": [], "right": []})
        sides[choice(item, "side", {"left", "right"})].append(piece)
    pairs = []
    unmatched = {}
    for sides in groups.values():
        left, right = sorted(sides["left"]), sorted(sides["right"])
        pairs.extend([a, b] for a, b in zip(left, right))
        for side, opposite, label in ((left, right, "right"), (right, left, "left")):
            has_any_opposite = any(group[label] for group in groups.values())
            reason = "quantity" if opposite or not has_any_opposite else "interface"
            unmatched.update({piece: reason for piece in side[len(opposite):]})
    return {"pairs": sorted(pairs), "unmatched": unmatched}


def build_facts(data: Row) -> list[Row]:
    return apply_rows(data, transform)
