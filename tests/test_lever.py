import json
import datetime as dt
import pytest

from leveropen.lever import Lever
from leveropen.dataset import Dataset
from tests.utils_for_tests import ACCESS_TOKEN, BASE_URL, VERSION, DATA_FOLDER


def load_json(file_path: str):
    return json.load(
        open(
            file_path,
        )
    )


@pytest.fixture
def mock_datasets_response(mocker):
    resp = mocker.Mock()
    resp.status_code = 200
    resp.json.return_value = load_json(file_path=DATA_FOLDER / "datasets.json")
    return resp


@pytest.fixture
def mock_datasets(mocker):
    return [
        Dataset(
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
            client=mocker.Mock(),
        ),
        Dataset(
            uuid="b",
            name="Example dataset b",
            released_on=dt.datetime(2021, 2, 12, 0, 0),
            processed_on=dt.datetime(2021, 3, 5, 0, 0),
            collection="Another collection",
            topic="Economy",
            link="example-base-url/v1/datasets/b",
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
            series_url="example-base-url/v1/datasets/b/series?token=example-access-token",
            client=mocker.Mock(),
        ),
        Dataset(
            uuid="c",
            name="Example dataset c",
            released_on=dt.datetime(2021, 2, 12, 0, 0),
            processed_on=dt.datetime(2021, 3, 5, 0, 0),
            collection="Another collection",
            topic="Another topic",
            link="example-base-url/v1/datasets/c",
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
            series_url="example-base-url/v1/datasets/c/series?token=example-access-token",
            client=mocker.Mock(),
        ),
    ]


@pytest.fixture
def mock_lever(mocker, mock_datasets_response):
    mocker.patch(
        "leveropen.protocol.Protocol.get",
        return_value=mock_datasets_response,
    )
    mocker.patch("leveropen.protocol.Protocol.get_session", return_value=mocker.Mock())
    return Lever(access_token=ACCESS_TOKEN, base_url=BASE_URL, version=VERSION)


def test_get_all_datasets(mock_lever, mock_datasets):
    datasets = mock_lever.get_all_datasets()
    assert datasets == mock_datasets


def test_get_datasets_by_collection(mock_lever, mock_datasets):
    actual = mock_lever.get_datasets_by_collection(collection="Any")
    assert actual == mock_datasets


def test_get_datasets_by_topic(mock_lever, mock_datasets):
    actual = mock_lever.get_datasets_by_topic(topic="Any")
    assert actual == mock_datasets


def test_get_datasets_by_name(mock_lever, mock_datasets):
    actual = mock_lever.get_datasets_by_name(name="Any")
    assert actual == mock_datasets


def test_get_datasets_by(mock_lever, mock_datasets):
    with pytest.raises(AssertionError):
        mock_lever._get_datasets_by(by="incorrect", query="Any")
    for by_option in ["name", "collection", "topic"]:
        actual = mock_lever._get_datasets_by(by=by_option, query="Another collection")
        assert actual == mock_datasets


def test__parse_datasets(mock_lever, mock_datasets):
    datasets = [
        dict(
            uuid="a",
            name="Monthly GDP and main sectors, chained volume indices of gross value added",
            released_on="2021-02-12",
            processed_on="2021-03-05",
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
            series="example-base-url/v1/datasets/a/series?token=example-access-token"
        )
    ]
    actual = mock_lever._parse_datasets(datasets=datasets)
    expected = [mock_datasets[0]]
    assert actual == expected
