
class lexer:
    def __init__(self,txt):
        self.txt = txt
        self.position = 0
        self.max = len(txt)-1
    
    def num(self) -> str:    # this function reads any digit and returns
        self.spaces()        # it as a string
        p = self.position    # if no digit is found it will just return
        m = self.max         # an empty string
        result = ""

        while (p<=m) and (digit := self.txt[p]) in "0123456789":
            result += digit
            p += 1
        self.position = p
        return result
    
    def read(self,token: str) -> str:   # a string is given to this function,
        p = self.position               # it will then read the character stream
        m = self.max                    # and if it's not match it will return an
                                        # empty string otherwise will returns the
        if len(token) > (m - p):        # original string
            return ""
        
        for t in token:
            if t != self.txt[p]:
                return ""
            p += 1
        self.position = p
        return token
    
    def choice(self,*tokens) -> str:     # given a list of strings, it will try to match
        self.spaces()                    # every one of them until one matches, otherwise
                                         # will just return an empty string
        for token in tokens:
            if (t := self.read(token)):
                return t
        return ""
    
    def spaces(self) -> None:                    # this function will jump the spaces
        p = self.position                 
        m = self.max

        while (p <= m) and self.txt[p] == ' ':
            p += 1
        self.position = p

infix = {
    "+": lambda x,y: x+y,
    "-": lambda x,y: x-y,
    "*": lambda x,y: x*y,
    "/": lambda x,y: x/y,
    "^": lambda x,y: x**y
}

def generic_func(token: lexer, func,*operators):  # this function is the one that does all
    n1 = func(token)                              # the magic, unfortunelly im not so good at english
    while op := token.choice(*operators):         # to explain how it does in detail
        n1 = infix[op](n1,func(token))
    return n1

def expr(t: lexer) -> float:
    return generic_func(t,term,"+","-")

def term(t: lexer) -> float:
    return generic_func(t,power,"*","/")

def power(t: lexer) -> float:
    return generic_func(t,fctr,"^")


def fctr(token: lexer) -> float:
    if n1 := token.num():
        if token.read("."):
            n2 = token.num()
            return float(n1+"."+n2)
        return float(n1)
    elif token.read("("):
        e = expr(token)
        token.read(")")
        return e

def main():
    print("pres ENTER to quit or write quit")
    while True:
        t = input(">>> ")
        if not t or t == "quit":
            break
        print(expr(lexer(t)))

if __name__ == "__main__":
    main()


