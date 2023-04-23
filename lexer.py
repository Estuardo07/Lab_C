from pythonds.basic.stack import Stack

def infix_to_postfix(infixexpr): 
    #precedencia de los operadores donde 
    prec = {}
    prec["*"] = 4
    prec["+"] = 4
    prec["."] = 3
    prec["|"] = 2
    prec["("] = 1
   
    opStack = Stack()
    postfixList = []
	#Definimos los tokens que se van a encontrar en la expresion regular obviamente separando los tokens de los operadores. 
    for token in infixexpr:
        
        if token in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or token in "abcdefghijklmnopqrstuvxwyz" or token in "0123456789#" or token in "ε:;'" or token in '"' or token in "-_":
            postfixList.append(token)
        elif token == '(':
            opStack.push(token)
        elif token == ')':
            topToken = opStack.pop()
            while topToken != '(':
                postfixList.append(topToken)
                topToken = opStack.pop()
        else:
            while (not opStack.isEmpty()) and \
               (prec[opStack.peek()] >= prec[token]):
                  postfixList.append(opStack.pop())
            opStack.push(token)

    while not opStack.isEmpty():
        postfixList.append(opStack.pop())
    return "".join(postfixList)
