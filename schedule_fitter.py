import numpy as np, random as rnd
def schedule_matrices(semestre):
  matrices = dict()
  for i, j in semestre.items():
    week = [0]; week *= 6
    month = [week]; month *= (24*2)
    month = np.array(month)
    a = 2 * np.array(j[3:])

    lunes_dur, marte_dur, mierc_dur, jueve_dur, viern_dur, sabad_dur = int(a[1] - a[0]), int(a[3] - a[2]), int(a[5] - a[4]), int(a[7] - a[6]), int(a[9] - a[8]), int(a[11] - a[10])

    lunes_loc, marte_loc, mierc_loc, jueve_loc, viern_loc, sabad_loc = int(a[0]), int(a[2]), int(a[4]), int(a[6]), int(a[8]), int(a[10])

    for x, y in enumerate(month):# x [0,47]
      for p, q in enumerate(y): # p [0, 5]
        if p == 0 and lunes_dur != 0:
          if (lunes_loc-1+lunes_dur) >= x >= lunes_loc-1: y[p] = 1
        elif p == 1 and marte_dur != 0:
          if (marte_loc-1+marte_dur) >= x >= marte_loc-1: y[p] = 1
        elif p == 2 and mierc_dur != 0:
          if (mierc_loc-1+mierc_dur) >= x >= mierc_loc-1: y[p] = 1
        elif p == 3 and jueve_dur != 0:
          if (jueve_loc-1+jueve_dur) >= x >= jueve_loc-1: y[p] = 1
        elif p == 4 and viern_dur != 0:
          if (viern_loc-1+viern_dur) >= x >= viern_loc-1: y[p] = 1
        elif p == 5 and sabad_dur != 0:
          if (sabad_loc-1+sabad_dur) >= x >= sabad_loc-1: y[p] = 1
        else: continue
    matrices[i] = month
  return matrices

def combination_finder(courses, semester, courses_groups, matrices, group= None):
  month = np.zeros((48,6))
  group = list()
  for p, h in enumerate(courses):
    crr_subj_id = rnd.choice(courses_groups[p])
    month += matrices[crr_subj_id]
    group.append(crr_subj_id)
    for y, i in enumerate(month): # Overlap Check
      for x, j in enumerate(i):
        if j >= 2:
          if month[ y - 1 ,x] >= 2 or month[ y - 1 ,x] >= 2:
            return combination_finder(courses, semester, courses_groups, matrices) # if Overlap then Recursion 
          else: continue
        else: continue
  return group

def group_separator(courses, matrices, course_data): # Creates a list of the keys of each course
  subject_id = np.array(matrices.keys())
  subject_groups = [ [] for _ in range(len(courses)) ]
  for k, l  in course_data.items(): 
    for q, course in enumerate(courses):
      if l[1] == course:
        subject_groups[q].append(k)
        pass
  return subject_groups

