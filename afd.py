from collections import defaultdict
import os
from parseTree import infixToPostfix
from metodos import addAppend

def postorden(arbol):
	if not arbol.leaf:
		if arbol.one:
			postorden(arbol.left_child)
			if arbol.value == "*":
				arbol.nullable = True
			else:
				arbol.nullable = arbol.left_child.nullable 
		else:
			postorden(arbol.left_child)
			postorden(arbol.right_child)
			if arbol.value == "|":
				arbol.nullable = arbol.left_child.nullable or arbol.right_child.nullable
			elif arbol.value == ".":
				arbol.nullable = arbol.left_child.nullable and arbol.right_child.nullable
	else:
		arbol.nullable = False

def postorden_followpos(arbol):
	if not arbol.leaf:
		if arbol.one:
			postorden_followpos(arbol.left_child)
			for i in range(len(arbol.lastpos)):
				for j in range(len(arbol.firstpos)):
					Node.followpos[arbol.lastpos[i]].append(arbol.firstpos[j])
		else:
			postorden_followpos(arbol.left_child)
			postorden_followpos(arbol.right_child)
			if arbol.value == ".":
				for i in range(len(arbol.left_child.lastpos)):
					for j in range(len(arbol.right_child.firstpos)):
						Node.followpos[arbol.left_child.lastpos[i]].append(arbol.right_child.firstpos[j])

def postorden_firstpos(arbol):
	if not arbol.leaf:
		if arbol.one:
			postorden_firstpos(arbol.left_child)
			arbol.firstpos = arbol.left_child.firstpos
			arbol.lastpos = arbol.left_child.lastpos
		else:
			postorden_firstpos(arbol.left_child)
			postorden_firstpos(arbol.right_child)
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

def createDictionary(arbol):
	if not arbol.leaf:
		if arbol.one:
			createDictionary(arbol.left_child)
		else:
			createDictionary(arbol.left_child)
			createDictionary(arbol.right_child)
	else:
		Node.dictionaryofpos[arbol.name] = arbol.value
			
class Node(object):
	a_gx = "" 
	a_gx2 = "" 
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



	def preordenConection(self):		
		s = "node" +str(self.number) + "[label=<<TABLE BORDER=\"0\" CELLBORDER=\"1\" CELLSPACING=\"0\"> \
			<TR><TD>"+str(self.firstpos)+"</TD><TD>  "+self.value+"  </TD><TD>"+str(self.lastpos)+"</TD></TR> \
			</TABLE>>];"
		Node.a_gx += s
		
		if not self.leaf:
			if not self.one:
				if self.left_child:
					
					s = "	node" + str(self.number) + " -> " + "node" + str(self.left_child.number) + "[dir=none]" + "\n"
					Node.a_gx2 += s
					self.left_child.preordenConection()
				if self.right_child:
					
					s = "	node" + str(self.number) + " -> " + "node" + str(self.right_child.number) + "[dir=none]" +  "\n"
					Node.a_gx2 += s
					self.right_child.preordenConection()
			else:
				if self.left_child:
					
					s = "	node" + str(self.number) + " -> " + "node" + str(self.left_child.number) + "[dir=none]" + "\n"
					Node.a_gx2 += s
					self.left_child.preordenConection()
	

class RegularExpresion(object):
	
	def __init__(self, regexp):
		self.infix = addAppend("(" + regexp + ")#") 
		self.postfix = infixToPostfix(self.infix) 

	

	def re_to_syntaxTree(self):
		stack = []
		postfix = infixToPostfix(self.infix)
		for s in postfix:
			
			if s == '*':
				t = stack.pop() 
				stack.append(Node(s,center_child=t)) 
			elif s == '+':
				t = stack.pop() 
				stack.append(Node(s,center_child=t)) 
			elif s == '|':
				right = stack.pop() 
				left = stack.pop() 
				stack.append(Node(s,one=False,right_child = right,left_child=left)) 
			elif s == '.':
				right = stack.pop() 
				left = stack.pop() 
				stack.append(Node(s,one=False,right_child = right,left_child=left)) 
			else:
				new_leaf = Node(s,leaf=True) 
				new_leaf.name = Node.namea_gx
				new_leaf.firstpos.append(new_leaf.name)
				new_leaf.lastpos.append(new_leaf.name)
				Node.namea_gx+=1
				stack.append(new_leaf) 
		return stack.pop() 

	def write_graphviz(self,syntax_tree):
		f= open("./output/tree.gv","w")
		f.write("digraph AFN{\n")
		f.write("rankdir=TB;\n    node[shape = plaintext] ;\n")
		f.write(Node.a_gx) 
		f.write(Node.a_gx2)
		f.write("\n}")
		f.close()
		os.system("dot -Tgif ./output/tree.gv > ./output/tree.png") 
		
		

class State(object):
	def __init__(self,values):
		self.marked = False 
		self.values = values 
		self.transitions = defaultdict(list) 

	def __str__(self):
		return "values: " + str(self.values) + "\ntransitions: " + str(list(self.transitions.items())) + "\n"

class DFA(object):
	def __init__(self,tree,dictionaryofpos,followpos):
		self.states = [] 
		self.tree = tree 
		self.dictionaryofpos = dictionaryofpos 
		self.followpos = followpos 
		self.initialState = State(tree.firstpos) 
		self.states.append(self.initialState)
		self.final_state = max(list(dictionaryofpos.keys())) 

	def printTransitions(self):
		for s in self.states:
			print(str(s))

	def write_dfa_graphviz(self):
		dic = {}
		i = 1
		f= open("./DFA.gv","w")
		f.write("digraph AFN{\n")
		f.write("rankdir=LR;\n    node[shape = circle] ;\n")
		f.write("nodeI [shape=point];\n")
		for s in self.states:
			n = "node"+str(i)
			dic[str(s.values)] = n
			if self.final_state not in s.values: 
				f.write(n + "[label=\""+str(s.values)+"\"];\n")
			else:
				f.write(n + "[label=\""+str(s.values)+"\" shape=\"doublecircle\"];\n")
			i+=1
		f.write("nodeI -> node1 [label=I];\n")
		for s in self.states:
			for label, state in s.transitions.items():
				f.write(dic[str(s.values)]+"->"+dic[str(state)] + "[label = "+label+"];\n")
		f.write("\n}")
		f.close()
		os.system("dot -Tgif ./DFA.gv > ./DFA.png") 

	def list_of_states(self):
		state_a_gx = []
		for s in self.states:
			state_a_gx.append(s.values)
		return state_a_gx

	def check_mark(self):
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

	def createDFA(self):
		while(self.check_mark() != True):
			print(self.check_mark())
			current_states = self.list_of_states()
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
	if "?" in regexp:
		regexp = regexp.replace("?","|e")
	re = RegularExpresion(regexp)
	tree = re.re_to_syntaxTree()
	postorden(tree)
	postorden_firstpos(tree)
	postorden_followpos(tree)
	tree.preordenConection()
	re.write_graphviz(tree)
	return tree
