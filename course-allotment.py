from ortools.sat.python import cp_model
import numpy as np
import random

model = cp_model.CpModel()

def compute_values(male_count,female_count):
    total_count = male_count+female_count
    y = (6-(total_count%6))%6 # no of 5 membered groups
    x = (male_count+female_count-5*y)/6 # no of 6 membered groups
    x1 = y # groups with 1 female and 4 males
    x2 = (5*female_count - male_count - y)/6 # 2 females 4 males
    x3 = x-x2 # 1 female 5 males
    return x1, x2, x3
    

num_projects = 6
student_count = 1325
female_count = 261
male_count = 1064

class Student:
    def __init__(self,rollnum,name,department,cpi,gender,preferences:list,groups):
        self.rollnum = rollnum
        self.name = name
        self.department = department
        self.cpi = cpi
        self.gender = gender # 0 if male, 1 if female (might add more later ;)
        self.preferences = [preferences[g.type] for g in groups]
        self.alpha = [model.new_bool_var(f"alpha_{self.rollnum}_{i}") for i in range(len(groups))]
        self.beta = [model.new_bool_var(f"beta_{self.rollnum}_{i}") for i in range(num_projects)]
        
        
class Project:
    def __init__(self,id,type,male_count,female_count):
        self.id = id # serial number
        self.type = type
        self.male_count = male_count
        self.female_count = female_count
        # self.average_cpi =   
    
    def __str__(self):
        return f"project type: {self.type}\ngroup id: {self.id}"     

def generate_nodes(x1, x2, x3):
    groups = []
    id=0
    for i in range(x1):
        groups.append(Project(id,i%num_projects,4,1))
        id+=1
    for i in range(x2):
        groups.append(Project(id,i%num_projects,4,2))
        id+=1
    for i in range(x3):
        groups.append(Project(id,i%num_projects,5,1))
        id+=1
    return groups
        
# take input of students

# toy dataset for now
cpi = [random.randint(700, 1000) for _ in range(student_count)]
rollnum = range(0,student_count)
gender = [1]*female_count + [0]*male_count
random.shuffle(gender)
department = [0]*student_count
preferences = [[random.randint(0, 100) for _ in range(num_projects)] for _ in range(student_count)]
x1,x2,x3 = compute_values(male_count,female_count)
groups = generate_nodes(int(x1),int(x2),int(x3))
students = []

for i in range(student_count):
    students.append(Student(rollnum[i], "John Doe", department[i], cpi[i], gender[i], preferences[i], groups))

median_cpi = int(np.median(cpi))

for student in students:
    model.add(sum(alpha for alpha in student.alpha) == 1)
    model.add(sum(beta for beta in student.beta) == 1)
    for i in range(num_projects):
        model.add(sum(student.alpha[id] for id in range(i, len(groups), num_projects)) == student.beta[i])
    
abs_cpi = []
    
for g in groups:
    model.add(sum(student.alpha[g.id] if student.gender == 0 else 0*student.alpha[g.id] for student in students) == g.male_count)
    model.add(sum(student.alpha[g.id] if student.gender == 1 else 0*student.alpha[g.id] for student in students) == g.female_count)
    abs_cpi.append(model.new_int_var(0,1000,f"abs_cpi_{i}"))
    model.add(sum(student.alpha[g.id]*(student.cpi - median_cpi) for student in students) <= (g.male_count+g.female_count)*abs_cpi[-1])
    model.add(sum(student.alpha[g.id]*(student.cpi - median_cpi) for student in students) >= -(g.male_count+g.female_count)*abs_cpi[-1])

    
model.maximize(sum(student.beta[i]*student.preferences[i] for student in students for i in range(num_projects))
               - sum(cpi_diff_from_median for cpi_diff_from_median in abs_cpi))
    
print(students[0].alpha[0])


solver = cp_model.CpSolver()
solver.solve(model)

def find_active_boolvar(solver, bool_vars):
    for i, var in enumerate(bool_vars):
        if solver.Value(var) == 1:
            return i  # or return var.Name() if you want the variable name
        
for student in students:
    id = find_active_boolvar(solver, student.alpha)
    print(groups[id])


