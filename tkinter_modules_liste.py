from tkinter_mdl import Module_Mdl

from tkinter_insts import i_MatMul, i_Biais, i_Somme2, i_Somme3, i_Mul2, i_Activation

conn = lambda sortie,inst,entree: (sortie, (inst,entree))

class DOT1D(Module_Mdl):	#	f(ax+b)
	nom = "DOT1D : f(AX+B)"
	X, Y = [0], [0]
	params = {
		'activation' : 0
	}
	def module_vers_model(self):
		#	Params
		activ = self.params['activation']
		X     = self.X[0]
		Y     = self.Y[0]

		#	------------------

		self.ix = [
			 ax :={'i':i_MatMul    , 'x':[None], 'y':[Y], 'p':[]},
			   b:={'i':i_Biais     , 'x':[]    , 'y':[Y], 'p':[]},
			 axb:={'i':i_Somme2    , 'x':[ax,b], 'y':[Y], 'p':[]},
			faxb:={'i':i_Activation, 'x':[axb] , 'y':[Y], 'p':[activ]}
		]

		#	---- Tres Important ----
		self.insts_et_connections(ix)

modules = [DOT1D]