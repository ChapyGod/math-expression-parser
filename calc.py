
class lexer:
    def __init__(self,txt):
        self.txt = txt
        self.position = 0
        self.max = len(txt)-1
    
    def num(self) -> str:
        self.spaces()
        p = self.position
        m = self.max
        result = ""

        while (p<=m) and (digit := self.txt[p]) in "0123456789":
            result += digit
            p += 1
        self.position = p
        return result
    
    def read(self,token) -> str:
        p = self.position
        m = self.max

        if len(token) > (m - p):
            return ""
        
        for t in token:
            if t != self.txt[p]:
                return ""
            p += 1
        self.position = p
        return token
    
    def choice(self,*tokens) -> str:
        self.spaces()

        for token in tokens:
            if (t := self.read(token)):
                return t
        return ""
    
    def spaces(self) -> None:
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

def generic_func(token: lexer, func,*operators):
    n1 = func(token)
    while op := token.choice(*operators):
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


