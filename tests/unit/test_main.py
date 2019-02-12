from collections import Counter
from unittest.mock import Mock, patch

from pytest import mark

from main import get_counter_from_file, main


@mark.parametrize(
    "text, sensitive, expected",
    [
        (b"Hello \n hello-hello", False, Counter({"hello": 3})),
        (b"Hello hello \n hello", True, Counter({"Hello": 1, "hello": 2})),
    ],
)
def test_get_counter_from_file(text, sensitive, expected):
    mock_get_file = Mock()
    patcher = patch("main.get_text_from_file", mock_get_file)
    mock_get_file.return_value = text
    with patcher:
        response = get_counter_from_file(
            "fake_file", "fake_bucket", sensitive=sensitive
        )
        assert response == expected


def test_main():
    def _mock_get_file(bucket_name, storage_file):
        return storage_file

    def _mock_create_response(bucket_name, files, words_counter, **kwargs):
        return words_counter

    mock_get_file = Mock()
    patcher_get_text = patch("main.get_text_from_file", mock_get_file)
    mock_get_file.side_effect = _mock_get_file
    mock_create_response = Mock()
    patcher_create_response = patch("main.create_response", mock_create_response)
    mock_create_response.side_effect = _mock_create_response
    files = [b"Hello hello", b"Hello by"]
    with patcher_get_text, patcher_create_response:
        response = main("fake_bucket", files)
    expected_counter = Counter({"hello": 3, "by": 1})
    mock_create_response.assert_called_with(
        "fake_bucket", files, expected_counter, pdf_output=False, store_csv=False
    )
