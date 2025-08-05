import java.io.FileWriter;
import java.io.IOException;
import java.util.*;

public class Main {
  // Global variables (for easy access)

  static int n;
  static int degree = 3;
  static int numberOfPaths = 5;

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

  // ESTIMATION STUFF
  static List<ArrayList<ArrayList<Integer>>> D; // to record acceptable candidates for each level
  static long[][] d; // d[p][k] is size of D[p][k] for path p
  static long[][] estimate; // estimated number of nodes for level k of path p
  static long[] scale; // scale used in estimation algorithm at path p
  static Random random;

  /*
  The main method facilitates the flow of the program including setup,
  running the algorithm, and printing the results.
   */
  public static void main(String[] args) {
    n = getUserInput(); // get value of n from user
    String output = "";

    // Precompute number of valid matrix rows for a 3-regular graph.
    numberOfValidRows = choose(n, degree);

    // Precompute all candidates (numbers from 0 to numberOfValidRows).
    candidates = computeCandidates();

    // Precompute and store all valid rows which can be indexed by rank.
    allValidRows = generateValidRows();


    // ESTIMATION STUFF INITIALIZATION
    D = new ArrayList<>(); // initialize all nested ArrayLists
    for (int i = 0; i < numberOfPaths; i++) {
      D.add(new ArrayList<>());
      for (int j = 0; j < n; j++) {
        D.get(i).add(new ArrayList<>());
      }
    }
    d = new long[numberOfPaths][n];
    estimate = new long[numberOfPaths][n];
    scale = new long[numberOfPaths];
    for (int i = 0; i < numberOfPaths; i++) {
      scale[i] = 1;
    }
    random = new Random();


    // BEGIN BACKTRACKING AND STORING SOLUTIONS
    // Variable to store all valid inequivalent graphs.
    List<List<Integer>> validGraphs = new ArrayList<>();

    // Call main backtracking algorithm to begin finding all valid graphs.
    estimateValidGraphs(validGraphs, new ArrayList<>(), 1, 0);

    // Calculate averages of all paths
    long[] averages = calculateAverages();

    // print estimates
    System.out.println("Estimated nodes for each level for n = " + n);
    output += "Estimated nodes for each level for n = " + n + "\n";

    for (int i = 1; i <= averages.length; i++) {
      System.out.print("Level " + i + ":\t");
      output += "Level " + i + ":\t";
      long num = averages[i - 1];
      System.out.println(String.format("%,d", num));
      output += String.format("%,d", num);
      output += "\n";
      if (num == 0) break;
    }

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
  This method is the main backtrack-estimation algorithm to estimate the number of
  nodes at each level of the search tree.
  It initiates 5 random paths from level 1.
   */
  private static void estimateValidGraphs(
          List<List<Integer>> validGraphs,
          List<Integer> partialSolution,
          int c,
          int p // the path number
  ) {
    for (int candidate : candidates) {
      if (isValidPartialSolution(partialSolution, candidate)) {
        D.get(p).get(c - 1).add(candidate); // record acceptable candidates
        d[p][c - 1]++; // increase number of acceptable candidates for this path and level
      }
    }

    // no need to continue if no candidates
    if (d[p][c - 1] == 0) return;

    // from backtrack estimation algorithm on slides
    estimate[p][c - 1] = scale[p] * d[p][c - 1];
    scale[p] *= d[p][c - 1];

    // get random index to select a random candidate
    int randomIndex = random.nextInt((D.get(p).get(c - 1).size()));
    int randomCandidate = D.get(p).get(c - 1).get(randomIndex);

    // add random candidate to solution
    List<Integer> newPartialSolution = new ArrayList<>(partialSolution);
    newPartialSolution.add(randomCandidate);
    // NOTE: the above 4 lines of code do nothing for c = 1, but are used for subsequent levels
    // INSTEAD: below if block handles level 1 so we can start 5 different paths
    if (c == 1) { // start 5 different paths
      // copy results above to all paths for level 1
      for (int i = 1; i < 5; i++) {
        estimate[i][c - 1] = estimate[0][c - 1];
        scale[i] = scale[0];
      }

      // populate set with 5 random candidates
      Set<Integer> randomIndices = new HashSet<>();
      while (randomIndices.size() < 5) {
        randomIndices.add(random.nextInt(D.get(p).get(0).size()));
      }

      // start 5 unique paths with the 5 random level 1 candidates
      for (int index : randomIndices) {
        List<Integer> newPath = new ArrayList<>();
        newPath.add(D.get(0).get(0).get(index));
        estimateValidGraphs(validGraphs, newPath, c + 1, p++);
      }

    } else if (c < n) { // path 2 and beyond
      // continue to next level
      estimateValidGraphs(validGraphs, newPartialSolution, c + 1, p);
    } else {
      // Processing solution.
      // Not bothering to check for isomorphism since we are just estimating
      // number of nodes.
      validGraphs.add(newPartialSolution);
    }
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
  This method accepts user input for the value of n.
  Includes full validation checking.
  Only accepts even values between 8 and 16 inclusive.
   */
  private static int getUserInput() {
    Scanner scanner = new Scanner(System.in);
    int n;

    while (true) {
      System.out.print("Please enter a value for n (even integer between 8 and 16): ");
      String input = scanner.nextLine().trim();

      try {
        n = Integer.parseInt(input);

        if (n >= 8 && n <= 16 && n % 2 == 0) {
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

  /*
  This method takes the estimate results from the 5 different paths and
  calculates the averages for each level.
   */
  private static long[] calculateAverages() {
    long[] averageResults = new long[n];

    for (int i = 0; i < n; i++) {
      long temp = 0;
      for (int j = 0; j < numberOfPaths; j++) {
        temp += estimate[j][i];
      }
      temp /= numberOfPaths;
      averageResults[i] = temp;
    }

    return averageResults;
  }
}