import argparse
import random
import time



def read_cnf(path):
    clauses = []
    clause = []
    with open(path,'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('c'):
                continue
            if line.startswith("p"):
                parts = line.split()
                num_variables = int(parts[2])
                num_clauses = int(parts[3])
                continue 
            for number in map(int,line.split()):
                if number == 0:
                    clauses.append(clause)
                    clause = []
                else:
                    clause.append(number)
    return clauses, num_variables, num_clauses        

def is_satisfied(clause, assignment):
    for literal in clause:
        variable = abs(literal)

        if literal > 0 and assignment[variable]:
            return True

        if literal < 0 and not assignment[variable]:
            return True

    return False


def break_count(variable, clauses, assignment):
    satisfied_before = [clause for clause in clauses
        if is_satisfied(clause, assignment)
    ]

    assignment[variable] = not assignment[variable]
    try:
        count = sum(
            not is_satisfied(clause, assignment)
            for clause in satisfied_before)
    
    
    
    finally:
        assignment[variable] = not assignment[variable]

    return count


def walksat(clauses, num_variables, p=0.7, max_flips=10000, max_restarts=100, timeout=60.0, seed=None,
):
    if not 0 <= p <= 1:

        raise ValueError("p must be between 0 and 1.")


    if max_flips < 1 or max_restarts < 0:
        raise ValueError(
            "max_flips must be positive and max_restarts cannot be negative.")



    if not 0 < timeout < float("inf"):
        raise ValueError("timeout must be positive and finite.")

    rng = random.Random(seed)


    start = time.perf_counter()

    if any(not clause for clause in clauses):
        
        return None, "UNSAT"

    for _ in range(max_restarts + 1):
        
        assignment = [False] + [
            bool(rng.getrandbits(1))
           
           
            for _ in range(num_variables)]

        for step in range(max_flips + 1):
            
            if time.perf_counter() - start >= timeout:
               
                return None, "TIMEOUT"

            unsatisfied = [clause for clause in clauses if not is_satisfied(clause, assignment)]

            if not unsatisfied:
                return assignment, "SAT"

            if step == max_flips:
                break


            clause = rng.choice(unsatisfied)
            
            candidates = [abs(literal) for literal in clause]


            chosen_variable = None
            minimum_break = None

            best_variables = []

            for variable in candidates:
             
             
                if time.perf_counter() - start >= timeout:
                  
                    return None, "TIMEOUT"

                count = break_count(variable, clauses, assignment)

                if count == 0:
                
                    chosen_variable = variable
                
                
                    break

                if minimum_break is None or count < minimum_break:
               
                    minimum_break = count
             
                    best_variables = [variable]
                elif count == minimum_break:

                    best_variables.append(variable)

            if chosen_variable is None:
                if rng.random() < p:

                    chosen_variable = rng.choice(best_variables)
                else:

                    chosen_variable = rng.choice(candidates)

            assignment[chosen_variable] = not assignment[chosen_variable]

    return None, "UNKNOWN"



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--p", type=float, default=0.7)
    parser.add_argument("--max-flips", type=int, default=10000)
    parser.add_argument("--max-restarts", type=int, default=100)
    parser.add_argument("--timeout", type=float, default=60.0)
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()



    clauses, num_variables, num_clauses = read_cnf(args.input)

    start = time.perf_counter()

    assignment, status = walksat(clauses, num_variables, p=args.p, max_flips=args.max_flips, max_restarts=args.max_restarts, timeout=args.timeout, seed=args.seed,)
    elapsed = time.perf_counter() - start

    print(f"Status: {status}")
    print(f"Variables: {num_variables}")
    print(f"Clauses: {num_clauses}")
    print(f"Runtime: {elapsed:.6f} seconds")

    if assignment is not None:
        if not all(is_satisfied(clause, assignment) for clause in clauses):
            
            raise RuntimeError("The returned assignment is invalid.")

        literals = [str(variable if assignment[variable] else -variable) for variable in range(1, num_variables + 1)
        ]

        print("Assignment:", " ".join(literals), "0")
        print("Verified: every clause is satisfied.")


if __name__ == "__main__":
    main()