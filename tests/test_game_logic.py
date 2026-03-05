import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from logic_utils import check_guess, get_range_for_difficulty, update_score, parse_guess


# --- check_guess: hints were swapped (bug: Too High said "Go HIGHER", Too Low said "Go LOWER") ---

def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high_outcome():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low_outcome():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

def test_guess_too_high_says_go_lower():
    # Bug fix: guessing too high should tell you to go LOWER, not HIGHER
    _, message = check_guess(60, 50)
    assert "LOWER" in message

def test_guess_too_low_says_go_higher():
    # Bug fix: guessing too low should tell you to go HIGHER, not LOWER
    _, message = check_guess(40, 50)
    assert "HIGHER" in message


# --- get_range_for_difficulty: Normal and Hard ranges were swapped ---

def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20

def test_normal_range():
    # Bug fix: Normal was incorrectly returning 1-100 (that's Hard's range)
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 50

def test_hard_range():
    # Bug fix: Hard was incorrectly returning 1-50 (that's Normal's range)
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 100


# --- update_score: wrong guesses were subtracting points, causing negative scores ---

def test_wrong_guess_does_not_change_score():
    # Bug fix: "Too High" was adding/subtracting 5 depending on attempt parity
    assert update_score(0, "Too High", 1) == 0
    assert update_score(0, "Too High", 2) == 0

def test_too_low_does_not_subtract_points():
    # Bug fix: "Too Low" was always subtracting 5
    assert update_score(0, "Too Low", 1) == 0

def test_score_never_goes_negative():
    score = 0
    for attempt in range(1, 9):
        score = update_score(score, "Too Low", attempt)
    assert score >= 0

def test_win_increases_score():
    score = update_score(0, "Win", 1)
    assert score > 0

def test_win_score_decreases_with_more_attempts():
    early_win = update_score(0, "Win", 1)
    late_win = update_score(0, "Win", 7)
    assert early_win > late_win

def test_win_score_minimum_is_10():
    # Even on a very late attempt, score added should be at least 10
    score = update_score(0, "Win", 100)
    assert score >= 10


# --- parse_guess: basic input validation ---

def test_parse_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_empty_string():
    ok, value, _ = parse_guess("")
    assert ok is False
    assert value is None

def test_parse_non_numeric():
    ok, value, _ = parse_guess("abc")
    assert ok is False
    assert value is None

def test_parse_decimal_truncates():
    ok, value, _ = parse_guess("7.9")
    assert ok is True
    assert value == 7
