#! /usr/bin/python3

import tkinter as tk
import struct as st
from tkinter import messagebox
from tkinter import filedialog

from tkinter_modules_liste import modules
from tkinter_modules_inst_liste import modules_inst

modules_models = modules_inst + modules

#   ==================== TK =========================

def rgb(r,g,b):
	return '#%02x%02x%02x' % (r,g,b)

class Entree(tk.Frame):
	def __init__(self, parent, A, val_ini, *args, **kwargs):
		tk.Frame.__init__(self, parent, *args, **kwargs)
		self.l = tk.Label(self, text=A)
		self.val = tk.StringVar()
		self.val.set(val_ini)
		self.e = tk.Entry(self, textvariable=self.val, width=8)
		#
		self.l.grid(row=0,column=0)
		self.e.grid(row=0,column=1)

class DraggableFrame(tk.Frame):
	def __init__(self, parent, x, y, module, numero, *args, **kwargs):
		tk.Frame.__init__(self, parent.canvas, *args, **kwargs)
		self.parent = parent
		self.bind("<Button-1>",  self.on_drag_start)
		self.bind("<B1-Motion>", self.on_drag_motion)
		self.place(x=x, y=y)
		#	---
		self.module = module
		#   ---
		self.numero = numero
		tk.Label(self, text=module.nom + f'  #{numero}').grid(row=0, column=0, columnspan=3)
		#	---------
		tk.Button(self, text="X", fg='red', command=self.suppr_la_frame).grid(row=0, column=4)
		#   --- X ---
		#self.xs = [Entree(self, f'X{i}', x) for i,x in enumerate(module.X)]
		self.ps = [Entree(self, f'{nom}', p) for i,(nom,p) in enumerate(module.params.items())]
		#self.ys = [Entree(self, f'Y{i}', y) for i,y in enumerate(module.Y)]

		self.xs = []
		for i,x in enumerate(module.X):
			self.xs += [Entree(self, f'X{i}', x)]
			tk.Button(self, text='.', command=lambda _x=i:self.sel_B(_x)).grid (row=1+i, column=0)
			self.xs[-1].grid                                                   (row=1+i, column=1)
		#
		for i,p in enumerate(self.ps): p.grid                                  (row=1+i, column=2)
		#
		self.ys = []
		for i,y in enumerate(module.Y):
			self.ys += [Entree(self, f'Y{i}', y)]
			self.ys[-1].grid                                                  (row=1+i, column=3)
			tk.Button(self, text='.', command=lambda _y=i:self.sel_A(_y)).grid(row=1+i, column=4)

	def sel_A(self, _y):
		self.parent.instA.set  (str(self.numero))
		self.parent.sortieA.set(str(     _y    ))
	
	def sel_B(self, _x):
		self.parent.instB.set  (str(self.numero))
		self.parent.entréeB.set(str(     _x    ))

	def suppr_la_frame(self):
		pass
	
	def on_drag_start(self, event):
		self._drag_start_x = event.x
		self._drag_start_y = event.y
	
	def on_drag_motion(self, event):
		delta_x = event.x - self._drag_start_x
		delta_y = event.y - self._drag_start_y
		new_x = self.winfo_x() + delta_x
		new_y = self.winfo_y() + delta_y
		#
		self.place(x=new_x, y=new_y)
		self.parent.canvas.update_lines()  # Update lines through parent canvas

