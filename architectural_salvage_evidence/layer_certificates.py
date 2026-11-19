from __future__ import annotations

from .contract import Row, apply_rows, index_rows, read_rows, text


def transform(row: Row) -> Row:
    """只把材质检测结论附给取样构件的对应层材。"""
    by_layer = {}
    for report, sample in index_rows(read_rows(row, "tests"), "report").items():
        key = (text(sample, "panel"), text(sample, "layer"))
        by_layer.setdefault(key, []).append({"report": report, "material": text(sample, "material")})
    result = {}
    for piece, layer in index_rows(read_rows(row, "recovered_layers"), "piece").items():
        key = (text(layer, "panel"), text(layer, "layer"))
        evidence = by_layer.get(key, [])
        materials = {x["material"] for x in evidence}
        result[piece] = dict(status="unproven" if not evidence else "supported" if len(materials) == 1 else "disputed", evidence=evidence)
    return {"layer_claims": result}


def build_facts(data: Row) -> list[Row]:
    return apply_rows(data, transform)
