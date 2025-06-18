from ortools.sat.python import cp_model
import numpy as np
import pandas as pd
from pydantic import BaseModel, Field, constr, conint, confloat, StringConstraints
from typing import Literal, List, Annotated
from typing_extensions import Annotated
import random
from utils import Project, Group, Section, variableContainer, absolute_value

def projectAllocator(section:Section, numberOfProjects:int) -> list[Project]:

        model = section._model #check, whether instantiation in Section class is ok or not, ask professor Dominic
        numberOfStudents = len(section.students)
        minNumberOfFemaleStudents = int((numberOfStudents//numberOfProjects) * 0.15)  # check, Assuming at least 15%
        # Constraints for project allocation
        for student_alphas in section._projectAlphas:
            model.add(sum(student_alphas) == 1)
         
        transpose = [[row[i] for row in section._projectAlphas] for i in range(numberOfProjects)]
        projectContainers=[]
        for projectId, alphas in enumerate(transpose):
             projectContainers.append(variableContainer(alphas,projectId))
        
        for project in projectContainers: #this project is of type variableContainer, dont confuse it with 'Project' class
            model.add(project.numberOfStudents() >= 6*((numberOfStudents//numberOfProjects)//6))
            model.add(project.numberOfStudents() <= 6*((numberOfStudents//numberOfProjects)//6)+6)  #check, this restriction of only allowing +1 range might fail to have a mathematical solution 

        projectsize_bools =[] #these represent whether project size is multiple of 6 or not
        for projectId, project in enumerate(projectContainers):
            projectsize_bools.append(model.new_bool_var(f'6multiple_{projectId}'))

            projectsize = model.new_int_var(0,200,f'projectCardinality_{projectId}') #integer version of the boolean sum: project.numOfStudents() so as to use for modulo
            model.add(projectsize==project.numberOfStudents())
            projectsize_remainder = model.new_int_var(0,10,f'remainder_{projectId}')
            model.add_modulo_equality(projectsize_remainder,projectsize,6)

            model.add(projectsize_remainder==0).only_enforce_if(projectsize_bools[-1])

        # Objective function to maximize the number of students in their preferred projects
        #ToDo: Edit the objective function to include more things
        scaled_median_cpi = int(100*np.median([student.cpi for student in section.students])) #check
        abs_cpi = []
        

        for projectId,project in enumerate(projectContainers):
            model.add(6*project.femaleSum()>= project.numberOfStudents()) #check
            abs_cpi.append(absolute_value(project.cpiSumScaled() - project.numberOfStudents()*scaled_median_cpi,model))

        
        model.maximize(1000*sum(project.preferencesSum() for project in projectContainers)
                        - sum(cpi_diff_from_median for cpi_diff_from_median in abs_cpi) + 10000*sum(projectsize_bools))

        solver = cp_model.CpSolver()
        status = solver.solve(model)
        if  status == 3:
            print("No solution found for project allocation.")
            print(f"Section: {section.section}, Number of students: {numberOfStudents}, Number of projects: {numberOfProjects}")
            female_count = 0
            for student in section.students:
                 if(student.gender=='female'):
                      female_count+=1
            print("Female count: ",female_count)
        projects = []

        for projectContainer in projectContainers:
            projects.append(Project(projectCode=projectContainer.id, section=section.section, students=projectContainer.getAllocation(solver)))
        return projects