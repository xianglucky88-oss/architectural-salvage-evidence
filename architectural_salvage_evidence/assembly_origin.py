from __future__ import annotations

from .contract import Row, apply_rows, index_rows, read_rows, text


def transform(row: Row) -> Row:
    """区分原装构件、可用替代候选和没有位置证据的拆出件。"""
    slots = index_rows(read_rows(row, "slots"), "slot")
    originals = {}
    loose = {}
    for part, item in index_rows(read_rows(row, "recovered"), "part").items():
        spec = text(item, "spec")
        slot = item["original_slot"]
        if slot is None:
            loose[part] = spec
        else:
            slot = text(item, "original_slot")
            if slot not in slots or slot in originals:
                raise ValueError("unknown or repeated original slot")
            originals[slot] = part
    return {"original_parts": originals, "missing_slots": sorted(slots.keys() - originals.keys()),
            "substitution_candidates": {slot: sorted(p for p, spec in loose.items() if spec == text(slots[slot], "spec"))
                                        for slot in sorted(slots.keys() - originals.keys())},
            "unknown_original_slots": sorted(loose)}


def build_facts(data: Row) -> list[Row]:
    return apply_rows(data, transform)
