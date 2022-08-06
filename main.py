class Show:
  def __init__(self, master):
    import tkinter as tk
    from tkinter import filedialog
    self.master = master
    self.frame = tk.Frame(self.master, bg= "white")
    self.frame.place(x= 0, y= 0, relwidth=1, relheight=1)

    self.blue_b = tk.PhotoImage( file= './assets/blue_box.png')
    self.golden_b = tk.PhotoImage(file= './assets/golden_box.png')
    self.logo = tk.PhotoImage(file= './assets/fes-a.png')
    
    self.title_name = tk.Canvas(self.frame, bd= 0, bg= 'white', highlightthickness= 0, relief= 'flat', height= 600, width= 1000,)
    self.title_name.create_text(400, 70, font=('Montserrat',28), text= "Schedule Fitter - ⊂(◉‿◉)つ")
    self.title_name.place(x= 0, y= 0 )

    self.open_file = tk.Button(self.frame, text= 'Open File',image = self.blue_b, bd=0, bg= 'white', highlightthickness= 0, relief= 'flat', command= self.open_f)
    self.save_file = tk.Button(self.frame, text= 'Save As',image = self.golden_b, bd=0, bg= 'white', highlightthickness= 0, relief= 'flat', command= self.generate)
    self.open_file.place(
      relx= 153.6/1000, rely= 200.64/600,
      relwidth= 258.24/1000, relheight= 63.36/600)
    
    self.label = tk.Label(self.frame, image= self.logo, bg= 'white')
    self.label.place(relx=868.8/1000, rely=463.68/600, relheight=93.12/600, relwidth=79.68/1000)
  
  def open_f(self):
    self.ret = filedialog.askopenfilename()
    try:
      self.semestre, self.avlb_courses = dr.data_getter(self.ret)
      self.title_name.delete('baddie')
    except:
      self.title_name.create_text(315, 280, font=('Montserrat',14), text= "Not a valid file. Only .xlsx and .csv", tag= 'baddie')
      #self.title_name.delete('goodie')
    else:
      self.title_name.create_text(220, 280, font=('Montserrat',14), text= "Data retrieved", tag= 'goodie')
      self.title_name.create_text(830, 70, font=('Montserrat',14), text= "Courses", tag= 'goodie')
      self.open_file.config(state='disabled')
      self.save_file.place(
      relx= 153.6/1000, rely= 349.44/600,
      relwidth= 258.24/1000, relheight= 63.36/600)
      self.materias_list = list()
      for h, i in enumerate(self.avlb_courses):
        self.materias_list.append(tk.StringVar())
        materia_check = tk.Checkbutton(self.frame, text= i, font= ('Montserrat',8), onvalue= i, bg= 'white',bd= 0, anchor='w', variable= self.materias_list[h])
        self.materias_list[h].set(0)
        materia_check.place(x= 700, y= 100 + 20*h, width= 300, height= 20)
    return 0

  def generate(self):
    self.new_materias = set()
    for i in self.materias_list:
      self.new_materias.add(i.get())
    self.new_materias = list(self.new_materias)
    try: self.new_materias.remove('0')
    except: pass
    
    import schedule_fitter as sf
    try: 
      sf.main(self.new_materias, self.ret)
      self.title_name.create_text(190, 420, font=('Montserrat',14), text= "Success", tag= 'ohyeah')
    except:
      self.title_name.create_text(190, 420, font=('Montserrat',14), text= "Error", tag= 'ohnoah')
    return 0

if __name__ == '__main__':
  import tkinter as tk, numpy as np, random as rnd, data_reader as dr
  from tkinter import filedialog
  root = tk.Tk()
  root.title("Schedule Fitter - ( ͡° ͜ʖ ͡°)")
  root.geometry("1000x600")
  root.iconbitmap('./assets/icono.ico')
  root.resizable(False, False)

  a = Show(root)

  root.mainloop()