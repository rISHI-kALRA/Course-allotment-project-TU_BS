from ortools.sat.python import cp_model
import numpy as np
import pandas as pd
import random

class Student():
    def __init__(self):
        pass

class Group():
    def __init__(self):
        pass

def sectionDivider(df:pd.DataFrame, numberOfSections:int) -> list[pd.DataFrame]: # Divides students into sections
    pass

def projectAllocator(df:pd.DataFrame, numberOfProjects) -> list[Group]:
    
    pass









































# model = cp_model.CpModel()

# num_projects = 6
# student_count = 1325
# female_count = 261
# male_count = 1064

# def compute_values(male_count,female_count):
#     total_count = male_count+female_count
#     y = (6-(total_count%6))%6 # no of 5 membered groups
#     x = (male_count+female_count-5*y)/6 # no of 6 membered groups
#     x1 = y # groups with 1 female and 4 males
#     x2 = (5*female_count - male_count - y)/6 # 2 females 4 males
#     x3 = x-x2 # 1 female 5 males
#     return x1, x2, x3

# class Student:
#     def __init__(self,rollnum,name,department,cpi,gender,preferences:list,groups):
#         self.rollnum = rollnum
#         self.name = name
#         self.department = department
#         self.cpi = cpi
#         self.gender = gender # 0 if male, 1 if female (might add more later ;)
#         self.preferences = [preferences[g.type] for g in groups]
#         self.alpha = [model.new_bool_var(f"alpha_{self.rollnum}_{i}") for i in range(len(groups))]
#         self.beta = [model.new_bool_var(f"beta_{self.rollnum}_{i}") for i in range(num_projects)]
        
        
# class Project:
#     def __init__(self,id,type,male_count,female_count):
#         self.id = id # serial number
#         self.type = type
#         self.male_count = male_count
#         self.female_count = female_count
#         # self.average_cpi =   
    
#     def __str__(self):
#         return f"project type: {self.type}\ngroup id: {self.id}"     

# def generate_nodes(x1, x2, x3):
#     groups = []
#     id=0
#     for i in range(x1):
#         groups.append(Project(id,i%num_projects,4,1))
#         id+=1
#     for i in range(x2):
#         groups.append(Project(id,i%num_projects,4,2))
#         id+=1
#     for i in range(x3):
#         groups.append(Project(id,i%num_projects,5,1))
#         id+=1
#     return groups