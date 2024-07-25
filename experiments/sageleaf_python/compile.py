class Compiler:
    def __init__(self, ast: dict):
        self.ast = ast
        self.data: list[bytes] = []

        self._collect_data()

        for statement in self.ast["statements"]:
            if (
                statement["type"] == "function_definition"
                and statement["name"] == "main"
            ):
                self.main = statement

    def compile(self) -> str:
        output = ""
        output += "section .data\n"

        for i, d in enumerate(self.data):
            output += f"\tstr_{i:04d} db {",".join([hex(b) for b in d])}\n"

        output += "\n"
        output += "section .text\n"
        output += "\n"
        output += "\tglobal _start\n"
        output += "\n"
        output += "_start:\n"

        for statement in self.main["body"]:
            if statement["type"] == "expression_statement":
                expression = statement["expression"]
                if expression["type"] == "function_call":
                    if expression["name"] == "print":
                        for arg in expression["arguments"]:
                            val = arg["value"]
                            output += "\tmov rax, 1\n"
                            output += "\tmov rdi, 1\n"
                            output += f"\tmov rsi, str_{val:04d}\n"
                            output += f"\tmov rdx, {len(self.data[val])}\n"
                            output += "\tsyscall\n\n"
                    else:
                        raise Exception(f"Unknown function call: {expression}")
                else:
                    raise Exception(f"Unknown expression: {expression}")
            elif statement["type"] == "return":
                exit_code = statement["value"]["value"]
                output += "\tmov rax, 60\n"
                output += f"\tmov rdi, {exit_code}\n"
                output += "\tsyscall\n\n"
            else:
                raise Exception(f"Unknown statement: {statement}")

        return output

    def _collect_data(self):
        def transformation(self, node: dict) -> dict:
            if node["type"] == "string":
                self.data.append(bytes(node["value"], "utf-8"))
                return node | {"value": len(self.data) - 1}
            return node

        self._transform(transformation)

    def _transform(self, func):
        self.ast = self._transform_recursive(func, self.ast)

    def _transform_recursive(self, func, node: dict) -> dict:
        new_node: dict = {}
        for k, v in node.items():
            if isinstance(v, dict):
                new_node[k] = self._transform_recursive(func, v)
            elif isinstance(v, list):
                new_node[k] = [self._transform_recursive(func, i) for i in v]
            else:
                new_node[k] = v
        return func(self, new_node)
