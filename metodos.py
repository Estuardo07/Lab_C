def lectura(file_path):
    results = []
    with open(file_path, 'r') as f:
        content = []
        for line in f:
            start_idx = line.find('(*')
            end_idx = line.find('*)')
            while start_idx != -1 and end_idx != -1:
                content.append(line[start_idx+2:end_idx])
                line = line[end_idx+2:]
                start_idx = line.find('(*')
                end_idx = line.find('*)')
            if content:
                results.append(''.join(content))
                content = []
    return results

def new_txt(cadena, a_reemplazar, nuevo_texto):
    lista_cadena = list(cadena)
    lista_a_reemplazar = list(a_reemplazar)
    lista_nuevo_texto = list(nuevo_texto)
    len_a_reemplazar = len(lista_a_reemplazar)
    len_nuevo_texto = len(lista_nuevo_texto)
    len_cadena = len(lista_cadena)
    
    i = 0
    while i < len_cadena:
        if lista_cadena[i:i+len_a_reemplazar] == lista_a_reemplazar:
            lista_cadena[i:i+len_a_reemplazar] = lista_nuevo_texto
            len_cadena = len_cadena - len_a_reemplazar + len_nuevo_texto
            i = i + len_nuevo_texto
        else:
            i = i + 1
            
    return ''.join(lista_cadena)

def miSplit(string, separator):
    result = []
    start = 0
    for i in range(len(string)):
        if string[i:i+len(separator)] == separator:
            result.append(string[start:i])
            start = i+len(separator)
    result.append(string[start:])
    return result

def separar_txt(cadena, separador):
    lista_cadena = list(cadena)
    lista_separador = list(separador)
    len_separador = len(lista_separador)
    len_cadena = len(lista_cadena)
    
    resultado = []
    palabra_actual = []
    
    i = 0
    while i < len_cadena:
        if lista_cadena[i:i+len_separador] == lista_separador:
            resultado.append(''.join(palabra_actual))
            palabra_actual = []
            i = i + len_separador
        else:
            palabra_actual.append(lista_cadena[i])
            i = i + 1
    
    resultado.append(''.join(palabra_actual))
            
    return resultado

def removeOr(texto):
    if texto and texto[0] == "|":
        return texto[1:]
    else:
        return texto
    
def contarSimbolos(filename):
    word_counts = {}

    with open(filename, 'r') as f:
        for line in f:
            word = ""
            pipe_found = False

            for c in line:
                if c == '|':
                    pipe_found = True
                    continue
                elif pipe_found and not c.isspace():
                    word += c
                elif pipe_found and c.isspace():
                    if word in word_counts:
                        word_counts[word] += 1
                    else:
                        word_counts[word] = 1
                    word = ""
                    pipe_found = False

            if word:
                if word in word_counts:
                    word_counts[word] += 1
                else:
                    word_counts[word] = 1

    return word_counts

def readRules(filename):
    lines = []
    with open(filename, "r") as file:
        found_tokens_rule = False
        for line in file:
            if found_tokens_rule:
                if line.startswith(" "):
                    lines.append(line.strip())
                else:
                    break
            elif line.startswith("Rule Tokens = "):
                found_tokens_rule = True
    return lines

def vaciarLlaves(texto):
    nuevo_texto = ""
    entre_llaves = False
    
    for caracter in texto:
        if caracter == '{':
            entre_llaves = True
        elif caracter == '}':
            entre_llaves = False
        elif not entre_llaves:
            nuevo_texto += caracter
    
    return nuevo_texto

def ignorarComentarios(texto):
    nuevo_texto = ""
    entre_llaves = False
    
    for caracter in texto:
        if caracter == '(*':
            entre_llaves = True
        elif caracter == '*)':
            entre_llaves = False
        elif not entre_llaves:
            nuevo_texto += caracter
    
    return nuevo_texto

def idRule(texto):
    encontrado_id = False
    nueva_cadena = ""
    for c in texto:
        if c == "i":
            encontrado_id = True
        elif encontrado_id and c == "d":
            nueva_cadena = nueva_cadena + "id"
            break
        else:
            nueva_cadena = nueva_cadena + c
    return nueva_cadena

def ignore_ws(texto):
    encontrado_id = False
    nueva_cadena = ""
    for c in texto:
        if c == "i":
            encontrado_id = True
        elif encontrado_id and c == "d":
            nueva_cadena = nueva_cadena + "ws"
            break
        else:
            nueva_cadena = nueva_cadena + c
    return nueva_cadena

def addAppend(re):
	op = ["(","|",".",")"]
	aux = ""
	i = 0
	n = 0
	while (i + 1) < len(re):
		
		if re[i] in op:
			if re[i] == ")" and re[i+1] == "+" or re[i+1] == "*":
				aux += re[i]
				aux += re[i+1]
			elif re[i] == ")" and re[i+1] not in op and re[i+1] != "+" and re[i+1] != "*":
				aux += re[i]
				aux+= "."
			else:
				aux += re[i]

		elif re[i] == "+" or re[i] == "*":
			if(re[i+1] not in op) or re[i+1] == "(":
				aux+= "."
			
			
		elif re[i] not in op and re[i + 1] not in op and re[i + 1] != "*" and re[i + 1] != "+":
			aux += re[i]
			aux += "."
					
		elif re[i] not in op and re[i + 1] == "*" or re[i + 1] == "+":
			aux += re[i]
			aux += re[i+1]
				
		elif (re[i] not in op and re[i+1] in op):
			aux += re[i]
	
		i+=1
		n = i
		if re[i] not in op and re[i] != "*" and re[i] != "+" and n + 1 == len(re):
			aux += re[i]
	return aux
