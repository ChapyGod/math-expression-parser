class ParseError(Exception):
    pass


class lexer:
    def __init__(self,txt: str) -> None: 
        self.txt = txt
        self.position = 0
        self.max = len(txt) - 1

    def num(self) -> str or None:
        self.spaces()
        p = self.position     # this is a small hack to
        m = self.max          # speed up a bit
        result = ''

        while (p <= m) and (digit := self.txt[p]) in "0123456789":
            result += digit
            p += 1
        
        self.position = p
        return result if result != '' else None
    
    def var(self) -> str or None:
        self.spaces()
        p = self.position
        m = self.max
        result = ''
        letters = "abcdefghijklmnopqrstuvwxyz"


        while (p <= m) and (letter := self.txt[p]) in letters:
            result += letter
            p += 1
        
        self.position = p
        return result if result != '' else None
    
    def read(self, token: str) -> str or None:
        self.spaces()
        p = self.position
        m = self.max
        
        if len(token)-1 > (m - p):  # if the token is bigger than the remaining
            return None             # input string then is an automatic false
        
        for i in token:             # iterates over the token, looking for 
            if i != self.txt[p]:    # a failure
                return None         # if happens to be a failure, then the position
            p += 1                  # never advances
        self.position = p
        return token

    def choice(self, *tokens: str) -> str or None:
        self.spaces()
        p = self.position
        m = self.max

        for token in tokens:
            if t := self.read(token):
                return t
        return None


    def spaces(self) -> None:
        p = self.position
        m = self.max

        while (p <= m) and self.txt[p] == ' ':
            p += 1
        self.position = p 


# stmt  -> decl 
# stmt  -> expr

# decl  -> "let" {spaces} {letter} [spaces] ":=" expr

# expr  -> term expr' 
# expr' -> "+" term expr' | empty
# term  -> fctr term'
# term' -> "*" fctr term' | empty
# fctr  -> "(" expr ")" | num | var   

operators = {
    "+": lambda x,y: x+y,
    "-": lambda x,y: x-y,
    "*": lambda x,y: x*y,
    "/": lambda x,y: x/y
}

stack = {}

def expr(token: lexer) -> float:
    n1 = term(token)
    global operators
    while p := token.choice("+"):
        n1 = operators[p](n1,term(token))
    return n1

def term(token: lexer) -> float:
    n1 = neg(fctr,token)
    global operators
    while p := token.choice("*","/"):
        n1 = operators[p](n1,fctr(token))
    return n1


def neg(parse, token: lexer):
    if token.read("-"):
        n1 = parse(token)
        return -n1
    else:
        return parse(token)


def fctr(token: lexer) -> float:
    if token.read("("):
        return bracket(token)
    
    elif n1 := token.num():
        return float(n1)
    
    elif n1 := token.var():
        if n1 in ["let","quit"]:
            raise ParseError
        else:
            global stack
            return stack[n1]

    else:
        raise ParseError


def bracket(token: lexer) -> float:
    n1 = expr(token)
    if token.read(")"):
        return n1
    else:
        raise ParseError


def decl(token: lexer) -> None:
    global stack
    var_name = token.var()
    
    if var_name in ["let","where","class"]: 
        raise ParseError
    
    if token.read(":="):
        var_value = expr(token)
        stack[var_name] = var_value
        return None
    else:
        raise ParseError


def stmt(token: lexer) -> None or float:
    if token.read("let "):
        return decl(token)
    else:
        return expr(token)


def run() -> None:
    print("enter expression")
    while True:
        l = input(">>> ")
        if not l: break

        n1 = stmt(lexer(l))
        if n1:
            print(f"=> {n1}")
    
if __name__ == "__main__":
    run()