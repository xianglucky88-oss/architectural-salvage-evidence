"""建筑拆解与构件再用数据"""

from . import assembly_origin, clear_lengths, trial_recovery, layer_certificates, grille_pairing
from .contract import Row

PIPELINES = {
    "assembly-origin": assembly_origin.build_facts,
    "clear-lengths": clear_lengths.build_facts,
    "trial-recovery": trial_recovery.build_facts,
    "layer-certificates": layer_certificates.build_facts,
    "grille-pairing": grille_pairing.build_facts,
}

def process(pipeline: str, data: Row) -> list[Row]:
    """Validate and transform an independent input dataset into keyed facts."""
    if pipeline not in PIPELINES:
        raise ValueError(f"unknown pipeline: {pipeline}")
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    return PIPELINES[pipeline](data)
