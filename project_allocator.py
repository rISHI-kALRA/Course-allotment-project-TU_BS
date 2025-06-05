from ortools.sat.python import cp_model
import numpy as np
import pandas as pd
from pydantic import BaseModel, Field, constr, conint, confloat, StringConstraints
from typing import Literal, List, Annotated
from typing_extensions import Annotated
import random
from utils import Project, Group, Section, variableContainer

def projectAllocator(section:Section, numberOfProjects:int) -> list[Project]:

        model = section.model
        numberOfStudents = len(section.students)
        minNumberOfFemaleStudents = int((numberOfStudents//numberOfProjects) * 0.2)  # Assuming at least 20%
        # Constraints for project allocation
        for student_alphas in section.projectAlphas:
            model.add(sum(student_alphas) == 1)
         
        transpose = [[row[i] for row in section.projectAlphas] for i in range(numberOfProjects)]
        projectContainers=[]
        for projectId, alphas in enumerate(transpose):
             projectContainers.append(variableContainer(alphas,projectId))
        
        for project in projectContainers: #this project is of type variableContainer, dont confuse it with 'Project' class
            model.add(project.numberOfStudents() >= numberOfStudents//numberOfProjects)
            model.add(project.numberOfStudents() <= (numberOfStudents+numberOfProjects-1)//numberOfProjects)
      
        # Objective function to maximize the number of students in their preferred projects
        #ToDo: Edit the objective function to include more things
        scaled_median_cpi = int(100*np.median([student.cpi for student in section.students])) #check
        abs_cpi = []
        

        for projectId,project in enumerate(projectContainers):
             model.add(project.femaleSum()>= minNumberOfFemaleStudents)
             abs_cpi.append(model.new_int_var(0,10000,f"abs_cpi_{projectId}")) #check
             model.add(project.cpiSumScaled() - project.numberOfStudents()*scaled_median_cpi <= abs_cpi[projectId])
             model.add(project.cpiSumScaled() - project.numberOfStudents()*scaled_median_cpi >= -1*abs_cpi[projectId])

        
        model.maximize(1000*sum(project.preferencesSum() for project in projectContainers)
                        - sum(cpi_diff_from_median for cpi_diff_from_median in abs_cpi))

        solver = cp_model.CpSolver()
        if solver.solve(model) == 3:
            print("No solution found for project allocation.")
            print(f"Number of students: {numberOfStudents}, Number of projects: {numberOfProjects}, Section: {section}")
            print(minNumberOfFemaleStudents)
        projects = []

        for projectContainer in projectContainers:
            projects.append(Project(projectCode=projectContainer.id, section=section, students=projectContainer.getAllocation(solver)))
        return projects