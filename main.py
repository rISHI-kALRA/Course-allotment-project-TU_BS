from course_allocator import CourseAllocator
from utils import list_of_students

if __name__ == "__main__":

    de250= CourseAllocator(list_of_students) #see utils.py for list_of_students
    de250.allocate()
    de250.get_allocation_metrics()
    de250.displayAllocation()