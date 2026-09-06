"""ESM-C subprocess entrypoint, isolated from fair-esm's package namespace."""

import json
from pathlib import Path
import sys

import numpy as np

from .runtime import RuntimeConfig, Substitution, _score_esmc_native


def main():
    request = json.loads(Path(sys.argv[1]).read_text())
    variants = tuple(
        tuple(Substitution(**mutation) for mutation in variant)
        for variant in request["variants"]
    )
    scores = _score_esmc_native(
        request["reference"], variants, RuntimeConfig(**request["config"])
    )
    np.save(sys.argv[2], scores, allow_pickle=False)


if __name__ == "__main__":
    main()
