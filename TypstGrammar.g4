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
fragment LETTER: [a-zA-Z];
fragment DIGIT: [0-9];
fragment PERIOD: '.';

MATH_START: '<typst_math_start>';
MATH_END: '<typst_math_end>';

WS: WS_CHAR+ -> skip;

ID:
	LETTER (LETTER | DIGIT)* (PERIOD LETTER (LETTER | DIGIT)*)* {self.setType()};

ADDITIVE_OP: '+' | '-';
MP_OP: '*' | '/' | '\\/';

L_PAREN: '(';
R_PAREN: ')';
L_BRACE: '{';
R_BRACE: '}';
L_BRACKET: '[';
R_BRACKET: ']';
QUOTE: '"';

UNDERSCORE: '_';
CARET: '^';
SEMICOLON: ';';
COMMA: ',';
BANG: '!';

NUMBER:
	DIGIT+ (COMMA DIGIT DIGIT DIGIT)*
	| DIGIT* (COMMA DIGIT DIGIT DIGIT)* PERIOD DIGIT+;

RELATION_OP: '=';

// --------------------------------------------------------------------------------

math: MATH_START relation MATH_END;

relation: relation RELATION_OP relation | expr;

expr: additive;

additive: additive ADDITIVE_OP additive | mp;

mp: mp MP_OP mp | unary;

unary: ADDITIVE_OP unary | postfix+;

postfix: NUMBER;
