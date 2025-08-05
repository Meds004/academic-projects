# Advanced Algorithms Assignment 1 Question 2
# Name: Anthony Medico

import math

def construct_array_1000(size):
    """
    Constructs an n*n array with values of 1000 down the diagonal.
    First row and column are index numbers.
    The rest of the array is 1-indexed.
    """

    arr = [[0]]
    for i in range(1, size + 1):
        arr[0].append(i)
        arr.append([i])
        for j in range(1, n + 1):
            if i == j:
                arr[i].append(1000)
            else:
                arr[i].append(0)

    return arr


def construct_array(n):
    """
    Constructs an n*n array populated with 0s
    First row and column are index numbers.
    The rest of the array is 1-indexed.
    """

    arr = [[0]]
    for i in range(1, n + 1):
        arr[0].append(i)
        arr.append([i])
        for j in range(1, n + 1):
            arr[i].append(0)

    return arr


def print_2d_array(arr):
    """
    Prints a 2D array to the console in an easy-to-read format.
    Used when testing the program.
    """

    for row in arr:
        for num in row:
            print(f"{num:>7}", end="")
        print()
    print()


def cost(i, j, tasks, M):
    """
    Calculate cost from task i to task j
    Returns cost if the tasks fit in a shift, or infinity otherwise
    """

    # Calculate total task time
    total_task_time = 0
    for task_num in range(i, j + 1):
        total_task_time += tasks[task_num][1]

    num_gaps = j - i  # Calculate required number of gaps

    req_time = total_task_time + num_gaps  # Required time including minimum gaps

    if req_time > M:  # If required time doesn't fit in a shift, return infinity
        return math.inf

    total_gap_time = M - total_task_time  # Calculate total gap time needed

    base_gap = total_gap_time // num_gaps  # Base gap splits gap times evenly (without remainder)
    gaps = []  # array to hold gap sizes
    for i in range(num_gaps):  # append base gap times to array
        gaps.append(base_gap)

    remainder_to_add = total_gap_time % num_gaps  # Calculate remainder to add to gaps
    for i in range(remainder_to_add):  # Add 1 to each gap until no remainder left
        gaps[i] += 1

    cost = 0
    for gap in gaps:  # Calculate total gap cost using given formula
        cost += (gap - 1)**2

    return cost


def get_split_points(i, j, s, split_points):
    """
    Recursive function to get all shift split points.
    The number representing a split point is the task number of the last task in a shift
    """
    if s[i][j] == 0:  # Base case: all tasks fit in 1 shift. Do nothing.
        return
    else:
        split_points.append(s[i][j])  # This value is a split point
        get_split_points(i, s[i][j], s, split_points)  # left subproblem
        get_split_points(s[i][j] + 1, j, s, split_points)  # right subproblem


output = ""  # String to hold output that gets written to file

with open('Assn1question2in.txt', 'r') as file:

    while True:  # run until no scenarios left (M = 0)

        # M = shift length, n = number of tasks
        first_line = file.readline().split()
        M = int(first_line[0])
        if M == 0:  # No scenarios left, done.
            break
        n = int(first_line[1])

        tasks = [None]  # dictionary to hold task name and time (1-indexed)

        for line in file:
            if line.strip() == "":
                break
            task = line.split()
            name = task[0]  # task name
            duration = int(task[1])  # task duration
            tasks.append((name, duration))  # tuple to hold name and duration, appended to task array

        c = construct_array_1000(n)  # 2D array cost lookup table
        for i in range(1, n + 1):  # Populate array with costs to have task[i] to task[j] in a shift
            for j in range(i + 1, n + 1):
                c[i][j] = cost(i, j, tasks, M)

        m = construct_array_1000(n)  # Minimum cost array (similar to Matrix Chain Multiplication)
        s = construct_array(n)  # Array to keep track of split points

        # Main DP algorithm (very similar to matrix chain multiplication)
        for t in range(2, n + 1):  # Subproblem size
            for i in range(1, n - t + 2):  # Look at each subproblem of size t
                j = i + t - 1  # Maintains subproblem size
                m[i][j] = math.inf
                for k in range(i, j):  # k is potential split point

                    # Cost is minimum of splitting tasks between shifts, or all tasks fit into one shift
                    q = min(m[i][k] + m[k+1][j], c[i][j])

                    # Find split point (0 if no split)
                    # It's 0 when c[i][j] is minimum cost
                    # c[i][j] at this point is cost of all subproblem tasks fit into 1 shift
                    split_point = 0
                    if m[i][k] + m[k+1][j] < c[i][j]:
                        split_point = k

                    # keep track of minimum cost for subproblem and corresponding split point
                    if q < m[i][j]:
                        m[i][j] = q
                        s[i][j] = split_point
                        # print(f"Updating: m[{i}][{j}]")

        # Scenario done, prepare output
        output += f"Total cost:\t\t{m[1][n]}\n"

        split_points = []  # Array to hold shift split points
        get_split_points(1, n, s, split_points)  # populate array
        split_points.sort()  # Sort the array
        split_points.append(n)  # To facilitate printing the shifts (to print the last shift)

        # Write tasks to output
        start = 1  # First task for a shift
        for num in split_points:  # Each line in output will be up to a split point (inclusive)
            j = num  # The last task for a shift (which is the split point)
            for i in range(start, j + 1):
                output += f"{tasks[i][0]} "
            output += "\n"
            start = j + 1  # Update start to be starting task for the next shift
        output += "\n"

# Write results to file
with open("Q2 Output.txt", "w") as file:
    file.writelines(output)

print(output)
