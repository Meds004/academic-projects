# Advanced Algorithms Assignment 1 Question 3
# Name: Anthony Medico


n = None  # number of steps in scenario
k = None  # number of stops at each step

a = []  # 2-dimensional array of times to perform the task at stop s[i][j]

output = ""  # String to collect all output data to be written to an output file

with open("Assn1question3in.txt", "r") as file:
    runs = int(file.readline())  # get number of scenarios in file

    for run in range(1, runs+1):  # run the algorithm for each scenario
        print(f"\n***** Scenario {run} *****")

        # total travel time is constant for each run
        # total_travel_time will sum up all the travel times (e, x and t)
        total_travel_time = 0

        temp = file.readline().split()  # read line with 'n' and 'k'
        n = int(temp[0])  # assign 'n' (number of steps in scenario)
        k = int(temp[1])  # assign 'k' (number of stops at each step)

        temp = file.readline().split()  # read line with 'e' and 'x'
        total_travel_time += int(temp[0])  # add entry time to travel_time
        total_travel_time += int(temp[1])  # add exit time to travel_time

        temp = file.readline().split()  # read line with 't' values
        for time in temp:
            total_travel_time += int(time)  # add all travel times to travel_time

        # Populate the 'a' array
        for i in range(n):
            temp = file.readline().split()  # read line with 'a' array for step i
            a.append([])
            for time in temp:
                a[i].append(int(time))

        print(f"n: {n}")
        print(f"k: {k}")
        print(f"a[i][j]: {a}")
        print(f"Total travel time: {total_travel_time}")

        # Matroid algorithm

        # Populate S with tuples representing each stop (step, stop, task_time)
        S = []
        for i in range(n):
            for j in range(k):
                S.append((i+1, j+1, a[i][j]))

        print(f"S: {S}")

        # Instead of first constructing the I array and then checking every element x
        # against that array, these steps can be combined to make the algorithm more
        # efficient. The only property of I is that there can't be more than one stop
        # for a given step, so when constructing the optimal subset A from the sorted
        # S array, the algorithm can check then if a stop at a given step has already
        # been selected, and if so, don't include it.

        # Also, instead of doing w0 - w(s), S can just be sorted in non-decreasing order
        # of task_time.

        S_sorted = sorted(S, key=lambda s: s[2])  # sorts S by the task_time

        # Construct optimal subset
        A = []  # the optimal subset
        chosen_steps = set()  # set to keep track of which steps a stop has been chosen for
        for stop in S_sorted:  # iterate through all stops in the sorted S array
            if stop[0] not in chosen_steps:  # check if we already selected a stop at this step
                chosen_steps.add(stop[0])  # add the step to chosen_steps
                A.append(stop)  # append the stop to A

        A.sort()  # sort A by step number

        print(f"A: {A}")

        # Calculate minimum overall time
        min_overall_time = total_travel_time  # add travel times to minimum overall time
        for stop in A:  # add chosen task times to minimum overall time
            min_overall_time += stop[2]

        print(f"Minimum overall time: {min_overall_time}")

        # Prepare output
        output += f"Scenario {run}\n"
        output += f"\tMinimum time:\t{min_overall_time}\n"

        for step, stop, _ in A:
            output += f"\tStep {step}:\t\t\tstop {stop}\n"

        output += "\n"

        # Reset global array for next scenario
        a = []

print(f"File output:\n{output}")

# Write results to file
with open("Q3 Output.txt", "w") as file:
    file.writelines(output)
