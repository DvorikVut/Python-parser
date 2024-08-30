## Parser.py

Parser.py is a script that analyzes IPPCode24. It takes the code from input, validates its syntax, and outputs XML representation of IPPCode24.

### Usage

```bash
python3 parse.py [--options] <file_name>
```

### Libraries

- **sys**: Used for handling command-line arguments and printing error messages.
- **xml.etree.ElementTree**: Used for generating an XML representation of the parsed data. It provides a convenient way to work with XML documents in Python, making it easy to create, modify, and traverse XML trees.
- **xml.dom.minidom**: Used to prettify the generated XML output before printing it. This makes the output more readable and understandable for users or other systems consuming the XML data.
- **re**: Used for pattern matching and validation of strings, particularly for checking the format of variable names, labels, symbols, and types.

### Function Descriptions

- **argument_check()**: Checks command-line arguments and handles help messages or invalid arguments.
- **string_gen()**: Generates a sanitized version of a string for XML representation.
- **remove_comments()**: Removes comments from a line in the input file.
- **operation_check()**: Checks if the provided operation code is valid.
- **arguments_parsing()**: Parses arguments of an instruction based on the operation code. This is the main function.

  - It first checks if the number of arguments matches the expected number defined in the `operation_code` list for the given operation.
  - Then it iterates over the arguments starting from index 1, as the opcode is at index 0 in the input line.
  - For each argument, it checks its type based on the operation code. If the argument type is "var", it validates the variable format using a regular expression. If the format is invalid, it exits the script with an error message indicating the wrong variable format.
  - If the argument type is "symb" (symbol), it further validates different types of symbols including variables, integers, booleans, nil, and strings. It uses regular expressions to validate each type and generates a sanitized version of the string for XML representation using the `string_gen` function.
  - For each valid argument, it creates an XML element representing the argument and appends it to the instruction element.

### Implementation

- First, using the argument_check() function, the correctness of command arguments is checked, and --help may be output.
- Then input is split into lines, after which the remove_comments() function is used to remove comments, they are not useful for us.
Inside the line we separate individual words.
- After that we should catch the header, this will be the beginning of IPPCode24. 
- Then we check if the first word of the string is a valid operation code, if yes - run arguments_parsing(), the principle of operation of which is described above.

