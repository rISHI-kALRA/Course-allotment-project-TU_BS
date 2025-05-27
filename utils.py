from ortools.sat.python import cp_model
import numpy as np
import pandas as pd
from pydantic import BaseModel, Field, constr, conint, confloat, StringConstraints
from typing import Literal, List, Annotated
from typing_extensions import Annotated
import random

class Student(BaseModel):
    name: str
    gender: Literal['male', 'female']
    rollNumber: Annotated[str,StringConstraints(pattern=r"2\dB\d{4}")]
    cpi: confloat(ge=0.00, le=10.00)
    department: str
    preferences: List[conint(ge=0, le=100)]

class Project(BaseModel):
    projectCode: int
    section: int
    students: List[Annotated[str,StringConstraints(pattern=r"2\dB\d{4}")]]

class Group(BaseModel):
    id: int
    projectCode: int
    section: int
    students: List[Annotated[str,StringConstraints(pattern=r"2\dB\d{4}")]] # list of roll numbers of students
    
class CourseAllocator:
    def __init__(self, students: List[Student]):
        self.students = pd.DataFrame([s.dict() for s in students])
        self.rollToIndex = {roll: i for i, roll in enumerate(self.students['rollNumber'])}
        self.groups = []  # List to store allocated groups
    
    def allocate(self, numberOfSections: int, numberOfProjects: int, groupSize: int) -> List[Group]:
        sections = self.sectionDivider(numberOfSections)
        projects = []
        for i,section in enumerate(sections):
            projects.extend(self.projectAllocator(section, numberOfProjects,i))
        groups = []
        for project in projects:
            groups.extend(self.groupAllocator(project, groupSize))
        self.groups = groups

    def sectionDivider(self,numberOfSections:int) -> list[pd.DataFrame]: # Divides students into sections
        
        #Divide randomly for now, can be improved later to divide based on department or other criteria
        if numberOfSections <= 0:
            raise ValueError("Number of sections must be greater than 0")
        if numberOfSections > len(self.students):
            raise ValueError("Number of sections cannot be greater than number of students")
        shuffled_students = self.students.sample(frac=1).reset_index(drop=True)
        section_size = len(shuffled_students) // numberOfSections
        sections = []
        for i in range(numberOfSections):
            start_index = i * section_size
            end_index = (i + 1) * section_size if i < numberOfSections - 1 else len(shuffled_students)
            sections.append(shuffled_students.iloc[start_index:end_index])
        return sections

    def projectAllocator(self,df:pd.DataFrame, numberOfProjects, section:int) -> list[Project]:
        model = cp_model.CpModel()
        alphas = [[model.new_bool_var(f"alpha_{rollnum}_{i}") for i in range(numberOfProjects)] for rollnum in df['rollNumber']]
        alphas = np.array(alphas, dtype=object)
        numberOfStudents = len(df)
        minNumberOfFemaleStudents = int((numberOfStudents//numberOfProjects) * 0.2)  # Assuming at least 20%
        # Constraints for project allocation
        for i in range(numberOfStudents):
            model.add(sum(alphas[i]) == 1)
        for j in range(numberOfProjects):
            model.add(sum(alphas[:, j]) >= numberOfStudents // numberOfProjects)
        for j in range(numberOfProjects):
            model.add(sum(alphas[:, j]) <= (numberOfStudents + numberOfProjects - 1) // numberOfProjects)
        # Objective function to maximize the number of students in their preferred projects
        #ToDo: Edit the objective function to include more things
        median_cpi = int(df['cpi'].median()*100)
        abs_cpi = []
        
        for i in range(numberOfProjects):
            model.add(sum(alphas[j][i] if df['gender'].iloc[j]=='female' else 0*alphas[j][i] for j in range(numberOfStudents)) >= minNumberOfFemaleStudents)
            abs_cpi.append(model.new_int_var(0,10000000,f"abs_cpi_{i}"))
            model.add(sum((int(df['cpi'].iloc[j]*100) - median_cpi)* alphas[j][i] for j in range(numberOfStudents)) <= abs_cpi[i])
            model.add(sum((int(df['cpi'].iloc[j]*100) - median_cpi)* alphas[j][i] for j in range(numberOfStudents)) >= -1*abs_cpi[i])
            
        
        model.maximize(1000*sum(df['preferences'].iloc[i][j]*alphas[i][j] for i in range(numberOfStudents) for j in range(numberOfProjects))
                        - sum(cpi_diff_from_median for cpi_diff_from_median in abs_cpi))

        solver = cp_model.CpSolver()
        if solver.solve(model) == 3:
            print("No solution found for project allocation.")
            print(f"Number of students: {numberOfStudents}, Number of projects: {numberOfProjects}, Section: {section}")
            print(minNumberOfFemaleStudents)
        projects = []
        for j in range(numberOfProjects):
            project_students = [df['rollNumber'].iloc[i] for i in range(numberOfStudents) if solver.value(alphas[i][j]) > 0.5]
            projects.append(Project(projectCode=j, section=section, students=project_students))
        
        return projects

    def groupAllocator(self, project: Project, groupSize: int) -> List[Group]:
        model = cp_model.CpModel()
        numberOfStudents = len(project.students)
        numberOfGroups = numberOfStudents// groupSize
        student_vars = [[model.new_bool_var(f"student_{student}_{i}") for i in range(numberOfGroups)] for student in project.students]
        student_vars = np.array(student_vars, dtype=object)
        minNumberOfFemaleStudents = 1  # Assuming at least 1 lmao, can be adjusted later
        
        # Constraints for group allocation
        for i in range(numberOfStudents):
            model.add(sum(student_vars[i]) == 1)
        for j in range(numberOfGroups):
            model.add(sum(student_vars[:, j]) >= groupSize)
        if(numberOfStudents % groupSize <=numberOfGroups): 
            for j in range(numberOfGroups):
                model.add(sum(student_vars[:, j]) <= groupSize+1)  # Allow one group to have one extra student if necessary
        else:
            for j in range(numberOfGroups):
                model.add(sum(student_vars[:, j]) <= groupSize+2)  # Allow one group to have one extra student if necessary
            
        # Objective function: ToDo
        indices = [self.rollToIndex[roll] for roll in project.students]
        median_cpi = int(self.students.iloc[indices]['cpi'].median()*100)
        # print(median_cpi)
        abs_cpi = []
        
        for i in range(numberOfGroups):
            model.add(sum(student_vars[j][i] if self.students.iloc[indices[j]]['gender'] == 'female' else 0*student_vars[j][i] for j in range(numberOfStudents)) >= minNumberOfFemaleStudents)
            abs_cpi.append(model.new_int_var(0,10000000,f"abs_cpi_{i}"))
            model.add(sum((int(self.students.iloc[indices[j]]['cpi']*100) - median_cpi)* student_vars[j][i] for j in range(numberOfStudents)) <= abs_cpi[i])
            model.add(sum((int(self.students.iloc[indices[j]]['cpi']*100) - median_cpi)* student_vars[j][i] for j in range(numberOfStudents)) >= -1*abs_cpi[i])
        
        model.minimize(sum(cpi_diff_from_median for cpi_diff_from_median in abs_cpi))
        
        solver = cp_model.CpSolver()
        if solver.solve(model) == 3:
            print("No solution found for group allocation.")
        #     print(numberOfGroups)
        #     print(numberOfStudents)
        groups = []
        for j in range(numberOfGroups):
            group_students = [project.students[i] for i in range(numberOfStudents) if solver.value(student_vars[i][j]) > 0.5]
            groups.append(Group(id=j, projectCode=project.projectCode, section=project.section, students=group_students))
        return groups
        
    
    def getAllocation(self) -> pd.DataFrame:
        list=[]
        if not self.groups:
            raise ValueError("No groups allocated yet. Please run allocate() method first.")
        for group in self.groups:
            for student in group.students:
                list.append({'rollNumber': student, 'section': group.section, 'projectCode': group.projectCode, 'groupId': group.id})
        return pd.DataFrame(list)
    
    

    

# def groupAllocator(students:List[Student]):
    









































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