from ply import yacc
from lexer import tokens as tk
from functools import reduce
from re import compile

tokens = tk
identifiers = {}

def p_program(p):
	"""program : stmt
			   | program stmt"""
	p[0] = [x for x in p if x]

def p_stmt(p):
	"""stmt : expr end
		    | assignment end
		    | io_operation end"""
	p[0] = ("stmt", p[1], p[2])

def p_expr(p):
	"""expr : expr plus term 
			| expr minus term 
			| term
			| string"""
	if len(p) == 4:
		if p[2] == '+':
			p[0] = p[1] + p[3]
		elif p[2] == '-':
			p[0] = p[1] - p[3]
	else:
		p[0] = p[1]

def p_term(p):
	"""term : term mult factor 
			| term div factor 
			| term mod factor
			| term pow factor
			| factor"""
	if len(p) == 4:
		if p[2] == '*':
			p[0] = p[1] * p[3]
		elif p[2] == '/':
			p[0] = p[1] / p[3]
		elif p[2] == '%':
			p[0] = p[1] % p[3]
		elif p[2] == '^':
			p[0] = p[1] ** p[3]
	else:
		p[0] = p[1]

def p_factor(p):
	"""factor : open_parenthesis expr close_parenthesis 
			  | name 
			  | number"""
	if len(p) == 4:
		p[0] = p[2]
	else:
		p[0] = p[1]

def parse_object(s):
	def isfloat(value):
		try:
			float(value)
			return True
		except ValueError:
			return False
	if isfloat(s):
		return float(s)
	else:
		if compile(r"\*.*\*").match(s):
			return s
		else:
			return "NIHIL"

def p_name(p):
	"""name : identifier"""
	if p[1] in identifiers:
		p[0] = parse_object(identifiers[p[1]])
	else:
		p[0] = parse_object(p[1])

def p_assignment_operator(p):
	"""assignment_operator : simple_assignment_operator
						   | addition_assignment_operator
						   | subtraction_assignment_operator
						   | multiplication_assignment_operator
						   | division_assignment_operator
						   | modulo_assignment_operator"""
	p[0] = p[1]

def p_assignment(p):
	"""assignment : identifier assignment_operator expr"""
	if len(p) == 4:
		if p[2] == '=':
			identifiers[p[1]] = parse_object(p[3])
		elif p[2] == "+=":
			identifiers[p[1]] += parse_object(p[3])
		elif p[2] == "-=":
			identifiers[p[1]] -= parse_object(p[3])
		elif p[2] == "*=":
			identifiers[p[1]] *= parse_object(p[3])
		elif p[2] == "/=":
			identifiers[p[1]] /= parse_object(p[3])
		p[0] = (p[1], p[2], p[3])

def p_io_operation(p):
	"""io_operation : input_operation
			 		| output_operation"""

def p_input_operation(p):
	"""input_operation : identifier send_operator input_operator
					   | identifier send_operator input_operator send_operator expr"""

def p_output_operation(p):
	"""output_operation : output_operator send_operator expr"""
	if len(p) == 4:
		print(p[3])

def p_error(t):
    print("Syntax error at '%s'" % t.value)

if __name__ == "__main__":
	yacc.yacc()
	result = yacc.parse(data)
	# flatten = lambda lst: reduce(lambda l, i: l + flatten(i) if isinstance(i, (list, tuple)) else l + [i], lst, [])  