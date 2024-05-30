import os
import sys

from .lex import Lexer
from .parse import Parser
from .compile import Compiler


def main():
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        code = f.read()

    lexer = Lexer(code)
    tokens = lexer.tokenize()
    # for token in tokens:
    #     t = token["type"]
    #     if "value" in token:
    #         t += f"({token['value']})"
    #     print(t)

    parser = Parser(tokens)
    ast = parser.parse()
    # print(json.dumps(ast))

    compiler = Compiler(ast)
    asm = compiler.compile()
    # print(asm)

    with open("hello.asm", 'w') as f:
        f.write(asm)
    os.system("nasm -f elf64 -o hello.o hello.asm")

    os.system("ld -o hello hello.o")

    os.system("./hello")
    os.system("rm hello.asm hello.o hello")


if __name__ == '__main__':
    main()
