from lexer import infix_to_postfix
from mylib import separar_por_puntos
from collections import defaultdict
import os

def postorden(arbol):
	if not arbol.leaf:
		if arbol.one:
			postorden(arbol.left_child)
            # Como dice el libro del dragon, solo el nodo asterisco es nullable
			if arbol.value == "*":
				arbol.nullable = True
			else:
				arbol.nullable = arbol.left_child.nullable 
		else:
			postorden(arbol.left_child)
			postorden(arbol.right_child)
            # El nodo | es nullable si alguno de sus hijos es nullable
			if arbol.value == "|":
				arbol.nullable = arbol.left_child.nullable or arbol.right_child.nullable
            # El nodo . es nullable si ambos hijos son nullable
			elif arbol.value == ".":
				arbol.nullable = arbol.left_child.nullable and arbol.right_child.nullable
	else:
		arbol.nullable = False

def followpos(arbol):
	# recorrido en postorden para agregar followpos
	if not arbol.leaf:
		if arbol.one:
			followpos(arbol.left_child)
			for i in range(len(arbol.lastpos)):
				for j in range(len(arbol.firstpos)):
					Node.followpos[arbol.lastpos[i]].append(arbol.firstpos[j])
		else:
			followpos(arbol.left_child)
			followpos(arbol.right_child)
            # Si n es un nodo-concat con el hijo izquierdo c1 y con el hijo derecho c2, entonces para cada posición i en ultimapos(c1), todas las posiciones en primerapos(c2) se encuentran en siguientepos(i)
			if arbol.value == ".":
				for i in range(len(arbol.left_child.lastpos)):
					for j in range(len(arbol.right_child.firstpos)):
						Node.followpos[arbol.left_child.lastpos[i]].append(arbol.right_child.firstpos[j])
	
		

def firstpos(arbol):
	# recorrido en postorden para agregar firstpos y lastpos
	if not arbol.leaf:
		if arbol.one:
			firstpos(arbol.left_child)
			arbol.firstpos = arbol.left_child.firstpos
			arbol.lastpos = arbol.left_child.lastpos
		else:
			firstpos(arbol.left_child)
			firstpos(arbol.right_child)
			if arbol.value == "|":
				arbol.firstpos = arbol.left_child.firstpos + arbol.right_child.firstpos
				arbol.lastpos = arbol.left_child.lastpos + arbol.right_child.lastpos
			else:
				if arbol.left_child.nullable == True:
					arbol.firstpos = arbol.left_child.firstpos + arbol.right_child.firstpos
				else:
					arbol.firstpos = arbol.left_child.firstpos
				if arbol.right_child.nullable == True:
					arbol.lastpos = arbol.left_child.lastpos + arbol.right_child.lastpos
				else:
					arbol.lastpos = arbol.right_child.lastpos

def crear_diccionario(arbol):
	# recorrido en preorden para crear diccionario
	if not arbol.leaf:
		if arbol.one:
			crear_diccionario(arbol.left_child)
		else:
			crear_diccionario(arbol.left_child)
			crear_diccionario(arbol.right_child)
	else:
		Node.dictionaryofpos[arbol.name] = arbol.value
			
class Node(object):
	# clase nodo
    #a_gxiliar para declarar .gv
	a_gx = "" 
    #a_gxiliar parara declarar conexiones .gv
	a_gx2 = "" 
    #atributo a_gxiliar para nombrar nodo
	total_of_nodes = 0 
	namea_gx = 1
	followpos = defaultdict(list)
	dictionaryofpos = {}
	def __init__(self,value,leaf = False,one=True,center_child=False,right_child=False,left_child=False,nullable=False,name = 0):
		self.firstpos = [] 
		self.lastpos  = []
		self.value = value
		self.leaf = leaf
		self.one = one
		self.nullable = nullable
		self.number = Node.total_of_nodes
		self.name = name
		Node.total_of_nodes += 1
		if leaf == False:
			if one:
				self.left_child = center_child
			else:
				self.left_child = left_child  
				self.right_child = right_child



	def conexiones(self):
		# recorrido en preorden para  declarar conexiones en archivo .gv
		
		s = "node" +str(self.number) + "[label=<<TABLE BORDER=\"0\" CELLBORDER=\"1\" CELLSPACING=\"0\"> \
			<TR><TD>"+str(self.firstpos)+"</TD><TD>  "+self.value+"  </TD><TD>"+str(self.lastpos)+"</TD></TR> \
			</TABLE>>];"
		Node.a_gx += s
		
		if not self.leaf:
			if not self.one:
				if self.left_child:
					
					s = "	node" + str(self.number) + " -> " + "node" + str(self.left_child.number) + "[dir=none]" + "\n"
					Node.a_gx2 += s
					self.left_child.conexiones()
				if self.right_child:
					
					s = "	node" + str(self.number) + " -> " + "node" + str(self.right_child.number) + "[dir=none]" +  "\n"
					Node.a_gx2 += s
					self.right_child.conexiones()
			else:
				if self.left_child:
					
					s = "	node" + str(self.number) + " -> " + "node" + str(self.left_child.number) + "[dir=none]" + "\n"
					Node.a_gx2 += s
					self.left_child.conexiones()
	

