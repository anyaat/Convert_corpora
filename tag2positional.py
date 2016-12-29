def gender(pos):
    if 'm' in pos:
        out = 'm'
    elif 'f' in pos:
        out = 'f'
    elif 'n' in pos:
        out = 'n'
    elif 'm-f' in pos:
        out = 'c'
    else:
        out = '-'
    return out

def number(pos):
    if 'sg' in pos:
        out = 's'
    elif 'pl' in pos:
        out = 'p'
    else:
        out = '-'
    return out

def case(pos):
    if 'nom' in pos:
        out = 'n'
    elif 'gen' in pos or 'adnum' in pos:
        out = 'g'
    elif 'dat' in pos or 'dat2' in pos:
        out = 'd'
    elif 'acc' in pos or 'acc2' in pos:
        out = 'a'
    elif 'vov' in pos:
        out = 'v'
    elif 'loc' in pos:
        out = 'l'
    elif 'ins' in pos:
        out = 'i'
    else:
        out = '-'
    return out

def anim(pos):
    if 'anim' in pos:
        out = 'y'
    elif 'inan' in pos:
        out = 'n'
    else:
        out = '-'
    return out
        
def extra_case(pos):
    if 'gen2' in pos:
        out = 'p'
    elif 'loc2' in pos:
        out = 'l'
    else:
        out = '-'
    return out

def verb_form(pos):
    if 'indic' in pos:
        out = 'i'
    elif 'imper' in pos or 'imper2' in pos:
        out = 'm'
    elif 'inf' in pos:
        out = 'n'
    elif 'ger' in pos:
        out = 'g'
    elif 'partcp' in pos:
        out = 'p'
    else:
        out = '-'
    return out

def tense(pos):
    if 'praes' in pos:
        out = 'p'
    elif 'fut' in pos:
        out = 'f'
    elif 'praet' in pos:
        out = 's'
    else:
        out = '-'
    return out
        
def person(pos):
    if '1p' in pos:
        out = '1'
    elif '2p' in pos:
        out = '2'
    elif '3p' in pos:
        out = '3'
    else:
        out = '-'
    return out

def voice(pos):
    if 'act' in pos:
        out = 'a'
    elif 'pass'in pos:
        out = 'p'
    elif 'med' in pos:
        out = 'm'
    else:
        out = '-'
    return out

def brev(pos):
    if 'brev' in pos:
        out = 's'
    elif 'plen' in pos:
        out = 'f'
    else:
        out = '-'
    return out

def aspect(pos):
    if 'ipf' in pos:
        out = 'p'
    elif 'pf' in pos:
        out = 'e'
    else:
        out = '-'
    return out

def synt(pos):
    if 'SPRO' in pos:
        out = 'n'
    elif 'ADVPRO' in pos:
        out = 'r'
    elif 'APRO' in pos:
        out = 'a'
    else:
        out = '-'
    return out

def degree(pos):
    if 'comp' in pos:
        out = 'c'
    elif 'supr' in pos:
        out = 's'
    else:
        out = 'p'
    return out

def noun(pos):
    pos = pos.replace('=', ',').split(',')
    tag = 'N'
    if 'patern' in pos or 'famn' in pos or 'persn' in pos or 'zoon' in pos:
        tag += 'p'
    else:
        tag += 'c'
    tag += gender(pos)
    tag += number(pos)
    tag += case(pos)
    tag += anim(pos)
    tag += extra_case(pos)
    return tag

def verb(pos):
    pos = pos.replace('=', ',').split(',')
    tag = 'Vm'
    tag += verb_form(pos)
    tag += tense(pos)
    tag += person(pos)
    tag += number(pos)
    tag += gender(pos)
    tag += voice(pos)
    tag += brev(pos)
    tag += aspect(pos)
    tag += case(pos)
    return tag

def pro(pos):
    pos = pos.replace('=', ',').replace('-', '').split(',')
    tag = 'P-'
    tag += person(pos)
    tag += gender(pos)
    tag += number(pos)
    tag += case(pos)
    tag += synt(pos)
    tag += anim(pos)
    return tag

def adj(pos):
    pos = pos.replace('=', ',').split(',')
    tag = 'Af'
    tag += degree(pos)
    tag += gender(pos)
    tag += number(pos)
    tag += case(pos)
    tag += brev(pos)
    return tag

def num(pos):
    pos = pos.replace('=', ',').replace('-', '').split(',')
    tag = 'M'
    if 'ANUM' in pos:
        tag += 'о'
    else:
        tag += 'c'
    tag += gender(pos)
    tag += number(pos)
    tag += case(pos)
    tag += '-'         # так как в рускорпоре только ciph («Цифровая запись»)
    tag += anim(pos)
    return tag

def ruscorpora2positional(pos):
    if pos.startswith('PARENTH') or pos.startswith('NONLEX') or pos.startswith('INIT'):
        tag = 'X'
    elif pos.startswith('V'):
        tag = verb(pos)
    elif 'PRO' in pos:
        tag = pro(pos)
    elif 'NUM' in pos:
        tag = num(pos)
    elif pos.startswith('S'):
        tag = noun(pos)
    elif pos.startswith('ADV') or pos.startswith('PRAEDIC'):
        tag = 'R'
    elif pos.startswith('A'):
        tag = adj(pos)
    elif pos.startswith('CONJ'):
        tag = 'C'
    elif pos.startswith('PR'):
        tag = 'S'
    elif pos.startswith('PART'):
        tag = 'Q'
    elif pos.startswith('INTJ'):
        tag = 'I'
    else:
        print(pos)
    return tag

# example 
print(ruscorpora2positional("V,pf,tran=partcp,n,sg,brev,pass,praet"))