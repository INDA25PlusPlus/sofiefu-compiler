import parser

variables = set()
def generate_cpp(node, indent):
    if node.node_type == "program":
        for child in node.children:
            generate_cpp(child, indent)
        
    elif node.node_type == "assignment":
        print(indent*"    ", end="")
        if node.children[0].value not in variables:
            print("int ", end="")
        generate_cpp(node.children[0], indent)
        print("=", end="")
        generate_cpp(node.children[1], indent)
        print(";")
    elif node.node_type == "while":
        print(indent*"    " + "while(", end="")
        generate_cpp(node.children[0], indent)
        print("){")
        for child in node.children[1:]:
            generate_cpp(child, indent+1)
        print(node.value, end="")
        print(indent*"    " + "}")
    elif node.node_type == "print":
        print(indent*"    " + "cout << ", end="")
        generate_cpp(node.children[0], indent)
        print(";")

    elif node.node_type == "comparison":
        generate_cpp(node.children[0], indent)
        print(node.value, end="")
        generate_cpp(node.children[1], indent)

    elif node.node_type == "addition":
        for child in node.children:
            generate_cpp(child, indent)
            if child != node.children[-1]:
                print("+", end="")

    elif node.node_type == "term":
        generate_cpp(node.children[0], indent)

    elif node.node_type == "variable":
        variables.add(node.value)
        print(node.value, end="")

    elif node.node_type == "number":
        print(node.value, end="")


generate_cpp(parser.root_node, 0)

