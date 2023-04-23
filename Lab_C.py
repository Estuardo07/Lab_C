from mylib import *
from afd import *

#Funciones basicas 
abcd = "a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z"
ABCD = "A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z"
digits = "0|1|2|3|4|5|6|7|8|9"

let_dic = {}
let_list = []
let_coments = []

tokens = []
filename = "./tests/slr-1.yal"
word_counts = read_lines_after_rules(filename)
tokens_dic = {}

tree_list = []

for x in word_counts:
    
    if maxValue(word_counts) == len(x):
        tokens.append(borrarOrs(reemplazar_txt(x, ' ', ''))[:2])
        
    else:
        tokens.append(remove_after_id(eliminar_comentarios(eliminar_entre_llaves(x))))
    

for i in range(len(tokens)):
    if '|' in tokens[i]:
        tokens[i] = reemplazar_txt(tokens[i], '|', '')
        tokens[i] = reemplazar_txt(tokens[i], ' ', '')

with open(filename, 'r') as file:
    for line in file:        
        if 'let' in line:
            let_list.append(separar_txt((separar_txt(line, '=')[0]), ' ')[1])
            let_dic[miesplit((separar_txt(line, '=')[0]), ' ')[1]] = miesplit(line, '=')[1]
        
    for element in let_dic:
        let_dic[element] = reemplazar_txt(let_dic[element], ' ', '')
        let_dic[element] = reemplazar_txt(let_dic[element], '\n', '')
        let_dic[element] = reemplazar_txt(let_dic[element], '"', '')
    
        if "['A'-'Z''a'-'z']" in let_dic[element]:
            
            let_dic[element] = abcd+"|"+ABCD
        if '0123456789' in let_dic[element]:
            
            let_dic[element] = digits
        if "['0'-'9']" in let_dic[element]:
            let_dic[element] = digits
        
        for key in let_dic.keys():
            if key in let_dic[element]:
                let_dic[element] = reemplazar_txt(let_dic[element], key, let_dic[key])
        
        for value in let_dic.values():
            if "''" in value:
                let_dic[element] = reemplazar_txt(let_dic[element], "'", "")
                let_dic[element] = reemplazar_txt(let_dic[element], "\x5C", "|")
                let_dic[element] = reemplazar_txt(let_dic[element], "[", "")  
                let_dic[element] = reemplazar_txt(let_dic[element], "]", "")              
            if "|" in value:
                let_dic[element] = borrarOrs(let_dic[element])
            
          
           
    for key in let_dic:
        if key in tokens:
            tokens_dic[key] = let_dic[key]
    
    for i in range(len(tokens)):
        for key in tokens_dic:
            if tokens[i] == key:
                tokens[i] = tokens_dic[key]
    
    print('arbol completo regex')
    tree= str(tokens[0]) + str(tokens[1])
    print(tree)

    arbol_sintactico(tree)
    
    
    for i in range(len(tokens)):
        if tokens[i] in let_dic[element]:
            let_dic[element] = reemplazar_txt(let_dic[element], tokens[i], tokens[i])

    print('Tokens:\n')
    print(tokens)
    print('Let:\n')
    print(let_dic)
