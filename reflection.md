# PawPal+ Project Reflection

## 1. System Design
Core actions
-add pet and owner info
-add tasks
-view tasks
-generate schedule

Objects
### Pet 
 Attributes: name, animal
 Methods: delete pet, add pet

### Task
Attributes - time to complete, priority
Methods - set time, set priority, view tasks, delete task, add task, update task

### Shcedule
Attributes- schedule
Methods - generate schedule, delete schedule

**a. Initial design**

- Briefly describe your initial UML design.
My initial UML design consists of 4 core classes
- What classes did you include, and what responsibilities did you assign to each? The classes were pet - Attributes: name, animal
 Methods: delete pet, add pet

 owner - attributes: name, pets. 
 Methods: delete pet, add pet

 task
 Attributes: time to complete, priority
 methods: set time, set priority, view tasks, delete task, add task, update task

 Shcedule
Attributes- schedule
Methods - generate schedule, delete schedule

 
**b. Design changes**

- Did your design change during implementation?
yes
- If yes, describe at least one change and why you made it.
I connected a couple of classes together makeing them have some kind of relationship. 
e.g linking task to pet, task now has a pet_name property to know what pet has a task

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
It first goes with priority above all, then breaks priority ties(same priority) using duration. shorter tasks first.
for the time constraint/budget, the tasks are picked in a greedy manner until no time left.
- How did you decide which constraints. mattered most?
The constraint thats very specific and chosen by the user "Priority" 

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
The greedy manner definitely, it does not go as deep to know which task should be done at what time. this can be bad because a high priority task may take too much time and leave little to no time left for another high priority task
- Why is that tradeoff reasonable for this scenario?
Its reasonable because there are other attributes used for sorting and prioritizing. 

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
brainstorming, generating tests(a lot), debugging and improvement suggestions
- What kinds of prompts or questions were most helpful?
The improvement sugestions were probably the most helpful and impactful

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
It over engineered a couple of things, especially the algorithm aspect
- How did you evaluate or verify what the AI suggested?
    I looked and tested how the app worked in the moment before deciding if it would be the right way to move.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
I tested four core behaviors: chronological sorting of tasks by HH:MM start time, recurring task logic (marking complete and generating the next occurrence), conflict detection between overlapping time windows, and filtering tasks by pet name or completion status. Each behavior was tested against both happy paths (normal expected input) and edge cases such as an empty task list, a single task, back-to-back tasks that touch but do not overlap, and non-recurring tasks that should produce no side effects.
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
I'm 97% confident it works correctly and how it should work. My confidence is based on the amount of testcases I set up.
- What edge cases would you test next if you had more time?
    How much tasks the app can handle while maintaining current speed. Basically work load test.
---

## 5. AI Ethics and Reliability

**Limitations of the System**

The most obvious limitation is that the knowledge base currently only covers dog breeds. If a user enters a cat, rabbit, or any other animal, the system falls back to Gemini's general knowledge with no retrieved context, meaning the RAG feature effectively stops working for non-dog pets. Within dogs, the knowledge base also only covers popular breeds, so uncommon or mixed breeds like a Mutt may not get a matched entry and instead receive general fallback suggestions. Additionally, the breed matching is a simple string search, which means typos or alternate spellings (e.g. "rotweiler" vs "rottweiler") can result in no match being found even when the breed exists in the knowledge base.

**How AI Could Be Misused and How to Prevent It**

The AI suggestion feature could be misused if a user treats Gemini's output as a substitute for actual veterinary advice. Someone could read a task suggestion like "reduce exercise" or "add joint supplements" and act on it without consulting a vet, potentially harming their pet. To prevent this, the app should include a clear disclaimer near the AI output stating that suggestions are for general planning purposes only and do not replace professional veterinary guidance. Rate limiting the API calls could also prevent abuse of the feature at scale.

**What Surprised Me While Testing the AI's Reliability**

The most surprising thing was how well the AI handled breeds that were not in the knowledge base. When "Mutt" was entered, a breed with no entry in the JSON, Gemini still returned useful, age-appropriate suggestions using its own general knowledge. I expected it to produce vague or useless output without retrieved context, but the response was structured and practical. On the other hand, I noticed the AI sometimes changed the format of its output between runs, occasionally using bullet points and other times numbered lists, even with the same input. The content was consistently good, but the formatting inconsistency was a small reliability issue.

**AI Collaboration**

AI was involved in nearly every stage of this project: brainstorming the initial class design, generating the test suite, debugging, and writing the RAG feature. The most helpful suggestion was during the test generation phase. When asked to write tests for conflict detection, the AI proactively included edge cases I had not thought of, like back-to-back tasks that touch at exactly the same minute but do not technically overlap. That saved time and caught a real boundary condition in the detection logic.

The flawed suggestion came when I asked the AI to improve the scheduling algorithm. It proposed replacing the greedy approach with a full knapsack optimization using dynamic programming. While technically more optimal, it was significantly more complex, harder to read, and unnecessary for the scale of this app. I rejected it because the added complexity introduced more surface area for bugs and made the code harder to maintain, a clear case of the AI over-engineering a solution to a problem that did not need it.

---

## 6. General Reflection

**a. What went well**

- What part of this project are you most satisfied with?
The sorting aspect. I like the brainstorming that I did with the AI assistance, I was able to weigh different tradeoffs and it came out great.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
definitely the UI component, I feel it needs more work and right now its a bit bland for a pet app.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
AI needs a lot of help in terms of where it should go. but when you tell it where to go and it knows, its mostly smooth and very productive.