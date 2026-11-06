# Project 2

## Part 1: The Robot Needs Help with Boolean SAT

![Robot seeking help with Boolean SAT](../pics/robot_boolean_sat.png)

You receive a new—but corrupted—transmission from the robot. It appears that the robot is headed to the Galactic Games, where it will compete against other robots to solve Boolean satisfiability (SAT) problems. This involves assigning *True* or *False* to each variable so that the given Boolean formula evaluates to *True*. The robot wants to use WalkSAT but does not know which restart probability will work best or which heuristics to use.

**Partner 1:** Implement the WalkSAT algorithm presented in the lecture as `robot_solver.py` and select an initial value for the parameter $p$. Your code should accept a `.cnf` file as input, following the specifications in the **CNF File Format** section below.

The second part of the transmission reveals that the robot may compete in a different challenge: creating a Boolean expression that is difficult to solve so that it can defeat the other robot contestants.

**Partner 2:** Implement `robot_generator.py`, which generates random Boolean expressions in conjunctive normal form (CNF) and writes them to a `.cnf` file. The generated Boolean expressions must be satisfiable and depend on at least two parameters.

### How Can You Generate Interesting, Satisfiable Random Boolean Expressions?

Recall the Dinner Party at Hogwarts seating assignment problem from the lecture. As discussed in class, the problem's constraints can be written as Boolean clauses. If you begin with a problem that is known to be solvable—or construct one with a known solution—the corresponding CNF formula will also be satisfiable. The objective is to construct problems whose CNF encodings are difficult for the solver.

For instance, consider the trivial seating assignment in which guest 1 sits in seat 1, guest 2 sits in seat 2, and so on. This assignment is the solution. You can generate different expressions by randomly creating different sets of friendships and enemies that do not invalidate the seating assignment. For example, guests $i$ and $i+1$ cannot be enemies. The number of friendship pairs ($p$) and the number of enemy pairs ($q$) you choose to create are the two parameters. Note that the number of guests, $n$, controls the size of the Boolean expressions but does not influence how many friendship and enemy clauses you add.

Having many enemy constraints can make the problem tightly constrained and easy to solve, as many possible seating assignments are ruled out and therefore easy to eliminate during a search. In such cases, the WalkSAT algorithm may quickly find a solution. Similarly, having too few friendship or enemy constraints can make the problem underconstrained and easy to solve, as many different seating assignments can satisfy all the constraints. In other words, many assignments of *True* or *False* to the Boolean variables make the expression *True*. However, for some values of $p$ and $q$, the problem yields a particularly challenging Boolean expression that WalkSAT struggles to solve.

### How Can You Find Good Problems to Convert into CNFs?

Choose an existing problem or develop your own. Examples include:

- **Dinner party planning:** Some number of guests are coming for dinner and will be seated at a single large table, with the host and hostess at the ends. Some pairs of guests have indicated that they must sit next to each other. Other pairs have indicated that they absolutely refuse to sit next to each other. Find a seating arrangement that satisfies all the constraints.
- **Wedding party planning:** Some number of guests are invited to a wedding and will be seated at some number of tables of a fixed size. Some pairs of guests must be together, and some must be separated. Find an arrangement that satisfies all the constraints.
- **Putting away the groceries:** Given grocery items of various types and sizes—boxes of cereal, jars of peanut butter, cans of soup, and so on—find a way to fit all of them into a pantry of a given size.
- **Robot navigation:** A robot must make its way through an environment with obstacles. It can move up, down, left, or right and must find a path from a start position to a goal position.
- **Pathfinding in a graph:** Given a graph, find a path from the start state to the goal state.
- **Hamiltonian cycles:** Given a graph, find a Hamiltonian cycle: a path through the graph that begins and ends at the same vertex and visits every vertex exactly once.
- **Jigsaw puzzle:** Given a set of jigsaw puzzle pieces, each with four sides of specified types, arrange the pieces in a grid so that only sides of the right types touch one another.

Bonus points are available for presenting the problem as a creative story—for example, Hagrid plans a party at Hogwarts for $n$ Cal Poly students, among whom there are $k$ secret crushes.

Choose or create a problem, describe its narrative, and encode it as a Boolean formula in CNF. There should be at least two parameters that control which clauses you generate and how constrained your problem is. For now, select initial values for $p$ and $q$.

