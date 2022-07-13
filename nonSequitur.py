import re, sys

try:
    f_name = sys.argv[1]
except IndexError:
    f_name = input()

with open(f_name) as file:

    def split_line(line):
        word = ""
        split = []
        for i in line.split():
            if i[-1:] == "\"":
                word += i
                split.append(word)
                word = ""
            elif i[:1] == "\"":
                word += i
                word += " "
            else:
                split.append(i)
        return split
                


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

        for word in split_line(current_line):
            if len(word) > 1:
                if word[0] == "$":
                    try:
                        current_line = current_line.replace(word, str(variables[word[1:]]))
                    except:
                        print(f"Line {line_num + 1}: \"{word}\" is not defined")
                elif word[0] == "(" and word[1]=="$":
                    try:
                        current_line = current_line.replace(word[1:], str(variables[word[2:]]))
                    except:
                        print(f"Line {line_num + 1}: \"{word[2:]}\" is not defined")

        '''if line contains brackets, evalute the value of the brackets, and replace the brackets with the value of the brackets'''
        if current_line.count("(") > 0:
            try:
                current_line = re.sub(r'\(([^()]+)\)', lambda x: str(eval(x.group(1))), current_line)
            except:
                print(f"Line {line_num + 1}: Brackets cannot be evaluated")
                break

        command = split_line(current_line)[0]
        
        if command == "GOTO":
            if len(split_line(current_line)) == 1:
                print(f"Line {line_num + 1}: GOTO command requires a label")
                break
            next_marker = split_line(current_line)[1]
            if not next_marker in markers:
                print(f"Line {line_num + 1}:Marker \"{next_marker}\" not found")
                break
            if len(split_line(current_line)) == 4 and split_line(current_line)[2] == "IF":
                if split_line(current_line)[3] == "True":
                    line_num = markers.get(next_marker)
                    continue
                else:
                    line_num += counter
                    line_num = line_num%no_of_lines
                    continue
            elif len(split_line(current_line)) == 3:
                print(f"Line {line_num + 1}: IF command requires a condition")
                break
            elif len(split_line(current_line)) > 4:
                print(f"Line {line_num + 1}: Invalid GOTO IF command")
                break
            elif len(split_line(current_line)) == 2:
                line_num = markers.get(next_marker)
                continue
            else:
                print(f"Line {line_num + 1}: Invalid GOTO command")
                break
        elif command == "END":
            break
        elif command == "COUNTER":
            if len(split_line(current_line)) != 2:
                print(f"Line {line_num + 1}:No value given for COUNTER")
                break
            if split_line(current_line)[1] == "++":
                counter += 1
            elif split_line(current_line)[1] == "--":
                counter -= 1
            elif not split_line(current_line)[1].isdigit():
                print(f"Line {line_num + 1}:Invalid value for COUNTER")
                break
            else:
                counter = int(split_line(current_line)[1])
        elif command == "VAR":
            if len(split_line(current_line)) != 3:
                print(f"Line {line_num + 1}:Invalid variable declaration")
                break
            variables[split_line(current_line)[1]] = split_line(current_line)[2]
        elif command == "INPUT":
            if len(split_line(current_line)) != 2:
                print(f"Line {line_num + 1}:Invalid input declaration")
                break
            variables[split_line(current_line)[1]] = input()
        elif command == "PRINT":
            [print(i, end = " ") for i in split_line(current_line)[1:]]
            print()
        elif command == ">":
            continue
        else:
            print(f"Line {line_num + 1}:Invalid command \"{command}\"")
            break

        

        #print(current_line)
        line_num += counter
        line_num = line_num%no_of_lines

