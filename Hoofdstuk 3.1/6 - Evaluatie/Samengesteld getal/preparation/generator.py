import os
import random
import subprocess
from typing import Text

# set fixed seed for generating test cases
random.seed(123456789)

# locate evaldir
evaldir = os.path.join('..', 'evaluation')
if not os.path.exists(evaldir):
    os.makedirs(evaldir)

# locate solutiondir
solutiondir = os.path.join('..', 'solution')
if not os.path.exists(solutiondir):
    os.makedirs(solutiondir)

# configuration settings
tab_name = 'Feedback'
settings = f'''
tab name: {tab_name}
python input without prompt: true
block count: multi
input block size: 1
output block size: ends with
comparison: exact match
'''

def is_prime(n):
    flag = True
    for i in range(2,n):
        if n % i == 0:
            flag = False
    return flag

def find_next_prime(n):
    result = n
    if not is_prime(n):
        flag = True
        while flag:
            n +=1
            flag = not is_prime(n)
        result = n
    return result

# generate test data
cases = [(2,), (12,),(24,)]
while len(cases) < 30:
    e = random.randint(1,6)
    n = random.randint(10**(e-1)+1,10**e)
    if random.randint(0,2) == 0:
        n = find_next_prime(n)
    cases.append((n, ))
    
# configure test files
infile = open(os.path.join(evaldir, '0.in'), 'w')
outfile = open(os.path.join(evaldir, '0.out'), 'w')

# generate unit tests
for stdin in cases:
    # add input to input file
    stdin = '\n'.join(f'{line}' for line in stdin)
    print(stdin, file=infile)

    # generate output to output file
    script = os.path.join(solutiondir, 'solution.nl.py')
    process= subprocess.run(
        ['python3', script],
        input=stdin,
        encoding='utf-8',
        capture_output=True
    )
    
    result_lines = process.stdout.split("\n")
    for line in result_lines:
        if not(line.startswith( 'Geef' )):
            print(line)
            print(line, file=outfile, end='\n')

    # add stdout to output file
    # print(stdout, file=outfile, end='')

# add settings to output file
print('-' * 41 + settings, file=outfile, end='')
