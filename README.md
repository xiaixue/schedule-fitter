# Schedule Fitter


With this tool you will be able to generate combinations of your schedule with no overlap given a set of courses and your *to sign-up* courses.

---
## How to use it
Your data must be written in a readable format, preferable in a _.xlsx_ file, but a _.csv_ is fine too.
The format ought to follow the next template.
| ID  | Grupo | Asignatura          | Profesor | Lunes      | Martes      | Miércoles   | Jueves      | Viernes    | Sábado |
|-----|-------|---------------------|----------|------------|-------------|-------------|-------------|------------|--------|
| 1   | 2103  | Thermodynamics | John Doe | 9:00-11:00 |             | 9:00-11:00  |             | 9:00-11:00 |        |
| 2   | 2104  | Thermodynamics  | Doe John | 11:00-1:00 | 11:00-12:00 | 11:00-12:00 | 11:00-12:00 |            |        |
| ... | ...   | ...                 | ...      | ...        | ...         | ...         | ...         | ...        | ...    |
| 25  | 2109  | Statistics        | Doe John | 7:00-9:00  | 7:00-9:00   |             |             | 7:00-9:00  |        |

> The language matters, so don't change the headers otherwise, it won't work.

Run the `main.py` file, click **Choose File**, pick your data file, check the courses you want to have and click **Generate** and you will have and `Schedule.xlsx` file in the program's folder.

The are some ***dont's*** of the program, it was kinda express so...

* It does not generate the best fitting schedule necessarily, it only generates _5_ combinations. Run it several times if you want to check more combinations.
* Do not put too many different courses data or it will fill up the entire window. You can run it with any data you want directly in the console, though.
* If there is no possible combination, it will fail.

---
## How does it work

The program consists in making each course class times into matrices itself.

`data_getter` reads the data and passes it to a dictionary.

`schedule_matrices` from the dictionary, it creates a matrix for each key.

`group_separator` creates groups of the courses. Ex: Dynamics, Calculus, etc.

`calc_sheet_gen` generates the .xlsx to see the results.

`combination_finder` is the algorithm.

So for the Fluid Mechanics class by professor John Doe from 9 to 10 (Tuesday and Friday), it will be exist a matrix of *48x6* dimension. Each rows represents a set of 30 minutes and the columns are the days from Monday to Saturday.
So that will be:

$FluidMech=\begin{bmatrix}
0 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 \\
... & ... & ... & ... & ... & ... \\
0_{18,1} & 1 & 0_{18,3} & 0_{18,4} & 1 & 0_{18,6} \\  
0_{19,1} & 1 & 0_{19,3} & 0_{19,4} & 1 & 0_{19,6} \\
0_{20,1} & 1 & 0_{20,3} & 0_{20,4} & 1 & 0_{20,6} \\
... & ... & ... & ... & ... & ... \\
0 & 0 & 0 & 0 & 0 & 0 \\
\end{bmatrix}  $

Assume that other two classes are available:

$Dynamics_A=\begin{bmatrix}
0 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 \\
... & ... & ... & ... & ... & ... \\
1 & 0_{20,2} & 0_{20,3} & 0_{20,4} & 1 & 0_{20,6} \\  
1 & 0_{21,2} & 0_{21,3} & 0_{21,4} & 1 & 0_{21,6} \\
1 & 0_{22,2} & 0_{22,3} & 0_{22,4} & 1 & 0_{22,6} \\
... & ... & ... & ... & ... & ... \\
0 & 0 & 0 & 0 & 0 & 0 \\
\end{bmatrix}  $

$Dynamics_B=\begin{bmatrix}
0 & 0 & 0 & 0 & 0 & 0 \\
... & ... & ... & ... & ... & ... \\
0_{19,1} & 1 & 0_{19,3} & 1 & 0_{19,5} & 0_{19,6} \\  
0_{20,1} & 1 & 0_{20,3} & 1 & 0_{20,5} & 0_{20,6} \\
0_{21,1} & 1 & 0_{21,3} & 1 & 0_{21,5} & 0_{21,6} \\
... & ... & ... & ... & ... & ... \\
0 & 0 & 0 & 0 & 0 & 0 \\
\end{bmatrix}  $

You cannot have Fluid Mechanics along with Dynamics B due to $a_{(i+1)j} \ge 2 $ or $a_{(i-1)j} \ge 2 $ restriction. It means that there is an overlap.

$FluidMech+Dynamics_B=\begin{bmatrix}
0 & 0 & 0 & 0 & 0 & 0 \\
... & ... & ... & ... & ... & ... \\
0_{18,1} & 1 & 0_{18,3} & 0_{18,4} & 1 & 0_{18,6} \\  
0_{19,1} & \bold{2}_{19,2} & 0_{19,3} & 1 & 1 & 0_{19,6} \\ 
0_{20,1} & \bold{2}_{20,2} & 0_{20,3} & 1 & 1 & 0_{20,6} \\
0_{21,1} & 1 & 0_{21,3} & 1 & 0_{21,5} & 0_{21,6} \\
... & ... & ... & ... & ... & ... \\
0 & 0 & 0 & 0 & 0 & 0 \\
\end{bmatrix}  $

But you can have Fluid Mechanics with Dynamics A because $a_{(i+1)j} \le 1 $ and $a_{(i-1)j} \le 1 $. 

Having an $a_{ij} = 2$ while $a_{(i+1)j} \le 1 $ or $a_{(i-1)j} \le 1 $ means that there is a benign overlap, where one class finishes and the other commences.

$FluidMech+Dynamics_A=\begin{bmatrix}
0 & 0 & 0 & 0 & 0 & 0 \\
... & ... & ... & ... & ... & ... \\
0_{18,1} & 1 & 0_{18,3} & 0_{18,4} & 1 & 0_{18,6} \\  
0_{19,1} & 1 & 0_{19,3} & 0_{19,4} & 1 & 0_{19,6} \\
1 & 1 & 0_{20,3} & 0_{20,4} & \bold{2}_{20,5} & 0_{20,6} \\  
1 & 0_{21,2} & 0_{21,3} & 0_{21,4} & 1 & 0_{21,6} \\
1 & 0_{22,2} & 0_{22,3} & 0_{22,4} & 1 & 0_{22,6} \\
... & ... & ... & ... & ... & ... \\
0 & 0 & 0 & 0 & 0 & 0 \\
\end{bmatrix}  $

When a combination with no overlaps or only *benign* overlaps is found, the problem is solved.