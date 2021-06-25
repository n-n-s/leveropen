import pandas as pd
from leveropen.utils import parse_categories


def test_parse_categories():
    categories = [
        {"type": "a type", "name": "a name"},
        {"type": "another type", "name": "another name"},
    ]
    actual = parse_categories(categories)
    expected = pd.DataFrame(
        data={"type": ["a type", "another type"], "name": ["a name", "another name"]}
    )
    pd.testing.assert_frame_equal(actual, expected)
