import sys

label_dict = {}
instr_types = {
    # r type instructions
    'add' : 'r', 'sub' : 'r',  'inc' : 'r', 'dec' : 'r', 'slt' : 'r',
    'slet' : 'r', 'seq' : 'r', 'sneq' : 'r', 'shfl' : 'r','shfr' : 'r',
    'not' : 'r', 'and' : 'r', 'or' : 'r', 'xor' : 'r',  'mult' : 'r',
    'div' : 'r', 'conc' : 'r',
    # i type instructions
    'addi' : 'i','subi' : 'i', 'ld' : 'i', 'ldi' : 'i', 
    'str' : 'i','beq' : 'i', 'bneq' : 'i', 'jmpr' : 'i', 'nop' : 'i',
    'hlt' : 'i','in' : 'i', 'out' : 'i', 'push' : 'i', 'pop' : 'i', 
    'send' : 'i', 'rcv' : 'i',
    # j type instructions
    'jmp' : 'j', 'jal' : 'j',
    # x type instructions
    'ldos' : 'x', 'btm' : 'x', 'mhdm' : 'x', 'strhd' : 'x',
    'cwsfh' : 'x', 'crsfh' : 'x', 'sprc' : 'x', 'cmsg' : 'x', 'gint' : 'x',
    'endp' : 'x', 'getpc' : 'x', 'setpc' : 'x', 'syscall' : 'x'
}

def zero_complete(num, field_size):
    if num == 'a': # register address
        bin_num = '11111'
    elif num == '$sp': # stack pointer
        bin_num = '11110'
    else:
        bin_num = bin(int(num))[2:]
        for i in range(int(field_size) - len(bin_num)):
            bin_num = '0' + bin_num
    return bin_num