### Part 1 Objective

**Partner 1:** Implement `robot_solver.py` with an initial default value for the restart parameter $p$.

**Partner 2:** Implement `robot_generator.py` with initial values for the parameters $p$ and $q$.

**Both partners:**

- Collaborate to test and debug both implementations.
- Agree on the number of items, dragons, or other entities in your problem or story, $n$, so that the generated CNF formulas can be solved in approximately 10 seconds.
- Write a joint preliminary report with a graph showing the distribution of the solver's running times, in seconds, for 100 randomly generated CNFs. State your default parameter choices and explain your implementation decisions. **Important:** Your choices of data structures and implementation methods for both parts may have a significant effect on runtime.

### Submit via Canvas by November 5 at 11:59 p.m.

- `prelim_report.pdf`
- `code.zip`

### CNF File Format

Both programs must use plain-text `.cnf` files following the simplified DIMACS convention:

1. **Comments:** Optional comment lines begin with `c` and appear before the header.
2. **Header:** Include exactly one header of the form `p cnf V C`, where `V` is the number of Boolean variables and `C` is the number of clauses. Number the variables consecutively from `1` to `V`.
3. **Literals:** Represent a positive literal $x_i$ by `i` and a negative literal $\neg x_i$ by `-i`. Every literal must have an absolute value between `1` and `V`.
4. **Clauses:** Write each clause on a separate line as space-separated literals followed by `0`. Within a clause, literals must be distinct, and a variable and its negation must not both appear. The number of clauses must match `C`.

A clause combines its literals with logical OR ($\lor$); the formula combines its clauses with logical AND ($\land$). The terminating `0` is a delimiter, not a variable or a truth value. See also [Aalto University's DIMACS CNF explanation](https://users.aalto.fi/~tjunttil/2021-DP-AUT/notes-sat/solving.html#the-dimacs-cnf-file-format).

For example, the formula

$$
(x_1 \lor \neg x_2 \lor x_3) \land (\neg x_1 \lor x_2) \land (\neg x_3)
$$

is represented as:

```text
c Example with three variables and three clauses
p cnf 3 3
1 -2 3 0
-1 2 0
-3 0
```

Here, `-3 0` is a clause containing the single literal $\neg x_3$. The example is satisfiable: setting all three variables to *False* satisfies every clause.

## Part 2: Learning from Your Opponent

Each partner aims to outperform the other by improving the generator to create more difficult instances or improving the solver to reduce solution time.

Explore the parameter space of your implementation. Plot performance with running time in seconds on the y-axis and the parameter value on the x-axis. Use the results to improve your solver or generator.

**Partner 1:** Using your `upgraded_robot_solver` against the `robot_generator` from Part 1, repeat the running-time comparison across 100 random CNFs.

**Partner 2:** Using your `upgraded_robot_generator` against the `robot_solver` from Part 1, repeat the running-time comparison across 100 random CNFs.

By how much did your implementation improve?

What performance do you predict when `upgraded_robot_solver` is evaluated against `upgraded_robot_generator`?

### Submit via Canvas by November 10 at 11:59 p.m.

- `prelim_report2.pdf`
- `code2.zip`

## Part 3: Further Iterations

Can you improve performance further by repeating the parameter search against your partner's upgraded implementation? Starting from your upgraded versions, each partner should search their parameter space again while keeping the opponent's upgraded version fixed. Plot the results and select new parameter values. Evaluate each revised implementation against the same fixed opponent over 100 randomly generated CNFs, and compare its performance with the previous iteration. How much additional improvement do you observe, and how do the selected parameter values change? Plot the magnitude of the changes in your parameters across several cycles.

### Submit via Canvas by November 11 at 11:59 p.m.

- `prelim_report3.pdf`
- `code3.zip`

## Final Submission and the Big Competition

CNF problem generators and solvers will compete to determine which generators produce the hardest problems and which solvers perform best. Each generated CNF instance will be tested against every competing solver, with problem generators ranked by the difficulty of their instances and solvers ranked by their performance. Bonus points will be awarded to the top-ranked competitors.

### Submit by November 11 at 11:59 p.m.

- `final_report.pdf`
- `final_code.zip`
