def data_getter(path):
  import pandas as pd

  try: file = pd.read_excel(path)
  except: file = pd.read_csv(path, encoding= 'latin-1')

  course_info = file.fillna(value=0)
  course_copy = course_info
  for i, j in enumerate(course_info):
    if i > 3 : # Looping in Days
      start_l, end_l = list(), list()
      curr_lis = course_info[j]
      for p in curr_lis: # In each hour - hour
        if type(p) == type(str()): # Format
          divided = p.split('-')
          start = divided[0].split(':')
          end = divided[1].split(':')
          s_main, s_frac = int(start[0]), int(start[1])/60
          e_main, e_frac = int(end[0]), int(end[1])/60
          s_work, e_work = s_main + s_frac, e_main + e_frac 
          start_l.append(s_work); end_l.append(e_work)
        else:
          start_l.append(p); end_l.append(p)
      del course_copy[j]; course_copy[f'{j}_s'] = start_l; course_copy[f'{j}_e'] = end_l
  # --> Dictionary
  course_form = course_copy.set_index('ID').T
  course_data, avlbl_course = course_form.to_dict('list'), set(course_info['Asignatura'])
  return course_data, avlbl_course

if __name__ == '__main__':
  """
  openpyxl
  pandas
  numpy
  tkinter
  xlsxwriter
  """
  from tkinter import filedialog
  ret = filedialog.askopenfilename()
  m, n = data_getter(ret)
  for i, k in m.items():
    print(i,':',k)
