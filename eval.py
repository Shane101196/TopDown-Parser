#!/usr/bin/python3

import sys

def lexan():
    global mitr
    try:
        return(next(mitr))
    ##When reaching the end of the list, set the lookahead to be an empty character
    except StopIteration:
        return('')

def match(ch):
    global lookahead
    if ch == lookahead:
        lookahead = lexan()
    else:
        print("Syntax Error:", lookahead, "did not match expected:", ch)
        exit()

##Logic is: <prog> -> <decl-list> <stmt-list>
def prog():
    declList()
    stmtList()

##Logic is: <declList> -> <decl> { <decl> }
def declList():
    global lookahead
    decl()
    if lookahead == 'int' or lookahead == 'real':
        declList()

##Logic is: <decl> -> <vartype> <idList> ;
def decl():
    global lookahead
    vartype()
    idList()
    if lookahead != ';':
        print("Syntax error: Missing Semicolon")
        exit()
    else:
        match(';')

##Logic is: <vartype> -> int | real ;
def vartype():
    global lookahead
    global isfloat
    if lookahead == 'int':
        match('int')
        isfloat = False
    elif lookahead == 'real':
        match('real')
        isfloat = True
    else:
        print("Syntax Error: Expected an int or real variable. Got:", lookahead)
        exit()

##Logic is: <idList> -> id | { , id } ;
def idList():
    global idDict
    global isfloat
    if isfloat == False:
       idDict[lookahead] = 0
       match(lookahead)
    else:
       idDict[lookahead] = 0.0
       match(lookahead)
    if lookahead != ';':
        match(',')
        idList()

##Logic is: <stmtList> -> <stmt> { <stmt> }
def stmtList():
    global lookahead
    global idDict
    stmt()
    for key in idDict:
        if lookahead == key:
           stmtList()
    if lookahead == 'printi' or lookahead == 'printr':
        stmtList()

##Logic is: <stmt> -> id = <expr> ; | id = <expr> if <cond> else <expr> ; | printi <expr> ; | printr <expr> ; 
def stmt():
    global lookahead
    global idDict
    global condBool
    for key in idDict:
        if lookahead == key:
           match(key)
           match('=')
           idDict[key] = expr()
           if lookahead == ';':
              match(';')
           elif lookahead == 'if':
              match('if')
              condBool = cond()
              match('else')
              if condBool == True:
                 idDict[key] = expr()
              else:
                 expr()
              match(';')
    if lookahead == 'printi':
       match('printi')
       print("Interger Expression:" +  str(expr()))
       match(';')
    elif lookahead == 'printr':
       match('printr')
       print("Real Expression:" + str(expr()))
       match(';')

##Logic is: <expr> -> <term> { + <term> | - <term> }
def expr():
    global lookahead
    temp = term()
    if lookahead == '+':
       match('+')
       if type(temp) == float:
          temp += float(expr())
          return temp
       else:
          temp += int(expr())
          return temp
    elif lookahead == '-':
       match('-')
       if type(temp) == float:
          temp -=  float(expr())
          return temp
       else:
          temp -= int(expr())
          return temp
    else:
       return temp

##Logic is: <term> -> <factor> { * <factor> | / <factor> }
def term():
    global lookahead
    temp = factor()
    if lookahead == '*':
       match('*')
       if type(temp) == float:
          temp *= float(term())
          return temp
       else:
          temp2 = term()
          temp *= int(temp2)
          return temp
    elif lookahead == '/':
       match('/')
       if type(temp) == float:
          temp /= float(term())
          return temp
       else:
          temp /= int(term())
          return temp
    else:
       return temp

##Logic is: <factor> -> <base> ^ <factor> | <base>
def factor():
    global lookahead
    temp = base()
    if lookahead == '^':
       match('^')
       return temp ** factor()
    else:
       return temp

##Logic is: <base> -> ( <expr> ) | id | intnum
def base():
    global lookahead
    global idDict
    
    for key in idDict:
       if lookahead == key:
          match(key)
          return idDict[key]
    if lookahead == '(':
       match('(')
       temp = expr()
       match(')')
       return temp
    else:
       temp = lookahead
       match(lookahead)
       try: 
          return int(temp)
       except ValueError:
          return float(temp)
          print("Syntax error: Invalid Expression at:", lookahead)

##Logic is: <cond> -> <oprnd> < <oprnd> | <oprnd> <= <oprnd> | <oprnd> > <oprnd>
## <oprnd >= <oprnd> | <oprnd> == <oprnd> | <oprnd> != <oprnd)
def cond():
    global lookahead
    temp = oprnd()
    if lookahead == '<':
       match('<')
       return temp < oprnd()
    elif lookahead == '<=':
       match('<=')
       return temp <= oprnd()
    elif lookahead == '>':
       match('>')
       return temp > oprnd()
    elif lookahead == '>=':
       match('>=')
       return temp >= oprnd()
    elif lookahead == '==':
       match('==')
       return temp == oprnd()
    elif lookahead == '!=':
       match('!=')
       return temp != oprnd()
    else:
       print("Syntax error during conditional statement at:", lookahead)

##Logic is: <oprnd> -> id | intnum
def oprnd():
    global lookahead
    global idDict
    if lookahead.isdigit() == True:
       temp = lookahead
       match(lookahead)
       try:
          return int(temp)
       except ValueError:
          return float(temp)
    else:
       for key in idDict:
           if lookahead == key:
              match(key)
              return idDict[key]
       print("Syntax Error: Unknown operand at:", lookahead)
   
isfloat = False    
condBool = False
idDict = {}
file = open(sys.argv[1], "r")
##Assuming the file has a space character between each terminal
wlist = file.read().split()
mitr = iter(wlist)
lookahead = lexan()

##Call the starting statement
prog()

##If all terminal characters have been successfully iterated through, the lookahead will return an empty character
if lookahead == '':
    print("No syntax errors")
else:
    print("Syntax Error at:", lookahead)