class RegularExpresion(object):
	
	def __init__(self, regexp):
        #agrega hashtag y pone puntos en las concatenaciones
		self.infix = separar_por_puntos("(" + regexp + ")#") 
        #convierte de infijo a postfijo
		self.postfix = infix_to_postfix(self.infix) 

	

	def regex_to_syntaxTree(self):
		# convierte expresion regular a syntax tree
		stack = []
		postfix = infix_to_postfix(self.infix)
		for s in postfix:
			
			if s == '*':
                #saca el ultimo dato de la lista 
				t = stack.pop() 
                #crea nodo con valor s y agrega t como único hijo
				stack.append(Node(s,center_child=t)) 
			elif s == '+':
                #saca el ultimo dato de la lista
				t = stack.pop() 
                #crea nodo con valor s y agrega t como único hijo
				stack.append(Node(s,center_child=t)) 
			elif s == '|':
                #saca ultimo dato de la lista
				right = stack.pop() 
                #saca penultimo dato de la lista
				left = stack.pop() 
                #crea nodo con valor s y agrega right como hijo derecho y left como hijo izquierdo
				stack.append(Node(s,one=False,right_child = right,left_child=left)) 
			elif s == '.':
                #saca ultimo dato de la lista
				right = stack.pop() 
                #saca penultimo dato de la lista
				left = stack.pop() 
                #crea nodo con valor s y agrega right como hijo derecho y left como hijo izquierdo
				stack.append(Node(s,one=False,right_child = right,left_child=left)) 
			else:
                #crea hoja, no agrega hijos al nodo 
				new_leaf = Node(s,leaf=True) 
				new_leaf.name = Node.namea_gx
				new_leaf.firstpos.append(new_leaf.name)
				new_leaf.lastpos.append(new_leaf.name)
				Node.namea_gx+=1
                #inserta al final de la lista
				stack.append(new_leaf) 
        #regresa el ultimo valor de la lista, que es el arbol final
		return stack.pop() 

	def write_graphviz(self,syntax_tree):
		# escribe el archivo .gv

		f= open("./output/arbol_sintactico.gv","w")
		f.write("digraph AFN{\n")
		f.write("rankdir=TB;\n    node[shape = plaintext] ;\n")
		f.write(Node.a_gx) 
		f.write(Node.a_gx2)
		f.write("\n}")
		f.close()
        #ejecuta comando para compilar gv y la salida es redirigida a una imagen .png
		os.system("dot -Tgif ./output/arbol_sintactico.gv > ./output/arbol_sintactico.png") 
		
		

class State(object):
	
	def __init__(self,values):
        #marked para saber si ya reviso 
		self.marked = False 
        #lista de valores del estado
		self.values = values 
        #diccionario de transisiones
		self.transitions = defaultdict(list) 

	def __str__(self):
		return "values: " + str(self.values) + "\ntransitions: " + str(list(self.transitions.items())) + "\n"

class AFD(object):
	def __init__(self,tree,dictionaryofpos,followpos):
        #lista de estados objetos tipo State
		self.states = [] 
        #arbol sintactico
		self.tree = tree 
        #diccionario {nombre = 'caracter'}
		self.dictionaryofpos = dictionaryofpos 
        #tabla de siguientes
		self.followpos = followpos 
        #estado inicial firstpos de la raiz del arbol
		self.initialState = State(tree.firstpos) 
        #agrega estado inicial a lista de estados
		self.states.append(self.initialState)
        #estado final nombre del hashtag
		self.final_state = max(list(dictionaryofpos.keys())) 

	def printTransitions(self):
		# Imprime las transiciones del AFD
		for s in self.states:
			print(str(s))

	def afd_graphviz(self):
		#escribe el archivo .gv
		dic = {}
		i = 1
		f= open("./output/afd.gv","w")
		f.write("digraph AFN{\n")
		f.write("rankdir=LR;\n    node[shape = circle] ;\n")
		f.write("nodeI [shape=point];\n")
		for s in self.states:
			n = "node"+str(i)
			dic[str(s.values)] = n
			if self.final_state not in s.values: 
				#si no es final
				f.write(n + "[label=\""+str(s.values)+"\"];\n")
			else:
				#si es final
				f.write(n + "[label=\""+str(s.values)+"\" shape=\"doublecircle\"];\n")
			i+=1
		f.write("nodeI -> node1 [label=I];\n")
		for s in self.states:
			for label, state in s.transitions.items():
				f.write(dic[str(s.values)]+"->"+dic[str(state)] + "[label = "+label+"];\n")
		f.write("\n}")
		f.close()
		os.system("dot -Tgif ./output/afd.gv > ./output/afd.png") 

	def lista_de_estados(self):
		#escribe lista de estados
		state_a_gx = []
		for s in self.states:
			state_a_gx.append(s.values)
		return state_a_gx

	def check_state(self):
		#verifica si el estado ya fue revisado
		r = True
		for s in self.states:
			if not s.marked:
				r = False
				break
			else:
				continue
		return r

	def get_unmarked_state(self):
		for s in self.states:
			if not s.marked:
				return s,self.states.index(s)

	def crearAFD(self):
		#crea automata y sus transiciones
		while(self.check_state() != True):
			print(self.check_state())
			current_states = self.lista_de_estados()
			state, i = self.get_unmarked_state()
			self.states[i].marked = True
			for v in state.values:
				if v == self.final_state:
					continue
				else:
					state.transitions[self.dictionaryofpos[v]] += self.followpos[v]
					state.transitions[self.dictionaryofpos[v]] = list(set(state.transitions[self.dictionaryofpos[v]]))
			print("Si")
			for ns in list(state.transitions.values()):
				if ns not in current_states:
					self.states.append(State(ns))
    

def arbol_sintactico(regexp):
	#crea arbol sintactico
	if "?" in regexp:
		regexp = regexp.replace("?","|e")
	re = RegularExpresion(regexp)
	tree = re.regex_to_syntaxTree()
	postorden(tree)
	firstpos(tree)
	followpos(tree)
	tree.conexiones()
	re.write_graphviz(tree)
	return tree
