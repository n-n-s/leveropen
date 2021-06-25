import pytest

from leveropen.api_errors import APIError


@pytest.fixture
def mock_response(mocker):
    return mocker.Mock()


def test_api_error(mock_response):
    mock_response.status_code = 404
    mock_response.json.return_value = {"Status": "Test"}

    def raise_error(resp):
        raise APIError(resp)

    with pytest.raises(APIError) as exc_info:
        raise_error(mock_response)
    exception_raised = exc_info.value
    info = (
        "See https://www.leveropen.com for information on "
        "how to obtain your personal Access Token."
    )
    resp_detail = "Response 404: {'Status': 'Test'}"
    assert exception_raised.info == info
    assert exception_raised.args[0] == f"{info}\n{resp_detail}"
