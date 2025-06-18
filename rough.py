import pandas as pd
from collections import defaultdict
student_df = pd.read_csv('students_data_2024.csv')
# sections_department_wise = defaultdict(lambda: defaultdict(int))
# for index, row in student_df.iterrows():
#     if(row['name'].split(' ')[0]=='Ms.'):
#         sections_department_wise[row['department']]['female']+=1
#     else:
#         sections_department_wise[row['department']]['male']+=1

# #print female ratio for each department
# for department in sections_department_wise.keys():
#     total_students = sections_department_wise[department]['male']+ sections_department_wise[department]['female']
#     female_students = sections_department_wise[department]['female']
#     print(f"Department: {department} has female ratio:{female_students/total_students:.2%}")

count_department_wise = defaultdict(int)
for index, row in student_df.iterrows():
    count_department_wise[row['department']] += 1

# Print the number of students in each department
print(count_department_wise)

#print the sections for each department
# for department, sections in sections_department_wise.items():
#     print(f"Department: {department}, Sections: {sections}")
    
# # Print the number of unique sections for each department
# for department, sections in sections_department_wise.items():
#     print(f"Department: {department}, Number of Unique Sections: {len(sections)}")

# print(sections_department_wise)

