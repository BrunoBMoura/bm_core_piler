from .gen.cminusParser import cminusParser
from .gen.cminusVisitor import cminusVisitor

class AbstractStNode:
    def __init__(self, line = -1):
        self.line = line

class AbstractStVisitor:
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class Program(AbstractStNode):
    def __init__(self, decls, line = -1):
        super().__init__(line)
        self.decls = decls

class Decl(AbstractStNode):
    def __init__(self, var_decl = None, funct_decl = None, line = -1):
        super().__init__(line)
        self.var_decl = var_decl
        self.funct_decl = funct_decl

class Var_decl(AbstractStNode):
    def __init__(self, type_, id_, num = None, line = -1):
        super().__init__(line)
        self.type_ = type_
        self.id_ = id_
        self.num = num

class Type_especifier(AbstractStNode):
    def __init__(self, type_, line = -1):
        super().__init__(line)
        self.type_ = type_

class Funct_decl(AbstractStNode):
    def __init__(self, type_, id_, params, comp_decls, line = -1):
        super().__init__(line)
        self.type_ = type_
        self.id_ = id_
        self.comp_decls = comp_decls
        self.params = params

class Params(AbstractStNode):
    def __init__(self, par_list = None, line = -1):
        super().__init__(line)
        self.par_list = par_list

class Param(AbstractStNode):
    def __init__(self, type_, id_, isArray = None, line = -1):
        super().__init__(line)
        self.type_ = type_
        self.id_ = id_
        self.isArray = isArray

class Comp_decl(AbstractStNode):
    def __init__(self, local_decl = None, stmt_list = None, line = -1):
        super().__init__(line)
        self.local_decl = local_decl
        self.stmt_list = stmt_list

class Local_decl(AbstractStNode):
    def __init__(self, var_decls, line = -1):
        super().__init__(line)
        self.var_decls = var_decls

class Stmt_list(AbstractStNode):
    def __init__(self, stmts, line = -1):
        super().__init__(line)
        self.stmts = stmts

class Stmt(AbstractStNode):
    def __init__(self, stmt_type = None, line = -1):
        super().__init__(line)
        self.stmt_type = stmt_type

class Exp_decl(AbstractStNode):
    def __init__(self, exp, line = -1):
        super().__init__(line)
        self.exp = exp

class Select_decl(AbstractStNode):
    def __init__(self, condition, if_body, else_body = None, line = -1):
        super().__init__(line)
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body

class Iter_decl(AbstractStNode):
    def __init__(self, condition, stmts, line = -1):
        super().__init__(line)
        self.condition = condition
        self.stmts = stmts

class Ret_decl(AbstractStNode):
    def __init__(self, exp = None, line = -1):
        super().__init__(line)
        self.exp = exp

class Exp(AbstractStNode):
    def __init__(self, var, exp = None, simple_exp = None, line = -1):
        super().__init__(line)
        self.var = var
        self.exp = exp
        self.simple_exp = simple_exp

class Var(AbstractStNode):
    def __init__(self, id_, exp = None, line = -1):
        super().__init__(line)
        self.id_ = id_
        self.exp = exp

class Simple_exp(AbstractStNode):
    def __init__(self, exp_left = None, relational = None, exp_right = None, generic_exp = None, line = -1):
        super().__init__(line)
        self.exp_left = exp_left
        self.relational = relational
        self.exp_right = exp_right
        self.generic_exp = generic_exp

class Relational(AbstractStNode):
    def __init__(self, type_, line = -1):
        super().__init__(line)
        self.type_ = type_

class Sum_exp(AbstractStNode):
    def __init__(self, term, sum_exp = None, op = None, line = -1):
        super().__init__(line)
        self.sum_exp = sum_exp
        self.op = op
        self.term = term

class Term(AbstractStNode):
    def __init__(self, op, fact, term = None, line = -1):
        super().__init__(line)
        self.term = term
        self.op = op
        self.fact = fact

