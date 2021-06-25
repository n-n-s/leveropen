import datetime as dt
import pytest
import pandas as pd

from leveropen.dataset import Dataset
from leveropen.l_series import LSeries


@pytest.fixture
def mock_client(mocker):
    return mocker.Mock()


@pytest.fixture
def mock_series(mock_client):
    return [
        LSeries(
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
            client=mock_client,
        ),
        LSeries(
            uuid="sab",
            name="UK, Seasonally adjusted, Services",
            units="Count",
            magnitude=1,
            link="example-base-url/v1/datasets/a/series/sab?token=example-access-token",
            date_time={"name": "Month", "range": ["January 1997", "December 2020"]},
            location={"type": "Country", "name": "UK"},
            categories=[
                {"type": "Sector", "name": "Services"},
                {"type": "Adjustment", "name": "Seasonally adjusted"},
            ],
            client=mock_client,
        ),
    ]


def _get_series_response(self):
    return [
        {
            "uuid": "saa",
            "name": "UK, Seasonally adjusted, Monthly GDP",
            "units": "Count",
            "magnitude": 1,
            "link": "example-base-url/v1/datasets/a/series/saa?token=example-access-token",
            "datetime": {
                "name": "Month",
                "range": ["January 1997", "December 2020"],
            },
            "location": {"type": "Country", "name": "UK"},
            "categories": [
                {"type": "Adjustment", "name": "Seasonally adjusted"},
                {"type": "Total", "name": "Monthly GDP"},
            ],
        },
        {
            "uuid": "sab",
            "name": "UK, Seasonally adjusted, Services",
            "units": "Count",
            "magnitude": 1,
            "link": "example-base-url/v1/datasets/a/series/sab?token=example-access-token",
            "datetime": {
                "name": "Month",
                "range": ["January 1997", "December 2020"],
            },
            "location": {"type": "Country", "name": "UK"},
            "categories": [
                {"type": "Sector", "name": "Services"},
                {"type": "Adjustment", "name": "Seasonally adjusted"},
            ],
        },
    ]


@pytest.fixture
def mock_dataset(mocker, mock_client):
    mocker.patch("leveropen.dataset.Dataset._get_series_by_url", _get_series_response)
    return Dataset(
        uuid="a",
        name="Monthly GDP and main sectors, chained volume indices of gross value added",
        released_on=dt.datetime(2021, 2, 12, 0, 0),
        processed_on=dt.datetime(2021, 3, 5, 0, 0),
        collection="Gross Domestic Product (GDP)",
        topic="Economy",
        link="example-base-url/v1/datasets/a",
        license={
            "name": "Open Government Licence v3.0",
            "url": "http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
        },
        datetimes=[{"name": "Month", "range": ["January 1997", "December 2020"]}],
        locations=[{"type": "Country", "name": "UK"}],
        categories=[
            {"type": "Sector", "name": "Construction"},
            {"type": "Sector", "name": "Services"},
        ],
        series_url="example-base-url/v1/datasets/a/series?token=example-access-token",
        client=mock_client,
    )


@pytest.fixture
def matching_series(mocker):
    series = mocker.Mock()
    series.uuid = "matching-uuid"
    series.name = "matching-name"
    return [series, series]


def test_get_metadata(mock_dataset):
    actual = mock_dataset.get_metadata()
    expected = pd.Series(
        dict(
            name="Monthly GDP and main sectors, chained volume indices of gross value added",
            topic="Economy",
            collection="Gross Domestic Product (GDP)",
            released_on=dt.datetime(2021, 2, 12, 0, 0, 0),
            processed_on=dt.datetime(2021, 3, 5, 0, 0, 0),
            link="example-base-url/v1/datasets/a",
            license_name="Open Government Licence v3.0",
            license_url="http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
            series_names_and_uuids=pd.DataFrame(
                data={
                    "name": [
                        "UK, Seasonally adjusted, Monthly GDP",
                        "UK, Seasonally adjusted, Services",
                    ],
                    "uuid": ["saa", "sab"],
                }
            ),
            categories=pd.DataFrame(
                data={
                    "type": ["Sector", "Sector"],
                    "name": ["Construction", "Services"],
                }
            ),
        ),
        name="a",
    )
    pd.testing.assert_series_equal(actual, expected)


def test_get_categories(mock_dataset):
    actual = mock_dataset.get_categories()
    expected = pd.DataFrame(
        data={"type": ["Sector", "Sector"], "name": ["Construction", "Services"]}
    )
    pd.testing.assert_frame_equal(actual, expected)


def test_get_series(mock_dataset, mock_series):
    actual = mock_dataset.get_series()
    expected = mock_series
    assert actual == expected


def test_get_series_names_and_uuids(mock_dataset):
    actual = mock_dataset.get_series_names_and_uuids()
    expected = pd.DataFrame(
        {
            "name": [
                "UK, Seasonally adjusted, Monthly GDP",
                "UK, Seasonally adjusted, Services",
            ],
            "uuid": ["saa", "sab"],
        }
    )
    pd.testing.assert_frame_equal(actual, expected)


def test_get_series_by_name(mock_dataset, mock_series, matching_series):
    actual = mock_dataset.get_series_by_name(name="UK, Seasonally adjusted, Services")
    expected = mock_series[1]
    assert actual == expected
    with pytest.raises(ValueError):
        mock_dataset.get_series_by_name(name="not a name")
    with pytest.raises(ValueError):
        mock_dataset.series = matching_series
        mock_dataset.get_series_by_name(name="matching-name")


def test_get_series_by_uuid(mock_dataset, mock_series, matching_series):
    actual = mock_dataset.get_series_by_uuid(uuid="saa")
    expected = mock_series[0]
    assert actual == expected
    with pytest.raises(ValueError):
        mock_dataset.get_series_by_uuid(uuid="not a uuid")
    with pytest.raises(ValueError):
        mock_dataset.series = matching_series
        mock_dataset.get_series_by_uuid(uuid="matching-uuid")


def test_get_series_by_name_containing(mock_dataset, mock_series):
    actual = mock_dataset.get_series_by_name_containing(name_containing_string="GDP")
    expected = [mock_series[0]]
    assert actual == expected
    actual = mock_dataset.get_series_by_name_containing(
        name_containing_string="Services"
    )
    expected = [mock_series[1]]
    assert actual == expected
    actual = mock_dataset.get_series_by_name_containing(name_containing_string="Season")
    expected = mock_series
    assert actual == expected
