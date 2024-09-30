import pytest
from backend.logic.gemini import Gemini

@pytest.fixture
def gemini():
    return Gemini()

def test_start_chat(gemini):
    result = gemini.start_chat()
    assert result is not None

# def test_send_message(gemini):
#     message = "Hello, how's the weather today?"
#     result = gemini.send_message(message)
#     assert isinstance(result, str)