def R_type_instruction(instr):
    if instr[0] == 'add': # [add $r4, $r1, $r6] => r[4] = r[1] + r[6]
        opcode = '000000'
        funct = '000000'
        shamt = '00000'
        rd = instr[1].replace('$r','').replace(',','')
        RD = zero_complete(rd, 5)
        rs = instr[2].replace('$r','').replace(',','')
        RS = zero_complete(rs, 5)
        rt = instr[3].replace('$r','').replace(',','')
        RT = zero_complete(rt, 5)
        comment = ' // r['+rd+'] = r['+rs+'] + ' + 'r['+rt+']'
        bin_instr = "32'b" + opcode +  '_' + RS +  '_' + RT +  '_' + RD +  '_' + shamt +  '_' + funct + ';' + comment

    elif instr[0] == 'sub': # [sub $r4, $r3, $r7] => r[4] = r[3] + r[7]
        opcode = '000001'
        funct = '000000'
        shamt = '00000'
        rd = instr[1].replace('$r','').replace(',','')
        RD = zero_complete(rd, 5)
        rs = instr[2].replace('$r','').replace(',','')
        RS = zero_complete(rs, 5)
        rt = instr[3].replace('$r','').replace(',','')
        RT = zero_complete(rt, 5)
        comment = ' // r['+rd+'] = r['+rs+'] - ' + 'r['+rt+']'
        bin_instr = "32'b" + opcode +  '_' + RS +  '_' + RT +  '_' + RD +  '_' + shamt +  '_' + funct + ';' + comment

    elif instr[0] == 'inc': # [inc $r4] => r[4] += 1
        opcode = '000100'
        funct = '000000'
        shamt = '00000'
        RD = '00000';
        rs = instr[1].replace('$r','').replace(',','')
        RS = zero_complete(rs, 5)
        rt = instr[1].replace('$r','').replace(',','')
        RT = zero_complete(rt, 5)
        comment = ' // $sp += 1' if rt == rs == '$sp' else ' // r['+rt+'] += 1'
        bin_instr = "32'b" + opcode +  '_' + RS +  '_' + RT +  '_' + RD +  '_' + shamt +  '_' + funct + ';' + comment

    elif instr[0] == 'dec': # [dec $r4] => r[4] -= 1
        opcode = '000101'
        funct = '000000'
        shamt = '00000'
        RD = '00000'
        rs = instr[1].replace('$r','').replace(',','')
        RS = zero_complete(rs, 5)
        rt = instr[1].replace('$r','').replace(',','')
        RT = zero_complete(rt, 5)
        comment = ' // $sp -= 1' if rt == rs == '$sp' else ' // r['+rt+'] -= 1'
        bin_instr = "32'b" + opcode +  '_' + RS +  '_' + RT +  '_' + RD +  '_' + shamt +  '_' + funct + ';' + comment

    elif instr[0] == 'slt': # [slt $r16, $r3, $r12] => (r[3] < r[12]) ? r[16] = 1 : r[16] = 0
        opcode = '000110'
        funct = '000000'
        shamt = '00000'
        rd = instr[1].replace('$r','').replace(',','')
        RD = zero_complete(rd, 5)
        rs = instr[2].replace('$r','').replace(',','')
        RS = zero_complete(rs, 5)
        rt = instr[3].replace('$r','').replace(',','')
        RT = zero_complete(rt, 5)
        comment = ' // (r[' + rs + '] < r[' + rt + ']) ? r[' + rd + '] = 1' + ' : r[' + rd + '] = 0'
        bin_instr = "32'b" + opcode +  '_' + RS +  '_' + RT +  '_' + RD +  '_' + shamt +  '_' + funct + ';' + comment

    elif instr[0] == 'slet': # [slet $r16, $r3, $r12] => (r[3] <= r[12]) ? r[16] = 1 : r[16] = 0
        opcode = '011101'
        funct = '000000'
        shamt = '00000'
        rd = instr[1].replace('$r','').replace(',','')
        RD = zero_complete(rd, 5)
        rs = instr[2].replace('$r','').replace(',','')
        RS = zero_complete(rs, 5)
        rt = instr[3].replace('$r','').replace(',','')
        RT = zero_complete(rt, 5)
        comment = ' // (r[' + rs + '] <= r[' + rt + ']) ? r[' + rd + '] = 1' + ' : r[' + rd + '] = 0'
        bin_instr = "32'b" + opcode +  '_' + RS +  '_' + RT +  '_' + RD +  '_' + shamt +  '_' + funct + ';' + comment

    elif instr[0] == 'seq': # [seq $r16, $r3, $r12] => (r[3] == r[12]) ? r[16] = 1 : r[16] = 0
        opcode = '011110'
        funct = '000000'
        shamt = '00000'
        rd = instr[1].replace('$r','').replace(',','')
        RD = zero_complete(rd, 5)
        rs = instr[2].replace('$r','').replace(',','')
        RS = zero_complete(rs, 5)
        rt = instr[3].replace('$r','').replace(',','')
        RT = zero_complete(rt, 5)
        comment = ' // (r[' + rs + '] == r[' + rt + ']) ? r[' + rd + '] = 1' + ' : r[' + rd + '] = 0'
        bin_instr = "32'b" + opcode +  '_' + RS +  '_' + RT +  '_' + RD +  '_' + shamt +  '_' + funct + ';' + comment

    elif instr[0] == 'sneq': # [sneq $r16, $r3, $r12] => (r[3] != r[12]) ? r[16] = 1 : r[16] = 0
        opcode = '011111'
        funct = '000000'
        shamt = '00000'
        rd = instr[1].replace('$r','').replace(',','')
        RD = zero_complete(rd, 5)
        rs = instr[2].replace('$r','').replace(',','')
        RS = zero_complete(rs, 5)
        rt = instr[3].replace('$r','').replace(',','')
        RT = zero_complete(rt, 5)
        comment = ' // (r[' + rs + '] != r[' + rt + ']) ? r[' + rd + '] = 1' + ' : r[' + rd + '] = 0'
        bin_instr = "32'b" + opcode +  '_' + RS +  '_' + RT +  '_' + RD +  '_' + shamt +  '_' + funct + ';' + comment

    elif instr[0] == 'shfl': # [shfl $r2, $r1, 6] => r[2] = sl(6)r[1]
        opcode = '000111'
        funct = '000000'
        RT = '00000'
        rd = instr[1].replace('$r','').replace(',','')
        RD = zero_complete(rd, 5)
        rs = instr[2].replace('$r','').replace(',','')
        RS = zero_complete(rs, 5)
        shamt = instr[3].replace('$r','').replace(',','')
        SHAMT = zero_complete(shamt, 5)
        comment = ' // r['+rd+'] = sl('+shamt+')r['+rs+']'
        bin_instr = "32'b" + opcode +  '_' + RS +  '_' + RT +  '_' + RD +  '_' + SHAMT +  '_' + funct + ';' + comment

    elif instr[0] == 'shfr': # [shfr $r14, $r1, 19] => r[14] = sl(19)r[1]
        opcode = '001000'
        funct = '000000'
        RT = '00000'
        rd = instr[1].replace('$r','').replace(',','')
        RD = zero_complete(rd, 5)
        rs = instr[2].replace('$r','').replace(',','')
        RS = zero_complete(rs, 5)
        shamt = instr[3].replace('$r','').replace(',','')
        SHAMT = zero_complete(shamt, 5)
        comment = ' // r['+rd+'] = sr('+shamt+')r['+rs+']'
        bin_instr = "32'b" + opcode +  '_' + RS +  '_' + RT +  '_' + RD +  '_' + SHAMT +  '_' + funct + ';' + comment

    elif instr[0] == 'not': # [not $r4, $r13] => r[4] = ~r[13]
        opcode = '001001'
        funct = '000000'
        shamt = '00000'
        RD = '00000'
        rt = instr[1].replace('$r','').replace(',','')
        RT = zero_complete(rt, 5)
        rs = instr[2].replace('$r','').replace(',','')
        RS = zero_complete(rs, 5)
        comment = ' // r['+rt+'] = ~r['+rs+']'
        bin_instr = "32'b" + opcode +  '_' + RS +  '_' + RT +  '_' + RD +  '_' + shamt +  '_' + funct + ';' + comment

    elif instr[0] == 'and': # [and $r1, $r2, $r3] => r[1] = r[2] & r[3]
        opcode = '001010'
        funct = '000000'
        shamt = '00000'
        rd = instr[1].replace('$r','').replace(',','')
        RD = zero_complete(rd, 5)
        rs = instr[2].replace('$r','').replace(',','')
        RS = zero_complete(rs, 5)
        rt = instr[3].replace('$r','').replace(',','')
        RT = zero_complete(rt, 5)
        comment = ' // r['+rd+'] = r['+rs+'] & ' + 'r['+rt+']'
        bin_instr = "32'b" + opcode +  '_' + RS +  '_' + RT +  '_' + RD +  '_' + shamt +  '_' + funct + ';' + comment

    elif instr[0] == 'or': # [or $r4, $r5, $r29] => r[4] = r[5] | r[29]
        opcode = '001011'
        funct = '000000'
        shamt = '00000'
        rd = instr[1].replace('$r','').replace(',','')
        RD = zero_complete(rd, 5)
        rs = instr[2].replace('$r','').replace(',','')
        RS = zero_complete(rs, 5)
        rt = instr[3].replace('$r','').replace(',','')
        RT = zero_complete(rt, 5)
        comment = ' // r['+rd+'] = r['+rs+'] | ' + 'r['+rt+']'
        bin_instr = "32'b" + opcode +  '_' + RS +  '_' + RT +  '_' + RD +  '_' + shamt +  '_' + funct + ';' + comment

    elif instr[0] == 'xor': # [xor $r6, $r6, $r22] => r[6] = r[6] ^ r[22]
        opcode = '001100'
        funct = '000000'
        shamt = '00000'
        rd = instr[1].replace('$r','').replace(',','')
        RD = zero_complete(rd, 5)
        rs = instr[2].replace('$r','').replace(',','')
        RS = zero_complete(rs, 5)
        rt = instr[3].replace('$r','').replace(',','')
        RT = zero_complete(rt, 5)
        comment = ' // r['+rd+'] = r['+rs+'] ^ ' + 'r['+rt+']'
        bin_instr = "32'b" + opcode +  '_' + RS +  '_' + RT +  '_' + RD +  '_' + shamt +  '_' + funct + ';' + comment

    elif instr[0] == 'mult': # [mult $r30, $r29, $r1] => r[30] = r[29] ^ r[1]
        opcode = '001101'
        funct = '000000'
        shamt = '00000'
        rd = instr[1].replace('$r','').replace(',','')
        RD = zero_complete(rd, 5)
        rs = instr[2].replace('$r','').replace(',','')
        RS = zero_complete(rs, 5)
        rt = instr[3].replace('$r','').replace(',','')
        RT = zero_complete(rt, 5)
        comment = ' // r['+rd+'] = r['+rs+'] * ' + 'r['+rt+']'
        bin_instr = "32'b" + opcode +  '_' + RS +  '_' + RT +  '_' + RD +  '_' + shamt +  '_' + funct + ';' + comment

    elif instr[0] == 'div': # [div $r3, $r29, $r18] => r[30] = r[29] ^ r[18]
        opcode = '001110'
        funct = '000000'
        shamt = '00000'
        rd = instr[1].replace('$r','').replace(',','')
        RD = zero_complete(rd, 5)
        rs = instr[2].replace('$r','').replace(',','')
        RS = zero_complete(rs, 5)
        rt = instr[3].replace('$r','').replace(',','')
        RT = zero_complete(rt, 5)
        comment = ' // r['+rd+'] = r['+rs+'] / ' + 'r['+rt+']'
        bin_instr = "32'b" + opcode +  '_' + RS +  '_' + RT +  '_' + RD +  '_' + shamt +  '_' + funct + ';' + comment

    elif instr[0] == 'conc': # [conc $r1, $r2, $r3] => r[1] = {r[2],r[3]}
        opcode = '100111'
        funct = '000000'
        shamt = '00000'
        rd = instr[1].replace('$r','').replace(',','')
        RD = zero_complete(rd, 5)
        rs = instr[2].replace('$r','').replace(',','')
        RS = zero_complete(rs, 5)
        rt = instr[3].replace('$r','').replace(',','')
        RT = zero_complete(rt, 5)
        comment = ' // r['+rd+'] = {r['+rs+'],r['+rt+']}'
        bin_instr = "32'b" + opcode +  '_' + RS +  '_' + RT +  '_' + RD +  '_' + shamt +  '_' + funct + ';' + comment

    return bin_instr

