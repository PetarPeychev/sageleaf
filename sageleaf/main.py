import os
import sys

from sageleaf.lex import Lexer
from sageleaf.parse import Parser
from sageleaf.compile import Compiler


def main():
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        code = f.read()

    tokens = Lexer(code).tokenize()
    ast = Parser(tokens).parse()
    print(ast)
    # asm = Compiler(ast).compile()

    # with open("hello.asm", 'w') as f:
    #     f.write(asm)
    # os.system("nasm -f elf64 -o hello.o hello.asm")

    # os.system("ld -o hello hello.o")

    # os.system("./hello")
    # os.system("rm hello.asm hello.o hello")


if __name__ == '__main__':
    main()
