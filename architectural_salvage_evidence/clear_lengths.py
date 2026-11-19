from __future__ import annotations

from .contract import Row, apply_rows, integer, merge_spans, read_rows, span


def transform(row: Row) -> Row:
    """从构件轴向范围扣除已知损伤和未测范围，交付确认连续可用的长度。"""
    length = integer(row, "length_mm", minimum=1)
    damage = [span(x, "start_mm", "end_mm") for x in read_rows(row, "damage")]
    unknown = [span(x, "start_mm", "end_mm") for x in read_rows(row, "uninspected")]
    excluded = merge_spans(damage + unknown)
    if excluded and excluded[-1][1] > length:
        raise ValueError("excluded span beyond component")
    result = []
    last = 0
    for a, b in excluded + [(length, length)]:
        if a > last:
            result.append([last, a])
        last = b
    return {"clear_spans_mm": result, "longest_clear_mm": max((b - a for a, b in result), default=0),
            "uninspected_mm": [list(pair) for pair in merge_spans(unknown)]}


def build_facts(data: Row) -> list[Row]:
    return apply_rows(data, transform)
