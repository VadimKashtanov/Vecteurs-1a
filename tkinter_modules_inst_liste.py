from tkinter_mdl import Module_Mdl

from tkinter_insts import i_MatMul, i_Biais, i_Somme2, i_Somme3, i_Mul2, i_Activation

insts = [i_MatMul, i_Biais, i_Somme2, i_Somme3, i_Mul2, i_Activation]

conn = lambda sortie,inst,entree: (sortie, (inst,entree))

modules_inst = []

for i in insts:
	nom_classe = str(i).split("'")[1].split('.')[1]
	s = f"""
class MODULE_{nom_classe}(Module_Mdl):	#	A+B
	nom = "inst:{i.nom}"
	X, Y = {i.Xs}, [0]
	params = {{
	"""
	for p in i.params_str:
		s += f"""
		'{p}' : 0,"""
	s += f"""
	}}
	def module_vers_model(self):
		#	Params
		Y     = self.Y[0]
		params = [p for _,p in self.params.items()]

		#	------------------

		self.ix = [
			{{'i':{nom_classe}, 'x':{[None for _ in i.Xs]}, 'y':[Y], 'p':params}},
		]

		#	---- Tres Important ----
		self.insts_et_connections(ix)

modules_inst += [MODULE_{nom_classe}]
"""
	exec(s)