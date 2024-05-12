class Inst:
	def __init__(self, X=[], Y=0, params=[]):
		self.X      = X
		self.Y      = Y
		self.params = params

	def assert_coherance(self):
		raise Exception("Doit etre implémenté")

class i_MatMul(Inst):
	i = 0
	nom = "x@P"
	params = []
	params_str = []
	Xs = [0]
	Y  =  0

	def assert_coherance(self):
		assert len(self.Xs) == 1
		assert self.Y > 0

		#	Params
		assert len(self.params) == 0

class i_Biais(Inst):
	nom = "+b"
	params = []
	params_str = []
	Xs = []
	Y  =  0

	def assert_coherance(self):
		assert len(self.Xs) == 0
		assert self.Y > 0

		#	Params
		assert len(self.params) == 0

class i_Somme2(Inst):
	nom = "A+B"
	params = []
	params_str = []
	Xs = [0,0]
	Y  =  0

	def assert_coherance(self):
		assert len(self.Xs) == 2
		assert self.Y == self.Xs[0] == self.Xs[1]

		#	Params
		assert len(self.params) == 0

class i_Somme3(Inst):
	nom = "A+B+C"
	params = []
	params_str = []
	Xs = [0,0,0]
	Y  =  0

	def assert_coherance(self):
		assert len(self.Xs) == 3
		assert self.Y == self.Xs[0] == self.Xs[1] == self.Xs[2]

		#	Params
		assert len(self.params) == 0

class i_Mul2(Inst):
	nom = "A*B"
	params = []
	params_str = []
	Xs = [0,0]
	Y  =  0

	def assert_coherance(self):
		assert len(self.Xs) == 2
		assert self.Y == self.Xs[0] == self.Xs[1]

		#	Params
		assert len(self.params) == 0

class i_Activation(Inst):
	nom = "activ(x)"
	params = [0]
	params_str = ['activation']
	Xs = [0]
	Y  =  0

	def assert_coherance(self):
		assert len(self.Xs) == 1
		assert self.Xs[0] == self.Y

		#	Params
		assert len(self.params) == 1
		#       tanh, logistic, gauss, relu
		activs = (0,     1,       2,     3)
		assert self.params[0] in activs