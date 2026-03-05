# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

- One bug i noticed was the notification letting you know to go higher or lower was incorrect. It would say go lower even if i got to 1, which was incorrect. 
- another thing i noticed was that upon clicking new game, it wouldnt actually start a new game. 
- the press enter to apply also doesnt work correctly because when i press enter it doesnt actually apply.
- another thing is if i change the difficulty it doesnt actually change the range of numbers either, so for easy ifs supposed to be 1 to 20, but it stays at 1 to 100(normal difficulty).
- easy should also be 1 to 20 ( correct )
- normal should be 1 to 50 ( incorrect )
- hard should be 1 to 100 ( incorrect )
- normal and hard should be switched

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

- What I did was I first identified the bugs. Then I looked at the logic and described the behavior that was actually supposed to occur. After I described the behavior. I showed them the code and the error, and told them to revise it and correct it to behave correctly.
- if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 50
  I verified the results by changing difficulties and seeing if the ranges changed as well.
- I got an suggestion that the attempt counter was correct, even though it wasn't. I then went to the website and looked at the counter and it wasnt working correctly and typed in the error i saw, gave the AI a full breakdown of how its supposed to behave, and what function needed fixing, I then reviewed to make sure it behaved correctly. 
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

1. I decided it was fixed based on the behavior that it was supposed to have originally, and once the code was changed I tested that behavior on the website. If it wasn't correct, I went and reviewed the code that was changed.

2. I ran a test to see how the counter for the attempts left was working. I typed in my guess and checked if the attempts left would decrease based on every attempt I tried, which led me to fix that issue and correct the attempts left counter.

3.Not really, I moreso did manual tests of the website myself to see if all of the fucntions were fixed correctly.
---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

1. it was called without checking if the secret already existed
2. basically everytime you interact with the app  someone erases everything and draw everything again 
3. wrap it in a guard and only generate a new secret if it didnt already exist in the session state
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
