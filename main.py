
import random

from utils import Student, Project, Group, CourseAllocator

if __name__ == "__main__":
    
    # toy dataset for now
    student_count=1325
    num_projects = 6
    num_sections=8
    group_size=6
    female_count = 261
    male_count = 1064
    cpis = [random.randint(600, 1000)/100 for _ in range(student_count)]
    genders = ['female']*female_count + ['male']*male_count
    random.shuffle(genders)
    departments = ['CSE']*student_count
    preferences = [[random.randint(0, 100) for _ in range(num_projects)] for _ in range(student_count)]
    rollnumbers = [f'23B{i:04d}' for i in range(student_count)]
    
    students = []
    for i in range(student_count):
        students.append(Student(name=f"Student_{i}", gender = genders[i] ,rollNumber=rollnumbers[i],cpi=cpis[i], department=departments[i], preferences=preferences[i]))
        
    de250= CourseAllocator(students)
    de250.allocate(numberOfSections=num_sections, numberOfProjects=num_projects, groupSize=group_size)
    df = de250.getAllocation()
    print(df)