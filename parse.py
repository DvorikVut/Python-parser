#Author: Artem Dvorychanskyi xdvory00


import sys
import xml.etree.ElementTree as ET
import xml.dom.minidom
import re

operation_code = [

    ['MOVE', 'var', 'symb'],
    ['CREATEFRAME'],
    ['PUSHFRAME'],
    ['POPFRAME'],
    ['DEFVAR', 'var'],
    ['CALL', 'label'],
    ['RETURN'],
    ['PUSHS', 'symb'],
    ['POPS', 'var'],
    ['ADD', 'var', 'symb', 'symb'],
    ['SUB', 'var', 'symb', 'symb'],
    ['MUL', 'var', 'symb', 'symb'],
    ['IDIV', 'var', 'symb', 'symb'],
    ['LT', 'var', 'symb', 'symb'],
    ['GT', 'var', 'symb', 'symb'],
    ['EQ', 'var', 'symb', 'symb'],
    ['AND', 'var', 'symb', 'symb'],
    ['OR', 'var', 'symb', 'symb'],
    ['NOT', 'var', 'symb'],
    ['INT2CHAR', 'var', 'symb'],
    ['STRI2INT', 'var', 'symb', 'symb'],
    ['READ', 'var', 'type'],
    ['WRITE', 'symb'],
    ['CONCAT', 'var', 'symb', 'symb'],
    ['STRLEN', 'var', 'symb'],
    ['GETCHAR', 'var', 'symb', 'symb'],
    ['SETCHAR', 'var', 'symb', 'symb'],
    ['TYPE', 'var', 'symb'],
    ['LABEL', 'label'],
    ['JUMP', 'label'],
    ['JUMPIFEQ', 'label', 'symb', 'symb'],
    ['JUMPIFNEQ', 'label', 'symb', 'symb'],
    ['EXIT', 'symb'],
    ['DPRINT', 'symb'],
    ['BREAK']
]

Header = False
line_number = 0

def argument_check(argv):
    if len(argv) == 2:
        if argv[1] == "--help":
            print("""Welcome to IPPCode24 parser!

                    Script takes IPPCode24 as input, creates XML representation and sends it to output
                    
                    Usage: python3 parser.py [options] <[file]
                    Default options:
                    --help prints help info
                 """)
            sys.exit(0)
        else:
            sys.stderr.write("Unknown argument")
            sys.exit(10)
    if len(argv) > 2:
        sys.stderr.write("Invalid number of arguments")
        sys.exit(10)

def string_gen(string):
    string = string.replace("&", "&amp;")
    string = string.replace("<", "&lt;")
    string = string.replace(">", "&gt;")
    string = string.replace("'", "&apos;")
    string = string.replace("\"", "&quot;")
    return string


def remove_comments(line):
    if line.find("#") != -1:
        line = line[:line.find("#")]
    return line


def operation_check(opcode):
    for i in range(len(operation_code)):
        if opcode.lower() == operation_code[i][0].lower():
            return i
    return -1
            

def arguments_parsing(line, opcode_num):
    if len(line) != len(operation_code[opcode_num]):
        sys.stderr.write("Wrong number of arguments")
        sys.exit(23)
    if(len(line) == 1):
        return 0
    for i in range(1, len(line)):
        
        if operation_code[opcode_num][i] == "var":
            regex_patter = r'^(GF|TF|LF)@[a-zA-Z_\-\$&%\*\!\?][a-zA-Z0-9_\-\$&%\*\!\?]*$'
            if not re.match(regex_patter, line[i]):
                sys.stderr.write("Wrong variable format")
                sys.exit(23) 
            argument = ET.SubElement(instruction, f'arg{i}',type = "var").text = line[i]

        
        elif operation_code[opcode_num][i] == "symb":
            if re.match(r'^(GF|TF|LF)@[a-zA-Z_\-\$&%\*\!\?][a-zA-Z0-9_\-\$&%\*\!\?]*$', line[i]):
                type = "var"
                value = line[i]
                argument = ET.SubElement(instruction, f'arg{i}', type = type).text = value
            elif re.match(r'^int@[-+]?[0-9]+$', line[i]):
                type = "int"
                value = line[i][line[i].find("@")+1:]
                line[i] = string_gen(line[i])
                argument = ET.SubElement(instruction, f'arg{i}', type = type).text = value
            elif re.match(r'^bool@(true|false)$', line[i]):
                type = "bool"
                value = line[i][line[i].find("@")+1:]
                line[i] = string_gen(line[i])
                argument = ET.SubElement(instruction, f'arg{i}', type = type).text = value
            elif re.match(r'^nil@nil$', line[i]):
                type = "nil"
                value = line[i][line[i].find("@")+1:]
                line[i] = string_gen(line[i])
                argument = ET.SubElement(instruction, f'arg{i}', type = type).text = value
            elif re.match (r'^string@.*$', line[i]):
                if line[i].find("@") != -1:
                    type = line[i][:line[i].find("@")]
                    value = line[i][line[i].find("@")+1:]
                line[i] = string_gen(line[i])
                argument = ET.SubElement(instruction,f'arg{i}', type = type).text = value
            else:
                sys.stderr.write("Wrong symbol format")
                sys.exit(23)
        
        
        elif operation_code[opcode_num][i] == "label":
            regex_patter = r'^[a-zA-Z_\-\$&%\*\!\?][a-zA-Z0-9_\-\$&%\*\!\?]*$'
            if not re.match(regex_patter, line[i]):
                sys.stderr.write("Wrong label format")
                sys.exit(23)
            argument = ET.SubElement(instruction, f'arg{i}', type = "label").text = line[i]
        
        
        elif operation_code[opcode_num][i] == "type":
            regex_patter = r'^(int|bool|string)$'
            if not re.match(regex_patter, line[i]):
                sys.stderr.write("Wrong type format")
                sys.exit(23)
            argument = ET.SubElement(instruction, f'arg{i}', type = "type").text = line[i]


argument_check(sys.argv) 
for line in sys.stdin:
    line = remove_comments(line)
    line = line.split()
    if(Header == False):

        if line == [".IPPcode24"]:
            Header = True
            line_number += 1
            program = ET.Element("program", language="IPPcode24")

        elif line == []:
            continue

        else:
            sys.stderr.write("Wrong header")
            sys.exit(21)
        
    else:
        if line == []:
            continue

        if line == [".IPPcode24"]:
            sys.exit(23)
            
        else:
            opcode = operation_check(line[0])
            if opcode == -1:
                sys.stderr.write("Wrong operation code")
                sys.exit(22)
            line_number += 1
            instruction = ET.SubElement(program, "instruction", order=str(line_number-1), opcode=line[0].upper())
            arguments_parsing(line, opcode)

tree = ET.ElementTree(program)
xml_str = ET.tostring(program)
dom = xml.dom.minidom.parseString(xml_str)
pretty_xml = dom.toprettyxml(indent="   ", encoding="utf-8")
print(pretty_xml.decode("utf-8"))
sys.exit(0)
            