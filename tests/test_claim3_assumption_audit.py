from src.claim3_assumption_audit import audit


def test_clean_union_of_subspaces_satisfies_the_finite_checks():
    result = audit()["finite_clean_room_example"]
    assert result["assumption_checks"] == {
        "union_support": True,
        "zero_intersection_mass": True,
        "subgaussian_mgf_le_two": True,
    }


def test_intersection_mass_negative_control_fails_only_separation():
    control = audit()["negative_control_intersection_mass"]
    assert control["still_subgaussian"] is True
    assert control["zero_intersection_mass"] is False
    assert control["intersection_mass"] > 0