def I_type_instruction(instr):
    if instr[0] == 'addi': # [addi $r4, $r5, 17]
        opcode = '000010'
        rt = instr[1].replace('$r','').replace(',','')
        RT = zero_complete(rt, 5)
        rs = instr[2].replace('$r','').replace(',','')
        RS = zero_complete(rs, 5)
        offset = instr[3].replace('$r','').replace(',','')
        OfS = zero_complete(offset, 16)
        comment =  ' // $sp = $sp + ' + offset if rt == rs == '$sp' else ' // r['+rt+'] = r['+rs+'] + ' + offset
        bin_instr = "32'b" + opcode +  '_' + RS +  '_' + RT +  '_' + OfS + ';' + comment

    elif instr[0] == 'subi': # [subi $r23, $r25, 317]
        opcode = '000011'
        rt = instr[1].replace('$r','').replace(',','')
        RT = zero_complete(rt, 5)
        rs = instr[2].replace('$r','').replace(',','')
        RS = zero_complete(rs, 5)
        offset = instr[3].replace('$r','').replace(',','')
        OfS = zero_complete(offset, 16)
        comment =  ' // $sp = $sp - ' + offset if rt == rs == '$sp' else ' // r['+rt+'] = r['+rs+'] - ' + offset
        bin_instr = "32'b" + opcode +  '_' + RS +  '_' + RT +  '_' + OfS + ';' + comment

    elif instr[0] == 'ld': # [ld $r6, $r10, 17] => r[6] = m[r[10]+17]
        opcode = '001111'
        rt = instr[1].replace('$r','').replace(',','')
        RT = zero_complete(rt, 5)
        rs = instr[2].replace('$r','').replace(',','')
        RS = zero_complete(rs, 5)
        offset = instr[3].replace('$r','').replace(',','')
        OfS = zero_complete(offset, 16)
        comment = ' // r['+rt+'] = m[r['+rs+'] + '+offset+']'
        bin_instr = "32'b" + opcode +  '_' + RS +  '_' + RT +  '_' + OfS + ';' + comment

    elif instr[0] == 'ldi': # [ldi $r6, 666] => r[6] = 666
        opcode = '010000'
        RS = '00000'
        rt = instr[1].replace('$r','').replace(',','')
        RT = zero_complete(rt, 5)
        offset = instr[2].replace('$r','').replace(',','')
        OfS = zero_complete(offset, 16)
        comment =' // $sp = '+offset if rt == '$sp' else ' // r['+rt+'] = '+offset
        bin_instr = "32'b" + opcode +  '_' + RS +  '_' + RT +  '_' + OfS + ';' + comment

    elif instr[0] == 'str': # [str $r0, 24, $r13] => m[r[0] + 24] = r[13]
        opcode = '010001'
        rs = instr[1].replace('$r','').replace(',','')
        RS = zero_complete(rs, 5)
        offset = instr[2].replace('$r','').replace(',','')
        OfS = zero_complete(offset, 16)
        rt = instr[3].replace('$r','').replace(',','')
        RT = zero_complete(rt, 5)
        comment = ' // m[r['+rs+'] + '+offset+'] = r['+rt+']'
        bin_instr = "32'b" + opcode +  '_' + RS +  '_' + RT +  '_' + OfS + ';' + comment

    elif instr[0] == 'beq': # [beq $r14, $r15, (address/label)] => if(r[14] == r[15]) jump to (address/label)
        opcode = '010010'
        rt = instr[1].replace('$r','').replace(',','')
        RT = zero_complete(rt, 5)
        rs = instr[2].replace('$r','').replace(',','')
        RS = zero_complete(rs, 5)
        offset = instr[3].replace('$r','').replace(',','')
        if offset in label_dict: # if it refers to a label
            OfS = zero_complete(label_dict[offset], 16)
            flag = True
        else:
            OfS = zero_complete(offset, 16)
            flag = False
        comment = ' // if(r['+rs+'] == r['+rt+']) jump to ' + ((str(label_dict[offset]) + '('+offset+')') if flag else offset)
        bin_instr = "32'b" + opcode +  '_' + RS +  '_' + RT +  '_' + OfS + ';' + comment

    elif instr[0] == 'bneq': # [bneq $r12, $r30, (address/label)] => if(r[12] != r[30]) jump to (address/label)
        opcode = '010011'
        rt = instr[1].replace('$r','').replace(',','')
        RT = zero_complete(rt, 5)
        rs = instr[2].replace('$r','').replace(',','')
        RS = zero_complete(rs, 5)
        offset = instr[3].replace('$r','').replace(',','')
        if offset in label_dict: # if it refers to a label
            OfS = zero_complete(label_dict[offset], 16)
            flag = True
        else:
            OfS = zero_complete(offset, 16)
            flag = True
        comment = ' // if(r['+rs+'] != r['+rt+']) jump to ' + ((str(label_dict[offset]) + '('+offset+')') if flag else offset)
        bin_instr = "32'b" + opcode +  '_' + RS +  '_' + RT +  '_' + OfS + ';' + comment

    elif instr[0] == 'jmpr': # [jmpr $r23] => jump to r[23]
        opcode = '010101'
        RT = '00000'
        offset = '0000000000000000'
        rs = instr[1].replace('$r','').replace(',','')
        RS = zero_complete(rs,5)
        comment = ' // jump to $ra' if rs == 'a' else ' // jump to r['+rs+']'
        bin_instr = "32'b" + opcode +  '_' + RS +  '_' + RT +  '_' + offset + ';' + comment

    elif instr[0] == 'nop': # nop
        opcode = '010110'
        comment = ' // nop'
        bin_instr = "32'b" + opcode +  '_' + '00000000000000000000000000' + ';' + comment

    elif instr[0] == 'hlt': # hlt
        opcode = '010111'
        comment = ' // hlt'
        bin_instr = "32'b" + opcode +  '_' + '11111111111111111111111111' + ';' + comment

    elif instr[0] == 'in': # [in $r23] => r[23] = SWITCHES
        opcode = '011000'
        rt = instr[1].replace('$r','').replace(',','')
        RT = zero_complete(rt, 5)
        comment = ' // r['+rt+'] = SWITCHES'
        bin_instr = "32'b" + opcode +  '_' + '00000' +  '_' + RT +  '_' + '0000000000000000' + ';' + comment

    elif instr[0] == 'out': # [out $r19] => LEDS = r[19]
        opcode = '011001'
        rs = instr[1].replace('$r','').replace(',','')
        RS = zero_complete(rs,5)
        comment = ' // LEDS = r['+rs+']'
        bin_instr = "32'b" + opcode +  '_' + RS +  '_' + '000000000000000000000' + ';' + comment

    elif instr[0] == 'push': # [push $r0, 123, $r4] => stack[r[0] + 123] = r[4]
        opcode = '011011'
        rs = instr[1].replace('$r','').replace(',','')
        RS = zero_complete(rs, 5)
        offset = instr[2].replace('$r','').replace(',','')
        OfS = zero_complete(offset, 16)
        rt = instr[3].replace('$r','').replace(',','')
        RT = zero_complete(rt, 5)
        foo = '$ra' if rt == 'a' else 'r['+rt+']'
        comment = ' // stack[$sp + '+offset+'] = ' + foo if rs == '$sp' else ' // stack[r['+rs+'] + '+offset+'] = ' + foo
        #comment = ' // stack[$sp + '+offset+'] = r['+rt+']' if rs == '$sp' else ' // stack[r['+rs+'] + '+offset+'] = r['+rt+']'
        bin_instr = "32'b" + opcode +  '_' + RS +  '_' + RT +  '_' + OfS + ';' + comment

    elif instr[0] == 'pop': # [pop $r16, $r1, 27] => r[16] = stack[r[1]+27]
        opcode = '011100'
        rt = instr[1].replace('$r','').replace(',','')
        RT = zero_complete(rt, 5)
        rs = instr[2].replace('$r','').replace(',','')
        RS = zero_complete(rs, 5)
        offset = instr[3].replace('$r','').replace(',','')
        OfS = zero_complete(offset, 16)
        foo = '$ra' if rt == 'a' else 'r['+rt+']'
        comment = ' // '+foo+' = stack[$sp + '+offset+']' if rs == '$sp' else ' // '+foo+' = stack[r['+rs+'] + '+offset+']'
        bin_instr = "32'b" + opcode +  '_' + RS +  '_' + RT +  '_' + OfS + ';' + comment

    #############################
    elif instr[0] == 'rcv': # [rcv $r23] => r[23] = UART_data
        opcode = '101101'
        rt = instr[1].replace('$r','').replace(',','')
        RT = zero_complete(rt, 5)
        comment = ' // r['+rt+'] = UART_data'
        bin_instr = "32'b" + opcode +  '_' + '00000' +  '_' + RT +  '_' + '0000000000000000' + ';' + comment

    elif instr[0] == 'send': # [send $r19] => UART_data = LEDS = r[19]
        opcode = '101110'
        rs = instr[1].replace('$r','').replace(',','')
        RS = zero_complete(rs,5)
        comment = ' // UART_data = LEDS = r['+rs+']'
        bin_instr = "32'b" + opcode +  '_' + RS +  '_' + '000000000000000000000' + ';' + comment

    #############################

    return bin_instr

