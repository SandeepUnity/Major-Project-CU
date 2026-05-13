"""Tests for small-talk routing (no RAG / no API keys required)."""

from src.core.small_talk import is_small_talk_message


def test_small_talk_greetings_and_identity():
    assert is_small_talk_message("Hi")
    assert is_small_talk_message("Hello!")
    assert is_small_talk_message("Hey")
    assert is_small_talk_message("How are you?")
    assert is_small_talk_message("Who are you")
    assert is_small_talk_message("What can you do?")
    assert is_small_talk_message("Hi there")
    assert is_small_talk_message("thank you")


def test_small_talk_not_substantive_queries():
    assert not is_small_talk_message("")
    assert not is_small_talk_message("how are your courses structured")
    assert not is_small_talk_message("who are the instructors")
    assert not is_small_talk_message("I need a refund for my payment")
