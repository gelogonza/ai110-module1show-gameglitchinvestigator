"""Number Guessing Game - Streamlit Application.

A web-based number guessing game where players attempt to guess a randomly
generated secret number within a limited number of attempts. Features multiple
difficulty levels, real-time feedback, score tracking, and guess history.

The game provides directional hints (higher/lower) and validates input to
ensure a fair and enjoyable gameplay experience.
"""

import random

import streamlit as st

from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    get_temperature_feedback,
    is_in_range,
    parse_guess,
    update_score,
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "difficulty" not in st.session_state:
    st.session_state.difficulty = difficulty

if ("secret" not in st.session_state or
        st.session_state.difficulty != difficulty):
    st.session_state.secret = random.randint(low, high)
    st.session_state.difficulty = difficulty
    st.session_state.attempts = 0
    st.session_state.status = "playing"
    st.session_state.history = []

if "attempts" not in st.session_state:
    st.session_state.attempts = 1

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Make a guess")

info_placeholder = st.empty()
debug_placeholder = st.empty()

col_hint, col_new = st.columns(2)
with col_hint:
    show_hint = st.checkbox("Show hint", value=True)
with col_new:
    new_game = st.button("New Game 🔁")

with st.form("guess_form"):
    raw_guess = st.text_input("Enter your guess:")
    submit = st.form_submit_button("Submit Guess 🚀")

if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.history = []
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

# Process submitted guess
if submit:
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.error(err)
    elif not is_in_range(guess_int, low, high):
        st.error(
            f"{guess_int} isn't within range. "
            f"Please enter a number between {low} and {high}."
        )
    else:
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        outcome, message = check_guess(guess_int, st.session_state.secret)
        
        # Get temperature feedback
        temp_level, temp_emoji, temp_color = get_temperature_feedback(
            guess_int, st.session_state.secret, high - low
        )

        if show_hint:
            # Display direction hint
            st.warning(message)
            
            # Display temperature feedback with color coding
            if outcome != "Win":
                st.markdown(
                    f":{temp_color}[**{temp_emoji} {temp_level}** - "
                    f"You're getting closer!]"
                )

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

# Update status display
info_placeholder.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

# Display game session summary table
if st.session_state.history:
    st.divider()
    st.subheader("📊 Game Session Summary")
    
    # Create data for the summary table
    summary_data = []
    for idx, guess in enumerate(st.session_state.history, 1):
        outcome, direction = check_guess(guess, st.session_state.secret)
        temp_level, temp_emoji, _ = get_temperature_feedback(
            guess, st.session_state.secret, high - low
        )
        
        summary_data.append({
            "Attempt": f"#{idx}",
            "Guess": guess,
            "Direction": direction,
            "Temperature": f"{temp_emoji} {temp_level}"
        })
    
    # Display as table
    import pandas as pd
    df = pd.DataFrame(summary_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Display summary metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Attempts", st.session_state.attempts)
    with col2:
        st.metric("Current Score", st.session_state.score)
    with col3:
        remaining = attempt_limit - st.session_state.attempts
        st.metric("Attempts Left", remaining)

with debug_placeholder.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
