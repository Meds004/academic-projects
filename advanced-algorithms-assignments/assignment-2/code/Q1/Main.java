import java.io.FileWriter;
import java.io.IOException;
import java.util.*;

public class Main {
  // Global variables (for easy access)

  static int n;
  static int degree = 3;

  // Precomputed using n choose k, to know how big of an array to make.
  static int numberOfValidRows;

  // All valid rows of degree 3 are precomputed and stored here.
  // A valid row is an array of size n with 0's and exactly three 1's.
  // These rows are constructed in lexicographic order, so the index they are
  // stored at is their rank.
  static int[][] allValidRows;

  // A candidate is just a potential row, stored as it's rank.
  // All candidates are the numbers 0 to numberOfValidRows - 1
  static int[] candidates;

  // A permutation is a reordering of node labels
  // With n nodes, all possible permutations of 0 to n - 1 are precomputed and
  // stored here.
  // Used as a mapping to generate or check for equivalent graphs
  static List<int[]> perms;

  /*
  The main method facilitates the flow of the program including setup,
  running the algorithm, and printing the results.
   */
  public static void main(String[] args) {
    n = getUserInput(); // get value of n from user
    String output = "";
    long startTime = System.currentTimeMillis(); // program start time

    // Precompute number of valid matrix rows for a 3-regular graph.
    numberOfValidRows = choose(n, degree);

    // Precompute all candidates (numbers from 0 to numberOfValidRows).
    candidates = computeCandidates();

    // Precompute and store all valid rows which can be indexed by rank.
    allValidRows = generateValidRows();



    // PERMUTATION STUFF
    // Set to store all possible graphs (including equivalent graphs) encoded
    // as a string.
    Set<String> allGraphs = new HashSet<>();

    // Precompute vertex numbers (0..n-1)
    int[] vertices = new int[n];
    for (int i = 0; i < n; i++) {
      vertices[i] = i;
    }

    // Compute and store all permutations of vertex labels to use a mappings.
    perms = new ArrayList<>();
    generatePermList(vertices, 0, perms);


    // BEGIN BACKTRACKING AND STORING SOLUTIONS
    // Variable to store all valid inequivalent graphs.
    List<List<Integer>> inequivalentGraphs = new ArrayList<>();

    // Call main backtracking algorithm to begin finding all valid graphs.
    generateValidGraphs(inequivalentGraphs, allGraphs, new ArrayList<>(), 1);

    // PRINT RESULTS
    if (inequivalentGraphs.size() == 1) {
      System.out.println("There is 1 inequivalent graph of degree 3 with " + n + " vertices.\n");
      output += "There is 1 inequivalent graph of degree 3 with " + n + " vertices.\n";
    } else {
      System.out.println("There are " +
              inequivalentGraphs.size() +
              " inequivalent graphs of degree 3 with " +
              n + " vertices.\n");
      output += "There are " +
              inequivalentGraphs.size() +
              " inequivalent graphs of degree 3 with " +
              n + " vertices.\n\n";
    }

    // print up to 4 of the graphs
    int numberToPrint = Math.min(inequivalentGraphs.size(), 4);
    for (int i = 0; i < numberToPrint; i++) {
      System.out.println("Solution " + (i + 1) + ":");
      output += "Solution " + (i + 1) + ":\n";
      printSolution(inequivalentGraphs.get(i));
      for (int j = 0; j < n; j++) {
        output += Arrays.toString(getGraph(inequivalentGraphs.get(i), n)[j]) + "\n";
      }
      output += "\n";
    }

    long endTime = System.currentTimeMillis(); // program end time

    // Calculate runtime and print
    long durationInMillis = endTime - startTime;

    long hours = (durationInMillis / (1000 * 60 * 60));
    long minutes = (durationInMillis / (1000 * 60)) % 60;
    long seconds = (durationInMillis / 1000) % 60;

    System.out.printf("Elapsed time: %02d:%02d:%02d\n", hours, minutes, seconds);
    output += String.format("Elapsed time: %02d:%02d:%02d\n", hours, minutes, seconds);

    writeOutputToFile(output);
  }

