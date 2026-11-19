from __future__ import annotations

from .contract import Row, apply_rows, flag, index_rows, integer, read_rows, text


def transform(row: Row) -> Row:
    """分固定方式和位置计算试拆完整率，对无试拆分组不作外推。"""
    census = {}
    for group in read_rows(row, "census"):
        key = (text(group, "fastener"), text(group, "position"))
        if key in census:
            raise ValueError("duplicate census group")
        census[key] = integer(group, "population")
    counts = {key: [0, 0] for key in census}
    for panel in index_rows(read_rows(row, "trials"), "panel").values():
        key = (text(panel, "fastener"), text(panel, "position"))
        if key not in census:
            raise ValueError("trial outside census groups")
        before = flag(panel, "intact_before")
        after = flag(panel, "intact_after")
        counts[key][0] += 1
        counts[key][1] += before and after
    result = []
    for (fastener, position), pop in sorted(census.items()):
        tested, intact = counts[fastener, position]
        if tested > pop:
            raise ValueError("trials exceed census population")
        result.append(dict(fastener=fastener, position=position, population=pop, tested=tested,
                           intact_recovered=intact, observed_rate=intact / tested if tested else None))
    return {"strata": result}


def build_facts(data: Row) -> list[Row]:
    return apply_rows(data, transform)
