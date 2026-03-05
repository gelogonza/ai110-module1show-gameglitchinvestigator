# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

**Game purpose:** A number guessing game where the player tries to guess a randomly chosen secret number within a set number of attempts. Each wrong guess provides a hint (go higher or lower), and the score is based on how few attempts it took to win.

**Bugs found:**

1. **Secret number reset on every rerun** — `random.randint()` was called unconditionally at the top level, so every button click generated a new secret.
2. **Hints were inverted** — `check_guess` returned "Go HIGHER!" when the guess was too high and "Go LOWER!" when it was too low.
3. **Normal and Hard difficulty ranges were swapped** — Normal returned 1–100 and Hard returned 1–50; it should be the opposite.
4. **New Game button didn't work** — clicking it reset the secret but never reset `status` back to `"playing"`, so the game immediately stopped again on rerun.
5. **Score went negative** — wrong guesses subtracted 5 points, and "Too High" on even attempts added 5, making scoring inconsistent and allowing negative scores.
6. **Attempts counter showed stale data** — the `st.info()` block rendered before the submit logic ran, so on the final guess the counter said "1 attempt left" while the bottom said "Out of attempts."
7. **Difficulty change didn't update the secret or range** — the secret was only guarded by `if "secret" not in st.session_state`, so switching difficulty had no effect.
8. **Out-of-range inputs counted as attempts** — entering a number outside the difficulty range wasted an attempt with no feedback.

**Fixes applied:**

1. Wrapped secret generation in `if "secret" not in st.session_state` and added a difficulty-change check that resets the game state when difficulty switches.
2. Swapped the hint messages in `check_guess` so `guess > secret` → "Go LOWER!" and `guess < secret` → "Go HIGHER!".
3. Corrected `get_range_for_difficulty`: Normal → 1–50, Hard → 1–100.
4. Added `st.session_state.status = "playing"` and history clear to the New Game handler.
5. Removed the point-subtraction logic from `update_score`; score only changes on a win.
6. Replaced `st.info()` and the debug panel with `st.empty()` placeholders filled after the submit block, so they always reflect the post-submission state.
7. Added difficulty tracking in session state; changing difficulty now resets the secret, attempts, and history.
8. Added range validation using `is_in_range()` from `logic_utils`; out-of-range inputs show an error and do not increment the attempt counter.

## 📸 Demo

-  [<img width="2525" height="1349" alt="shot-1772685126" src="https://github.com/user-attachments/assets/4a27add8-73f9-4eb6-abd5-ee886a4f0f84" />
]

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
