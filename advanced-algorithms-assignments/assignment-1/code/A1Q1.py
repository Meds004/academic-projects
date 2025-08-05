# Advanced Algorithms Assignment 1 Question 1
# Name: Anthony Medico

import math

n = None  # number of steps in scenario
k = None  # number of stops at each step

e = []  # array of entry times from starting location to step 1, stop j
x = []  # array of exit times from step n, stop j to final destination

t = []  # 3-dimensional array of times to travel from s[i][j] to s[i+1][j']
a = []  # 2-dimensional array of times to perform the task at stop s[i][j]

# 2-dimensional array to store best times so far
# using stops (j) as rows and steps (i) as columns (visualizing the race moving left to right)
# min_times[j][i] = minimum time to get to stop j at step i
min_times = []

# 2-dimensional array to store previous stop for s[i][j]
# using stops (j) as rows and steps (i) as columns (visualizing the race moving left to right)
# prev_stop[j][i] = previous stop at s[i-1] to achieve minimum time at s[i][j]
# when i = 0 (which is step 1), there is no previous step, so prev_stop[j][0] = None
prev_stops = []

output = ""  # String to collect all output data to be written to an output file

with open("Assn1question1in.txt", "r") as file:
    runs = int(file.readline())  # get number of scenarios in file

    for run in range(1, runs + 1):  # run the algorithm for each scenario
        print(f"***** Scenario {run} *****")

        temp = file.readline().split()  # read line with 'n' and 'k'
        n = int(temp[0])  # assign 'n' (number of steps in scenario)
        k = int(temp[1])  # assign 'k' (number of stops at each step)

        temp = file.readline().split()  # read line with 'e' array
        # Populate the 'e' array
        for j in range(k):
            e.append(int(temp[j]))

        temp = file.readline().split()  # read line with 'x' array
        # Populates the 'x' array
        for j in range(k):
            x.append(int(temp[j]))

        # Populates the 't' array
        for i in range(n - 1):  # step
            temp = file.readline().split()  # read line with 't' array for step i
            t.append([])
            for j in range(k):  # stop at step i
                t[i].append([])
                for j_prime in range(k):  # stop at step i + 1
                    # In line below: [j * k + l] calculates 0, 1, 2, 3,... to access elements in temp
                    t[i][j].append(int(temp[j * k + j_prime]))

        # Populates the 'a' array
        for i in range(n):
            temp = file.readline().split()  # read line with 'a' array for step i
            a.append([])
            for num in temp:
                a[i].append(int(num))

        print(f"n: {n}")
        print(f"k: {k}")
        print(f"e[j]: {e}")
        print(f"x[j]: {x}")
        print(f"t[i][j][j']: {t}")
        print(f"a[i][j]: {a}")

        # Dynamic Programming algorithm:
        # Step 1: Calculate min times at step 1 (index 0)
        for j in range(k):
            min_times.append([e[j] + a[0][j]])

        print(f"Minimum times after step 1: {min_times}")

        # Step 2: Calculate min times from step 2 to n (index 1 to n - 1)
        # Initialize prev_stops to have 0's in first column
        prev_stops = [[0] for _ in range(k)]

        # Find minimum time for stop j by checking all min times from stop i - 1
        for i in range(1, n):  # i = step
            for j in range(k):  # j = stop at current step to calculate min time for
                best_min_time = math.inf
                best_prev_stop = 0
                for j_prime in range(k):  # j' = stop at previous step (i - 1)
                    # calculate min time coming from each stop at step i - 1
                    curr_min_time = min_times[j_prime][i - 1] + t[i - 1][j_prime][j] + a[i][j]
                    if curr_min_time < best_min_time:  # keep track of best
                        best_min_time = curr_min_time
                        best_prev_stop = j_prime
                min_times[j].append(best_min_time)  # store best time
                prev_stops[j].append(best_prev_stop + 1)  # store best previous stop

        print(f"Minimum times after step 2: {min_times}")
        print(f"Previous stops after step 2: {prev_stops}")

        # Step 3: Calculate f_star (minimum overall time) and s_star (stop at last step)
        # Calculate f_star (minimum of min_times at step n + respective exit time)
        # and s_star (final stop at the last step)
        f_star = math.inf
        s_star = 0

        for j in range(k):
            curr_min_time = min_times[j][n - 1] + x[j]
            if curr_min_time < f_star:
                f_star = curr_min_time
                s_star = j + 1

        print(f"Minimum overall time: {f_star}")
        print(f"Final stop at step n: {s_star}")

        # Output results
        output += f"Scenario {run}\n"
        output += f"\tMinimum time:\t{f_star}\n"

        # Create list to use like a stack
        # Working backwards, populate stops stack to get path
        stops = [s_star]
        j = s_star
        for i in range(n - 1, 0, -1):
            j = prev_stops[j - 1][i]  # using j - 1 for 0 indexing
            stops.append(j)

        # Pop from stops stack to output path in order
        for i in range(len(stops)):
            output += f"\tStep {i + 1}:\t\t\tstop {stops.pop()}\n"

        output += "\n"
        print(f"***** End of scenario {run} *****\n")

        # Reset variables for next scenario
        e = []
        x = []
        t = []
        a = []
        min_times = []
        prev_stops = []


print(f"File output:\n{output}")

# write results to file
with open("Q1 Output.txt", "w") as file:
    file.writelines(output)
