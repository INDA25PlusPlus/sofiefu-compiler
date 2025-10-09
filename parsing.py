


code = """
a = 0
b = 1
i = 0
while i < n:
    summa = a + b
    a = b
    b = summa
    i = i + 1
print(a)
"""
tokens = []

def tokenize(text=code):
    pos = 0
    i = 0
    while i < len(text):
        ch = text[i]

        if ch.isspace():
            i += 1
            continue

        if ch == "<":
            tokens.append(("comparator", "<"))
            i += 1
            continue
        elif ch == "+":
            tokens.append(("addition", "+"))
            i += 1
            continue
        elif ch == "=":
            tokens.append(("assignment", "="))
            i += 1 
            continue
        elif ch == "(":
            tokens.append(("(", "("))
            i += 1
            continue
        elif ch == ")":
            tokens.append((")", ")"))
            i += 1
            continue 
        elif ch == ":":
            tokens.append((":", ":"))
            i += 1
            continue

        if ch.isdigit():
            tokens.append(("number", ch))
            i += 1
            continue
        
        
        if ch.isalpha() or ch == "_": 
            i += 1
            word = ch
            while i < len(text) and (text[i].isalnum() or text[i]=="_"): #alnum=alphanumeric
                word += text[i]
                i += 1

            if word == "while":
                tokens.append((word, word))
            elif word == "print":
                tokens.append((word, word))
            else:
                tokens.append(("variable", word))
            continue

pos = 0
def ast(space, val):
    print(space * "     ", "[" + val[0]+"["+val[1]+"]]")
def pop_token(expected_type):
    global pos
    if pos >= len(tokens) or tokens[pos][0] != expected_type:
        print("Error")
        exit(0)
    
    pos += 1    
    return tokens[pos-1][1]

def parse_variable(dep):
    ast(dep, tokens[pos])
    return pop_token("variable")
def parse_number(dep):
    ast(dep, tokens[pos])
    return pop_token("number")
def parse_comparator(dep):
    ast(dep, tokens[pos])
    return pop_token("comparator")

def parse_while(dep):
    pop_token("while")

    parse_variable(dep+1)
    parse_comparator(dep+1)
    parse_variable(dep+1)
    pop_token(":")

def parse_print(dep):
    pop_token("print")
    ast(dep, ("print", "print"))

    pop_token("(")
    parse_variable(dep+1)
    pop_token(")")


def parse_assignment(dep):
    var = pop_token("variable")
    pop_token("assignment")

    ast(dep, ("assignment", "="))
    ast(dep+1, ("variable", var))
    parse_addition(dep+1)


def parse_term(dep):
    global pos
    ast(dep, ("term", "t"))

    if tokens[pos][0] == "variable":
        return parse_variable(dep+1)
    else:
        return parse_number(dep+1)

def parse_addition(dep):
    ast(dep, ("addition", "+"))
    parse_term(dep+1)

    if tokens[pos][0] == "addition":
        pop_token("addition")
        parse_term(dep+1)
    


def parse_code(dep=0):
    global pos
    while pos < len(tokens):
        token = tokens[pos][0]
        if token == "while":
            parse_while(dep)
        elif token == "print":
            parse_print(dep)
        elif token == "variable":
            parse_assignment(dep)

tokenize()
print(tokens)
parse_code()
