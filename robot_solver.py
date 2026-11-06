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

def main():
    print(read_cnf("test.cnf")[0][0])
    print(is_satisfied(read_cnf("test.cnf")[0][0],[0,True,True,False]))
if __name__== "__main__":
    main()