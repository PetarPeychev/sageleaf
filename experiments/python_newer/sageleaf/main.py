import os
import sys

from sageleaf.tokens import Lexer
from sageleaf.ast import Parser


def main():
    filename = sys.argv[1]
    with open(filename, "r") as f:
        code = f.read()

    tokens = Lexer(code).tokenize()
    print(" ".join([str(t) for t in tokens]))

    ast = Parser(tokens).parse()
    print(ast)

    # print(json.dumps(asdict(ast)))
    # asm = Compiler(ast).compile()

    # with open("hello.asm", 'w') as f:
    #     f.write(asm)
    # os.system("nasm -f elf64 -o hello.o hello.asm")

    # os.system("ld -o hello hello.o")

    # os.system("./hello")
    # os.system("rm hello.asm hello.o hello")


if __name__ == "__main__":
    main()
