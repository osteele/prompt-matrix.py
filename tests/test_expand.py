import prompt_matrix


def test_expand():
    results = prompt_matrix.expand("The <dog|cat> in the <cardigan|hat>")
    assert len(results) == 4
    assert "The dog in the cardigan" in results
    assert "The dog in the hat" in results
    assert "The cat in the cardigan" in results
    assert "The cat in the hat" in results


def test_expand_nested():
    results = prompt_matrix.expand(
        "The <<small|large> <brown|black> dog|<red|blue> fish>"
    )
    assert len(results) == 6
    assert "The small brown dog" in results
    assert "The small black dog" in results
    assert "The large brown dog" in results
    assert "The large black dog" in results
    assert "The red fish" in results
    assert "The blue fish" in results


def test_expand_with_keywords():
    results = prompt_matrix.expand(
        "The {dog,cat} in the {cardigan,hat}", brackets=["{", "}"], alt=","
    )
    assert "The dog in the cardigan" in results
    assert "The dog in the hat" in results
    assert "The cat in the cardigan" in results
    assert "The cat in the hat" in results
