from ortools.sat.python import cp_model
import numpy as np
import pandas as pd
from pydantic import BaseModel, Field, constr, conint, confloat, StringConstraints
from typing import Literal, List, Annotated
from typing_extensions import Annotated
import random
from utils import Student, Section


def sectionDivider(students: List[Student],numberOfSections:int) -> list[Section]: # Divides students into sections
    #Divide randomly for now, can be improved later to divide based on department or other criteria
    
    if numberOfSections <= 0:
        raise ValueError("Number of sections must be greater than 0")
    if numberOfSections > len(students):
        raise ValueError("Number of sections cannot be greater than number of students")
    shuffled_students = random.sample(students,k=len(students))
    sections = []
    section_size = len(shuffled_students)//numberOfSections
    for i in range(numberOfSections):
        start_index = i*section_size
        end_index = (i+1)*section_size if i<numberOfSections-1 else len(shuffled_students)
        sections.append(Section(section=i,students=shuffled_students[start_index:end_index]))
    return sections


