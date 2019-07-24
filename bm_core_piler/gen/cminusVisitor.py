# Generated from cminus.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .cminusParser import cminusParser
else:
    from cminusParser import cminusParser

# This class defines a complete generic visitor for a parse tree produced by cminusParser.

class cminusVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by cminusParser#program.
    def visitProgram(self, ctx:cminusParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by cminusParser#decl.
    def visitDecl(self, ctx:cminusParser.DeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by cminusParser#var_decl.
    def visitVar_decl(self, ctx:cminusParser.Var_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by cminusParser#type_especifier.
    def visitType_especifier(self, ctx:cminusParser.Type_especifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by cminusParser#funct_decl.
    def visitFunct_decl(self, ctx:cminusParser.Funct_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by cminusParser#params.
    def visitParams(self, ctx:cminusParser.ParamsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by cminusParser#param.
    def visitParam(self, ctx:cminusParser.ParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by cminusParser#comp_decl.
    def visitComp_decl(self, ctx:cminusParser.Comp_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by cminusParser#local_decl.
    def visitLocal_decl(self, ctx:cminusParser.Local_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by cminusParser#stmt_list.
    def visitStmt_list(self, ctx:cminusParser.Stmt_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by cminusParser#stmt.
    def visitStmt(self, ctx:cminusParser.StmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by cminusParser#exp_decl.
    def visitExp_decl(self, ctx:cminusParser.Exp_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by cminusParser#select_decl.
    def visitSelect_decl(self, ctx:cminusParser.Select_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by cminusParser#iter_decl.
    def visitIter_decl(self, ctx:cminusParser.Iter_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by cminusParser#ret_decl.
    def visitRet_decl(self, ctx:cminusParser.Ret_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by cminusParser#exp.
    def visitExp(self, ctx:cminusParser.ExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by cminusParser#var.
    def visitVar(self, ctx:cminusParser.VarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by cminusParser#simple_exp.
    def visitSimple_exp(self, ctx:cminusParser.Simple_expContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by cminusParser#relational.
    def visitRelational(self, ctx:cminusParser.RelationalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by cminusParser#sum_exp.
    def visitSum_exp(self, ctx:cminusParser.Sum_expContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by cminusParser#term.
    def visitTerm(self, ctx:cminusParser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by cminusParser#fact.
    def visitFact(self, ctx:cminusParser.FactContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by cminusParser#activation.
    def visitActivation(self, ctx:cminusParser.ActivationContext):
        return self.visitChildren(ctx)



del cminusParser