  /*
  This method will generate all possible valid adjacency matrix rows for a
  regular graph of degree 3 with n vertices.
  A row is represented as an array of 0s and 1s.
   */
  private static int[][] generateValidRows() {
    int[][] allRows = new int[numberOfValidRows][];

    // Initialize first row representation for lexicographic ordering of the
    // 3-subset: [1, 1, 1, 0, 0,...,0]
    allRows[0] = new int[n];
    for (int i = 0; i < 3; i++) {
      allRows[0][i] = 1;
    }

    // Use successor algorithm to populate the rest of allRows in lexicographic
    // order.
    for (int i = 1; i < allRows.length; i++) {
      allRows[i] = kSubsetLexSuccessor(allRows[i - 1]);
    }

    return allRows;
  }

  /*
  This method takes in the current row and generates the next row in
  lexicographic order. It converts the adjacency matrix row to a k-subset
  and uses that to find the next row.
  E.g. [1,1,1,0,0,0,...,0] ==> [1, 2, 3] ==> [1, 2, 4] ==> [1,1,0,1,0,...,0]
   */
  private static int[] kSubsetLexSuccessor(int[] row) {
    int[] currentRowKSet = new int[degree]; // array to represent row as k-subset

    // Convert adjacency matrix row to k-subset array.
    int index = 0;
    for (int i = 0; i < row.length; i++) {
      if (row[i] == 1) {
        currentRowKSet[index++] = i + 1;
      }
    }

    // Array for next k-subset successor and successor algorithm given in class.
    int[] nextRow = Arrays.copyOf(currentRowKSet, 3);

    int i = degree;

    while (i >= 1 && currentRowKSet[i - 1] == n - degree + i) {
      i--;
    }

    nextRow[i - 1] = currentRowKSet[i - 1] + 1;

    for (int j = i + 1; j <= degree; j++) {
      nextRow[j - 1] = nextRow[j - 2] + 1;
    }

    // Convert to adjacency matrix row.
    int[] result = new int[n];
    for (int num : nextRow) {
      result[num - 1] = 1;
    }

    return result;
  }

  /*
  This method is the main backtracking algorithm to generate all valid graphs.
  It begins with each candidate and builds complete valid solutions.
  It uses helper methods for pruning and testing for equivalence.
   */
  private static void generateValidGraphs(
          List<List<Integer>> validGraphs,
          Set<String> allGraphs,
          List<Integer> partialSolution,
          int c
  ) {
    for (int candidate : candidates) {
      if (c == 1) {
        double percentComplete = ((candidate + 1) * 100.0) / numberOfValidRows;
        System.out.println("Working on branch " + (candidate + 1) + " of " + numberOfValidRows);
        System.out.println(String.format("%.2f", percentComplete) + "% complete.");
      }

      // only proceed if partial solution is valid (pruning)
      if (isValidPartialSolution(partialSolution, candidate)) {
        List<Integer> newPartialSolution = new ArrayList<>(partialSolution);
        newPartialSolution.add(candidate); // add new candidate to solution
        if (c < n) {
          // continue to next level
          generateValidGraphs(validGraphs, allGraphs, newPartialSolution, c + 1);
        } else {
          // At this point, we have a complete valid solution (pre-equivalence
          // checking)

          // Now check for equivalence
          if (!isIsomorphic(newPartialSolution, allGraphs)) {
            // no equivalent graphs found, add to overall solution
            validGraphs.add(newPartialSolution);

            // Generate and store all permutations of this valid solution
            generateEquivalentGraphs(newPartialSolution, allGraphs);
          }
        }
      }
    }
  }

  /*
  This method performs equivalence checking.
  When a valid solution is found, it is stored in the Set allGraphs, encoded
  as a string, along with all of its equivalent graphs.
  As long as this graph is not in the Set, it will be unique (inequivalent)
   */
  private static boolean isIsomorphic(List<Integer> newGraph, Set<String> allGraphs) {
    // Convert solution (list of candidates) to an actual adjacency matrix.
    int[][] graph = getGraph(newGraph, newGraph.size());

    // Encode the graph to a unique string.
    String graphString = convertGraphToString(graph);

    // Return true if there is already an isomorphic (equivalent) solution.
    return allGraphs.contains(graphString);
  }

