"""Tests for broad-topic query expansion (no API keys required)."""

from src.core.query_expander import expand_query, is_broad_topic_query


def test_expand_courses_overview():
    assert is_broad_topic_query("Tell me about the courses")
    expanded = expand_query("Tell me about the courses")
    assert expanded[0] == "Tell me about the courses"
    assert len(expanded) == 2
    assert "bootcamp" in expanded[1].lower()


def test_expand_enrollment_overview():
    assert is_broad_topic_query("Tell me about enrollment")
    assert len(expand_query("Tell me about enrollment")) == 2


def test_expand_technical_support_overview():
    assert is_broad_topic_query("Tell me about technical support")
    assert len(expand_query("Tell me about technical support")) == 2


def test_no_expand_specific_questions():
    assert not is_broad_topic_query("How do I enroll in a course?")
    assert expand_query("How do I enroll in a course?") == ["How do I enroll in a course?"]


def test_expand_what_courses_offer():
    assert is_broad_topic_query("What courses do you offer?")
    assert len(expand_query("What courses do you offer?")) == 2
