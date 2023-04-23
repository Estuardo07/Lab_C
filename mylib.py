def maxValue(lista):
    return max(len(elemento) for elemento in lista)

def borrarOrs(texto):
    if texto and texto[0] == "|":
        return texto[1:]
    else:
        return texto

def miesplit(string, separator):
    """Función que divide una cadena en función de un separador dado"""
    result = []
    start = 0
    for i in range(len(string)):
        if string[i:i+len(separator)] == separator:
            result.append(string[start:i])
            start = i+len(separator)
    result.append(string[start:])
    return result

def comentarios(file_path):
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

def eliminar_comentarios(texto):
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

def eliminar_entre_llaves(texto):
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

def remove_after_ws(texto):
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

def remove_after_id(texto):
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

def read_lines_after_rules(filename):
    lines = []
    with open(filename, "r") as file:
        found_tokens_rule = False
        for line in file:
            if found_tokens_rule:
                if line.startswith(" "):
                    lines.append(line.strip())
                else:
                    break
            elif line.startswith("rule tokens ="):
                found_tokens_rule = True
    return lines

def reemplazar_txt(cadena, a_reemplazar, nuevo_texto):
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

def separar_por_puntos(re):
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

def count_words_after_pipe(filename):
    # diccionario para almacenar las palabras después de |
    word_counts = {}

    # abrir el archivo de texto en modo lectura
    with open(filename, 'r') as f:
        # leer línea por línea del archivo
        for line in f:
            # inicializar la variable para almacenar la palabra después de |
            word = ""
            # indicador para saber si se ha encontrado el caracter |
            pipe_found = False

            # iterar carácter por carácter en la línea
            for c in line:
                # si se encuentra el caracter |, se empieza a agregar la palabra
                # hasta encontrar un espacio en blanco o el final de la línea
                if c == '|':
                    pipe_found = True
                    continue
                elif pipe_found and not c.isspace():
                    word += c
                elif pipe_found and c.isspace():
                    # si se ha encontrado la palabra, se agrega al diccionario
                    if word in word_counts:
                        word_counts[word] += 1
                    else:
                        word_counts[word] = 1
                    # se reinicia la variable para almacenar la palabra
                    word = ""
                    pipe_found = False

            # si se ha encontrado la palabra al final de la línea, se agrega al diccionario
            if word:
                if word in word_counts:
                    word_counts[word] += 1
                else:
                    word_counts[word] = 1

    # devolver el diccionario con las palabras y su contador de apariciones
    return word_counts
