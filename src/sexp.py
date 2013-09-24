from pyparsing import *
from base64 import b64decode
import pprint

LPAREN, RPAREN, LBRACK, RBRACK = map(Suppress, "()[]")
base_64_char = alphanums + "+/="
simple_punc = "-./_:*+="
token_char = alphanums + simple_punc
bytes = Word( printables )
decimal = ("0" | Word( srange("[1-9]"), nums )).setParseAction(lambda t: int(t[0]))
token = Word( token_char )
hexadecimal = "#" + ZeroOrMore( Word(hexnums) ) + "#"
dblQuotedString.setParseAction( removeQuotes )
quoted_string = Optional( decimal.setResultsName("length") ) + dblQuotedString.setResultsName("data")
base_64_body = OneOrMore(Word(base_64_char))
base_64_body.setParseAction(lambda t:b64decode("".join(t)))
base_64 = Optional(decimal.setResultsName("length")) + "|" + base_64_body.setResultsName("data") + "|"
raw = (decimal.setResultsName("length") + ":" + bytes.setResultsName("data"))
simple_string = raw | token | base_64 | hexadecimal | quoted_string
display = LBRACK + simple_string + RBRACK
string_ = Optional(display) + simple_string
sexp = Forward()
list_ = Group( LPAREN + ZeroOrMore( sexp ) + RPAREN )
sexp << ( string_ | list_ )

def validateDataLength( tokens ):
	if tokens.length != "":
		if len(tokens.data) != int(tokens.length):
			raise ParseFatalException ("invalid data length, %d specified, found %s (%d chars)" % (int(tokens.length), tokens.data, len(tokens.data)))

quoted_string.setParseAction( validateDataLength )
base_64.setParseAction( validateDataLength )
raw.setParseAction( validateDataLength )

######### Test data ###########
if __name__ == '__main__':
	t = """
		

		(parallel (sequence (send A B hello)
							(send B A hello-ack)
				  )
				  (sequence (send C D hello)
				  	        (send D C hello-ack)
				  )
			)
	"""
	sexpr = sexp.parseString(t)
	pprint.pprint(sexpr.asList())
