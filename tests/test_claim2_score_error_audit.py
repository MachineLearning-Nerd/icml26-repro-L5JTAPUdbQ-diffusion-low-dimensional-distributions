from src.claim2_score_error_audit import run, score_factor


def test_k_uses_intrinsic_dimension_with_floor_two():
    assert score_factor(1, t=0.5, sigma=1.5) == score_factor(2, t=0.5, sigma=1.5)
    assert score_factor(3, t=0.5, sigma=1.5) > score_factor(2, t=0.5, sigma=1.5)


def test_ambient_substitution_is_rejected():
    result = run()
    assert result["ambient_substitution_ratio"] > 1_000
    assert result["verdict"] == "verified_scoped"
