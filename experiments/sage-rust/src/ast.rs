struct Module {
    name: String,
    body: Vec<Declaration>,
}

enum Declaration {
    FunctionDeclaration {
        name: String,
        args: Vec<FunctionArgument>,
        return_type: Type,
        body: Vec<Statement>,
    },
}

struct FunctionArgument {
    name: String,
    type_: Type,
}

enum Type {
    UnitType,
}

enum Statement {
    ExpressionStatement { expression: Expression },
}

enum Expression {
    StringLiteral { value: String },
    FunctionCall { name: String, args: Vec<Expression> },
}