class LineCanvas(tk.Canvas):
	def __init__(self, parent, *args, **kwargs):
		tk.Canvas.__init__(self, parent, *args, **kwargs)
		self.parent = parent
		self.lignes = []
		self.textes = []

		self.connections = [
			# (instA,sortieA), (instB,entreeB)
		]

	def B_a_déjà_cette_entrée_assignée(self, A, B):
		for (iA,sA), (iB,eB) in self.connections:
			if B[0] == iB:
				if eB == B[1]:
					return True
		return False

	def ajouter_connections(self, A, B):
		if len(A) == len(B) == 2:
			if (A[0] in self.parent.numeros() and B[0] in self.parent.numeros()):
				if (A[1] < len(self.parent.trouver_frame(A[0]).ys) and B[1] < len(self.parent.trouver_frame(B[0]).xs)):
					if not (A,B) in self.connections:
						if not self.B_a_déjà_cette_entrée_assignée(A, B):
							self.connections += [(A,B)]
						else:
							messagebox.showwarning("Attention", f"{B[0]} a déjà son entrée {B[1]} assignée")
					else:
						messagebox.showwarning("Attention", f"La connection {A[0]}.{A[1]} -> {B[0]}.{B[1]} existe déjà")
				else:
					messagebox.showwarning("Attention", f"A ou B n'a pas d'entree ou de sortie {A[1]} ou {B[1]}")
			else:
				messagebox.showwarning("Attention", f"A:{A[0]} et/ou B:{B[0]} n'existe pas")
		else:
			messagebox.showwarning("Attention", f"La connection A={A} B={B} est invalide")

		self.update_lines()
	
	def add_line(self, depart, fin):
		ligne = self.create_line(depart[0], depart[1], fin[0], fin[1], width=2, arrow=tk.LAST)
		texte = self.create_text(
			depart[0] + (fin[0]-depart[0])/2,
			depart[1] + (fin[1]-depart[1])/2,
			text = f'#{len(self.lignes)}',
			anchor="nw")
		self.lignes += [ligne] #gc()
		self.textes += [texte] #gc()
	
	def update_lines(self):
		self.delete("all")
		#
		self.lignes      = []
		#self.connections = []
		"""for f1 in self.parent.frames:
			for f2 in self.parent.frames:
				if f1!=f2:
					for i,_ in enumerate(f1.ys):
						for j,_ in enumerate(f2.xs):
							self.connections += [((f1.numero,i), (f2.numero,j))]"""
		#
		for (instA, sortieA), (instB,entreeB) in self.connections:
			frameA, frameB = self.parent.trouver_frame(instA), self.parent.trouver_frame(instB)
			"""Ax = frame1.winfo_rootx() + frame1.winfo_width () // 2 - self.winfo_rootx()
			Ay = frame1.winfo_rooty() + frame1.winfo_height() // 2 - self.winfo_rooty()
			Bx = frame2.winfo_rootx() + frame2.winfo_width () // 2 - self.winfo_rootx()
			By = frame2.winfo_rooty() + frame2.winfo_height() // 2 - self.winfo_rooty()"""
			#
			Xa = frameA.winfo_width ()
			Ya = frameA.winfo_height()
			Xb = frameB.winfo_width ()
			Yb = frameB.winfo_height()
			#
			Ax, Ay = frameA.winfo_x(), frameA.winfo_y()
			Bx, By = frameB.winfo_x(), frameB.winfo_y()
			#
			depart = [Ax+Xa, Ay+40+sortieA*25]
			fin    = [Bx,    By+40+entreeB*25]
			#
			#	Ajouter un léger décalage
			depart[0] += 10
			fin   [0] -= 10
			#
			self.add_line(depart, fin)