  /*
  This method is used to check if a partial solution is valid, which will prune branches
  in the backtracking algorithm.
  Pruning techniques include:
  1. Checking the diagonal of the new row (must be 0)
  2. Ensure all columns have at max degree 3.
  3. Ensure A[i][j] == A[j][i] i.e. symmetrical about the diagonal
  To increase efficiency, most of this testing is only done to the new candidate, since
  the previous candidates in the partial solution would have already been tested.
   */
  private static boolean isValidPartialSolution(List<Integer> partialSolution, int newCandidate) {

    // Check diagonal is 0 for where the new row will be placed in the matrix.
    if (allValidRows[newCandidate][partialSolution.size()] == 1)
      return false;

    // Add the new candidate to the solution
    List<Integer> potentialSolution = new ArrayList<>(partialSolution);
    potentialSolution.add(newCandidate);

    // Array to represent the degree count for each column.
    int[] degreeCount = new int[n];

    for (int rank : potentialSolution) {
      // Unrank the row (index of allValidRows is that rows rank).
      int[] row = allValidRows[rank];

      // Increment degreeCount for each column that has an edge.
      for (int j = 0; j < n; j++) {
        if (row[j] == 1) {
          degreeCount[j]++;
          if (degreeCount[j] > 3) // Column has degree > 3 -> return false
            return false;
        }
      }
    }

    // Get adjacency matrix for partial solution
    int[][] partialGraph = getGraph(potentialSolution, potentialSolution.size());

    // Ensure that A[i][j] == A[j][i] for the new candidate
    for (int j = 0; j < potentialSolution.size() - 1; j++) {
      int i = potentialSolution.size() - 1; // row index of new candidate

      if (partialGraph[i][j] != partialGraph[j][i]) // ensure symmetry
        return false;
    }

    return true;
  }

  /*
  This method computes all candidates for partial solutions. A candidate is just
  a rank number, since all valid rows are precomputed in lexicographic order and
  stored in allValidRows.
  This method simply returns an array of integers from 0 to numberOfValidRows - 1.
   */
  private static int[] computeCandidates() {
    int[] candidates = new int[numberOfValidRows];

    for (int i = 0; i < numberOfValidRows; i++) {
      candidates[i] = i;
    }
    return candidates;
  }

  /*
  This method returns an adjacency matrix representation of a (partial) solution.
  A solution is just a list of integers representing the ranks of the
  precomputed rows.
  This method unranks each row and constructs a complete adjacency matrix.
   */
  private static int[][] getGraph(List<Integer> solution, int numRows) {
    int[][] graph = new int[numRows][n]; // The adjacency matrix to return

    for (int i = 0; i < numRows; i++) {
      int rank = solution.get(i); // Unrank row
      int[] row = Arrays.copyOf(allValidRows[rank], n); // Make a copy
      graph[i] = row; // Add it to the adjacency matrix
    }

    return graph;
  }

  /*
  This method prints a solution to the console as an adjacency matrix.
   */
  private static void printSolution(List<Integer> solution) {
    for (int rank : solution) {
      int[] row = allValidRows[rank]; // Unrank row
      System.out.println(Arrays.toString(row));
    }
    System.out.println();
  }

  /*
  This method saves the requested output to a file.
   */
  private static void writeOutputToFile(String output) {
    String filename = "output_n" + n + ".txt";

    try (FileWriter fw = new FileWriter(filename)) {
      fw.write(output);
    } catch (IOException e) {
      System.out.println(e.getMessage());
    }
  }

  /*
  This method efficiently calculates a binomial coefficient for n and k.
  Used to calculate the array size to hold all valid row representations.
  Also used in the getRank algorithm.
   */
  private static int choose(int n, int k) {
    int result = 1;
    for (int i = 1; i <= k; i++) {
      result = result * (n - i + 1) / i;
    }
    return result;
  }