class Fact(AbstractStNode):
    def __init__(self, exp = None, var = None, activ = None, num = None, line = -1):
        super().__init__(line)
        self.exp = exp
        self.var = var
        self.activ = activ
        self.num = num

class Activation(AbstractStNode):
    def __init__(self, id_, args_list, line = -1):
        super().__init__(line)
        self.id_ = id_
        self.args_list = args_list

class AbstractStNodeConstructVisitor(cminusVisitor):

    def visitProgram(self, ctx:cminusParser.ProgramContext): # OK
        return Program(
            decls = [self.visit(decl) for decl in ctx.list_decls],
            line = ctx.start.line,
        )

    def visitDecl(self, ctx: cminusParser.DeclContext): # OK
        return Decl(
            var_decl = self.visit(ctx.var_decl()) if ctx.var_decl() else None,
            funct_decl = self.visit(ctx.funct_decl()) if ctx.funct_decl() else None,
            line = ctx.start.line,
        )

    def visitVar_decl(self, ctx: cminusParser.Var_declContext): # OK
        return Var_decl(
            type_ = self.visit(ctx.type_especifier()),
            id_ = ctx.ID().getText(),
            num = ctx.NUM().getText() if ctx.NUM() else None,
            line = ctx.start.line,
        )

    def visitType_especifier(self, ctx: cminusParser.Type_especifierContext): # OK
        return Type_especifier(
            type_ = 'int' if ctx.INT() else 'void',
            line = ctx.start.line,
        )

    def visitFunct_decl(self, ctx: cminusParser.Funct_declContext): # OK
        return Funct_decl(
            type_ = (self.visit(ctx.type_especifier())),
            id_ = ctx.ID().getText(),
            params = self.visit(ctx.params()),
            comp_decls = self.visit(ctx.comp_decl()),
            line = ctx.start.line,
        )

    def visitParams(self, ctx: cminusParser.ParamsContext): # OK
        return Params(
            par_list = [self.visit(param) for param in ctx.params_list] if not ctx.VOID() else [],
        )

    def visitParam(self, ctx:cminusParser.ParamContext): # OK
        return Param(
            type_ = (self.visit(ctx.type_especifier())),
            id_ = ctx.ID().getText(),
            isArray = True if ctx.LSBRACK() else False,
            line = ctx.start.line,
        )

    def visitComp_decl(self, ctx:cminusParser.Comp_declContext): # OK    
        return Comp_decl(
            local_decl = [self.visit(decl) for decl in ctx.loc_decls] if ctx.local_decl() else [],
            stmt_list = [self.visit(stmt) for stmt in ctx.stmts_list] if ctx.stmt_list() else [],
            line = ctx.start.line,
        )


    def visitLocal_decl(self, ctx:cminusParser.Local_declContext): # OK
        return Local_decl(
            var_decls = [self.visit(decl) for decl in ctx.decl_list],
            line = ctx.start.line,
        )

    def visitStmt_list(self, ctx:cminusParser.Stmt_listContext): # OK
        return Stmt_list(
            stmts = [self.visit(stmt) for stmt in ctx.stmts_list],
            line = ctx.start.line,
        )

    def visitStmt(self, ctx:cminusParser.StmtContext): # OK
        if ctx.exp_decl():
            return Stmt(
                stmt_type = self.visit(ctx.exp_decl()),
                line = ctx.start.line,
            )          
        elif ctx.comp_decl():
            return Stmt(
                stmt_type = self.visit(ctx.comp_decl()),
                line = ctx.start.line,
            )
        elif ctx.select_decl():
            return Stmt(
                stmt_type = self.visit(ctx.select_decl()),
                line = ctx.start.line,
            )
        elif ctx.iter_decl():
            return Stmt(
                stmt_type = self.visit(ctx.iter_decl()),
                line = ctx.start.line,
            )
        elif ctx.ret_decl():
            return Stmt(
                stmt_type = self.visit(ctx.ret_decl()),
                line = ctx.start.line,
            )

    def visitExp_decl(self, ctx:cminusParser.Exp_declContext): # OK
        return Exp_decl(
            exp = self.visit(ctx.exp()) if ctx.exp() else None,
            line = ctx.start.line,
        )

    def visitSelect_decl(self, ctx:cminusParser.Select_declContext): # OK
        return Select_decl(
            condition = self.visit(ctx.condition),
            if_body = [self.visit(foo) for foo in ctx.if_body],
            else_body = [self.visit(stmt) for stmt in ctx.else_body] if ctx.else_body else [],
            line = ctx.start.line,
        )

    def visitIter_decl(self, ctx:cminusParser.Iter_declContext): # OK
        return Iter_decl(
            condition = (self.visit(ctx.exp())),
            stmts = (self.visit(ctx.stmt())),
            line = ctx.start.line,
        )

    def visitRet_decl(self, ctx:cminusParser.Ret_declContext): # OK
        return Ret_decl(
            exp = self.visit(ctx.exp()) if ctx.exp() else None,
            line = ctx.start.line,
        )

    def visitExp(self, ctx:cminusParser.ExpContext): # OK
        return Exp(
            var = self.visit(ctx.var()) if ctx.var() else None,
            exp = self.visit(ctx.exp()) if ctx.exp() else None,
            simple_exp = self.visit(ctx.simple_exp()) if ctx.simple_exp() else None,
            line = ctx.start.line,
        )

    def visitVar(self, ctx:cminusParser.VarContext): # OK
        return Var(
            id_ = ctx.ID().getText(),
            exp = self.visit(ctx.exp()) if ctx.exp() else [],
            line = ctx.start.line,
        )

    def visitSimple_exp(self, ctx:cminusParser.Simple_expContext): # OK
        return Simple_exp(
            exp_left = self.visit(ctx.sum_exp_left) if ctx.sum_exp_left else None,
            relational = self.visit(ctx.relational()) if ctx.relational() else None,
            exp_right = self.visit(ctx.sum_exp_right) if ctx.sum_exp_right else None,
            generic_exp = self.visit(ctx.g_exp) if ctx.g_exp else None,
            line = ctx.start.line,
        )

    def visitRelational(self, ctx:cminusParser.RelationalContext): # OK

        def find_relational():
            if ctx.LET():
                return ctx.LET().getText() 
            if ctx.LT():
                return ctx.LT().getText()
            if ctx.GT():
                return ctx.GT().getText()
            if ctx.GET():
                return ctx.GET().getText()
            if ctx.EQ():
                return ctx.EQ().getText()
            if ctx.NEQ():
                return ctx.NEQ().getText()

        return Relational(
            type_ = find_relational(),
            line = ctx.start.line,
        )

    def visitSum_exp(self, ctx:cminusParser.Sum_expContext): # OK
        return Sum_exp(
            sum_exp = (self.visit(ctx.sum_exp())) if ctx.sum_exp() else None,
            op = ctx.op.text if ctx.op else None,
            term = (self.visit(ctx.term())),
            line = ctx.start.line,
        )

    def visitTerm(self, ctx:cminusParser.TermContext): # OK
        return Term(
            term = (self.visit(ctx.term())) if ctx.op else None,
            op = ctx.op.text if ctx.op else None,
            fact = self.visit(ctx.fact()),
            line = ctx.start.line,
        )

    def visitFact(self, ctx:cminusParser.FactContext): # OK
        return Fact(
            exp = self.visit(ctx.exp()) if ctx.exp() else None,
            var = self.visit(ctx.var()) if ctx.var() else None,
            activ = self.visit(ctx.activation()) if ctx.activation() else None,
            num = ctx.NUM().getText() if ctx.NUM() else None,
            line = ctx.start.line,
        )

    def visitActivation(self, ctx:cminusParser.ActivationContext): # OK
        return Activation(
            id_ = ctx.ID().getText(),
            args_list = [self.visit(arg) for arg in ctx.args],
            line = ctx.start.line,
        )

