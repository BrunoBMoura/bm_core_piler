# Generated from cminus.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .cminusParser import cminusParser
else:
    from cminusParser import cminusParser

# This class defines a complete listener for a parse tree produced by cminusParser.
class cminusListener(ParseTreeListener):

    # Enter a parse tree produced by cminusParser#program.
    def enterProgram(self, ctx:cminusParser.ProgramContext):
        pass

    # Exit a parse tree produced by cminusParser#program.
    def exitProgram(self, ctx:cminusParser.ProgramContext):
        pass


    # Enter a parse tree produced by cminusParser#decl.
    def enterDecl(self, ctx:cminusParser.DeclContext):
        pass

    # Exit a parse tree produced by cminusParser#decl.
    def exitDecl(self, ctx:cminusParser.DeclContext):
        pass


    # Enter a parse tree produced by cminusParser#var_decl.
    def enterVar_decl(self, ctx:cminusParser.Var_declContext):
        pass

    # Exit a parse tree produced by cminusParser#var_decl.
    def exitVar_decl(self, ctx:cminusParser.Var_declContext):
        pass


    # Enter a parse tree produced by cminusParser#type_especifier.
    def enterType_especifier(self, ctx:cminusParser.Type_especifierContext):
        pass

    # Exit a parse tree produced by cminusParser#type_especifier.
    def exitType_especifier(self, ctx:cminusParser.Type_especifierContext):
        pass


    # Enter a parse tree produced by cminusParser#funct_decl.
    def enterFunct_decl(self, ctx:cminusParser.Funct_declContext):
        pass

    # Exit a parse tree produced by cminusParser#funct_decl.
    def exitFunct_decl(self, ctx:cminusParser.Funct_declContext):
        pass


    # Enter a parse tree produced by cminusParser#params.
    def enterParams(self, ctx:cminusParser.ParamsContext):
        pass

    # Exit a parse tree produced by cminusParser#params.
    def exitParams(self, ctx:cminusParser.ParamsContext):
        pass


    # Enter a parse tree produced by cminusParser#param.
    def enterParam(self, ctx:cminusParser.ParamContext):
        pass

    # Exit a parse tree produced by cminusParser#param.
    def exitParam(self, ctx:cminusParser.ParamContext):
        pass


    # Enter a parse tree produced by cminusParser#comp_decl.
    def enterComp_decl(self, ctx:cminusParser.Comp_declContext):
        pass

    # Exit a parse tree produced by cminusParser#comp_decl.
    def exitComp_decl(self, ctx:cminusParser.Comp_declContext):
        pass


    # Enter a parse tree produced by cminusParser#local_decl.
    def enterLocal_decl(self, ctx:cminusParser.Local_declContext):
        pass

    # Exit a parse tree produced by cminusParser#local_decl.
    def exitLocal_decl(self, ctx:cminusParser.Local_declContext):
        pass


    # Enter a parse tree produced by cminusParser#stmt_list.
    def enterStmt_list(self, ctx:cminusParser.Stmt_listContext):
        pass

    # Exit a parse tree produced by cminusParser#stmt_list.
    def exitStmt_list(self, ctx:cminusParser.Stmt_listContext):
        pass


    # Enter a parse tree produced by cminusParser#stmt.
    def enterStmt(self, ctx:cminusParser.StmtContext):
        pass

    # Exit a parse tree produced by cminusParser#stmt.
    def exitStmt(self, ctx:cminusParser.StmtContext):
        pass


    # Enter a parse tree produced by cminusParser#exp_decl.
    def enterExp_decl(self, ctx:cminusParser.Exp_declContext):
        pass

    # Exit a parse tree produced by cminusParser#exp_decl.
    def exitExp_decl(self, ctx:cminusParser.Exp_declContext):
        pass


    # Enter a parse tree produced by cminusParser#select_decl.
    def enterSelect_decl(self, ctx:cminusParser.Select_declContext):
        pass

    # Exit a parse tree produced by cminusParser#select_decl.
    def exitSelect_decl(self, ctx:cminusParser.Select_declContext):
        pass


    # Enter a parse tree produced by cminusParser#iter_decl.
    def enterIter_decl(self, ctx:cminusParser.Iter_declContext):
        pass

    # Exit a parse tree produced by cminusParser#iter_decl.
    def exitIter_decl(self, ctx:cminusParser.Iter_declContext):
        pass


    # Enter a parse tree produced by cminusParser#ret_decl.
    def enterRet_decl(self, ctx:cminusParser.Ret_declContext):
        pass

    # Exit a parse tree produced by cminusParser#ret_decl.
    def exitRet_decl(self, ctx:cminusParser.Ret_declContext):
        pass


    # Enter a parse tree produced by cminusParser#exp.
    def enterExp(self, ctx:cminusParser.ExpContext):
        pass

    # Exit a parse tree produced by cminusParser#exp.
    def exitExp(self, ctx:cminusParser.ExpContext):
        pass


    # Enter a parse tree produced by cminusParser#var.
    def enterVar(self, ctx:cminusParser.VarContext):
        pass

    # Exit a parse tree produced by cminusParser#var.
    def exitVar(self, ctx:cminusParser.VarContext):
        pass


    # Enter a parse tree produced by cminusParser#simple_exp.
    def enterSimple_exp(self, ctx:cminusParser.Simple_expContext):
        pass

    # Exit a parse tree produced by cminusParser#simple_exp.
    def exitSimple_exp(self, ctx:cminusParser.Simple_expContext):
        pass


    # Enter a parse tree produced by cminusParser#relational.
    def enterRelational(self, ctx:cminusParser.RelationalContext):
        pass

    # Exit a parse tree produced by cminusParser#relational.
    def exitRelational(self, ctx:cminusParser.RelationalContext):
        pass


    # Enter a parse tree produced by cminusParser#sum_exp.
    def enterSum_exp(self, ctx:cminusParser.Sum_expContext):
        pass

    # Exit a parse tree produced by cminusParser#sum_exp.
    def exitSum_exp(self, ctx:cminusParser.Sum_expContext):
        pass


    # Enter a parse tree produced by cminusParser#term.
    def enterTerm(self, ctx:cminusParser.TermContext):
        pass

    # Exit a parse tree produced by cminusParser#term.
    def exitTerm(self, ctx:cminusParser.TermContext):
        pass


    # Enter a parse tree produced by cminusParser#fact.
    def enterFact(self, ctx:cminusParser.FactContext):
        pass

    # Exit a parse tree produced by cminusParser#fact.
    def exitFact(self, ctx:cminusParser.FactContext):
        pass


    # Enter a parse tree produced by cminusParser#activation.
    def enterActivation(self, ctx:cminusParser.ActivationContext):
        pass

    # Exit a parse tree produced by cminusParser#activation.
    def exitActivation(self, ctx:cminusParser.ActivationContext):
        pass


