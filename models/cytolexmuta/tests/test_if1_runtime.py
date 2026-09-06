import pytest

torch = pytest.importorskip("torch")

from proteingym.models.cytolexmuta.runtime import RuntimeConfig, score_esm_if1
from torch_scatter import scatter


@pytest.mark.parametrize(
    ("reduction", "expected"),
    [("sum", [4.0, 2.0]), ("mean", [2.0, 2.0]), ("max", [3.0, 2.0])],
)
def test_fair_esm_scatter_interface(reduction, expected):
    result = scatter(
        torch.tensor([1.0, 3.0, 2.0]),
        torch.tensor([0, 0, 1]),
        reduce=reduction,
    )
    torch.testing.assert_close(result, torch.tensor(expected))


def test_if1_imports_before_reading_structure(tmp_path):
    # No model is loaded: a missing PDB must reach the structure loader,
    # not fail first on the torch_scatter or biotite compatibility imports.
    with pytest.raises(FileNotFoundError):
        score_esm_if1(["ACDE"], "ACDE", tmp_path / "missing.pdb", "A", RuntimeConfig())
