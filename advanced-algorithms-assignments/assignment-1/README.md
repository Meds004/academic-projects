# Assignment 1 - Advanced Algorithms

## Description

This assignment focuses on solving the given problems using dynamic programming or greedy algorithms.  
It includes solutions to the following questions:

1. Find the fastest way possible to get from the start to the end (like a race, travelling to chosen stops, completing a task, then going to the next stop). You pass through a number of stops along the way. At each step, there are *k* possible stops to choose from. All travel paths have a cost, and chosen stops have associated task costs. Choose the stop at each step that minimizes total cost. Solved using dynamic programming.
2. Given a number of tasks and their associated completion time, find the split points to fit the given tasks into the minimum number of shifts given the following constraints:
- Given shift length (all shifts are the same length)
- One "employee" works at a time
- No task is allowed to be split across shifts
- Tasks have various time lengths
- Must be a gap of at least 1 time unit between tasks
- More than 1 time unit between tasks is considered excessive - cost of gap of *k* time units is (*k*-1)^2
- Exception: Cost of scheduling only 1 task in a shift is 1000
3. Question 1 modified:
- Travel time between any stop to any stop at the next step is constant
- Travel time from start to any stop at step 1 is the same
- Travel time from any stops at the last step to the end is the same
Prove it can now be represented as a **weighted matroid** and use the general greedy algorithm for matroids to produce an optimal answer.

For full explanations and analysis, please refer to the included report 'a1-answers'.

## Technologies Used

- Language: Python3
- Platform: PyCharm IDE (can be run easily on the Command Line)

## How to Run

1. Clone the repository and run (modify filename to A1Q2.py or A1Q3.py):
   ```bash
   git clone https://github.com/Meds004/academic-projects/advanced-algorithms-assignments/assignment-1.git
   cd code
   python3 A1Q1.py
