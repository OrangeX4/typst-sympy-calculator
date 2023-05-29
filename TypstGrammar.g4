grammar TypstGrammar;

@lexer::members {
id2type = {}

def setType(self):
    if self.text in self.id2type:
        if hasattr(self, self.id2type[self.text]):
            self.type = getattr(self, self.id2type[self.text])
        else:
            raise Exception("Unknown ID: " + self.text + " for type " + self.id2type[self.text])
    else:
        raise Exception("Unknown ID: " + self.text)
}

options {
	language = Python3;
}

fragment WS_CHAR: [ \t\r\n];
fragment DIGIT: [0-9];
fragment LETTER: [a-zA-Z];

MATH_START: '<typst_math_start>';
MATH_END: '<typst_math_end>';

WS: WS_CHAR+ -> skip;
USELESS_SIGN: [&\\] -> skip;

L_PAREN: '(';
R_PAREN: ')';
L_BRACE: '{';
R_BRACE: '}';
L_BRACKET: '[';
R_BRACKET: ']';
BAR: '|';
EVAL_BAR: '"|"' | 'bar';
QUOTE: '"';

UNDERSCORE: '_';
CARET: '^';
SEMICOLON: ';';
COMMA: ',';
PERIOD: '.';
BANG: '!';
TRANSPOSE: '^T' | '^top';
LIM_APPROACH_SYM: '->';

RELATION_OP: '=' | '==' | '!=' | '<' | '>' | '<=' | '>=';
ADDITIVE_OP: '+' | '-';
MP_OP: '*' | '/' | '\\/';
POSTFIX_OP: BANG | TRANSPOSE;
ACCENT_OP: '<typst_math_accent>';
REDUCE_OP: '<typst_math_reduce>';

FUNC: '<typst_math_func>';
FUNC_MAT: 'mat';
FUNC_LIM: 'lim';
FUNC_INTEGRAL: 'integral';
DIF: 'dif';
DIFF: 'diff';

SYMBOL_BASE: LETTER;

NUMBER:
	DIGIT+ (COMMA DIGIT DIGIT DIGIT)*
	| DIGIT* (COMMA DIGIT DIGIT DIGIT)* PERIOD DIGIT+;

ID:
	LETTER (LETTER | DIGIT)* (PERIOD LETTER (LETTER | DIGIT)*)* {self.setType()};

// --------------------------------------------------------------------------------

math: MATH_START relation MATH_END;

relation: relation RELATION_OP relation | expr;

expr: additive;

additive: additive ADDITIVE_OP additive | mp;

mp: mp MP_OP mp | unary;

unary: ADDITIVE_OP unary | postfix+;

postfix: exp POSTFIX_OP*;

subargs: UNDERSCORE (atom | L_PAREN args R_PAREN);

subexpr: UNDERSCORE (atom | L_PAREN expr R_PAREN);
supexpr: CARET (exp | L_PAREN expr R_PAREN);
subsupexpr: subexpr supexpr | supexpr subexpr;

subassign: UNDERSCORE (atom | L_PAREN (expr | relation) R_PAREN);
supassign: CARET (exp | L_PAREN (expr | relation) R_PAREN);
subsupassign: subassign | supassign | subassign supexpr | supexpr subassign;

eval_at: EVAL_BAR subsupassign;

exp: comp supexpr?;

comp: group | abs_group | func | matrix | reduceit | lim | integral | atom;

group:
	L_PAREN expr R_PAREN
	| L_BRACE expr R_BRACE
	| L_BRACKET expr R_BRACKET;

abs_group: BAR expr BAR;

args: (relation COMMA)* relation COMMA?;

mat_args: (args SEMICOLON)* args SEMICOLON?;

func: FUNC (L_PAREN args R_PAREN | mp);

matrix: FUNC_MAT L_PAREN mat_args R_PAREN;

reduceit: REDUCE_OP subsupassign mp;

lim: FUNC_LIM L_PAREN symbol LIM_APPROACH_SYM expr R_PAREN additive;

integral: FUNC_INTEGRAL subsupexpr? additive DIF symbol;

text: QUOTE .*? QUOTE;

accent: ACCENT_OP L_PAREN expr R_PAREN;

symbol_base: SYMBOL_BASE | text | accent;

symbol: symbol_base subargs?;

atom: NUMBER | symbol;