def J_type_instruction(instr):
    if instr[0] == 'jmp': # [jmp (address/label)] => jump to (address/label)
        opcode = '010100'
        offset = instr[1].replace('$r','').replace(',','')
        if offset in label_dict: # if it refers to a label
            OfS = zero_complete(label_dict[offset], 26)
            flag = True
        else:
            OfS = zero_complete(offset, 26)
            flag = False
        comment = ' // jump to ' + ((str(label_dict[offset]) + '('+offset+')') if flag else offset)
        bin_instr = "32'b" + opcode +  '_' + OfS + ';' + comment

    elif instr[0] == 'jal': # [jal (address/label)] => jump to (address/label), $ra = PC + 1
        opcode = '011010'
        offset = instr[1].replace('$r','').replace(',','')
        if offset in label_dict: # if it refers to a label
            OfS = zero_complete(label_dict[offset], 26)
            flag = True
        else:
            OfS = zero_complete(offset, 26)
            flag = False
        comment = ' // jump to ' + (str(label_dict[offset]) + ('('+offset+')') if flag else offset) + ', $ra = PC + 1'
        bin_instr = "32'b" + opcode +  '_' + OfS + ';' + comment

    return bin_instr

def X_type_instruction(instr):
    if instr[0] == 'ldos': # [ldos $r1, $r2, $r3] => mem[OS][line=r[3]] <= hd[proc=r[1]][line=r[2]]
        opcode = '100010'
        funct = '000000'
        shamt = '00000'
        rs = instr[1].replace('$r','').replace(',','')
        RS = zero_complete(rs, 5)
        rt = instr[2].replace('$r','').replace(',','')
        RT = zero_complete(rt, 5)
        rd = instr[3].replace('$r','').replace(',','')
        RD = zero_complete(rd, 5)

        comment = ' // mem[OS][line=r['+rd+']] <= hd[proc=r['+rs+']][line=r['+rt+']]'
        bin_instr = "32'b" + opcode +  '_' + RS +  '_' + RT +  '_' + RD +  '_' + shamt + funct + ';' + comment

    elif instr[0] == 'btm': # BIOS to Memory context
        opcode = '100000'
        funct = '000000'
        shamt = '00000'
        RS = '00000'
        RT = '00000'
        RD = '00000'

        comment = ' // BIOS to Memory context'
        bin_instr = "32'b" + opcode +  '_' + RS +  '_' + RT +  '_' + RD +  '_' + shamt + funct + ';' + comment
        
    elif instr[0] == 'mhdm': # [mhdm $r1, $r2, $r3] => mem[proc=r[1]][line=r[3]] <= hd[proc=r[1]][line=r[2]]
        opcode = '100011'
        funct = '000000'
        shamt = '00000'
        rs = instr[1].replace('$r','').replace(',','')
        RS = zero_complete(rs, 5)
        rt = instr[2].replace('$r','').replace(',','')
        RT = zero_complete(rt, 5)
        rd = instr[3].replace('$r','').replace(',','')
        RD = zero_complete(rd, 5)

        comment = ' // mem[proc=r['+rs+']][line=r['+rd+']] <= hd[proc=r['+rs+']][line=r['+rt+']]'
        bin_instr = "32'b" + opcode +  '_' + RS +  '_' + RT +  '_' + RD +  '_' + shamt + funct + ';' + comment

    elif instr[0] == 'strhd': # [strhd $r1, $r2, $r3] => hd[proc=r[1]][line=r[2]] <= r[3]
        opcode = '100101'
        funct = '000000'
        shamt = '00000'
        rs = instr[1].replace('$r','').replace(',','')
        RS = zero_complete(rs, 5)   
        rt = instr[2].replace('$r','').replace(',','')
        RT = zero_complete(rt, 5)
        rd = instr[3].replace('$r','').replace(',','')
        RD = zero_complete(rd, 5)

        comment = ' // hd[proc=r['+rs+']][line=r['+rt+']] <= reg['+rd+']'
        bin_instr = "32'b" + opcode +  '_' + RS +  '_' + RT +  '_' + RD +  '_' + shamt + funct + ';' + comment

    elif instr[0] == 'cwsfh': # [cwsfh]
        opcode = '101001'
        instr_body = '00000000000000000000000000'

        comment = '// change registers write shift'
        bin_instr = "32'b" + opcode + '_' + instr_body + ';' + comment

    elif instr[0] == 'crsfh': # [crsfh]
        opcode = '101010'
        instr_body = '00000000000000000000000000'

        comment = ' // change registers read shift'
        bin_instr = "32'b" + opcode + '_' + instr_body + ';' + comment

    elif instr[0] == 'sprc': # [sprc $r1] => process_number <= RS(r[1])
        opcode = '100110'
        rs = instr[1].replace('$r','').replace(',','')
        RS = zero_complete(rs, 5)   
        instr_body = '000000000000000000000'

        comment = ' // process_number <= RS(r['+rs+'])'
        bin_instr = "32'b" + opcode + '_' + RS + '_' + instr_body + ';' + comment

    elif instr[0] == 'cmsg': # [cmsg 12] => lcd_msg = 12
        opcode = '101000'
        offset = str(instr[1])
        OfS = zero_complete(offset, 16)
        instr_body = '0000000000'

        comment = ' // lcd_msg = ' + offset
        bin_instr = "32'b" + opcode + '_' + instr_body + '_' + OfS + ';' + comment
 
    elif instr[0] == 'endp':
        opcode = '111111'
        instr_body = '00000000000000000000000000'
        
        comment = ' // end of the program'
        bin_instr = "32'b" + opcode + '_' + instr_body + ';' + comment
    
    elif instr[0] == 'getpc': # [getpc] => r[28] = process_pc
        opcode = '101011'
        instr_body = '00000000000000000000000000'
        
        comment = ' // r[28] = process_pc'
        bin_instr = "32'b" + opcode + '_' + instr_body + ';' + comment

    elif instr[0] == 'setpc': # [setpc $r1] => process_pc <= RS(r[1])
        opcode = '101100'
        rs = instr[1].replace('$r','').replace(',','')
        RS = zero_complete(rs, 5)   
        instr_body = '000000000000000000000'

        comment = ' // process_pc = RS(r['+rs+'])'
        bin_instr = "32'b" + opcode + '_' + RS + '_' + instr_body + ';' + comment
    
    # 0 -> input, 1 -> output, 2 -> receive, 3 -> send
    elif instr[0] == 'syscall': # syscall 0
        opcode = '111110'
        offset = str(instr[1])
        OfS = zero_complete(offset, 16)
        instr_body = '0000000000'
        if offset == '0':
            syscall_name = 'input'
        elif offset == '1':
            syscall_name = 'output'
        elif offset == '2':
            syscall_name = 'uart_input'
        elif offset == '3':
            syscall_name = 'uart_output'
        comment = ' // ' + syscall_name + ' syscall'
        bin_instr = "32'b" + opcode + '_' + instr_body + '_' + OfS + ';' + comment
        
    return bin_instr

