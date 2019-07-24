import re

class AssemblyGenerator():

	def __init__(self, semantic_analysis, intermediate, init_stack, mode):
		self.source_functions = semantic_analysis.source_functions
		self.symbol_table = semantic_analysis.table
		self.intermediate_code = intermediate
		self.init_stack = init_stack
		self.mode = mode

		self.temp_regs = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]
		self.source_funct_args = []
		self.reg_map = {} # reg_map[temporary value] = register number
		self.label_map = {} # label_map[label] = register number
		self.ra_stored = {} # ra_stored[function_name] = true/false
		self.array_temp = [] # identifyes temporaryes that hold an array address
		self.actual_scope = '' # holds the actual scope for specific treatments
		self.comparisons = ['less_or_equal_than', 'less_than', 'greater_than', 'greater_or_equal_than', 'equal', 'not_equal']
		self.asm_list = []

		#set $sp and start at main function
		self.asm_list.append(['ldi', '$sp,', f'{self.init_stack}'])
		self.asm_list.append(['jmp','main'])
		self.synthesis()
		self.asm_list.append(['nop'])
		self.asm_list.append(['endp'])
		self.asm_list.append(['nop'])
		self.asm_list.append(['hlt'])

	# check if token is a declared variable, prioritizing local scope ones
	def is_declared(self, token): 
		if f'{self.actual_scope}.{token}' in self.symbol_table:
			return True
		elif f'global.{token}' in self.symbol_table:
			return True
		else:
			return False

	# get the intermediate's operand type, as declared variable, immediate or temporary
	def intermediate_tkn_type(self, token): 
		if self.is_declared(token):
			return 'var'
		elif re.match('t[0-9]', token):
			return 'temp'
		else:
			return 'num'

	# creates a symbol_table key depending if the symbol's scope is global or local
	def build_table_key(self, token): 
		if f'{self.actual_scope}.{token}' in self.symbol_table:
			return f'{self.actual_scope}.{token}'
		elif f'global.{token}' in self.symbol_table:
			return f'global.{token}'

	# updates the register, marking it as able to be overwritten
	def set_reg_free(self, reg_number): 
		self.temp_regs[int(reg_number)] = 0

	# updates the register, marking it so it can't be overwritten
	def set_reg_busy(self, reg_number): 
		self.temp_regs[int(reg_number)] = 1

	# returns the index of the next free register
	def get_free_reg(self): 
		for i in range(1,len(self.temp_regs)):
			if self.temp_regs[i] == 0:
				return i

	def get_symbol_id_type(self, symbol):
		return symbol.id_type

	def get_symbol_data_type(self, symbol):
		return symbol.data_type

	def get_symbol_mem_location(self, symbol):
		return symbol.mem_location

	def get_symbol_parameters(self, symbol):
		return symbol.params

	# main method
	def synthesis(self):
		for inter in self.intermediate_code:
			inter_op = inter[0]
			if inter_op == 'addition' or inter_op == 'subtraction':
				instr_name = 'add' if inter_op == 'addition' else 'sub'
				# (+|-) two declared variables
				if self.intermediate_tkn_type(inter[1]) == self.intermediate_tkn_type(inter[2]) == 'var':
					# loading first variable value
					reg = self.get_free_reg()
					self.set_reg_busy(reg)
					aux_reg = self.get_free_reg()
					self.asm_list.append(['ld', f'$r{reg},', '$r0,', self.get_symbol_mem_location(self.symbol_table[self.build_table_key(inter[2])])])
					# loading second variable value
					self.asm_list.append(['ld', f'$r{aux_reg},', '$r0,', self.get_symbol_mem_location(self.symbol_table[self.build_table_key(inter[1])])])
					self.asm_list.append([instr_name, f'$r{reg},', f'$r{reg},', f'$r{aux_reg}'])
					self.reg_map[inter[3]] = reg

				# (+|-) two non declared values
				elif self.intermediate_tkn_type(inter[1]) == self.intermediate_tkn_type(inter[2]) == 'num':
					reg = self.get_free_reg()
					self.asm_list.append(['ldi', f'$r{reg},', inter[1]])
					self.asm_list.append([f'{instr_name}i',f'$r{reg},', f'$r{reg},',inter[2]])
					self.reg_map[inter[3]] = reg
					self.set_reg_busy(reg)

				# (+|-) two temporary values
				elif self.intermediate_tkn_type(inter[1]) == self.intermediate_tkn_type(inter[2]) == 'temp':
					# if neither temporaries are array addresses
					if inter[1] not in self.array_temp and inter[2] not in self.array_temp:
						self.asm_list.append([instr_name, f'$r{self.reg_map[inter[2]]},', f'$r{self.reg_map[inter[2]]},', f'$r{self.reg_map[inter[1]]}'])
						self.reg_map[inter[3]] = self.reg_map[inter[2]]
						self.set_reg_free(self.reg_map[inter[1]])
						self.reg_map[inter[2]] = -1
					# if first temporary is an array address
					elif inter[1] in self.array_temp and inter[2] not in self.array_temp:
						array_val_reg = self.reg_map[inter[1]]
						aux_reg = self.get_free_reg()
						# getting the value on the address stored on the temporary's respective register
						self.asm_list.append(['ld', f'$r{aux_reg},', f'$r{array_val_reg},', '0'])
						self.asm_list.append([instr_name, f'$r{self.reg_map[inter[2]]},', f'$r{self.reg_map[inter[2]]},', f'$r{aux_reg}'])
						self.reg_map[inter[3]] = self.reg_map[inter[2]]
						self.set_reg_free(self.reg_map[inter[1]])
						self.reg_map[inter[2]] = -1
					# if second temporary is an array address
					elif inter[1] not in self.array_temp and inter[2] in self.array_temp:
						array_val_reg = self.reg_map[inter[2]]
						aux_reg = self.get_free_reg()
						# getting the value on the address stored on the temporary's respective register
						self.asm_list.append(['ld', f'$r{aux_reg},', f'$r{array_val_reg},', '0'])
						self.asm_list.append([instr_name, f'$r{self.reg_map[inter[1]]},', f'$r{self.reg_map[inter[1]]},', f'$r{aux_reg}'])
						self.reg_map[inter[3]] = self.reg_map[inter[1]]
						self.set_reg_free(self.reg_map[inter[2]])
						self.reg_map[inter[1]] = -1
					# if both temporaries are array addresses
					else:
						# getting the value on the address stored on the first temporary's respective register
						first_array_val_reg = self.reg_map[inter[1]]
						first_val_reg = self.get_free_reg()
						self.set_reg_busy(first_val_reg)
						self.asm_list.append(['ld', f'$r{first_val_reg},', f'$r{first_array_val_reg},', '0'])
						# getting the value on the address stored on the second temporary's respective register
						second_array_val_reg = self.reg_map[inter[2]]
						second_val_reg = self.get_free_reg()
						self.asm_list.append(['ld', f'$r{second_val_reg},', f'$r{second_array_val_reg},', '0'])
						# finally (+|-) them for the operation result
						self.asm_list.append([instr_name, f'$r{first_val_reg},', f'$r{first_val_reg},', f'$r{second_val_reg}'])
						self.reg_map[inter[3]] = first_val_reg
						# clearing the auxiliar registers
						self.set_reg_free(first_array_val_reg)
						self.reg_map[inter[1]] = -1
						self.set_reg_free(second_array_val_reg)
						self.reg_map[inter[2]] = -1

				# (+|-) one declared variable and one non declared value
				elif self.intermediate_tkn_type(inter[1]) == 'var' and self.intermediate_tkn_type(inter[2]) == 'num' or self.intermediate_tkn_type(inter[1]) == 'num' and self.intermediate_tkn_type(inter[2]) == 'var':
					# first case [a (+|-) 1]
					if self.intermediate_tkn_type(inter[1]) == 'var' and self.intermediate_tkn_type(inter[2]) == 'num':
						reg = self.get_free_reg()
						self.asm_list.append(['ld', f'$r{reg},', '$r0,', self.get_symbol_mem_location(self.symbol_table[self.build_table_key(inter[1])])])
						self.asm_list.append([f'{instr_name}i', f'$r{reg},', f'$r{reg},', inter[2]])
						self.reg_map[inter[3]] = reg
						self.set_reg_busy(reg)
					# second case [1 (+|-) a]
					else:
						reg = self.get_free_reg()
						self.asm_list.append(['ld', f'$r{reg},', '$r0,', self.get_symbol_mem_location(self.symbol_table[self.build_table_key(inter[2])])])
						self.asm_list.append(['addi', f'$r{reg},', f'$r{reg},', inter[1]])
						self.reg_map[inter[3]] = reg
						self.set_reg_busy(reg)

				# (+|-) one declared variable and one temporary value
				elif self.intermediate_tkn_type(inter[1]) == 'var' and self.intermediate_tkn_type(inter[2]) == 'temp' or self.intermediate_tkn_type(inter[1]) == 'temp' and self.intermediate_tkn_type(inter[2]) == 'var':
					# first case [a (+|-) t0]
					if self.intermediate_tkn_type(inter[1]) == 'var' and self.intermediate_tkn_type(inter[2]) == 'temp':
						# if temporary holds an array address
						if inter[2] in self.array_temp:
							reg = self.get_free_reg()
							self.set_reg_busy(reg)
							self.asm_list.append(['ld', f'$r{reg},', '$r0,', self.get_symbol_mem_location(self.symbol_table[self.build_table_key(inter[1])])])
							aux_reg = self.get_free_reg()
							array_val_reg = self.reg_map[inter[2]]
							self.asm_list.append(['ld', f'$r{aux_reg},', f'$r{array_val_reg},', '0'])
							self.asm_list.append([instr_name, f'$r{reg},', f'$r{reg},', f'$r{aux_reg}'])
							self.reg_map[inter[3]] = reg
							self.set_reg_free(array_val_reg)
							self.reg_map[2] = -1
						else:
							reg = self.get_free_reg()
							self.set_reg_busy(reg)
							self.asm_list.append(['ld', f'$r{reg},', '$r0,', self.get_symbol_mem_location(self.symbol_table[self.build_table_key(inter[1])])])
							self.asm_list.append([instr_name, f'$r{reg},', f'$r{reg},', f'$r{self.reg_map[inter[2]]}'])
							self.reg_map[inter[3]] = reg
							self.set_reg_free(self.reg_map[inter[2]])
							self.reg_map[inter[2]] = -1
					# second case [t0 (+|-) a]
					else:
						# if temporary holds an array address
						if inter[1] in self.array_temp:
							reg = self.get_free_reg()
							self.set_reg_busy(reg)
							self.asm_list.append(['ld', f'$r{reg},', '$r0,', self.get_symbol_mem_location(self.symbol_table[self.build_table_key(inter[2])])])
							aux_reg = self.get_free_reg()
							array_val_reg = self.reg_map[inter[1]]
							self.asm_list.append(['ld', f'$r{aux_reg},', f'$r{array_val_reg},', '0'])
							self.asm_list.append([instr_name, f'$r{reg},', f'$r{reg},', f'$r{aux_reg}'])
							self.reg_map[inter[3]] = reg
							self.set_reg_free(array_val_reg)
							self.reg_map[1] = -1
						else:
							reg = self.get_free_reg()
							self.asm_list.append(['ld', f'$r{reg},', '$r0,', self.get_symbol_mem_location(self.symbol_table[self.build_table_key(inter[2])])])
							self.asm_list.append([instr_name, f'$r{self.reg_map[inter[1]]},', f'$r{self.reg_map[inter[1]]},', f'$r{reg}'])
							self.reg_map[inter[3]] = self.reg_map[inter[1]]
							self.set_reg_busy(self.reg_map[inter[3]])
							self.reg_map[inter[1]] = -1

				# (+|-) one temporary and one non declared value
				elif self.intermediate_tkn_type(inter[1]) == 'temp' and self.intermediate_tkn_type(inter[2]) == 'num' or self.intermediate_tkn_type(inter[1]) == 'num' and self.intermediate_tkn_type(inter[2]) == 'temp':
					# first case [t0 (+|-) 1]
					if self.intermediate_tkn_type(inter[1]) == 'temp' and self.intermediate_tkn_type(inter[2]) == 'num':
						# if temporary holds an array address
						if inter[1] in self.array_temp:
							reg = self.get_free_reg()
							self.set_reg_busy(reg)
							array_val_reg = self.reg_map[inter[1]]
							self.asm_list.append(['ld', f'$r{reg},', f'$r{array_val_reg},', '0'])
							self.asm_list.append([f'{instr_name}i', f'$r{reg},', f'$r{reg},', inter[2]])
							self.reg_map[inter[3]] = reg
							self.reg_map[inter[1]] = -1
						else:
							reg = self.reg_map[inter[1]]
							self.set_reg_busy(reg)
							self.asm_list.append([f'{instr_name}i', f'$r{reg},', f'$r{reg},', inter[2]])
							self.reg_map[inter[3]] = reg
							self.reg_map[inter[1]] = -1
					# second case [1 (+|-) t0]
					else:
						# if temporary holds an array address
						if inter[2] in self.array_temp:
							reg = self.get_free_reg()
							self.set_reg_busy(reg)
							array_val_reg = self.reg_map[inter[2]]
							self.asm_list.append(['ld', f'$r{reg},', f'$r{array_val_reg},', '0'])
							self.asm_list.append([f'{instr_name}i', f'$r{reg},', f'$r{reg},', inter[1]])
							self.reg_map[inter[3]] = reg
							self.reg_map[inter[2]] = -1
						else:
							reg = self.reg_map[inter[2]]
							self.set_reg_busy(reg)
							self.asm_list.append([f'{instr_name}i', f'$r{reg},', f'$r{reg},', inter[1]])
							self.reg_map[inter[3]] = reg
							self.reg_map[inter[2]] = -1

			elif inter_op == 'multiplication' or inter_op == 'division':
				instr_name = 'mult' if inter_op == 'multiplication' else 'div'
				# (*|/) two declared variables
				if self.intermediate_tkn_type(inter[1]) == self.intermediate_tkn_type(inter[2]) == 'var':
					# (*|/) first variable value
					reg = self.get_free_reg()
					self.set_reg_busy(reg)
					aux_reg = self.get_free_reg()
					self.asm_list.append(['ld', f'$r{reg},', '$r0,', self.get_symbol_mem_location(self.symbol_table[self.build_table_key(inter[1])])])
					# loading second variable value
					self.asm_list.append(['ld', f'$r{aux_reg},', '$r0,', self.get_symbol_mem_location(self.symbol_table[self.build_table_key(inter[2])])])
					self.asm_list.append([instr_name, f'$r{reg},', f'$r{reg}', f'$r{aux_reg}'])
					self.reg_map[inter[3]] = reg

				# (*|/) two non declared values
				elif self.intermediate_tkn_type(inter[1]) == self.intermediate_tkn_type(inter[2]) == 'num':
					# loading first immediate value
					reg = self.get_free_reg()
					self.set_reg_busy(reg)
					aux_reg = self.get_free_reg()
					self.asm_list.append(['ldi',f'$r{reg},',inter[1]])
					# loading second immediate value
					self.asm_list.append(['ldi',f'$r{aux_reg},', inter[2]])
					self.asm_list.append([instr_name, f'$r{reg},', f'$r{reg},', f'$r{aux_reg}'])
					self.reg_map[inter[3]] = reg;

				# (*|/) two temporary values
				elif self.intermediate_tkn_type(inter[1]) == self.intermediate_tkn_type(inter[2]) == 'temp':
					# if neither temporaries are array addresses
					if inter[1] not in self.array_temp and inter[2] not in self.array_temp:
						self.asm_list.append([instr_name, f'$r{self.reg_map[inter[1]]},', f'$r{self.reg_map[inter[1]]},', f'$r{self.reg_map[inter[2]]}'])
						self.reg_map[inter[3]] = self.reg_map[inter[1]]
						self.set_reg_free(self.reg_map[inter[2]])
						self.reg_map[inter[1]] = -1
					# if first temporary is an array address
					elif inter[1] in self.array_temp and inter[2] not in self.array_temp:
						array_val_reg = self.reg_map[inter[1]]
						aux_reg = self.get_free_reg()
						# getting the value on the address stored on the temporary's respective register
						self.asm_list.append(['ld', f'$r{aux_reg},', f'$r{array_val_reg},', '0'])
						self.asm_list.append([instr_name, f'$r{self.reg_map[inter[1]]},', f'$r{self.reg_map[inter[1]]},', f'$r{aux_reg}'])
						self.reg_map[inter[3]] = self.reg_map[inter[1]]
						self.set_reg_free(self.reg_map[inter[2]])
						self.reg_map[inter[1]] = -1
					# if second temporary is an array address
					elif inter[1] not in self.array_temp and inter[2] in self.array_temp:
						array_val_reg = self.reg_map[inter[2]]
						aux_reg = self.get_free_reg()
						# getting the value on the address stored on the temporary's respective register
						self.asm_list.append(['ld', f'$r{aux_reg},', f'$r{array_val_reg},', '0'])
						self.asm_list.append([instr_name, f'$r{self.reg_map[inter[1]]},', f'$r{self.reg_map[inter[1]]},', f'$r{aux_reg}'])
						self.reg_map[inter[3]] = self.reg_map[inter[1]]
						self.set_reg_free(self.reg_map[inter[2]])
						self.reg_map[inter[1]] = -1
					# if both temporaries are array addresses
					else:
						# getting the value on the address stored on the first temporary's respective register
						first_array_val_reg = self.reg_map[inter[1]]
						first_val_reg = self.get_free_reg()
						self.set_reg_busy(first_val_reg)
						self.asm_list.append(['ld', f'$r{first_val_reg},', f'$r{first_array_val_reg},', '0'])
						# getting the value on the address stored on the second temporary's respective register
						second_array_val_reg = self.reg_map[inter[2]]
						second_val_reg = self.get_free_reg()
						self.asm_list.append(['ld', f'$r{second_val_reg},', f'$r{second_array_val_reg},', '0'])
						# finally (*|/) them for the operation result
						self.asm_list.append([instr_name, f'$r{first_val_reg},', f'$r{first_val_reg},', f'$r{second_val_reg}'])
						self.reg_map[inter[3]] = first_val_reg
						# clearing the auxiliar registers
						self.set_reg_free(self.reg_map[inter[1]])
						self.reg_map[inter[1]] = -1
						self.set_reg_free(self.reg_map[inter[2]])
						self.reg_map[inter[2]] = -1

				# (*|/) one declared variable and one non declared value
				elif self.intermediate_tkn_type(inter[1]) == 'var' and self.intermediate_tkn_type(inter[2]) == 'num' or self.intermediate_tkn_type(inter[1]) == 'num' and self.intermediate_tkn_type(inter[2]) == 'var':
					# first case [a (*|/) 1]
					if self.intermediate_tkn_type(inter[1]) == 'var' and self.intermediate_tkn_type(inter[2]) == 'num':
						# loading variable value
						reg = self.get_free_reg();
						self.set_reg_busy(reg)
						aux_reg = self.get_free_reg()
						self.asm_list.append(['ld', f'$r{reg},', '$r0,', self.get_symbol_mem_location(self.symbol_table[self.build_table_key(inter[1])])])
						# loading immediate value
						self.asm_list.append(['ldi',f'$r{aux_reg},', inter[2]])
						self.asm_list.append([instr_name, f'$r{reg},', f'$r{reg},', f'$r{aux_reg}'])
						self.reg_map[inter[3]] = reg
					# second case [1 (*|/) a]
					else:
						# loading variable value
						reg = self.get_free_reg();
						self.set_reg_busy(reg)
						aux_reg = self.get_free_reg()
						self.asm_list.append(['ld', f'$r{reg},', '$r0,', self.get_symbol_mem_location(self.symbol_table[self.build_table_key(inter[2])])])
						# loading immediate value
						self.asm_list.append(['ldi',f'$r{aux_reg},', inter[1]])
						self.asm_list.append([instr_name, f'$r{reg},', f'$r{reg},', f'$r{aux_reg}'])
						self.reg_map[inter[3]] = reg

				# multiplicating one declared variable and one temporary value
				elif self.intermediate_tkn_type(inter[1]) == 'var' and self.intermediate_tkn_type(inter[2]) == 'temp' or self.intermediate_tkn_type(inter[1]) == 'temp' and self.intermediate_tkn_type(inter[2]) == 'var':
					# first case [a (*|/) t0]
					if self.intermediate_tkn_type(inter[1]) == 'var' and self.intermediate_tkn_type(inter[2]) == 'temp':
						# if temporary holds an array address
						if inter[2] in self.array_temp:
							reg = self.get_free_reg()
							self.set_reg_busy(reg)
							self.asm_list.append(['ld', f'$r{reg},', '$r0,', self.get_symbol_mem_location(self.symbol_table[self.build_table_key(inter[1])])])
							aux_reg = self.get_free_reg()
							array_val_reg = self.reg_map[inter[2]]
							self.asm_list.append(['ld', f'$r{aux_reg},', f'$r{array_val_reg},', '0'])
							self.asm_list.append([instr_name, f'$r{reg},', f'$r{reg},', f'$r{aux_reg}'])
							self.reg_map[inter[3]] = reg
							self.set_reg_free(array_val_reg)
							self.reg_map[2] = -1
						else:
							reg = self.get_free_reg()
							self.set_reg_busy(reg)
							self.asm_list.append(['ld', f'$r{reg},', '$r0,', self.get_symbol_mem_location(self.symbol_table[self.build_table_key(inter[1])])])
							self.asm_list.append([instr_name, f'$r{reg},', f'$r{reg},', f'$r{self.reg_map[inter[2]]}'])
							self.reg_map[inter[3]] = reg
							self.set_reg_free(self.reg_map[inter[2]])
							self.reg_map[inter[2]] = -1
					# second case [t0 (*|/) a]
					else:
						# if temporary holds an array address
						if inter[1] in self.array_temp:
							reg = self.get_free_reg()
							self.set_reg_busy(reg)
							self.asm_list.append(['ld', f'$r{reg},', '$r0,', self.get_symbol_mem_location(self.symbol_table[self.build_table_key(inter[2])])])
							aux_reg = self.get_free_reg()
							array_val_reg = self.reg_map[inter[1]]
							self.asm_list.append(['ld', f'$r{aux_reg},', f'$r{array_val_reg},', '0'])
							self.asm_list.append([instr_name, f'$r{reg},', f'$r{reg},', f'$r{aux_reg}'])
							self.reg_map[inter[3]] = reg
							self.set_reg_free(array_val_reg)
							self.reg_map[1] = -1
						else:
							reg = self.get_free_reg()
							self.asm_list.append(['ld', f'$r{reg},', '$r0,', self.get_symbol_mem_location(self.symbol_table[self.build_table_key(inter[2])])])
							self.asm_list.append([instr_name, f'$r{self.reg_map[inter[1]]},', f'$r{self.reg_map[inter[1]]}', f'$r{reg}'])
							self.reg_map[inter[3]] = self.reg_map[inter[1]]
							self.set_reg_busy(self.reg_map[inter[3]])
							self.reg_map[inter[1]] = -1


				# (*|/) one temporary and one non declared value
				elif self.intermediate_tkn_type(inter[1]) == 'temp' and self.intermediate_tkn_type(inter[2]) == 'num' or self.intermediate_tkn_type(inter[1]) == 'num' and self.intermediate_tkn_type(inter[2]) == 'temp':
					# first case [t0 (*|/) 1]
					if self.intermediate_tkn_type(inter[1]) == 'temp' and self.intermediate_tkn_type(inter[2]) == 'num':
						if inter[1] in self.array_temp:
							reg = self.get_free_reg()
							self.set_reg_busy(reg)
							aux_reg = self.get_free_reg()
							self.asm_list.append(['ldi', f'$r{aux_reg},', inter[2]])
							array_val_reg = self.reg_map[inter[1]]
							self.asm_list.append(['ld', f'$r{reg},', f'$r{array_val_reg},', '0'])
							self.asm_list.append([instr_name, f'$r{reg},', f'$r{reg},', f'$r{aux_reg}'])
							self.reg_map[inter[3]] = reg
							self.set_reg_free(array_val_reg)
							self.reg_map[1] = -1
						else:
							reg = self.get_free_reg()
							# loading immediate value
							self.asm_list.append(['ldi', f'$r{reg},', inter[2]])
							# (*|/) result goes on register who's already holding the temporary value
							self.asm_list.append([instr_name, f'$r{self.reg_map[inter[1]]},', f'$r{self.reg_map[inter[1]]},', f'$r{reg}'])
							self.reg_map[inter[3]] = self.reg_map[inter[1]]
							self.set_reg_busy(self.reg_map[inter[3]])
							self.reg_map[inter[1]] = -1
					# second case [1 (*|/) t0]
					else:
						if inter[2] in self.array_temp:
							reg = self.get_free_reg()
							self.set_reg_busy(reg)
							self.asm_list.append(['ldi', f'$r{reg},', inter[1]])
							aux_reg = self.get_free_reg()
							array_val_reg = self.reg_map[inter[2]]
							self.asm_list.append(['ld', f'$r{aux_reg},', f'$r{array_val_reg},', '0'])
							self.asm_list.append([instr_name, f'$r{reg},', f'$r{reg},', f'$r{aux_reg}'])
							self.reg_map[inter[3]] = reg
							self.set_reg_free(array_val_reg)
							self.reg_map[1] = -1
						else:
							reg = self.get_free_reg()
							# loading immediate value
							self.asm_list.append(['ldi', f'$r{reg},', inter[1]])
							# (*|/) result goes on register who's already holding the temporary value
							self.asm_list.append([instr_name, f'$r{self.reg_map[inter[2]]},', f'$r{self.reg_map[inter[2]]},', f'$r{reg}'])
							self.reg_map[inter[3]] = self.reg_map[inter[2]]
							self.set_reg_busy(self.reg_map[inter[3]])
							self.reg_map[inter[2]] = -1

			elif inter_op == 'assign':
				# assigning a declared variable to another [a = b]
				if self.intermediate_tkn_type(inter[1]) == self.intermediate_tkn_type(inter[2]) == 'var':
					self.asm_list.append(['ld', f'$r{self.get_free_reg()},', '$r0,', self.get_symbol_mem_location(self.symbol_table[self.build_table_key(inter[2])])])
					self.asm_list.append(['str', '$r0,', str(self.get_symbol_mem_location(self.symbol_table[self.build_table_key(inter[1])]))+',', f'$r{self.get_free_reg()}'])

				# assigning a non declared value to a variable [a = 1]
				elif self.intermediate_tkn_type(inter[1]) == 'var' and self.intermediate_tkn_type(inter[2]) == 'num':
					self.asm_list.append(['ldi', f'$r{self.get_free_reg()},', inter[2]])
					self.asm_list.append(['str', '$r0,', str(self.get_symbol_mem_location(self.symbol_table[self.build_table_key(inter[1])]))+',', f'$r{self.get_free_reg()}'])

				# assigning a temporary result to a declared variable [a = t0]
				elif self.intermediate_tkn_type(inter[1]) == 'var' and self.intermediate_tkn_type(inter[2]) == 'temp':
					# checking if array temporary is beeing assigned, cause if it is, it's value must first be loaded
					if inter[2] in self.array_temp:
						array_val_reg = self.reg_map[inter[2]]
						aux_reg = self.get_free_reg()
						self.asm_list.append(['ld', f'$r{aux_reg},', f'$r{array_val_reg},', '0'])
						self.asm_list.append(['str', '$r0,', str(self.get_symbol_mem_location(self.symbol_table[self.build_table_key(inter[1])]))+',', f'$r{aux_reg}'])
						self.set_reg_free(self.reg_map[inter[2]]) # making already solved register able to be used again
						self.reg_map[inter[2]] = -1
					else:
						self.asm_list.append(['str', '$r0,', str(self.get_symbol_mem_location(self.symbol_table[self.build_table_key(inter[1])]))+',', f'$r{self.reg_map[inter[2]]}'])
						self.set_reg_free(self.reg_map[inter[2]]) # making already solved register able to be used again
						self.reg_map[inter[2]] = -1

			elif inter_op == 'weak_assign':
				# calculating array index by variable value [vet[a] = value]
				if self.intermediate_tkn_type(inter[3]) == 'var':
					reg = self.get_free_reg()
					self.set_reg_busy(reg)
					# getting reference to array initial position
					aux_position = self.get_symbol_mem_location(self.symbol_table[self.build_table_key(inter[2])])
					if(type(aux_position) is not int):
						arr_ini_position = self.get_symbol_mem_location(self.symbol_table[self.build_table_key(inter[2])])[0]
					else:
						arr_ini_position = self.get_symbol_mem_location(self.symbol_table[self.build_table_key(inter[2])])
					# if array is used directly into the main function or if it was passed by reference to another one
					#instr = ['ldi', f'$r{reg},', arr_ini_position] if self.actual_scope == 'main' else ['ld', f'$r{reg},', '$r0,', arr_ini_position]
					if f'global.{inter[2]}' in self.symbol_table or self.actual_scope == 'main':
						instr = ['ldi', f'$r{reg},', arr_ini_position] 
					else:
						instr = ['ld', f'$r{reg},', '$r0,', arr_ini_position]					
					self.asm_list.append(instr)
					self.reg_map[inter[1]] = reg
					# getting the variable value and adding it to the array's initial position address
					aux_reg = self.get_free_reg()
					var_mem_position = self.get_symbol_mem_location(self.symbol_table[self.build_table_key(inter[3])])
					self.asm_list.append(['ld', f'$r{aux_reg},', '$r0,', f'{var_mem_position}'])
					self.asm_list.append(['add', f'$r{reg},', f'$r{reg},', f'$r{aux_reg}'])
					# identifying reg as a array address to be loaded from, not as a array position value
					self.array_temp.append(inter[1])

				# calculating array index by immediate value [vet[2] = value]
				elif self.intermediate_tkn_type(inter[3]) == 'num':
					reg = self.get_free_reg()
					self.set_reg_busy(reg)
					# getting reference to array initial position
					aux_position = self.get_symbol_mem_location(self.symbol_table[self.build_table_key(inter[2])])
					if(type(aux_position) is not int):
						arr_ini_position = self.get_symbol_mem_location(self.symbol_table[self.build_table_key(inter[2])])[0]
					else:
						arr_ini_position = self.get_symbol_mem_location(self.symbol_table[self.build_table_key(inter[2])])
					# if array is used directly into the main function or if its global, or if it was passed by reference to another one
					#instr = ['ldi', f'$r{reg},', arr_ini_position] if self.actual_scope == 'main' else ['ld', f'$r{reg},', '$r0,', arr_ini_position]
					# global array
					if f'global.{inter[2]}' in self.symbol_table or self.actual_scope == 'main':
						instr = ['ldi', f'$r{reg},', arr_ini_position] 
					else:
						instr = ['ld', f'$r{reg},', '$r0,', arr_ini_position]					
					self.asm_list.append(instr)
					self.reg_map[inter[1]] = reg
					# adding it to the offset to access the real array's position
					idx_offset = inter[3]
					self.asm_list.append(['addi', f'$r{reg},', f'$r{reg},', idx_offset])
					# identifying reg as a array address to be loaded from, not a array position value
					self.array_temp.append(inter[1])

				# calculating array index by temporary value [vet[t0] = value]
				elif self.intermediate_tkn_type(inter[3]) == 'temp':
					# checking if temporary of vector index reffers to an normal or array temporary
					if inter[3] in self.array_temp:
						reg = self.get_free_reg()
						self.set_reg_busy(reg)
						# getting reference to array initial position
						aux_position = self.get_symbol_mem_location(self.symbol_table[self.build_table_key(inter[2])])
						if(type(aux_position) is not int):
							arr_ini_position = self.get_symbol_mem_location(self.symbol_table[self.build_table_key(inter[2])])[0]
						else:
							arr_ini_position = self.get_symbol_mem_location(self.symbol_table[self.build_table_key(inter[2])])
						# if array is used directly into the main function or if it was passed by reference to another one
						#instr = ['ldi', f'$r{reg},', arr_ini_position] if self.actual_scope == 'main' else ['ld', f'$r{reg},', '$r0,', arr_ini_position]
						if f'global.{inter[2]}' in self.symbol_table or self.actual_scope == 'main':
							instr = ['ldi', f'$r{reg},', arr_ini_position] 
						else:
							instr = ['ld', f'$r{reg},', '$r0,', arr_ini_position]					
						self.asm_list.append(instr)
						self.reg_map[inter[1]] = reg
						# getting the value on the address stored on the temporary's respective register
						aux_reg = self.get_free_reg()
						array_val_reg = self.reg_map[inter[3]]
						self.asm_list.append(['ld', f'$r{aux_reg},', f'$r{array_val_reg},', '0'])
						self.asm_list.append(['add', f'$r{reg},', f'$r{reg},', f'$r{aux_reg}'])
						self.array_temp.append(inter[1])
					else:
						reg = self.get_free_reg()
						self.set_reg_busy(reg)
						# getting reference to array initial position
						aux_position = self.get_symbol_mem_location(self.symbol_table[self.build_table_key(inter[2])])
						if(type(aux_position) is not int):
							arr_ini_position = self.get_symbol_mem_location(self.symbol_table[self.build_table_key(inter[2])])[0]
						else:
							arr_ini_position = self.get_symbol_mem_location(self.symbol_table[self.build_table_key(inter[2])])
						# if array is used directly into the main function or if it was passed by reference to another one
						#instr = ['ldi', f'$r{reg},', arr_ini_position] if self.actual_scope == 'main' else ['ld', f'$r{reg},', '$r0,', arr_ini_position]
						if f'global.{inter[2]}' in self.symbol_table or self.actual_scope == 'main':
							instr = ['ldi', f'$r{reg},', arr_ini_position] 
						else:
							instr = ['ld', f'$r{reg},', '$r0,', arr_ini_position]					
						self.asm_list.append(instr)
						self.reg_map[inter[1]] = reg
						# getting the temporary value and adding it to the array's initial position address
						aux_reg = self.get_free_reg()
						temp_reg = self.reg_map[inter[3]]
						self.set_reg_free(self.reg_map[inter[3]])
						self.reg_map[inter[3]] = -1
						self.asm_list.append(['add', f'$r{reg},', f'$r{reg},', f'$r{temp_reg}'])
						self.array_temp.append(inter[1])

			elif inter_op == 'array_assign':
				# assigning a variable to an array position [vet[idx] = a]
				if self.intermediate_tkn_type(inter[2]) == 'var':
					# loading the variable value to an auxiliar register
					aux_reg = self.get_free_reg()
					var_pos = self.get_symbol_mem_location(self.symbol_table[self.build_table_key(inter[2])])
					self.asm_list.append(['ld', f'$r{aux_reg},', '$r0,', var_pos ])
					self.asm_list.append(['str', f'$r{self.reg_map[inter[1]]},', '0,', f'$r{aux_reg}'])
					self.set_reg_free(self.reg_map[inter[1]])
					self.reg_map[inter[1]] = -1

				# assigning a numeric value to an array position [vet[idx] = 1]
				elif self.intermediate_tkn_type(inter[2]) == 'num':
					# loading the offset to an auxiliar register
					offset = inter[2]
					aux_reg = self.get_free_reg()
					self.asm_list.append(['ldi', f'$r{aux_reg},', offset])
					self.asm_list.append(['str', f'$r{self.reg_map[inter[1]]},', '0,', f'$r{aux_reg}'])
					self.set_reg_free(self.reg_map[inter[1]])
					self.reg_map[inter[1]] = -1

				# assigning a temporary value to an array position [vet[idx] = t0]
				elif self.intermediate_tkn_type(inter[2]) == 'temp':
					# checking if temporary of vector index reffers to an normal or array temporary
					if inter[2] in self.array_temp:
						# getting the value on the address stored on the temporary's respective register
						array_val_reg = self.reg_map[inter[2]]
						aux_reg = self.get_free_reg()
						self.asm_list.append(['ld', f'$r{aux_reg},', f'$r{array_val_reg},', '0'])
						self.asm_list.append(['str', f'$r{self.reg_map[inter[1]]},', '0,', f'$r{aux_reg}'])
						self.set_reg_free(self.reg_map[inter[1]])
						self.reg_map[inter[1]] = -1
						self.set_reg_free(self.reg_map[inter[2]])
						self.reg_map[inter[2]] = -1
					else:
						temp_reg = self.reg_map[inter[2]]
						self.asm_list.append(['str', f'$r{self.reg_map[inter[1]]},', '0,', f'$r{temp_reg}'])
						self.set_reg_free(self.reg_map[inter[1]])
						self.reg_map[inter[1]] = -1
						self.set_reg_free(self.reg_map[inter[2]])
						self.reg_map[inter[2]] = -1

			elif inter_op == 'label':
				label_name = inter[1]
				self.asm_list.append([f'{label_name}:'])

			elif inter_op == 'end_label':
				label_name = inter[1]
				if label_name in self.label_map:
					label_bool_reg = self.label_map[label_name]
					self.set_reg_free(label_bool_reg)
					self.reg_map[label_bool_reg] = -1

			elif inter_op == 'goto':
				label_name = inter[1]
				self.asm_list.append(['jmp', label_name])

			elif inter_op in self.comparisons:
				# first value decision
				first_val_reg = self.get_free_reg()
				self.set_reg_busy(first_val_reg)

				if self.intermediate_tkn_type(inter[1]) == 'var':
					self.asm_list.append(['ld', f'$r{first_val_reg},', '$r0,', self.get_symbol_mem_location(self.symbol_table[self.build_table_key(inter[1])])])

				elif self.intermediate_tkn_type(inter[1]) == 'num':
					self.asm_list.append(['ldi', f'$r{first_val_reg},', inter[1]])

				elif self.intermediate_tkn_type(inter[1]) == 'temp':
					if inter[1] in self.array_temp:
						array_val_reg = self.reg_map[inter[1]]
						self.asm_list.append(['ld', f'$r{first_val_reg},', f'$r{array_val_reg},', '0'])
						self.set_reg_free(array_val_reg)
					else:
						first_val_reg = self.reg_map[inter[1]]

				# second value decision
				second_val_reg = self.get_free_reg()
				self.set_reg_busy(second_val_reg)

				if self.intermediate_tkn_type(inter[2]) == 'var':
					self.asm_list.append(['ld', f'$r{second_val_reg},', '$r0,', self.get_symbol_mem_location(self.symbol_table[self.build_table_key(inter[2])])])

				elif self.intermediate_tkn_type(inter[2]) == 'num':
					self.asm_list.append(['ldi', f'$r{second_val_reg},', inter[2]])

				elif self.intermediate_tkn_type(inter[2]) == 'temp':
					if inter[2] in self.array_temp:
						array_val_reg = self.reg_map[inter[2]]
						self.asm_list.append(['ld', f'$r{second_val_reg},', f'$r{array_val_reg},', '0'])
						self.set_reg_free(array_val_reg)
					else:
						second_val_reg = self.reg_map[inter[2]]

				# operation decision
				bool_reg = self.get_free_reg()
				self.set_reg_busy(bool_reg)

				if inter_op == 'equal':
					self.asm_list.append(['seq', f'$r{bool_reg},', f'$r{first_val_reg},', f'$r{second_val_reg}'])

				elif inter_op == 'not_equal':
					self.asm_list.append(['sneq', f'$r{bool_reg},', f'$r{first_val_reg},', f'$r{second_val_reg}'])

				elif inter_op == 'less_than':
					self.asm_list.append(['slt', f'$r{bool_reg},', f'$r{first_val_reg},', f'$r{second_val_reg}'])

				elif inter_op == 'greater_than':
					self.asm_list.append(['slt', f'$r{bool_reg},', f'$r{second_val_reg},', f'$r{first_val_reg}'])

				elif inter_op == 'less_or_equal_than':
					self.asm_list.append(['slet', f'$r{bool_reg},', f'$r{first_val_reg},', f'$r{second_val_reg}'])

				elif inter_op == 'greater_or_equal_than':
					self.asm_list.append(['slet', f'$r{bool_reg},', f'$r{second_val_reg},', f'$r{first_val_reg}'])

				# intermediate mapping
				self.reg_map[inter[3]] = bool_reg
				# clearing auxiliar registers
				self.set_reg_free(first_val_reg)
				self.set_reg_free(second_val_reg)

			elif inter_op == 'jump_if_false':
				bool_reg = self.reg_map[inter[1]]
				label_name = inter[2]
				self.asm_list.append(['beq', f'$r{bool_reg},', '$r0,', label_name])
				self.label_map[label_name] = bool_reg

			elif inter_op == 'arg':
				param = inter[2]
				function_name = inter[1]
				reg = self.get_free_reg()
				# output treatment
				#if function_name == 'output':
				if function_name == 'output' or function_name == 'UART_output':
					io_reg = 27
					if self.intermediate_tkn_type(param) == 'var':
						self.asm_list.append(['ld', f'$r{reg},', '0,', self.get_symbol_mem_location(self.symbol_table[self.build_table_key(param)])])

					elif self.intermediate_tkn_type(param) == 'num':
						self.asm_list.append(['ldi', f'$r{reg},', param])

					elif self.intermediate_tkn_type(param) == 'temp':
						if param in self.array_temp:
							array_val_reg = self.reg_map[param]
							self.asm_list.append(['ld', f'$r{reg},', f'$r{array_val_reg},', '0'])
							self.set_reg_free(array_val_reg)
							self.reg_map[param] = -1
						else:
							aux_reg = self.reg_map[param]
							self.reg_map[param] = -1
							self.set_reg_free(aux_reg)
							self.asm_list.append(['addi', f'$r{reg},', f'$r{aux_reg},', '0'])

					# output is done through a special register [27]
					self.asm_list.append(['addi', f'$r{io_reg},', f'$r{reg},', '0'])
					continue

				elif function_name == 'load_os':
					# software treatment
					self.source_funct_args.append(param)
					continue

				elif function_name == 'end_bios':
					# no treatment, should never happen
					continue

				elif function_name == 'move_HD_mem':
					# software treatment
					self.source_funct_args.append(param)
					continue

				elif function_name == 'store_HD':
					# software treatment
					self.source_funct_args.append(param)
					continue

				elif function_name == 'move_reg_proc_OS':
					# software treatment
					self.source_funct_args.append(param)
					continue

				elif function_name == 'move_reg_OS_proc':
					# software treatment
					self.source_funct_args.append(param)
					continue

				elif function_name == 'swap_process':
					# software treatment
					self.source_funct_args.append(param)
					continue

				elif function_name == 'write_lcd':
					# software treatment
					self.source_funct_args.append(param)
					continue

				elif function_name == 'concatenate':
					# software treatment
					self.source_funct_args.append(param)
					continue

				elif function_name == 'get_interruption':
					# no treatment, should never happen
					continue

				elif function_name == 'load_reg_context':
					# software treatment
					self.source_funct_args.append(param)
					continue

				elif function_name == 'store_reg_context':
					# software treatment
					self.source_funct_args.append(param)
					continue

				elif function_name == 'recover_OS':
					# no treatment, should never happen
					continue

				elif function_name == 'get_proc_pc':
					# no treatment, should never happen
					continue

				elif function_name == 'set_proc_pc':
					# software treatment
					self.source_funct_args.append(param)
					continue

				else:
					# parameter type decision
					if self.intermediate_tkn_type(param) == 'var':
						# if parameter is an array
						if self.get_symbol_id_type(self.symbol_table[self.build_table_key(param)]) == 'var[]':
							if(type(self.get_symbol_mem_location(self.symbol_table[self.build_table_key(param)])) is int):
								arr_ini_position = self.get_symbol_mem_location(self.symbol_table[self.build_table_key(param)])
							else:
								arr_ini_position = self.get_symbol_mem_location(self.symbol_table[self.build_table_key(param)])[0]
							# passing array as an parameter treatment
							instr = ['ldi', f'$r{reg},', arr_ini_position] if self.actual_scope == 'main' else ['ld', f'$r{reg},', '$r0,', arr_ini_position]
							self.asm_list.append(instr)
						# if it is a normal variable
						else:
							self.asm_list.append(['ld', f'$r{reg},', '$r0,', self.get_symbol_mem_location(self.symbol_table[self.build_table_key(param)])])

					elif self.intermediate_tkn_type(param) == 'num':
						self.asm_list.append(['ldi', f'$r{reg},', param])

					elif self.intermediate_tkn_type(param) == 'temp':
						if param in self.array_temp:
							array_val_reg = self.reg_map[param]
							self.asm_list.append(['ld', f'$r{reg},', f'$r{array_val_reg},', '0'])
							self.set_reg_free(array_val_reg)
							self.reg_map[param] = -1
						else:
							reg = self.reg_map[param]
							self.reg_map[param] = -1
				
					self.asm_list.append(['inc', '$sp'])
					# stacking the parameter
					self.asm_list.append(['push', '$sp,', '0,', f'$r{reg}'])

			elif inter_op == 'function':
				function_name = inter[1]
				self.ra_stored[function_name] = True if function_name == 'main' else False
				self.asm_list.append([f'{function_name}:'])
				self.actual_scope = function_name

				pop_params = True
				if function_name != 'main': 
					param_list = self.get_symbol_parameters(self.symbol_table[function_name])
					if len(param_list) == 1 and param_list[0] == None:
						pop_params = False

				if function_name != 'main' and pop_params:
					function_params = self.get_symbol_parameters(self.symbol_table[function_name])
					# poping stacked parameters
					aux_reg = self.get_free_reg()
					for param in reversed(function_params):
						# poped value goes on auxiliar register then is stored on it's respective memory position
						self.asm_list.append(['pop', f'$r{aux_reg},', '$sp,', 0])
						self.asm_list.append(['dec', '$sp'])
						self.asm_list.append(['str', '$r0,', str(self.get_symbol_mem_location(self.symbol_table[self.build_table_key(param)]))+',', f'$r{aux_reg}'])

				if self.ra_stored[self.actual_scope] == False:
					self.ra_stored[self.actual_scope] = True
					self.asm_list.append(['inc', '$sp'])
					self.asm_list.append(['push', '$sp,', '0,', '$ra'])


			elif inter_op == 'call':
				function_name = inter[1]
				if function_name in self.source_functions:
					if function_name == 'output':
						io_reg = 27
						if self.mode == 'os':
							self.asm_list.append(['out', f'$r{io_reg}'])	
						else:
							self.asm_list.append(['syscall', '1'])
							self.asm_list.append(['nop'])
						
						self.source_funct_args.clear()

					elif function_name == 'input':
						if self.mode == 'os':
							reg = self.get_free_reg()
							self.asm_list.append(['in', f'$r{reg}'])	
							self.reg_map[inter[3]] = reg
						else:
							io_reg = 27
							self.asm_list.append(['syscall', '0'])
							self.asm_list.append(['nop'])
							self.reg_map[inter[3]] = io_reg

						self.source_funct_args.clear()

					elif function_name == 'load_os':
						# seting registers for the three arguments
						param_reg_1 = self.get_free_reg()
						self.set_reg_busy(param_reg_1)
						param_reg_2 = self.get_free_reg()
						self.set_reg_busy(param_reg_2)
						param_reg_3 = self.get_free_reg()
						self.set_reg_busy(param_reg_3)
						# geting those registers to hold the parameters respective values
						self.asm_list.append(['ld', f'$r{param_reg_1},', '$r0,', self.get_symbol_mem_location(self.symbol_table[self.build_table_key(self.source_funct_args[0])])])
						self.asm_list.append(['ld', f'$r{param_reg_2},', '$r0,', self.get_symbol_mem_location(self.symbol_table[self.build_table_key(self.source_funct_args[1])])])
						self.asm_list.append(['ld', f'$r{param_reg_3},', '$r0,', self.get_symbol_mem_location(self.symbol_table[self.build_table_key(self.source_funct_args[2])])])
						self.asm_list.append(['ldos', f'$r{param_reg_1},', f'$r{param_reg_2},', f'$r{param_reg_3}'])

						self.set_reg_free(param_reg_1)
						self.set_reg_free(param_reg_2)
						self.set_reg_free(param_reg_3)
						
						self.source_funct_args.clear()

					elif function_name == 'end_bios':
						self.asm_list.append(['btm'])

					elif function_name == 'move_HD_mem':
						# seting registers for the three arguments
						param_reg_1 = self.get_free_reg()
						self.set_reg_busy(param_reg_1)
						param_reg_2 = self.get_free_reg()
						self.set_reg_busy(param_reg_2)
						param_reg_3 = self.get_free_reg()
						self.set_reg_busy(param_reg_3)
						# geting those registers to hold the parameters respective values
						self.asm_list.append(['ld', f'$r{param_reg_1},', '$r0,', self.get_symbol_mem_location(self.symbol_table[self.build_table_key(self.source_funct_args[0])])])
						self.asm_list.append(['ld', f'$r{param_reg_2},', '$r0,', self.get_symbol_mem_location(self.symbol_table[self.build_table_key(self.source_funct_args[1])])])
						self.asm_list.append(['ld', f'$r{param_reg_3},', '$r0,', self.get_symbol_mem_location(self.symbol_table[self.build_table_key(self.source_funct_args[2])])])
						self.asm_list.append(['mhdm', f'$r{param_reg_1},', f'$r{param_reg_2},', f'$r{param_reg_3}'])
						
						self.set_reg_free(param_reg_1)
						self.set_reg_free(param_reg_2)
						self.set_reg_free(param_reg_3)
						
						self.source_funct_args.clear()

					# data, proc_num, track_line
					elif function_name == 'store_HD':
						# seting registers for the three arguments
						# param_reg_1 = file_num
						param_reg_1 = self.get_free_reg()
						self.set_reg_busy(param_reg_1)
						# param_reg_2 = track_line			
						param_reg_2 = self.get_free_reg()
						self.set_reg_busy(param_reg_2)
						# param_reg_3 = data
						param_reg_3 = self.get_free_reg()
						self.set_reg_busy(param_reg_3)
						# geting those registers to hold the parameters respective values
						self.asm_list.append(['ld', f'$r{param_reg_1},', '$r0,', self.get_symbol_mem_location(self.symbol_table[self.build_table_key(self.source_funct_args[0])])])
						self.asm_list.append(['ld', f'$r{param_reg_2},', '$r0,', self.get_symbol_mem_location(self.symbol_table[self.build_table_key(self.source_funct_args[1])])])
						self.asm_list.append(['ld', f'$r{param_reg_3},', '$r0,', self.get_symbol_mem_location(self.symbol_table[self.build_table_key(self.source_funct_args[2])])])
						self.asm_list.append(['strhd', f'$r{param_reg_1},', f'$r{param_reg_2},', f'$r{param_reg_3}'])
						
						self.set_reg_free(param_reg_1)
						self.set_reg_free(param_reg_2)
						self.set_reg_free(param_reg_3)
						
						self.source_funct_args.clear()

					# move_reg_OS_proc( io_var, 27 )
					elif function_name == 'move_reg_OS_proc':
						# seting registers for the two arguments
						variable_reg = self.get_free_reg()
						reg_destiny = self.source_funct_args[1]
						# loading the data to be moved to the proccess
						symbol = self.symbol_table[self.build_table_key(self.source_funct_args[0])]
						mem_loc = self.get_symbol_mem_location(symbol)
						self.asm_list.append(['ld', f'$r{variable_reg},', '$r0,', f'{mem_loc}' ])						
						#self.asm_list.append(['ld', f'$r{variable_reg},', '$r0,', self.get_symbol_mem_location(self.symbol_table[self.build_table_key(self.source_funct_args[0])])])
						# changing the write shift for register bank
						self.asm_list.append(['cwsfh'])
						# writing the data on process reg[27]
						self.asm_list.append(['add', f'$r{reg_destiny},',f'$r{variable_reg},','$r0'])
						# changing back the write shift for the register bank
						self.asm_list.append(['cwsfh'])

						self.source_funct_args.clear()

					# move_reg_proc_OS( 27, io_var ); 
					elif function_name == 'move_reg_proc_OS':
						# seting registers for the two arguments
						reg_destiny = self.get_free_reg()
						reg_source = self.source_funct_args[0]
						# changing the read shift for register bank
						self.asm_list.append(['crsfh'])
						# moving the data from process region to OS region
						self.asm_list.append(['add', f'$r{reg_destiny},',f'$r{reg_source},','$r0'])
						# changing the back read shift fromr register bank
						self.asm_list.append(['crsfh'])
						# storing the value moved from process to OS on OS variable
						symbol = self.symbol_table[self.build_table_key(self.source_funct_args[1])]
						mem_loc = self.get_symbol_mem_location(symbol)						
						self.asm_list.append(['str','$r0,', f'{mem_loc}', f'$r{reg_destiny}'])
						
						self.source_funct_args.clear()						
						
					elif function_name == 'swap_process':
						proc_num_reg = 25 # ensurance
						self.asm_list.append(['nop'])
						self.asm_list.append(['crsfh'])
						self.asm_list.append(['cwsfh'])
						self.asm_list.append(['ld', f'$r{proc_num_reg},', '$r0,', self.get_symbol_mem_location(self.symbol_table[self.build_table_key(self.source_funct_args[0])])])
						self.asm_list.append(['sprc', f'$r{proc_num_reg}']) 
						
						self.source_funct_args.clear()

					elif function_name == 'write_lcd':
						offset_msg = self.source_funct_args[0]
						self.asm_list.append(['cmsg', f'{offset_msg}'])
						
						self.source_funct_args.clear()

					elif function_name == 'concatenate':
						# seting registers for the three arguments
						param_reg_1 = self.get_free_reg()
						self.set_reg_busy(param_reg_1)
						param_reg_2 = self.get_free_reg()
						self.set_reg_busy(param_reg_2)
						self.asm_list.append(['ld', f'$r{param_reg_1},', '$r0,', self.get_symbol_mem_location(self.symbol_table[self.build_table_key(self.source_funct_args[0])])])
						self.asm_list.append(['ld', f'$r{param_reg_2},', '$r0,', self.get_symbol_mem_location(self.symbol_table[self.build_table_key(self.source_funct_args[1])])])
						
						return_reg = 29 # return register
						self.asm_list.append(['conc', f'$r{return_reg},',f'$r{param_reg_1},',f'$r{param_reg_2}'])
						self.reg_map[inter[3]] = return_reg
						
						self.source_funct_args.clear()

					elif function_name == 'get_interruption':
						intrpt_reg = 28
						return_reg = 29
						self.asm_list.append(['addi', f'$r{return_reg}', f'$r{intrpt_reg}', '0'])
						self.reg_map[inter[3]] = return_reg

						self.source_funct_args.clear()

					elif function_name == 'store_reg_context': ######
						# seting registers for the three arguments
						param_reg_1 = self.source_funct_args[0]
						self.set_reg_busy(param_reg_1)
						param_reg_2 = self.get_free_reg()
						self.set_reg_busy(param_reg_2)
						param_offs_3 = self.source_funct_args[2] 
						aux_reg = self.get_free_reg()

						# loading the value of variable argument to a register
						self.asm_list.append(['ld', f'$r{param_reg_2},', '$r0,', self.get_symbol_mem_location(self.symbol_table[self.build_table_key(self.source_funct_args[1])])])
						self.asm_list.append(['addi', f'$r{param_reg_2},', f'$r{param_reg_2},', f'{param_offs_3}'])
						self.asm_list.append(['crsfh'])
						self.asm_list.append(['addi', f'$r{aux_reg},', f'$r{param_reg_1},', '0'])
						self.asm_list.append(['crsfh'])
						self.asm_list.append(['str', f'$r{param_reg_2},', '0,', f'$r{aux_reg}'])

						self.set_reg_free(param_reg_1)
						self.set_reg_free(param_reg_2)
						self.set_reg_free(aux_reg)
						self.source_funct_args.clear()

					elif function_name == 'load_reg_context':
						# seting registers for the three arguments
						param_reg_1 = self.source_funct_args[0]
						self.set_reg_busy(param_reg_1)
						param_reg_2 = self.get_free_reg()
						self.set_reg_busy(param_reg_2)
						param_offs_3 = self.source_funct_args[2]

						# loading the value of variable argument to a register
						self.asm_list.append(['ld', f'$r{param_reg_2},', '$r0,', self.get_symbol_mem_location(self.symbol_table[self.build_table_key(self.source_funct_args[1])])])
						self.asm_list.append(['addi', f'$r{param_reg_2}', f'$r{param_reg_2}', f'{param_offs_3}'])
						self.asm_list.append(['cwsfh'])
						self.asm_list.append(['ld', f'$r{param_reg_1}', f'$r{param_reg_2}', '0'])
						self.asm_list.append(['cwsfh'])

						self.set_reg_free(param_reg_1)
						self.set_reg_free(param_reg_2)
						self.source_funct_args.clear()

					elif function_name == 'recover_OS':
						# ensurance
						self.asm_list.append(['nop'])
						# recovering OS access to it's own registers
						self.asm_list.append(['crsfh'])
						self.asm_list.append(['cwsfh'])
						# ensurance
						self.asm_list.append(['nop'])

						self.source_funct_args.clear()

					elif function_name == 'get_proc_pc': 
						proc_pc_reg = 28
						return_reg = 29
						self.asm_list.append(['getpc'])
						self.asm_list.append(['addi', f'$r{return_reg},', f'$r{proc_pc_reg},', '0'])
						self.reg_map[inter[3]] = return_reg

						self.source_funct_args.clear()

					elif function_name == 'set_proc_pc': 
						reg = self.get_free_reg()
						self.asm_list.append(['ld', f'$r{reg},', '$r0,', self.get_symbol_mem_location(self.symbol_table[self.build_table_key(self.source_funct_args[0])])])
						self.asm_list.append(['setpc', f'$r{reg}'])

						self.source_funct_args.clear()

					elif function_name == 'UART_input':
						if self.mode == 'os':
							reg = self.get_free_reg()
							self.asm_list.append(['rcv', f'$r{reg}'])
							self.reg_map[inter[3]] = reg
						else:
							io_reg = 27
							self.asm_list.append(['syscall','2'])
							self.asm_list.append(['nop'])
							self.reg_map[inter[3]] = io_reg

					elif function_name == 'UART_output':
						if self.mode == 'os':
							io_reg = 27
							self.asm_list.append(['send', f'$r{io_reg}'])
						else:
							self.asm_list.append(['syscall','3'])
							self.asm_list.append(['nop'])

						self.source_funct_args.clear()

				#normal function call
				elif function_name != self.actual_scope:
					self.reg_map[inter[3]] = 29
					self.asm_list.append(['jal', function_name])

				#recursion
				else:
					self.reg_map[inter[3]] = 29
					self.asm_list.append(['jal', function_name])
					# correcting $ra if there are multiple function calls other than the ones from the main function
					if self.actual_scope != 'main':
						self.asm_list.append(['pop', '$ra,', '$sp,', 0])
						self.asm_list.append(['dec', '$sp'])

			elif inter_op == 'return':
				if self.actual_scope != 'main':
					# void function does not need to assign return value to $r29
					if self.get_symbol_data_type(self.symbol_table[self.actual_scope]) != 'void':
						ret_val = inter[1]
						reg = 29 # return register

						# return value type decision
						if self.intermediate_tkn_type(ret_val) == 'var':
							self.asm_list.append(['ld', f'$r{reg},', '$r0,', self.get_symbol_mem_location(self.symbol_table[self.build_table_key(ret_val)])])

						elif self.intermediate_tkn_type(ret_val) == 'num':
							self.asm_list.append(['ldi', f'$r{reg},', ret_val])

						elif self.intermediate_tkn_type(ret_val) == 'temp':
							if ret_val in self.array_temp:
								array_val_reg = self.reg_map[ret_val]
								self.asm_list.append(['ld', f'$r{reg},', f'$r{array_val_reg},', '0'])
								self.set_reg_free(array_val_reg)
								self.reg_map[ret_val] = -1
							else:
								aux_reg = self.reg_map[ret_val]
								self.reg_map[ret_val] = -1
								self.set_reg_free(aux_reg)
								self.asm_list.append(['addi', f'$r{reg},', f'$r{aux_reg},', '0'])

					# correcting $ra if there are multiple function calls other than the ones from the main function
					if self.ra_stored[self.actual_scope] == True:
						self.asm_list.append(['pop', '$ra,', '$sp,', 0])
						self.asm_list.append(['dec', '$sp'])
						# returning to the correct register address
					self.asm_list.append(['jmpr', '$ra'])

			else:
				continue
				# se viu até aqui tem que dar uma risadinha