  /*
  This method computes and stores a list of all permutations of a list of vertex labels.
  This is done recursively. A list of labels is just the numbers 0 to n-1.
  These are used as mappings to generate all equivalent graphs from a given graph.
   */
  private static void generatePermList(int[] currentPerm, int start, List<int[]> results) {
    if (start == n - 1) { // have a complete permutation, store it
      results.add(Arrays.copyOf(currentPerm, n));
    } else {
      for (int i = start; i < n; i++) {
        swap(currentPerm, start, i); // swap two labels
        generatePermList(currentPerm, start + 1, results); // branch recursively
        swap(currentPerm, start, i); // swap them back for next iteration
      }
    }
  }

  /*
  This helper method swaps two elements of an array.
   */
  private static void swap(int[] array, int i, int j) {
    int temp = array[i];
    array[i] = array[j];
    array[j] = temp;
  }

  /*
  This method takes a given solution, and generates and stores all equivalent graphs.
  Uses the precalculated permutations list perms as mappings to construct all the
  equivalent graphs.
  Graphs are encoded to a unique string representation, and stored in a set, so duplicates
  don't get stored as well.
   */
  private static void generateEquivalentGraphs(List<Integer> solution, Set<String> allGraphs) {
    int[][] graph = getGraph(solution, solution.size()); // get adjacency matrix for solution
    int[][] newPerm = new int[n][n]; // array to construct an equivalent graph

    for (int i = 1; i < perms.size(); i++) { // permutation number
      for (int j = 0; j < n; j++) {
        Arrays.fill(newPerm[j], 0); // reset newPerm to be all 0's
      }
      for (int j = 0; j < n; j++) { // matrix row
        for (int k = 0; k < n; k++) { // matrix column
          if (graph[j][k] == 1) {
            newPerm[perms.get(i)[j]][perms.get(i)[k]] = 1; // map to new equivalent graph
          }
        }
      }
      String newPermRep = convertGraphToString(newPerm); // encode the graph as a string

      allGraphs.add(newPermRep);  // add to allGraphs set
    }
  }

  /*
  This method encodes a graph (adjacency matrix) to a unique string, so it can be
  efficiently stored in a Set.
  The encoding is just the rank numbers of a solution separated by a '-' character.
  E.g. the solution [1, 2, 3, 4] is the string "1-2-3-4"
   */
  private static String convertGraphToString(int[][] graph) {
    StringBuilder sb = new StringBuilder();

    for (int i = 0; i < n; i++) {
      sb.append(getRank(graph[i])).append("-");
    }
    sb.deleteCharAt(sb.length() - 1); // get rid of the extra "-"

    return sb.toString();
  }

  /*
  This method gets the rank of an adjacency matrix row.
   */
  private static int getRank(int[] row) {
    int[] t = new int[degree];

    // Convert row to a 3-subset
    int index = 0;
    for (int i = 0; i < n; i++) {
      if (row[i] == 1) {
        t[index++] = i + 1;
      }
    }

    // Algorithm given in class to get rank
    int rank = 0;
    t[0] = 0;
    for (int i = 1; i < degree; i++) {
      for (int j = t[i - 1] + 1; j <= t[i] - 1; j++) {
        rank = rank + choose(n - j, degree - i);
      }
    }

    return rank;
  }

  /*
  This method accepts user input for the value of n.
  Includes full validation checking.
  Only accepts even values between 4 and 16 inclusive.
   */
  private static int getUserInput() {
    Scanner scanner = new Scanner(System.in);
    int n;

    while (true) {
      System.out.print("Please enter a value for n (even integer between 4 and 16): ");
      String input = scanner.nextLine().trim();

      try {
        n = Integer.parseInt(input);

        if (n >= 4 && n <= 16 && n % 2 == 0) {
          break;
        }

      } catch (Exception e) {
        System.out.println(e.getMessage());
      }

      System.out.println("Invalid input. Please try again.");
    }

    scanner.close();
    return n;
  }
}