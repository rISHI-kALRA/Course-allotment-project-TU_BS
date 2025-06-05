from ortools.sat.python import cp_model
import numpy as np
import pandas as pd
from pydantic import BaseModel, Field, constr, conint, confloat, StringConstraints
from typing import Literal, List, Annotated
from typing_extensions import Annotated
import random
from utils import Group, Project, variableContainer

def groupAllocator(project: Project, groupSize: int) -> List[Group]:
        model = project._model
        numberOfStudents = len(project.students)
        numberOfGroups = numberOfStudents// groupSize
        minNumberOfFemaleStudents = 1  # Assuming at least 1, can be adjusted later
        
        # Constraints for group allocation
        for student_alphas in project._groupAlphas:
            model.add(sum(student_alphas) == 1)

        transpose = [[row[i] for row in project._groupAlphas] for i in range(numberOfGroups)]
        groupContainers=[]
        for groupId, alphas in enumerate(transpose):
             groupContainers.append(variableContainer(alphas,groupId))


        for group in groupContainers: #this group is of type variableContainer, dont confuse it with 'Group' class
            model.add(group.numberOfStudents() >= groupSize)
           
        if(numberOfStudents % groupSize <=numberOfGroups):  #We are doing this to resolve an issue, which is: If suppose total 15 students in project and you want to divide them into groups, then it is not possible to divide them using only groups of size 6,7. We need atleast one group of size 8
            for group in groupContainers:
                model.add(group.numberOfStudents() <= groupSize+1)
        else:
            for group in groupContainers: 
                model.add(group.numberOfStudents() <= groupSize+3)  #Currently this simple trick is enough for solving, if still this doesnt solve the issue, then do something in future. 
            

        scaled_median_cpi = int(100*np.median([student.cpi for student in project.students])) #check
        abs_cpi = []

        for groupId,group in enumerate(groupContainers):
            #  model.add(group.femaleSum()>= minNumberOfFemaleStudents) #check, instead try to add objective as : maximise number of groups with atleast one female
             abs_cpi.append(model.new_int_var(0,10000,f"abs_cpi_{groupId}")) #check 10000 
             model.add(group.cpiSumScaled() - group.numberOfStudents()*scaled_median_cpi <= abs_cpi[groupId])
             model.add(group.cpiSumScaled() - group.numberOfStudents()*scaled_median_cpi >= -1*abs_cpi[groupId])
        
        model.minimize(sum(cpi_diff_from_median for cpi_diff_from_median in abs_cpi))
        
        solver = cp_model.CpSolver()
        status = solver.solve(model)
        if status == 3:
            print("No solution found for group allocation.")

        groups = []
        for groupContainer in groupContainers:
            groups.append(Group(groupId=groupContainer.id, projectCode=project.projectCode, section=project.section, students=groupContainer.getAllocation(solver)))

        return groups