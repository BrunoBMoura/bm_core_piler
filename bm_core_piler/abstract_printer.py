from . import cminus_abstract_st

IDENT = 2
SUBINDENT = IDENT/2

class AbstractStPrinter(cminus_abstract_st.AbstractStVisitor):

    def __init__ (self):
        super().__init__()
        self.ident = 0 
        
    def visit_Program(self, node: cminus_abstract_st.Program):
        self.ident += IDENT
        
        print('Program:')
        print(' |' * self.ident, 'Declarations:')
        for decl in node.decls:
            self.visit(decl)
		#print(self.visit(decl))
        
        self.ident -= IDENT

    def visit_Decl(self, node: cminus_abstract_st.Decl):
        if node.funct_decl is None:
            self.visit(node.var_decl)
        else:
            self.visit(node.funct_decl)
    
    def visit_Var_decl(self, node: cminus_abstract_st.Var_decl):
        self.ident += IDENT
        
        if node.num is None:
            print(' |' * self.ident, 'Variable declaration:{')
            print(' |' * self.ident, 'Id:{', node.id_ + ' }')
            print(' |' * self.ident, 'Type:', self.visit(node.type_))
            print(' |' * self.ident, '}')
        else:
            print(' |' * self.ident, ' Array variable declaration:{')
            print(' |' * self.ident, 'Id:{', node.id_ + ' }')
            print(' |' * self.ident, 'Type:', self.visit(node.type_))
            print(' |' * self.ident, 'Array size:', node.num)
            print(' |' * self.ident, '}')

        self.ident -= IDENT

    def visit_Type_especifier(self, node: cminus_abstract_st.Type_especifier):
        return (node.type_)
        
    def visit_Funct_decl(self, node: cminus_abstract_st.Funct_decl):
        self.ident += IDENT
        
        print(' |' * self.ident, 'Function declaration:{')
        print(' |' * self.ident, 'Id:{', node.id_+ ' }')
        print(' |' * self.ident, 'Type:{', self.visit(node.type_)+ ' }') 
        print(' |' * self.ident, 'Function parameters:{')
        self.visit(node.params)
        print(' |' * self.ident, '}')
        print(' |' * self.ident, 'Function body:{')
        self.visit(node.comp_decls)
        print(' |' * self.ident,'}')
        self.ident -= IDENT

    def visit_Params(self, node: cminus_abstract_st.Params):
        if node.par_list is not None:
            for param in node.par_list:
                self.visit(param)

    def visit_Param(self, node: cminus_abstract_st.Param):
        self.ident += IDENT
        
        if not node.isArray:
            print(' |' * self.ident, 'Parameter:{')
            print(' |' * self.ident, 'Id:{', node.id_ + ' }')
            print(' |' * self.ident, 'Type:{', self.visit(node.type_)+ ' }')
        else:
            print(' |' * self.ident, 'Parameter:{')
            print(' |' * self.ident, 'Id:{', node.id_ + ' }')
            print(' |' * self.ident, 'Type:{', self.visit(node.type_) +'[]' + ' }')
            print(' |' * self.ident, '}')

        self.ident -= IDENT
    
    def visit_Comp_decl(self, node: cminus_abstract_st.Comp_decl):
        self.ident += IDENT
        
        print(' |' * self.ident, 'Declarations:{')
        for decl in node.local_decl:
            print(' |' * self.ident, self.visit(decl))
        for stmt in node.stmt_list:
            print(' |' * self.ident, self.visit(stmt))
        print(' |' * self.ident, '}')

        self.ident -= IDENT
    
    def visit_Local_decl(self, node: cminus_abstract_st.Local_decl):
        self.ident += IDENT
        
        print(' |' * self.ident, 'Local declarations:{')
        for decl in node.var_decls:
            print(' |' * self.ident, self.visit(decl))
        print(' |' * self.ident, '}')
        self.ident -= IDENT
    
    def visit_Stmt_list(self, node: cminus_abstract_st.Stmt_list):
        self.ident+= IDENT
        
        print(' |' * self.ident, 'Statements:{')
        for stmt in node.stmts:
            print(' |' * self.ident, self.visit(stmt))
        print(' |' * self.ident, '}')

        self.ident -= IDENT

    def visit_Stmt(self, node: cminus_abstract_st.Stmt):
        self.ident+= IDENT
        print(' |' * self.ident, 'Statement type:{') #
        self.visit(node.stmt_type)
        print(' |' * self.ident, '}')
        self.ident -= IDENT
    
    def visit_Exp_decl(self, node: cminus_abstract_st.Exp_decl):
        self.ident+= IDENT
        print(' |' * self.ident, 'Expression:{')
        self.visit(node.exp)
        print(' |' * self.ident, '}')
        self.ident -= IDENT

    def visit_Select_decl(self, node: cminus_abstract_st.Select_decl):
        self.ident += IDENT
        
        print(' |' * self.ident, 'If: {')
        print(' |' * self.ident, 'Condition:{') 
        self.visit(node.condition)
        
        print(' |' * self.ident, '}') 
        print(' |' * self.ident, 'If body:{')
        for decl in node.if_body:
            print(' |' * self.ident, self.visit(decl))
        print(' |' * self.ident, '}')
        
        print(' |' * self.ident, 'Else body:{')
        for decl in node.else_body:
            print(' |' * self.ident,self.visit(decl))
        
        print(' |' * self.ident, '}')
        print(' |' * self.ident, '}')
        
        self.ident -= IDENT
        

    def visit_Iter_decl(self, node: cminus_abstract_st.Iter_decl):
        self.ident+= IDENT
        
        print(' |' * self.ident, 'While:{')
        print(' |' * self.ident, 'Condition:{')
        self.visit(node.condition)
        print(' |' * self.ident, '}')
        print(' |' * self.ident, 'Iteration body:{')
        self.visit(node.stmts)
        print(' |' * self.ident, '}')        
        print(' |' * self.ident, '}')
        self.ident -= IDENT

    def visit_Ret_decl(self, node: cminus_abstract_st.Ret_decl):
        self.ident += IDENT
        
        print(' |' * self.ident, 'Return:{')
        if node.exp:
            print(' |' * self.ident, 'Expression:{')
            self.visit(node.exp) 
            print(' |' * self.ident, '}')
        else:
            print(' |' * self.ident, 'Empty')
        print(' |' * self.ident, '}')

        self.ident -= IDENT

    def visit_Exp(self, node: cminus_abstract_st.Exp):
        self.ident+= IDENT
        
        print(' |' * self.ident, 'Assignement:{')
        if node.var:
            print(' |' * self.ident, self.visit(node.var)) 
        if node.simple_exp or node.exp:
            self.visit(node.simple_exp) if node.simple_exp else self.visit(node.exp)
        
        print(' |' * self.ident, '}')
        self.ident -= IDENT
    
    def visit_Var(self, node: cminus_abstract_st.Var):
        self.ident += IDENT
        
        if node.exp:
            print(' |' * self.ident, 'Array variable:{')
            print(' |' * self.ident, 'Id:{', node.id_ + ' }')
            print(' |' * self.ident, 'Array expression:')
            self.visit(node.exp)
            print(' |' * self.ident, '}')
        else:
            print(' |' * self.ident, 'Variable:{')
            print(' |' * self.ident, 'Id:{', node.id_ + ' }')
            print(' |' * self.ident, '}')
    
        self.ident -= IDENT
    
    def visit_Simple_exp(self, node: cminus_abstract_st.Simple_exp):
    
        if node.exp_left:
            self.ident += IDENT
            print(' |' * self.ident, 'Left expression:{')
            self.visit(node.exp_left)
            print(' |' * self.ident, '}')
            print(' |' * self.ident, 'Relational operator:{', self.visit(node.relational)+' }') 
            print(' |' * self.ident, 'Right expression:{')
            self.visit(node.exp_right)
            print(' |' * self.ident, '}')
            
            self.ident -= IDENT
        else:
            self.visit(node.generic_exp)

    def visit_Relational(self, node: cminus_abstract_st.Relational):
        return(node.type_)
        
        
    def visit_Sum_exp(self, node: cminus_abstract_st.Sum_exp):
        self.ident += IDENT
        
        if node.op:
            print(' |' * self.ident, 'Left expression:{')
            self.visit(node.sum_exp)
            print(' |' * self.ident, '}')
            print(' |' * self.ident, 'Operator:{', node.op +' }')
            print(' |' * self.ident, 'Right expression:{')
            self.visit(node.term)
            print(' |' * self.ident, '}')
        else:
            self.visit(node.term)

        self.ident -= IDENT
        
    def visit_Term(self, node: cminus_abstract_st.Term):
        self.ident += IDENT
        
        if node.op:
            print(' |' * self.ident, 'Left expression:{')
            self.visit(node.term)
            print(' |' * self.ident, '}')
            print(' |' * self.ident, 'Operator:{', node.op +' }')
            print(' |' * self.ident, 'Right expression:{')
            self.visit(node.fact)
            print(' |' * self.ident, '}')
        else:
            self.visit(node.fact)

        self.ident -= IDENT
        
        
    def visit_Fact(self, node: cminus_abstract_st.Fact):
        if node.exp:
            self.visit(node.exp)
        if node.var:
            self.visit(node.var)
        if node.activ:
            self.visit(node.activ)
        if node.num:
            self.ident += IDENT        
            print(' |' * self.ident, 'Number:{', node.num + ' }')
            self.ident -= IDENT    

    def visit_Activation(self, node: cminus_abstract_st.Activation):
        self.ident += IDENT    
    
        print(' |' * self.ident, 'Function call:{')
        print(' |' * self.ident, 'Id:{', node.id_ + ' }')
        
        print(' |' * self.ident, 'Arguments:{')
        for arg in node.args_list:
            self.visit(arg)
        print(' |' * self.ident, '}')
        print(' |' * self.ident, '}')

        self.ident -= IDENT
    
