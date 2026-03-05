"""Logic utilities for the Number Guessing Game.

This module contains core game logic functions including difficulty management,
guess validation, guess checking, and score calculation for the number guessing
game application.
"""


def get_range_for_difficulty(difficulty: str) -> tuple[int, int]:
    """Get the number range for a given difficulty level.

    Determines the minimum and maximum values for the guessing range based
    on the selected difficulty. Higher difficulties have wider ranges.

    Args:
        difficulty: The difficulty level ('Easy', 'Normal', or 'Hard').

    Returns:
        A tuple containing (min_value, max_value) for the difficulty:
            - Easy: (1, 20)
            - Normal: (1, 50)
            - Hard: (1, 100)
            - Default: (1, 50)

    Examples:
        >>> get_range_for_difficulty('Easy')
        (1, 20)
        >>> get_range_for_difficulty('Hard')
        (1, 100)
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 50


def parse_guess(raw: str) -> tuple[bool, int | None, str | None]:
    """Parse and validate user input into an integer guess.

    Converts string input into an integer, handling edge cases like empty
    strings, None values, and decimal numbers. Provides descriptive error
    messages when parsing fails.

    Args:
        raw: The raw string input from the user.

    Returns:
        A tuple containing:
            - success (bool): True if parsing succeeded, False otherwise.
            - guess (int | None): The parsed integer value, or None if failed.
            - error_message (str | None): Error description if failed, None if
              succeeded.

    Examples:
        >>> parse_guess("42")
        (True, 42, None)
        >>> parse_guess("42.7")
        (True, 42, None)
        >>> parse_guess("")
        (False, None, 'Enter a guess.')
        >>> parse_guess("abc")
        (False, None, 'That is not a number.')
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def is_in_range(guess: int, low: int, high: int) -> bool:
    """Check if a guess falls within the valid range.

    Validates that the guessed number is within the inclusive range defined
    by the difficulty level's minimum and maximum values.

    Args:
        guess: The number to validate.
        low: Minimum allowed value (inclusive).
        high: Maximum allowed value (inclusive).

    Returns:
        True if the guess is within the valid range [low, high], False
        otherwise.

    Examples:
        >>> is_in_range(25, 1, 50)
        True
        >>> is_in_range(75, 1, 50)
        False
        >>> is_in_range(1, 1, 50)
        True
        >>> is_in_range(50, 1, 50)
        True
    """
    return low <= guess <= high


def check_guess(guess: int, secret: int) -> tuple[str, str]:
    """Compare a guess against the secret number and provide feedback.

    Evaluates whether the player's guess is correct, too high, or too low,
    and returns both a status outcome and a user-friendly message with emoji.

    Args:
        guess: The player's guessed number.
        secret: The secret number to match.

    Returns:
        A tuple containing:
            - outcome (str): The result status ('Win', 'Too High', or
              'Too Low').
            - message (str): A user-friendly feedback message with emoji.

    Examples:
        >>> check_guess(50, 75)
        ('Too Low', '📈 Go HIGHER!')
        >>> check_guess(80, 75)
        ('Too High', '📉 Go LOWER!')
        >>> check_guess(75, 75)
        ('Win', '🎉 Correct!')
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    else:
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str,
                 attempt_number: int) -> int:
    """Calculate and update the player's score based on game outcome.

    Awards points when the player wins, with more points given for fewer
    attempts. The score decreases by 10 points per attempt, with a minimum
    bonus of 10 points guaranteed for any win.

    Args:
        current_score: The player's current cumulative score.
        outcome: The result of the guess ('Win', 'Too High', or 'Too Low').
        attempt_number: The current attempt number (0-indexed).

    Returns:
        The updated score. If the outcome is 'Win', adds bonus points based
        on attempt count. Otherwise, returns the current score unchanged.

    Examples:
        >>> update_score(0, 'Win', 0)
        90
        >>> update_score(100, 'Win', 5)
        150
        >>> update_score(50, 'Too High', 2)
        50

    Note:
        Score calculation: base_points = 100 - 10 * (attempt_number + 1)
        Minimum bonus points per win: 10
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points
    return current_score
