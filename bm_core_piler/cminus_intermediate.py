from . import cminus_abstract_st

class IntermediateCodeGenerator(cminus_abstract_st.AbstractStVisitor):

    def __init__(self, abstract_st):
        super().__init__()
        self.intermediate_list = []
        self.temp_num = 0
        self.label_num = 1

        self.visit(abstract_st)

    def visit_Program(self, node: cminus_abstract_st.Program):
        for decl in node.decls:
            self.visit(decl)

    def visit_Decl(self, node: cminus_abstract_st.Decl):
        if node.funct_decl is None:
            self.visit(node.var_decl)
        else:
            self.visit(node.funct_decl)

    def visit_Var_decl(self, node: cminus_abstract_st.Var_decl):
        self.visit(node.type_)

    def visit_Type_especifier(self, node: cminus_abstract_st.Var_decl):
        return node.type_

    def visit_Funct_decl(self, node: cminus_abstract_st.Funct_decl):
        temp = ['function', node.id_, '_', '_']
        self.intermediate_list.append(temp)
        self.visit(node.params)
        self.visit(node.comp_decls)

    def visit_Params(self, node: cminus_abstract_st.Params):
        if node.par_list is not None:
            for param in node.par_list:
                self.visit(param)

    def visit_Param(self, node: cminus_abstract_st.Params):
        self.visit(node.type_)

    def visit_Comp_decl(self, node: cminus_abstract_st.Comp_decl):
        for decl in node.local_decl:
            self.visit(decl)
        for stmt in node.stmt_list:
            self.visit(stmt)

    def visit_Local_decl(self, node:cminus_abstract_st.Local_decl):
        for decl in node.var_decls:
            self.visit(decl)

    def visit_Stmt_list(self, node:cminus_abstract_st.Stmt_list):
        for stmt in node.stmts:
            self.visit(stmt)

    def visit_Stmt(self, node: cminus_abstract_st.Stmt):
        self.visit(node.stmt_type)

    def visit_Exp_decl(self, node: cminus_abstract_st.Exp_decl):
        self.visit(node.exp)

    def visit_Select_decl(self, node: cminus_abstract_st.Select_decl):
        left = right = logic_op = None
        self.visit(node.condition)

        if node.condition.simple_exp and node.condition.simple_exp.relational:
            node_simple_exp = node.condition.simple_exp
            node_fact_left = self.get_factor_child(node_simple_exp.exp_left)
            node_fact_right = self.get_factor_child(node_simple_exp.exp_right)

            if node_fact_left.var:
                left = node_fact_left.var.id_
            elif node_fact_left.num:
                left = node_fact_left.num
            elif node_fact_left.activ:
                left = node_fact_left.activ.id_

            if node_fact_right.var:
                right = node_fact_right.var.id_
            elif node_fact_right.num:
                right = node_fact_right.num
            elif node_fact_right.activ:
                right = node_fact_right.activ.id_

            logic_op = self.get_relational_operator(node_simple_exp.relational)

            #old_label = self.label_num
            new_label = self.label_num+1
            temp = [logic_op, left, right, f't{self.temp_num}']
            # [jump if, this value is True, to this label, _ ]
            label_jump = ['jump_if_false', f't{self.temp_num}', f'L{new_label}', '_']
            self.intermediate_list.append(temp)
            self.intermediate_list.append(label_jump)
            self.temp_num += 1
            self.label_num += 1

        for stmt in node.if_body:
            self.visit(stmt)

        self.label_num += 1

        if node.else_body: # if there are else statements
            aux = self.label_num
            goto = ['goto',f'L{self.label_num}','_','_']
            self.intermediate_list.append(goto)
            label = ['label', f'L{new_label}', '_', '_']
            self.intermediate_list.append(label)
            #
            end_label = ['end_label', f'L{new_label}', '_', '_']
            self.intermediate_list.append(end_label)

            for stmt in node.else_body:
                self.visit(stmt)

            goto_destiny = ['label', f'L{aux}', '_', '_']
            self.intermediate_list.append(goto_destiny)
            #
            end_label = ['end_label', f'L{aux}', '_', '_']
            self.intermediate_list.append(end_label)

        else: # if there aren't else statements
            label = ['label', f'L{new_label}', '_', '_']
            self.intermediate_list.append(label)
            #
            end_label = ['end_label', f'L{new_label}', '_', '_']
            self.intermediate_list.append(end_label)

    def visit_Iter_decl(self, node: cminus_abstract_st.Iter_decl):
        left = right = logic_op = None

        self.label_num += 1
        label = ['label', f'L{self.label_num}', '_', '_']
        self.intermediate_list.append(label)

        self.visit(node.condition)

        if node.condition.simple_exp and node.condition.simple_exp.relational:
            node_simple_exp = node.condition.simple_exp
            node_fact_left = self.get_factor_child(node_simple_exp.exp_left)
            node_fact_right = self.get_factor_child(node_simple_exp.exp_right)

            if node_fact_left.var:
                left = node_fact_left.var.id_
            elif node_fact_left.num:
                left = node_fact_left.num
            elif node_fact_left.activ:
                left = node_fact_left.activ.id_

            if node_fact_right.var:
                right = node_fact_right.var.id_
            elif node_fact_right.num:
                right = node_fact_right.num
            elif node_fact_right.activ:
                left = node_fact_right.activ.id_

            logic_op = self.get_relational_operator(node_simple_exp.relational)

            old_label = self.label_num
            new_label = self.label_num + 1
            #label = ['label', f'L{old_label}', '_', '_']
            temp = [logic_op, left, right, f't{self.temp_num}']
            # [jump if, this value is True, to this label, _ ]
            label_jump = ['jump_if_false', f't{self.temp_num}', f'L{new_label}', '_']
            #self.intermediate_list.append(label)
            self.intermediate_list.append(temp)
            self.intermediate_list.append(label_jump)
            self.temp_num += 1
            self.label_num += 2

            self.visit(node.stmts)

            goto = ['goto', f'L{old_label}','_','_']
            end_label = ['end_label', f'L{old_label}', '_', '_']
            label = ['label', f'L{new_label}', '_', '_']
            new_end_label = ['end_label', f'L{new_label}', '_', '_']
            self.intermediate_list.append(goto)
            self.intermediate_list.append(end_label)
            self.intermediate_list.append(label)
            self.intermediate_list.append(new_end_label)

    def visit_Ret_decl(self, node: cminus_abstract_st.Ret_decl):
        value = index = None
        if node.exp:
            self.visit(node.exp)

            node_fact = self.get_factor_child(node.exp)
            if node_fact.num:
                value = node_fact.num
            elif node_fact.activ:
                value = node_fact.activ.id_
            elif node_fact.var:
                value = node_fact.var.id_

        # [return, this value (if it exists), _ , _ ]
        ret = ['return', value if value else '_', '_', '_']
        self.intermediate_list.append(ret)

    def visit_Exp(self, node: cminus_abstract_st.Exp):
        if node.simple_exp:
            self.visit(node.simple_exp)
        else:
            self.visit(node.exp)
            self.visit(node.var)

            val = None
            node_fact = self.get_multiple_assign_factor(node.exp)

            if node_fact.num:
                val = node_fact.num
            elif node_fact.var:
                val = node_fact.var.id_
            elif node_fact.activ:
                val = node_fact.activ.id_
            if node_fact.exp:
                aux_node = self.get_non_exp_factor(node_fact.exp)
                if aux_node.num:
                    val = aux_node.num
                elif aux_node.var:
                    val = aux_node.var.id_
                elif aux_node.activ:
                    val = aux_node.activ.id_

            # 'array assign' is made to an array position and 'assign' is made to normal variables
            # [assign, to this value, this other value, _ ]
            assign_type = 'array_assign' if node.var.exp else 'assign'
            temp = [assign_type, node.var.id_, val if val else '_', '_']
            self.intermediate_list.append(temp)
            if assign_type == 'array_assign':
                self.temp_num += 1

    def visit_Var(self, node: cminus_abstract_st.Var):
        if node.exp:
            self.visit(node.exp)

            node_fact = self.get_factor_child(node.exp)
            if node_fact.num:
                index = node_fact.num
            elif node_fact.var:
                index = node_fact.var.id_
            elif node_fact.activ:
                index = node_fact.activ.id_

            # if var node has an exp, it is a array, so it's index must be evaluated as a temporary
            # [assign, to this temporary, the value of this array, on this position]
            aux_temp = ['weak_assign', f't{self.temp_num}', node.id_, index]
            node.id_ = f't{self.temp_num}'
            self.intermediate_list.append(aux_temp)
            self.temp_num += 1

    def visit_Simple_exp(self, node: cminus_abstract_st.Simple_exp): ##
        if node.relational:
            self.visit(node.exp_left)
            self.visit(node.exp_right)
        else:
            self.visit(node.generic_exp)

    def visit_Sum_exp(self, node: cminus_abstract_st.Sum_exp):
        left = right = old_var = old_num = None
        self.visit(node.term)
        if node.op:
            self.visit(node.sum_exp)

            # right operand determination
            node_r = self.get_factor_child(node)
            if node_r is not None:
                if node_r.var:  # if fact node has variable child
                    right = node_r.var.id_
                    old_var = right
                    node_r.var.id_ = f't{self.temp_num}'

                elif node_r.num: # if fact node has number child
                    right = node_r.num
                    old_num = right
                    node_r.num = f't{self.temp_num}'

                elif node_r.activ: # if fact node has activation child
                    right = node_r.activ.id_
                    node_r.activ.id_ = f't{self.temp_num}'

                elif node_r.exp: # if fact node has expression child
                    aux_node = self.get_non_exp_factor(node_r.exp)
                    if aux_node.num:
                        right = aux_node.num
                        aux_node.num = f't{self.temp_num}'
                    elif aux_node.var:
                        right = aux_node.var.id_
                        aux_node.var.id_ = f't{self.temp_num}'
                    elif aux_node.activ:
                        right = aux_node.activ.id_
                        aux_node.activ.id_ = f't{self.temp_num}'

            # left operand determination
            node_l = self.get_factor_child(node.sum_exp)
            if node_l is not None:
                if node_l.var: # if fact node has variable child
                    left = node_l.var.id_
                    old_var = left
                    node_l.var.id_ = f't{self.temp_num}'

                elif node_l.num: # if fact node has number child
                    left = node_l.num
                    old_num = left
                    node_l.num = f't{self.temp_num}'

                elif node_l.activ: # if fact node has activation child
                    left = node_l.activ.id_
                    node_l.activ.id_ = f't{self.temp_num}'

                elif node_l.exp: # if fact node has expression child
                    aux_node = self.get_non_exp_factor(node_l.exp)
                    if aux_node.num:
                        left = aux_node.num
                        aux_node.num = f't{self.temp_num}'
                    elif aux_node.var:
                        left = aux_node.var.id_
                        aux_node.var.id_ = f't{self.temp_num}'
                    elif aux_node.activ:
                        left = aux_node.activ.id_
                        aux_node.activ.id_ = f't{self.temp_num}'

            if right is None: # variable/array and number as expression operands treatment
                right = old_num if old_num else old_var
            if left is None:
                left = old_var if old_var else old_num

            # [this operation, with this value, and this value, will result in this value]
            operation = 'addition' if node.op == '+' else 'subtraction'
            temp = [operation, left, right, f't{self.temp_num }']
            self.intermediate_list.append(temp)
            self.temp_num += 1

    def visit_Term(self, node: cminus_abstract_st.Term):
        left = right = old_var = old_num = None
        self.visit(node.fact)
        if node.op:
            self.visit(node.term)

            # right operand determination
            node_r = self.get_factor_child(node)
            if node_r is not None:
                if node_r.var:  # if fact node has variable child
                    right = node_r.var.id_
                    old_var = right
                    node_r.var.id_ = f't{self.temp_num}'

                elif node_r.num: # if fact node has number child
                    right = node_r.num
                    old_num = right
                    node_r.num = f't{self.temp_num}'

                elif node_r.activ: # if fact node has activation child
                    right = node_r.activ.id_
                    node_r.activ.id_ = f't{self.temp_num}'

                elif node_r.exp: # if fact node has expression child
                    aux_node = self.get_non_exp_factor(node_r.exp)
                    if aux_node.num:
                        right = aux_node.num
                        aux_node.num = f't{self.temp_num}'
                    elif aux_node.var:
                        right = aux_node.var.id_
                        aux_node.var.id_ = f't{self.temp_num}'
                    elif aux_node.activ:
                        right = aux_node.activ.id_
                        aux_node.activ.id_ = f't{self.temp_num}'

            # left operand determination
            node_l = self.get_factor_child(node.term)
            if node_l is not None:
                if node_l.var: # if fact node has variable child
                    left = node_l.var.id_
                    old_var = left
                    node_l.var.id_ = f't{self.temp_num}'

                elif node_l.num: # if fact node has number child
                    left = node_l.num
                    old_num = left
                    node_l.num = f't{self.temp_num}'

                elif node_l.activ: # if fact node has activation child
                    left = node_l.activ.id_
                    node_l.activ.id_ = f't{self.temp_num}'

                elif node_l.exp: # if fact node has expression child
                    aux_node = self.get_non_exp_factor(node_l.exp)
                    if aux_node.num:
                        left = aux_node.num
                        aux_node.num = f't{self.temp_num}'
                    elif aux_node.var:
                        left = aux_node.var.id_
                        aux_node.var.id_ = f't{self.temp_num}'
                    elif aux_node.activ:
                        left = aux_node.activ.id_
                        aux_node.activ.id_ = f't{self.temp_num}'

            if right is None: # variable/array and number as expression operands treatment
                right = old_num if old_num else old_var
            if left is None:
                left = old_var if old_var else old_num

            # [this operation, with this value, and this value, will result in this value]
            operation = 'multiplication' if node.op == '*' else 'division'
            temp = [operation, left, right, f't{self.temp_num }']
            self.intermediate_list.append(temp)
            self.temp_num += 1

    def visit_Fact(self ,node: cminus_abstract_st.Fact):
        if node.exp:
            self.visit(node.exp)
        if node.var:
            self.visit(node.var)
        if node.activ:
            self.visit(node.activ)
        # num node is not treated since it's value is accessible directly

    def visit_Activation(self, node: cminus_abstract_st.Activation):
        for arg in node.args_list:
            self.visit(arg)
            node_fact = self.get_factor_child(arg)

            if node_fact.num:
                res = node_fact.num
            elif node_fact.var:
                res = node_fact.var.id_
            elif node_fact.activ:
                res = node_fact.activ.id_

            # [an argument, to this function, is this value, _ ]
            funct_arg = [f'arg', node.id_, res, '_']
            self.intermediate_list.append(funct_arg)

        # [call, this function, with this number of arguments, and put it's return value on this temporary]
        funct = ['call', node.id_, len(node.args_list), f't{self.temp_num}']
        node.id_ = f't{self.temp_num}'
        self.intermediate_list.append(funct)
        self.temp_num += 1


    # auxiliar functions

    def get_factor_child(self, node): # return is simply a fact node, which might have and exp child
        if type(node).__name__ == 'Exp':
            if node.exp:
                self.get_factor_child(node.exp)
            else:
                return self.get_factor_child(node.simple_exp)

        elif type(node).__name__ == 'Simple_exp':
            if node.exp_left:
                self.get_factor_child(node.exp_left)
                self.get_factor_child(node.exp_right)
            else:
                return self.get_factor_child(node.generic_exp)

        elif type(node).__name__ == 'Sum_exp':
            if node.sum_exp:
                self.get_factor_child(node.sum_exp)
            if node.term:
                return self.get_factor_child(node.term)

        elif type(node).__name__ == 'Term':
            if node.term:
                self.get_factor_child(node.term)
            if node.fact:
                return node.fact

    def get_non_exp_factor(self, node): # return is guaranteed to be a fact node whose child can be everything except an exp
        if type(node).__name__ == 'Exp':
            if node.exp:
                self.get_non_exp_factor(node.exp)
            else:
                return self.get_non_exp_factor(node.simple_exp)

        elif type(node).__name__ == 'Simple_exp':
            if node.exp_left:
                self.get_non_exp_factor(node.exp_left)
                self.get_non_exp_factor(node.exp_right)
            else:
                return self.get_non_exp_factor(node.generic_exp)

        elif type(node).__name__ == 'Sum_exp':
            if node.sum_exp:
                self.get_non_exp_factor(node.sum_exp)
            if node.term:
                return self.get_non_exp_factor(node.term)

        elif type(node).__name__ == 'Term':
            if node.term:
                self.get_non_exp_factor(node.term)
            if node.fact:
                return self.get_non_exp_factor(node.fact)

        elif type(node).__name__ == 'Fact':
            if node.exp is None: # ensuring not a exp factor node
                return node
            else:
                return self.get_non_exp_factor(node.exp)

    def get_multiple_assign_factor(self, node): # return is the final factor node of the multiple assignement
        if type(node).__name__ == 'Exp':
            return self.get_multiple_assign_factor(node.exp) if node.exp else self.get_factor_child(node.simple_exp)

    def get_relational_operator(self, node: cminus_abstract_st.Relational):
        if node.type_ == "<=":
            op = 'less_or_equal_than'
        elif node.type_ == "<":
            op = 'less_than'
        elif node.type_ == ">":
            op = 'greater_than'
        elif node.type_ == ">=":
            op = 'greater_or_equal_than'
        elif node.type_ == "==":
            op = 'equal'
        elif node.type_ == "!=":
            op = 'not_equal'
        return op
