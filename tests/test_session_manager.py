import pytest
from src.session_manager import SessionManager

MAX_SESSIONS = 1000


def create_dummy_sessions(manager, count):
    """Helper that creates *count* dummy sessions and returns the list of generated ids."""
    ids = []
    for i in range(count):
        # session_data can be anything; we just use a simple dict with an index
        session_data = {"index": i}
        session_id = manager.create_session(session_data)
        ids.append(session_id)
    return ids


def test_fix_original_bug():
    """should fix the original bug"""
    manager = SessionManager()
    # Create more than the max allowed sessions to trigger eviction
    created_ids = create_dummy_sessions(manager, MAX_SESSIONS + 500)

    # The internal dictionary should never exceed MAX_SESSIONS
    assert len(manager.sessions) <= MAX_SESSIONS

    # The oldest session (the first one we created) must have been evicted
    oldest_id = created_ids[0]
    assert oldest_id not in manager.sessions

    # A newer session (e.g., the 100th) should still be present
    still_present_id = created_ids[100]
    assert still_present_id in manager.sessions


def test_edge_case_max_sessions():
    """should handle edge case X"""
    manager = SessionManager()
    created_ids = create_dummy_sessions(manager, MAX_SESSIONS)

    # Exactly MAX_SESSIONS entries should be stored – no eviction yet
    assert len(manager.sessions) == MAX_SESSIONS
    for sid in created_ids:
        assert sid in manager.sessions


def test_no_regression_basic_functionality():
    """should not regress on Y"""
    manager = SessionManager()
    session_data = {"user": "alice", "role": "admin"}
    session_id = manager.create_session(session_data)

    # The returned id must be present in the internal store and map to the original data
    assert session_id in manager.sessions
    assert manager.sessions[session_id] == session_data


def test_error_case_invalid_input():
    """should handle error case Z"""
    manager = SessionManager()
    # Passing None as session data – the manager should still store the entry (no crash)
    session_id = manager.create_session(None)
    assert session_id in manager.sessions
    assert manager.sessions[session_id] is None
