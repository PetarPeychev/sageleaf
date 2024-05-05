%token <int> INT
%token PLUS MINUS TIMES DIVIDE LPAREN RPAREN
%token EOF

%start main
%type <int> main

%%

main:
  | expr EOF            { $1 }

expr:
  | term                { $1 }
  | expr PLUS term      { $1 + $3 }
  | expr MINUS term     { $1 - $3 }

term:
  | factor              { $1 }
  | term TIMES factor   { $1 * $3 }
  | term DIVIDE factor  { $1 / $3 }

factor:
  | INT                 { $1 }
  | LPAREN expr RPAREN  { $2 }
