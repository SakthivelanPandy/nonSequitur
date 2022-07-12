import re, sys

try:
    f_name = sys.argv[1]
except IndexError:
    f_name = input()

with open(f_name) as file:

    program = file.readlines()
    
    '''search through file for word MARKER and add line number and line to dictionary'''
    markers = {}
    for i, line in enumerate(program):
        if line.startswith("MARKER"):
            markers[line.split()[1]] = i

    variables = {}
        

    line_num = 0
    counter = 1
    no_of_lines = len(program)

    while True:
        current_line = program[line_num]

        for word in current_line.split():
            if word[0] == "$":
                current_line = current_line.replace(word, str(variables[word[1:]]))
            elif word[0] == "(" and word[1]=="$":
                current_line = current_line.replace(word[1:], str(variables[word[2:]]))

        '''if line contains brackets, evalute the value of the brackets, and replace the brackets with the value of the brackets'''
        if current_line.count("(") > 0:
            current_line = re.sub(r'\(([^()]+)\)', lambda x: str(eval(x.group(1))), current_line)

            
        
        if current_line.startswith("GOTO "):
            if len(current_line.split()) > 3 and current_line.split()[2] == "IF":
                if current_line.split()[3] == "True":
                    next_marker = current_line.split()[1]
                    line_num = markers.get(next_marker)
                    continue
                else:
                    line_num += counter
                    line_num = line_num%no_of_lines
                    continue
            next_marker = current_line.split()[1]
            line_num = markers.get(next_marker)
            continue
        
        if current_line == "END" or current_line == "END\n":
            break

        if current_line.startswith("COUNTER "):
            counter = int(current_line.split()[1])

        if current_line.startswith("VAR "):
            variables[current_line.split()[1]] = current_line.split()[2]

        if current_line.startswith("PRINT"):
            [print(i, end = " ") for i in current_line.split()[1:]]
            print("\n")

        

        #print(current_line)
        line_num += counter
        line_num = line_num%no_of_lines