def calc_sheet_gen(schdl_matrix, crs_data, solutions_set):
  zhou = [0]; zhou *= 6
  yue = [zhou]; yue *= (24*2)
  zhou_mingzi = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
  for i, matrix in schdl_matrix.items(): # Converts it to showable matrices
    for y, banxiaoshi in enumerate(matrix):
      for x, q in enumerate(banxiaoshi):
        if y != len(yue)-1:
          if matrix[ y + 1, x ] == 0 and q == 1:
            matrix[ y, x ] = 0

  import  xlsxwriter
  workbook = xlsxwriter.Workbook('./COMBINATION.xlsx')
  worksheet = workbook.add_worksheet('Combinaciones')
  cell_format, info_format = workbook.add_format(), workbook.add_format()
  cell_format.set_align('center')
  cell_format.set_align('vcenter')
  cell_format.set_font_name('Open Sans')
  cell_format.set_font_size(10)
  cell_format.set_border()
  cell_format.set_text_wrap()

  worksheet.set_column('C1:EB1', 22, cell_format); worksheet.write(0, 0, "Start", cell_format); worksheet.write(0, 1, "End", cell_format)
  counter = 0
  for h, i in enumerate(zhou_mingzi): # Format 
    worksheet.write(0, h+2, i, cell_format)
    worksheet.write(0, h+9, i, cell_format)
    worksheet.write(0, h+16, i, cell_format)
    worksheet.write(0, h+23, i, cell_format)
    worksheet.write(0, h+30, i, cell_format)
  for x, y in enumerate(yue):
    worksheet.set_row(x+1, 35, cell_format)
    if x % 2 == 0:
      worksheet.write(x+1, 0, f"{int(round(x/2, 0))}:00", cell_format)
      worksheet.write(x+1, 1, f"{int(round(x/2, 0))}:30", cell_format)
    else:
      if counter % 2 == 0:
        worksheet.write(x+1, 0, f"{int(round(x/2, 0))}:30", cell_format)
        worksheet.write(x+1, 1, f"{int(round(x/2, 0))+1}:00", cell_format)
      else:
        worksheet.write(x+1, 0, f"{int(round(x/2, 0))-1}:30", cell_format)
        worksheet.write(x+1, 1, f"{int(round(x/2, 0))}:00", cell_format)
      counter += 1

  colors = ['#7030A0','#CC04A1','#59E2FD','#62F493','#B0BD07','#FF7D2D','#BFBFBF','#D5A8D6','#FE4C4C','#93B3D1','#339933']
  colors_copy = colors

  formats = list()
  for k, solution in enumerate(solutions_set):
    offset = 7*k
    colors_copy = colors.copy()
    for h, i in enumerate(solution):
      # Tricks for colors
      color = rnd.choice(colors_copy)
      unique_format = workbook.add_format(); unique_format.set_align('center'); unique_format.set_align('vcenter'); unique_format.set_font_name('Open Sans'); unique_format.set_font_size(10); unique_format.set_border(); unique_format.set_text_wrap(); unique_format.set_bg_color(color)
      formats.append(unique_format) # Tricks for colors end

      matrix_zhouxiaoshi, ke_de_xinxi = schdl_matrix[i], crs_data[i]
      for row, xiaoshi in enumerate(matrix_zhouxiaoshi):
        for col, element in enumerate(xiaoshi):
          if element == 1:
            worksheet.write(row+2, col+2 + offset, f"{ke_de_xinxi[1].lower()}\n{ke_de_xinxi[0]}", formats[h])#\n{ke_de_xinxi[2]}")
          else: continue
      colors_copy.remove(color)
      if len(colors_copy) == 0: colors_copy = colors

  workbook.close()
  return 0

def main(materias, path):
  import numpy as np, random as rnd, data_reader as dr

  semestre, _ = dr.data_getter(path) # Parses data
  matrices = schedule_matrices(semestre) # Makes matrices for each course
  subject_groups = group_separator(materias, matrices, semestre) # Sorts by courses
  solutions_set = list()
  for _ in range(5):
    solutions_set.append(combination_finder(materias, semestre, subject_groups, matrices))
  calc_sheet_gen(matrices, semestre, solutions_set)

if __name__ == '__main__':
  #materias = ["ECUACIONES DIFERENCIALES","CIRCUITOS ELECTRICOS", "METROLOGIA DIMENSIONAL", "ADMINISTRACION", "CIENCIA DE LOS MATERIALES I", "ESTATICA"]
  """
  Si quieres meter las materias manualmente, solo escríbelas entre comillas y termínalas con una coma. Ejemplo:
  "Cáculo I",
  "Álgebra Lineal",
  "Carreteras",
  |
  |
  |
  v

  """
  materias = [
  "FLUIDMECH", 
  "DYNAMC"
  ]
  
  from tkinter import filedialog
  ret = filedialog.askopenfilename()
  main(materias,ret)