def main():
    instr_num = 0
    asm_list = [line.rstrip('\n') for line in open('bmcore_asm.txt')]
    # first pass to set label line numbers
    for line in asm_list:
        instr = line.split()
        instr_name = instr[0]
        if instr_name not in instr_types:
            label_dict[instr_name.replace(':','')] = instr_num
        else:
            instr_num += 1

    if len(sys.argv) < 3:
        print("To run this file insert memory name and it's respective initial index!")
        return
        
    mem_name = str(sys.argv[1])
    instr_num = int(sys.argv[2]) 
    # second pass through the list to generate the coresponding binary
    out_file = open('bmcore_bin.txt', 'w')
    for line in asm_list:
        instr = line.split()
        instr_name = instr[0]
        if instr_name in instr_types: # actual line is a instruction
            instr_type = instr_types[instr_name]
            if instr_type == 'r':
                binary = R_type_instruction(instr)
            elif instr_type == 'i':
                binary = I_type_instruction(instr)
            elif instr_type == 'j':
                binary = J_type_instruction(instr)
            else: # os related instructions
                binary = X_type_instruction(instr)
            out = mem_name +'['+str(instr_num)+'] <= ' + binary
            instr_num += 1
            out_file.write(out+'\n')
        # actual line is a label already set on the first pass
        else: 
            continue

    out_file.close()
    # printing the written file
    file_lines = [line.rstrip('\n') for line in open('bmcore_bin.txt', 'r')]
    for file_line in file_lines:
        print(file_line)

    print('Program size: ', len(file_lines))

    

