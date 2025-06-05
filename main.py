
import random
import pandas as pd
from course_allocator import CourseAllocator
from utils import Student, Project, Group, no_of_projects, no_of_sections, groupSize

if __name__ == "__main__":

    ##Last year's DE 250 dataset
    student_df = pd.read_csv('students_data.csv')
    student_df['gender'] = student_df['name'].apply(lambda x: 'female' if x.split(" ")[0]=='Ms.' else 'male')
    student_count=  len(student_df)
    preferences = [[random.randint(0, 100) for _ in range(no_of_projects)] for _ in range(student_count)] #randomly generated preferences
    cpis = [random.randint(600, 1000)/100 for _ in range(student_count)]    #randomly generated CPIs
    students = []
    for i,student in enumerate(student_df):
        students.append(Student(name=student['name'], gender =student['gender']  ,rollNumber=student['rollNumber'],cpi=cpis[i], department=student['department'], preferences=preferences[i]))
        
    de250= CourseAllocator(students)
    de250.allocate()
    de250.get_allocation_metrics()
    de250.displayAllocation()