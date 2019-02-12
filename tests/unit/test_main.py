from collections import Counter
from pytest import mark
from unittest.mock import patch
from main import get_counter_from_file


@mark.parametrize('text, sensitive, expected', [
    (b'Hola \n hola-hola', False, Counter({'hola': 3})),
    (b'Hola hola \n hola', True, Counter({'Hola': 1, 'hola': 2}))
])
def test_get_counter_from_file(text, sensitive, expected, mock_get_file):
    patcher = patch('main.get_text_from_file', mock_get_file)
    mock_get_file.return_value = text
    with patcher:
        response = get_counter_from_file('fake_file', 'fake_bucket',
                                         sensitive=sensitive)
        assert response == expected
