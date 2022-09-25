import pytest
from main import main
import filecmp

def cmp_res(r1, r2):
    for s1, s2 in zip(r1, r2):
        if s1.strip() != s2.strip():
            return False
    return True

@pytest.mark.parametrize(
    "input,output",
    [
        ("test1_input.txt", "test1_output.txt"),
        ("test2_input.txt", "test2_output.txt"),
    ]
)
def test_main(input,output):
    main(input)
    with open("output.txt", "r", encoding="utf-8") as f:
        res1 = f.readlines()
    with open(output, "r", encoding="utf-8") as f:
        res2 = f.readlines()
    assert cmp_res(res1, res2)