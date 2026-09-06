import json
import os
import sys
from pathlib import Path

import numpy as np
import pytest

from proteingym.models.cytolexmuta import runtime


@pytest.mark.parametrize("output", [[0.0, -1.5], [float("nan"), 1.0], [1.0]])
def test_esmc_worker_isolated_and_validated(tmp_path, monkeypatch, output):
    source = tmp_path / "biohub-esm"
    model = source / "esm/models/esmc/model.py"
    model.parent.mkdir(parents=True)
    model.touch()
    monkeypatch.setenv("CYTOLEXMUTA_ESMC_REPO", str(source))
    variants = ((), (runtime.Substitution("C", 2, "F"),))
    config = runtime.RuntimeConfig(device="cuda")

    def worker(command, *, env, check):
        assert command[:3] == [
            sys.executable,
            "-m",
            "proteingym.models.cytolexmuta.esmc_worker",
        ]
        assert env["PYTHONPATH"].split(os.pathsep)[0] == str(source)
        assert check is True
        request = json.loads(Path(command[3]).read_text())
        assert request["reference"] == "ACDE"
        assert request["variants"] == [[], [{"wt": "C", "position": 2, "mutant": "F"}]]
        assert request["config"]["device"] == "cuda"
        assert set(request) == {"reference", "variants", "config"}
        np.save(command[4], np.asarray(output))

    monkeypatch.setattr(runtime.subprocess, "run", worker)
    if len(output) != 2 or not np.isfinite(output).all():
        with pytest.raises(ValueError, match="invalid ESM-C worker output"):
            runtime.score_esmc("ACDE", variants, config)
    else:
        assert np.array_equal(runtime.score_esmc("ACDE", variants, config), output)


def test_esmc_requires_native_source(tmp_path, monkeypatch):
    monkeypatch.setenv("CYTOLEXMUTA_ESMC_REPO", str(tmp_path))
    with pytest.raises(FileNotFoundError, match="Biohub ESM-C source"):
        runtime.score_esmc(
            "ACDE",
            ((runtime.Substitution("C", 2, "F"),),),
            runtime.RuntimeConfig(),
        )
