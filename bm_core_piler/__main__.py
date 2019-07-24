import sys
import argparse
import antlr4

from .cminus_semantic import SymbolTableGenerator
from .cminus_abstract_st import AbstractStNodeConstructVisitor
from .abstract_printer import AbstractStPrinter
from .cminus_intermediate import IntermediateCodeGenerator
from .cminus_assembler import AssemblyGenerator
from .gen.cminusParser import cminusParser
from .gen.cminusLexer import cminusLexer


def main(argv):
    parser = argparse.ArgumentParser(description='Cminus compiler')
    # file usage
    parser.add_argument('--file') 
    # lexical analysis
    parser.add_argument('--lex', action = 'store_true') 
    # syntactic analysis
    parser.add_argument('--syn', action = 'store_true') 
    # semantic analysis
    parser.add_argument('--sem', action = 'store_true') 
    # intermediate code generation
    parser.add_argument('--inter', action = 'store_true') 
    # file synthesis
    parser.add_argument('--synth', action = 'store_true') 
    # initial memory position
    parser.add_argument('--mem', action = 'store', default = 0, required = False) 
    # initial stack pointer value
    parser.add_argument('--stack', action = 'store', default = 0, required = False) 
    # mode for synthesis, 'os' means io operations are in fact realized, 
    # mode for synthesis, 'prog' means that io operations are due by syscalls
    parser.add_argument('--mode', action = 'store', default = 'os', required = False)

    args = parser.parse_args()

    input_ = antlr4.FileStream(args.file)
    lexer = cminusLexer(input_)
    stream = antlr4.CommonTokenStream(lexer)
    parser = cminusParser(stream)
    tree = parser.program()
 
    if args.lex:
        for tkn in stream.tokens:
            print(tkn.line, ":", tkn.text)

    abstract_st = AbstractStNodeConstructVisitor().visit(tree)

    if args.syn:
         AbstractStPrinter().visit(abstract_st)
	
    mem_loc = args.mem
    semantic_analysis = SymbolTableGenerator(abstract_st, mem_loc)
    
    if args.sem:
        print(semantic_analysis)
                
    if semantic_analysis.errors:
        print('There are still semantic errors...')        
        for err in semantic_analysis.errors:
                print(err)
    else:    
        if args.inter:
            with open(args.file, 'r') as file:
                print(' ')
                print(file.read())
            inter = IntermediateCodeGenerator(abstract_st)
            print_imediate(inter)
        
        if args.synth:
            if not args.inter:
                with open(args.file, 'r') as file:
                    print(' ')
                    print(file.read())
            abstract_st_asm = AbstractStNodeConstructVisitor().visit(tree)
            inter = IntermediateCodeGenerator(abstract_st_asm)
            init_stack = args.stack
            mode = args.mode
            asm = AssemblyGenerator(semantic_analysis, inter.intermediate_list, init_stack, mode)
            print_asm(asm)
            
def print_asm(asm):
    single_mnemonic_instr = ['nop','hlt','btm','cwsfh','crsfh','gint','endp','getpc','setpc']
    out_file = open('bmcore_asm.txt', 'w')
    for instr in asm.asm_list:
        if len(instr) == 1 and instr[0] not in single_mnemonic_instr: 
            out_file.write(instr[0])
            out_file.write('\n')
        else:
            out_file.write('    ')
            for field in instr:
                out_file.write(str(field)+' ')
            out_file.write('\n')
    out_file.close()

def print_imediate(inter):
    cont = 0
    for i in inter.intermediate_list:
        print(cont,' : (', end = '')
        print(*i, sep = ', ', end = '')
        print(') ')
        cont += 1

if __name__ == '__main__':
    main(sys.argv)