class DraggableApp(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.geometry("1800x1120")

		self.frames = []
		self.canvas = LineCanvas(
			self,
			width=1620, height=1110,
			scrollregion=(0, 0, 1900, 2000),
			bg=rgb(240,240,240),
		)

		self.canvas.grid(row=0, column=0)

		####################### Partie Bouttons ########################
		
		self.frame_boutons = tk.LabelFrame(self, text='Bouttons')
		self.frame_boutons.grid(row=0, column=1, sticky="ns")

		#	----------------------
		ajout_module = tk.LabelFrame(self.frame_boutons, text='Ajouter Modules')
		for m in modules_models:
			tk.Button(ajout_module, text=f'Module<{m.nom}>', command=lambda _m=m:self.add_frame(_m())).pack()
		ajout_module.pack(fill=tk.Y, expand=True)

		self.prochain_numero_a_donner = 0

		#	-------------------------

		# Create a frame for arrow buttons
		self.fleches_frame = tk.LabelFrame(self.frame_boutons, text='Deplacement')
		self.fleches_frame.pack(fill=tk.Y, expand=True)

		# Load arrow images
		arrow_up_img    = tk.PhotoImage(file="arrow_up.png"   )
		arrow_down_img  = tk.PhotoImage(file="arrow_down.png" )
		arrow_left_img  = tk.PhotoImage(file="arrow_left.png" )
		arrow_right_img = tk.PhotoImage(file="arrow_right.png")

		# Create arrow buttons
		move_up_btn    = tk.Button(self.fleches_frame, image=arrow_up_img,    command=self.move_objects_up   )
		move_up_btn.grid   (row=0, column=1)
		move_down_btn  = tk.Button(self.fleches_frame, image=arrow_down_img,  command=self.move_objects_down )
		move_down_btn.grid (row=2, column=1)
		move_left_btn  = tk.Button(self.fleches_frame, image=arrow_left_img,  command=self.move_objects_left )
		move_left_btn.grid (row=1, column=0)
		move_right_btn = tk.Button(self.fleches_frame, image=arrow_right_img, command=self.move_objects_right)
		move_right_btn.grid(row=1, column=2)

		# Keep reference to the images to prevent garbage collection
		self.arrow_images = [arrow_up_img, arrow_down_img, arrow_left_img, arrow_right_img]

		# Keep references to the buttons
		self.arrow_buttons = [move_up_btn, move_down_btn, move_left_btn, move_right_btn]

		#	---------- Ajout de Connections -----------
		conn_frame = tk.LabelFrame(self.frame_boutons, text='Connections')

		tk.Label(conn_frame, text='Inst ').grid(row=0, column=1)
		tk.Label(conn_frame, text='Point').grid(row=0, column=2)
		tk.Label(conn_frame, text='A'    ).grid(row=1, column=0)
		tk.Label(conn_frame, text='B'    ).grid(row=2, column=0)

		self.instA = tk.StringVar(); self.sortieA = tk.StringVar();
		self.instB = tk.StringVar(); self.entréeB = tk.StringVar();
		self.instA.set('0');         self.sortieA.set('0');
		self.instB.set('0');         self.entréeB.set('0');
		self.e_instA   = tk.Entry(conn_frame, textvariable=self.instA,   width=8)
		self.e_instB   = tk.Entry(conn_frame, textvariable=self.instB,   width=8)
		self.e_sortieA = tk.Entry(conn_frame, textvariable=self.sortieA, width=8)
		self.e_entréeB = tk.Entry(conn_frame, textvariable=self.entréeB, width=8)
		self.e_instA.grid  (row=1,column=1)
		self.e_instB.grid  (row=2,column=1)
		self.e_sortieA.grid(row=1,column=2)
		self.e_entréeB.grid(row=2,column=2)

		tk.Button(conn_frame, text="+", fg=rgb(0,128,0), command=self.ajouter_une_connection  ).grid(row=3, column=1)
		tk.Button(conn_frame, text="x", fg=rgb(255,0,0), command=self.supprimer_une_connection).grid(row=3, column=2)
		conn_frame.pack(fill=tk.Y, expand=True)

		#	-------------------- Ordre Connections --------------

		ordre_frame = tk.LabelFrame(self.frame_boutons, text='Modifier Ordre Insts')

		self.ordre_de = Entree(ordre_frame, '#', '0')
		self.ordre_a  = Entree(ordre_frame, '#', '0')

		self.ordre_de.grid(row=0,column=0)
		tk.Label(ordre_frame, text='->').grid(row=0,column=1)
		self.ordre_a.grid(row=0,column=2)
		tk.Button(ordre_frame, text='Changer Ordre', command=self.changer_ordre).grid(row=1,column=0,columnspan=2)

		ordre_frame.pack(fill=tk.Y, expand=True)

		#	-------------- Fichier Enregistrer / Ouvire -----------------

		eo = tk.LabelFrame(self.frame_boutons, text='Sauvgarde & Ouverture')

		tk.Button(eo, text="Enregistrer", fg='blue',   command=self.sauvgarder).grid(row=0, column=0, sticky="nsew")
		tk.Button(eo, text="Ouvrire",     fg='yellow', command=self.ouvrire   ).grid(row=1, column=0, sticky="nsew")

		self.bind('<Control-s>', self.sauvgarder)
		self.bind('<Control-o>', self.ouvrire   )

		tk.Button(eo, text="Module -> Mdl_t", command=self.module_vers_mdl).grid(row=2, column=0)

		eo.pack(fill=tk.Y, expand=True)

	def changer_ordre(self):
		de = int(self.ordre_de.val.get())
		a  = int(self.ordre_a.val.get())

		l = self.canvas.connections

		l = l[:a] + [l[de]] + l[:de] + l[de+1:]

		self.canvas.connections = l

		self.canvas.update_lines()

	def ajouter_une_connection(self):
		iA, sA = int(self.instA.get()), int(self.sortieA.get())
		iB, eB = int(self.instB.get()), int(self.entréeB.get())
		self.canvas.ajouter_connections((iA,sA), (iB, eB))

	def supprimer_une_connection(self):
		iA, sA = int(self.instA.get()), int(self.sortieA.get())
		iB, eB = int(self.instB.get()), int(self.entréeB.get())
		if ((iA,sA), (iB,eB)) in self.canvas.connections:
			del self.canvas.connections[self.canvas.connections.index(((iA,sA), (iB,eB)))]
			self.canvas.update_lines()
		else:
			messagebox.showwarning('Attention', f"Il n'existe pas de connection iA={iA} sA={sA} iB={iB} eB={eB}")

	def trouver_frame(self, numero):
		for f in self.frames:
			if f.numero == numero:
				return f
		raise Exception(f"Pas trouvé le numéro {numero}")

	def numeros(self):
		return [f.numero for f in self.frames]

	def add_frame(self, module, x=0, y=0):
		frame = DraggableFrame(self, x, y, module, self.prochain_numero_a_donner, 
			width=100, height=135, bg=rgb(255,255,255))
		frame.pack_propagate(0)
		self.frames.append(frame)
		self.canvas.update_lines()
		#
		self.prochain_numero_a_donner += 1

	def move_objects_up(self):
		for frame in self.frames:
			frame.place_configure(y=frame.winfo_y() - -400)
		self.canvas.update()
		self.canvas.update_lines()

	def move_objects_down(self):
		for frame in self.frames:
			frame.place_configure(y=frame.winfo_y() + -400)
		self.canvas.update()
		self.canvas.update_lines()

	def move_objects_left(self):
		for frame in self.frames:
			frame.place_configure(x=frame.winfo_x() - -400)
		self.canvas.update()
		self.canvas.update_lines()

	def move_objects_right(self):
		for frame in self.frames:
			frame.place_configure(x=frame.winfo_x() + -400)
		self.canvas.update()
		self.canvas.update_lines()

	# ========================================================================

	def ouvrire(self, event=None):
		fichier = filedialog.askopenfilename()

	def sauvgarder(self, event=None):
		fichier = filedialog.asksaveasfilename()

	def module_vers_mdl(self):
		pass

if __name__ == "__main__":
	DraggableApp().mainloop()