if __name__ == '__main__':
    main()


'''
Fibonacci Sequence wombo example:

main:
    ldi $r1, 1
    ldi $r2, 2
    ldi $r3, 3
    ldi $r13, 0
    in $r20
    beq $r20, $r1, Label1
    beq $r20, $r2, Label2
    beq $r20, $r3, Label2
    subi $r20, $r20, 3
    addi $r4, $r0, 1
    addi $r5, $r0, 1
Label3:
    beq $r31, $r13, Label4
    addi $r13, $r13, 1
    add $r6, $r5, $r4
    add $r4, $r5, $r0
    add $r5, $r6, $r0
    jmp Label3
Label1:
    out $r0
Label2:
    out $r1
Label4:
    out $r6
    hlt

Output:

instrmem[0] <= 32'b010000_00000_00001_0000000000000001; // r[1] = 1
instrmem[1] <= 32'b010000_00000_00010_0000000000000010; // r[2] = 2
instrmem[2] <= 32'b010000_00000_00011_0000000000000011; // r[3] = 3
instrmem[3] <= 32'b010000_00000_01101_0000000000000000; // r[13] = 0
instrmem[4] <= 32'b011000_00000_10100_0000000000000000; // r[20] = SWITCHES
instrmem[5] <= 32'b010010_00001_10100_0000000000010001; // if(r[1] == r[20]) jump to 17(Label1)
instrmem[6] <= 32'b010010_00010_10100_0000000000010010; // if(r[2] == r[20]) jump to 18(Label2)
instrmem[7] <= 32'b010010_00011_10100_0000000000010010; // if(r[3] == r[20]) jump to 18(Label2)
instrmem[8] <= 32'b000011_10100_10100_0000000000000011; // r[20] = r[20] - 3
instrmem[9] <= 32'b000010_00000_00100_0000000000000001; // r[4] = r[0] + 1
instrmem[10] <= 32'b000010_00000_00101_0000000000000001; // r[5] = r[0] + 1
instrmem[11] <= 32'b010010_01101_11111_0000000000010011; // if(r[13] == r[31]) jump to 19(Label4)
instrmem[12] <= 32'b000010_01101_01101_0000000000000001; // r[13] = r[13] + 1
instrmem[13] <= 32'b000000_00101_00100_00110_00000_000000; // r[6] = r[5] + r[4]
instrmem[14] <= 32'b000000_00101_00000_00100_00000_000000; // r[4] = r[5] + r[0]
instrmem[15] <= 32'b000000_00110_00000_00101_00000_000000; // r[5] = r[6] + r[0]
instrmem[16] <= 010100_00000000000000000000001011 // jump to 11(Label3)
instrmem[17] <= 32'b011001_00000_000000000000000000000; // LEDS = r[0]
instrmem[18] <= 32'b011001_00001_000000000000000000000; // LEDS = r[1]
instrmem[19] <= 32'b011001_00110_000000000000000000000; // LEDS = r[6]
instrmem[20] <= 32'b010111_11111111111111111111111111; // hlt

'''
