with open("fib.txt", "r") as f:
    code = f.read()

class AST:
    def __init__(self, node_type, value):
        self.children = []
        self.node_type = node_type
        self.value = value
tokens = []
indent = []

def get_indent(line):
    return len(line) - len(line.lstrip("    "))
def tokenize(code=code):
    row = 0
    lines = code.strip().splitlines()
    for row in range(len(lines)):
        line = lines[row]

        indent.append(get_indent(line))
        tokens.append([])
        raw_tokens = line.strip().split()
        for token in raw_tokens:
            if token in ["==", "<", ">"]:
                tokens[-1].insert(1, ("comparison", token)) # put first to simplify parsing
            elif token == "+":
                tokens[-1].append(("addition", token))
            elif token == "=":
                tokens[-1].insert(0, ("assignment", "=")) # put first to simplify parsing
            elif token.isdigit():
                tokens[-1].append(("number", token))
            elif token.isalpha(): # alphanumeric
                if token == "while":
                    tokens[-1].append((token, token))
                elif token == "print":
                    tokens[-1].append((token, token))
                else:
                    tokens[-1].append(("variable", token))
                continue



def pop_token(expected_type):
    global pos
    global line
    if line >= len(tokens) or pos >= len(tokens[line]) or tokens[line][pos][0] != expected_type:
        print("Error")
        exit(0)
    pos += 1   
    return tokens[line][pos-1][1]

def parse_variable(parent_node):
    x = pop_token("variable")
    node = AST("variable", x)
    parent_node.children.append(node)

def parse_number(parent_node):
    x = pop_token("number")
    node = AST("number", x)
    parent_node.children.append(node)

def parse_comparison(parent_node):
    x = pop_token("comparison")
    node = AST("comparison", x)
    parent_node.children.append(node)

    parse_addition(node)
    parse_addition(node)

def parse_while(parent_node):
    global line
    pop_token("while")
    node = AST("while", "")
    parent_node.children.append(node)

    parse_comparison(node)

    while_line = line
    line += 1
    while line < len(tokens) and indent[while_line] < indent[line]:
        parse_line(node)

def parse_print(parent_node):
    pop_token("print")
    node = AST("print", "")
    parent_node.children.append(node)

    parse_addition(node)


def parse_assignment(parent_node):
    pop_token("assignment")
    node = AST("assignment", "")
    parent_node.children.append(node)

    parse_variable(node)
    parse_addition(node)


def parse_term(parent_node):
    global pos
    global line
    node = AST("term", "")
    parent_node.children.append(node)

    if tokens[line][pos][0] == "variable":
        return parse_variable(node)
    else:
        return parse_number(node)

def parse_addition(parent_node):
    global pos
    global line 
    node = AST("addition", "")
    parent_node.children.append(node)
    parse_term(node)

    if pos<len(tokens[line]) and tokens[line][pos][0] == "addition":
        pop_token("addition")
        parse_term(node)
    
def generate_ast(node, dep):
    with open("ast.txt", "a") as f:
        f.write(dep * "     " + "[" + node.node_type+"["+ str(node.value) +"]]\n")
    for child in node.children:
        generate_ast(child, dep+1)

root_node = AST("program", "")
# scope = [root_node]
line = 0
pos = 0
def parse_line(parent_node):
    global line
    global pos
    pos = 0
    
    token = tokens[line][pos][0]
    if token == "while":
        parse_while(parent_node)
    elif token == "print":
        parse_print(parent_node)
        line += 1
    elif token == "assignment":
        parse_assignment(parent_node)
        line += 1

def parse_code():
    # parse tokens and create syntax tree
    while line<len(tokens):
        parse_line(root_node)

# turn into tokens
tokenize()
parse_code()

# dfs in the syntax tree to visualize it
with open("ast.txt", "w") as f:
    f.write("This is the syntax tree of fib.txt\n")
generate_ast(root_node, 0)
