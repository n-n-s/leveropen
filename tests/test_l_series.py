import json
import pytest
import pandas as pd

from leveropen.l_series import LSeries
from tests.utils_for_tests import DATA_FOLDER


@pytest.fixture
def mock_response(mocker):
    f = open(
        DATA_FOLDER / "series_data.json",
    )
    data = json.load(f)
    f.close()
    resp = mocker.Mock()
    resp.json.return_value = data
    return resp


@pytest.fixture
def mock_lseries(mocker, mock_response):
    client = mocker.Mock()
    client.host_url = "example-base-url/v1/"
    client.get.return_value = mock_response
    return LSeries(
        uuid="saa",
        name="UK, Seasonally adjusted, Monthly GDP",
        units="Count",
        magnitude=1,
        link="example-base-url/v1/datasets/a/series/saa?token=example-access-token",
        date_time={"name": "Month", "range": ["January 1997", "December 2020"]},
        location={"type": "Country", "name": "UK"},
        categories=[
            {"type": "Adjustment", "name": "Seasonally adjusted"},
            {"type": "Total", "name": "Monthly GDP"},
        ],
        client=client,
    )


def test_get_categories(mock_lseries):
    actual = mock_lseries.get_categories()
    expected = pd.DataFrame(
        data={
            "type": ["Adjustment", "Total"],
            "name": ["Seasonally adjusted", "Monthly GDP"],
        }
    )
    pd.testing.assert_frame_equal(actual, expected)


def test_get_data(mock_lseries):
    actual = mock_lseries.get_data()
    expected = pd.read_csv(
        DATA_FOLDER / "series_data.csv",
        index_col=0,
        parse_dates=True,
        dtype={
            "Value": float,
            "DateTime": object,
            "SeriesName": object,
            "Country": object,
        },
    )
    expected["DateFrom"] = pd.to_datetime(expected["DateFrom"])
    expected["DateTo"] = pd.to_datetime(expected["DateTo"])
    pd.testing.assert_frame_equal(actual, expected)
