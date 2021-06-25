import pytest
import requests
from leveropen.protocol import Protocol
from leveropen.api_errors import APIError
from tests.utils_for_tests import ACCESS_TOKEN, BASE_URL, VERSION


@pytest.fixture
def mock_response(mocker):
    return mocker.Mock()


@pytest.fixture
def mock_protocol(mocker):
    def get_resp(url: str, params: dict = None):
        resp = mocker.Mock()
        resp.status_code = 200
        resp.url = url
        if params:
            params_list = []
            for count, (k, v) in enumerate(params.items()):
                if count == 0:
                    first_char = "?"
                else:
                    first_char = "&"
                params_list.append(first_char + k + "=" + str(v))
            resp.url = resp.url + "".join(params_list)
        return resp

    mocker.patch("requests.get", get_resp)
    return Protocol(access_token=ACCESS_TOKEN, base_url=BASE_URL, version=VERSION)


def test_host_url(mock_protocol):
    assert mock_protocol.host_url == BASE_URL + VERSION + "/"


def test_get_session(mock_protocol):
    session = mock_protocol.get_session(ACCESS_TOKEN)
    assert isinstance(session, requests.Session)
    assert session.params == {"token": ACCESS_TOKEN}


def test__validate_response(mock_protocol, mock_response):
    mock_response.status_code = 404
    with pytest.raises(APIError):
        mock_protocol._validate_response(mock_response)
    mock_response.status_code = 200
    assert mock_response == mock_protocol._validate_response(mock_response)


def test_get(mock_protocol, mock_response):
    # Without params
    resp = mock_protocol.get("any url")
    expected = mock_response
    expected.status_code = 200
    expected.url = BASE_URL + VERSION + "/any url?token=" + ACCESS_TOKEN
    assert resp.status_code == expected.status_code
    assert resp.url == expected.url
    # With params
    resp = mock_protocol.get("any url", params={"page": 1})
    expected = mock_response
    expected.status_code = 200
    expected.url = BASE_URL + VERSION + "/any url?token=" + ACCESS_TOKEN + "&page=1"
    assert resp.status_code == expected.status_code
    assert resp.url == expected.url
