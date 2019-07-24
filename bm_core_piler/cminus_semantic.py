from tabulate import tabulate

from . import cminus_abstract_st

class Symbol:
    def __init__(self, name, scope, line, id_type, data_type, mem_location = -1, params = None):
        self.name = name
        self.scope = scope
        self.lines = {line}
        self.id_type = id_type
        self.data_type = data_type
        self.mem_location = mem_location
        self.params = [params]

    def as_tuple(self):
        return self.name, self.scope, ', '.join(map(str, sorted(self.lines))), self.id_type, self.data_type, self.mem_location, ', '.join(map(str, self.params))

class SymbolTableGenerator(cminus_abstract_st.AbstractStVisitor):
    def __init__(self, abstract_st, mem_init):
        self.table = {}
        self.errors = []
        self._scope = ''
        self._mem_loc = int(mem_init)
        self.source_functions = [
            'input','output','load_os','end_bios',
            'move_HD_mem', 'store_HD','move_reg_proc_OS','move_reg_OS_proc', 
            'swap_process','write_lcd', 'concatenate', 'get_interruption',
            'load_reg_context', 'store_reg_context', 'recover_OS',
            'set_proc_pc', 'get_proc_pc', 'UART_input', 'UART_output'
        ]
        for sf in self.source_functions:
            self.table[sf] = Symbol(sf, 'source', 0, 'funct', 'Source function')

        self.visit(abstract_st)

        if 'main' not in self.table:
                self.errors.append(f'No main function declared')

    def __str__ (self):
        return tabulate(
            tabular_data=[(key,) + symbol.as_tuple() for key, symbol in self.table.items()],
            headers=['Key', 'Id', 'Scope', 'Lines', 'Id Type', 'Var Type', 'Mem Loc', 'Parameters'],
            tablefmt='grid',
        )

    def scoped_name(self, name):
        if not self._scope:
            return f'global.{name}'
        else:
            return f'{self._scope}.{name}'
    
    def check_activation(self, node: cminus_abstract_st.Exp): #lul
        if node.simple_exp: 
            if node.simple_exp.generic_exp:
                if node.simple_exp.generic_exp.term:
                    if node.simple_exp.generic_exp.term.fact:
                        if node.simple_exp.generic_exp.term.fact.activ:
                            return True

    def visit_Program(self, node: cminus_abstract_st.Program):
        for decl in node.decls:
            self.visit(decl)

    def visit_Decl(self, node: cminus_abstract_st.Decl):
        if node.var_decl:
            self.visit(node.var_decl)
        elif node.funct_decl:
            self.visit(node.funct_decl)

    def visit_Var_decl(self, node: cminus_abstract_st.Var_decl):
        name = self.scoped_name(node.id_)
        if name in self.table:
            self.errors.append(f'{node.line}: Variable "{node.id_}" already declared')
            return False
        if node.id_ in self.table:
            self.errors.append(f'{node.line}: Variable "{node.id_}" shares name with a function')
        if node.type_.type_ == 'void':
            self.errors.append(f'{node.line}: Void variable cannot be declared')
        
        if node.num:
            true_scope = self._scope if self._scope != '' else 'global' #
            old_loc = self._mem_loc
            self._mem_loc += int(node.num) 
            self.table[name] = Symbol(node.id_, true_scope, node.line, 'var[]', node.type_.type_, [old_loc, self._mem_loc - 1])
        else:
            true_scope = self._scope if self._scope != '' else 'global' #
            self.table[name] = Symbol(node.id_, true_scope, node.line, 'var', node.type_.type_, self._mem_loc)
            self._mem_loc += 1
        return True

    def visit_Funct_decl(self, node: cminus_abstract_st.Funct_decl):
        if node.id_ in self.table:
            if node.id_ in self.source_functions:
                self.errors.append(f'{node.line}: Function "{node.id_}" atempting to be an override to an source function')
                return
            else:
                self.errors.append(f'{node.line}: Function "{node.id_}" already declared')
                return
        
        if self._scope == '':
            self.table[node.id_] = Symbol(node.id_,'global', node.line, 'funct', node.type_.type_)
        else:
            self.table[node.id_] = Symbol(node.id_, self._scope, node.line, 'funct', node.type_.type_)

        self._scope = node.id_
        self.visit(node.params)
        self.visit(node.comp_decls)
        self._scope = ''

    def visit_Params(self, node: cminus_abstract_st.Params): 
        if node.par_list:
            for param in node.par_list:
                self.visit(param)
            

    def visit_Param(self, node: cminus_abstract_st.Param):
        if None in self.table[self._scope].params:
            self.table[self._scope].params.remove(None) #gambs

        self.table[self._scope].params.append(node.id_)
        name = self.scoped_name(node.id_)
        if name in self.table:
            self.errors.append(f'{node.line}: Variable "{node.id_}" already declared')
            return False
        if node.type_.type_ == 'void':
            self.errors.append(f'{node.line}: Void variable cannot be used as a function parameter')

        if node.isArray: 
            self.table[name] = Symbol(node.id_, self._scope, node.line, 'var[]', node.type_.type_, self._mem_loc)
        else:
            self.table[name] = Symbol(node.id_, self._scope, node.line, 'var', node.type_.type_, self._mem_loc)
        self._mem_loc += 1        

    def visit_Comp_decl(self, node: cminus_abstract_st.Comp_decl):
        if node.local_decl:
            for decl in node.local_decl:
                self.visit(decl)
        if node.stmt_list:
            for stmt in node.stmt_list:
                self.visit(stmt)

    def visit_Local_decl(self, node: cminus_abstract_st.Local_decl):
        for decl in node.var_decls:
            self.visit(decl)
    
    def visit_Stmt_list(self, node: cminus_abstract_st.Stmt_list):
        for stmt in node.stmts:
            self.visit(stmt)

    def visit_Stmt(self, node: cminus_abstract_st.Stmt):
        self.visit(node.stmt_type)

    def visit_Exp_decl(self, node: cminus_abstract_st.Exp_decl):
        if node.exp:
            self.visit(node.exp)

    def visit_Select_decl(self, node: cminus_abstract_st.Select_decl):
        self.visit(node.condition)
        for stmt in node.if_body:
            self.visit(stmt)
        if node.else_body:
            for stmt in node.else_body:
                self.visit(stmt)

    def visit_Iter_decl(self, node: cminus_abstract_st.Iter_decl):
        self.visit(node.condition)
        self.visit(node.stmts)

    def visit_Ret_decl(self, node: cminus_abstract_st.Ret_decl):
        if node.exp:
            self.visit(node.exp)
    
    def visit_Exp(self, node: cminus_abstract_st.Exp):
        var_type = None
        if node.var:
            self.visit(node.var)
            var = self.scoped_name(node.var.id_)
            if var not in self.table:
                var = f'global.{node.var.id_}'
            var_type = self.table[var].data_type
        if node.simple_exp:
            self.visit(node.simple_exp)
        if node.exp:
            self.visit(node.exp)
        # if no variable is beeing assigned to the void value return, the void function can be called
        if self.check_activation(node):
            activ_node = node.simple_exp.generic_exp.term.fact.activ            
            if activ_node.id_ in self.table:
                funct_call = self.table[activ_node.id_]
                true_type = funct_call.data_type
                if true_type == 'void' and var_type == 'int':
                    self.errors.append(f'{node.line}: Invalid assignment of type {true_type}')

    '''
    def visit_Exp(self, node: cminus_abstract_st.Exp):
        var_type = None
        if node.var:
            self.visit(node.var)
            var = self.scoped_name(node.var.id_)
            var_type = self.table[var].data_type
        if node.simple_exp:
            self.visit(node.simple_exp)
        if node.exp:
            self.visit(node.exp)
        # if no variable is beeing assigned to the void value return, the void function can be called
        if self.check_activation(node):
            activ_node = node.simple_exp.generic_exp.term.fact.activ            
            if activ_node.id_ in self.table:
                funct_call = self.table[activ_node.id_]
                true_type = funct_call.data_type
                if true_type == 'void' and var_type == 'int':
                    self.errors.append(f'{node.line}: Invalid assignment of type {true_type}')
    '''

    def visit_Var (self, node: cminus_abstract_st.Var):
        var_id = node.id_
        name = self.scoped_name(node.id_)
        global_name = f'global.{node.id_}'
        in_local_scope = name in self.table
        in_global_scope = global_name in self.table
        
        if in_local_scope:
            self.table[name].lines.add(node.line)
        elif in_global_scope:
            self.table[global_name].lines.add(node.line)
        else:
            self.errors.append(f'{node.line}: Variable "{node.id_}" used whitout previous declaration')
            return False
        return True          
    
    def visit_Simple_exp(self, node: cminus_abstract_st.Simple_exp):
        if node.exp_left:
            self.visit(node.exp_left)
            self.visit(node.exp_right)
        else:
            self.visit(node.generic_exp)
             
    def visit_Sum_exp(self, node: cminus_abstract_st.Sum_exp):
        if node.op:
            self.visit(node.sum_exp)
            self.visit(node.term)
        else:
            self.visit(node.term)

    def visit_Term(self, node: cminus_abstract_st.Term):
        if node.op:
            self.visit(node.term)
            self.visit(node.fact)
        else:
            self.visit(node.fact)

    def visit_Fact(self, node: cminus_abstract_st.Fact):
        if node.exp:
            self.visit(node.exp)
        if node.var:
            self.visit(node.var)
        if node.activ:
            self.visit(node.activ)

    def visit_Activation(self, node: cminus_abstract_st.Activation):
        name = node.id_
        in_global_scope = node.id_ in self.table
        if not in_global_scope:
            self.errors.append(f'{node.line}: Function "{node.id_}" used whitout declaration')
            return False

        self.table[name].lines.add(node.line)
        
        param_count = 0
        if name != 'input' and name not in self.source_functions:
            if len(self.table[name].params) == 1 and self.table[name].params[0] is None:
                expected_param_num = 0
            else:
                expected_param_num = len(self.table[name].params)
            for arg in node.args_list:
                param_count += 1
                self.visit(arg)
            
            if param_count != expected_param_num:
                self.errors.append(f'{node.line}: Function "{node.id_}" expects {expected_param_num} arguments, but {param_count} were given')


    '''
    def visit_Activation(self, node: cminus_abstract_st.Activation):
        name = node.id_
        in_global_scope = node.id_ in self.table
        if not in_global_scope:
            self.errors.append(f'{node.line}: Function "{node.id_}" used whitout declaration')
            return False

        self.table[name].lines.add(node.line)
        
        param_count = 0
        if name != 'input' and name not in self.source_functions:
            expected_param_num = len(self.table[name].params)
            for arg in node.args_list:
                param_count += 1
                self.visit(arg)
            
            if param_count != expected_param_num:
                self.errors.append(f'{node.line}: Function "{node.id_}" expects {expected_param_num} arguments, but {param_count} were given')


    '''