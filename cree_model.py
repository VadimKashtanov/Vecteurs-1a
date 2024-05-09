#! /usr/bin/python3

import struct as st

class Inst:
	PARAMS = 0
	_str_params  = []
	params_choix = {}
	params       = []
	Xs = []
	Y  = 0

	def assert_coherance(self):
		pass

class i_MatMul(Inst):
	PARAMS = 0
	_str_params  = []
	params_choix = {}
	params       = []
	Xs = [0]
	Y  =  0

	def assert_coherance(self):
		assert len(self.Xs) == 0
		assert self.Y > 0
		assert len(self.params) = 0

class i_Activation(Inst):
	PARAMS = 0
	_str_params  = ['activation']
	params_choix = {'tanh':0, 'logistic':1, 'gauss':2, 'relu':3}
	params       = []
	Xs = [0]
	Y  =  0

	def assert_coherance(self):
		assert len(self.Xs) == 0
		assert self.Xs[0] == self.Y

class Mdl:
	def __init__(self, insts, connections):
		pass

class DraggableWidget:
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.bind("<Button-1>", self.on_drag_start)
        self.bind("<B1-Motion>", self.on_drag_motion)
        self.bind("<ButtonRelease-1>", self.on_drag_release)
        self.dragging = False

    def on_drag_start(self, event):
        self.dragging = True
        self.start_x = event.x
        self.start_y = event.y

    def on_drag_motion(self, event):
        if self.dragging:
            delta_x = event.x - self.start_x
            delta_y = event.y - self.start_y
            self.place(x=self.winfo_x() + delta_x, y=self.winfo_y() + delta_y)

    def on_drag_release(self, event):
        self.dragging = False

if __name__ == "__main__":
	pass