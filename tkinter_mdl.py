class Module_Mdl:
	def insts_et_connections(self, ix):
		self.insts       = [] # Inst()
		self.connections = [] # [(sortie,inst,entree)]
		self.entrées     = [] # [(inst,entree)]
		self.sorties     = [] # [inst]
		for d in ix:
			self.insts += [
				d['i'](
					X      = [(ix[_x]['y'] if x!=None else None) for x in d['x']],
					Y      = d['y'],
					params = d['p']
				)
			]
			self.insts[-1].assert_coherance()

			self.connections = [
				conn(sortie=ix.index(x),inst=ix.index(d),entree=i)
				for i,x in enumerate(d['x'])
					if x != None
			]

			for i,x in enumerate(d['x']):
				if x == None:
					self.entrées += [(ix.index(d), i)]

			est_utilisé_qlq_part = False
			for elm in ix:
				if d != elm:
					if d in elm['x']:
						est_utilisé_qlq_part = True
			
			if not est_utilisé_qlq_part:
				self.sorties += [ix.index(d)]

def unir_N_modules(modules, connections_inter_modulaires):
	for module in modules:
		print(f"Module {module}")
		for elm in modules.ix:
			print(elm)