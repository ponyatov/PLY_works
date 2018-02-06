class AST:
    def __init__(self,T,V):
        self.tag = T ; self.val = V
        self.nest=[] ; self.attr={}
    def __repr__(self): return self.dump()
    def head(self): return '<%s:%s>'%(self.tag,self.val)
    def pad(self,N): return '\n'+'\t'*N
    def dump(self,depth=0):
        S = self.pad(depth)+self.head()
        for i in self.attr:
            S += ',%s = %s'%(i,self.attr[i])
        for j in self.nest:
            S += j.dump(depth+1)
        return S
    def __lshift__(self,o): self.nest.append(o) ; return self
    def __setitem__(self,K,V): self.attr[K]=V; return self

import ply.lex  as lex
import ply.yacc as yacc

tokens = ['OP','LP','RP','ID']

t_ignore = ' \t\r\n'

def t_error(t): raise SyntaxError(t)

def t_LP(t):
    r'\('
    return t
def t_RP(t):
    r'\)'
    return t

def t_OP(t):
    r'INTERSECT|UNION|MINUS'
    t.value = AST(t.type,t.value) ; return t

def t_ID(t):
    r'[a-zA-Z0-9_]+'
    t.value = AST(t.type,t.value) ; return t
    
def p_error(p): raise SyntaxError(p)

def p_REPL_none(p): 'REPL : '
def p_REPL_recur(p):
    'REPL : REPL ex '
    print p[2]
def p_ex_OP(p):
    'ex : OP'
    p[0] = p[1]
def p_ex_FN(p):
    'ex : ex LP ex RP '
    p[0] = p[1] << p[3]
    p[1]['type']='function' ; p[3]['parameter']=True
def p_ex_BINOP(p):
    'ex : ex OP ex '
    p[0] = p[2] << p[1] << p[3]
def p_ex_PARENS(p):
    'ex : LP ex RP '
    p[0] = p[2]
def p_ex_ID(p):
    'ex : ID'
    p[0] = p[1]

lexer = lex.lex()

syntax=yacc.yacc(debug=None,write_tables=None)
syntax.parse('''
    (func1(b) INTERSECT func1(c)) UNION func2(a)
''')
syntax.parse('''
    func3(func1(b)) MINUS func1(d)
''')
