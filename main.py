from course_allocator import CourseAllocator
from utils import Student, generate_and_save_students_data
import pandas as pd

if __name__ == "__main__":
    print("hole")
    print(Student)
    # generate_and_save_students_data()  #If this is not called, then each time same dataset will be used
    list_of_students = [Student(**row) for row in pd.read_csv('students_data_with_preferences.csv').to_dict(orient='records')]
    de250= CourseAllocator(list_of_students) #see utils.py for list_of_students
    de250.allocate()
    de250.save_allocation()
    de250.get_allocation_metrics()
   
    