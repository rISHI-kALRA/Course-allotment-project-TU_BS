# import streamlit as st
# import pandas as pd
# import numpy as np
# from collections import defaultdict
# from utils import Group, Student, Project, allocated_student
# from typing import List
# import os
# import copy
# import json

# #These must be hardcoded
# project_names = {1:'theme 1: Food wastage mitigation', 2:'theme 2: Outdoor spaces improvement', 3:'theme 3: Improving lifes of labourers', 4:'theme 4: Solution for easy cleaning', 5:'theme 5: Automating watering of plants', 6:'theme 6: Wheelchair design improvement'}
# section_names = {1:'S1: Mon 2PM-5PM', 3:'S3: Tue 2PM-5PM', 5:'S5: Thu 2PM-5PM', 7:'S7: Fri 2PM-5PM', 2:'S2: Mon 5:30PM-8:30PM', 4:'S4: Tue 5:30PM-8:30PM', 6:'S6: Thu 5:30PM-8:30PM', 8:'S8: Fri 5:30PM-8:30PM'}


# def display_allocation(students_data: List[allocated_student]):
#     st.title("Student Allocations by Section, Project, and Group")
#     min_avg_group_cpi = 10
#     max_avg_group_cpi = 0
#     min_cpi_placeholder = st.empty()
#     max_cpi_placeholder = st.empty()

#     # Organize students by section → project → group
#     section_map = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
#     student_lookup = copy.deepcopy(students_data)

#     for student in students_data:
#         section_map[student.section][student.project][student.group].append(student)

#     # -------------------- Search Box --------------------
#     search_name = st.text_input("🔍 Search student by name (partial allowed)").strip().lower()

#     if search_name:
#         matching_students = [s for s in student_lookup if search_name in s.name.lower()]

#         if matching_students:
#             options = [s.name for s in matching_students]
#             selected_name = st.selectbox("Select a matching student", options)

#             selected = next(s for s in matching_students if s.name == selected_name)
#             st.success(f"📌 {selected_name} is in Section {section_names[selected.section]}, "
#                        f"Project {project_names[selected.project]}, Group {selected.group}")
#         else:
#             st.warning("No matching student found.")

#     # -------------------- Full Allocation Display --------------------
#     for section in sorted(section_map):
#         with st.expander(f"📘 Section {section_names[section]}", expanded=False):
#             project_list = sorted(section_map[section].keys())

#             selected_project = st.selectbox(
#                 f"Select a project in Section {section_names[section]}",
#                 project_list,
#                 key=f"select_project_section_{section}"
#             )
#             avg_project_cpi = np.mean([s.cpi for group_students in section_map[section][selected_project].values() for s in group_students ])
#             avg_preference = np.mean([s.allocated_preference for group_students in section_map[section][selected_project].values() for s in group_students])
            
#             st.markdown(f"### 📁 Project {project_names[selected_project]}")
#             st.markdown(f""" **📌 Project Overview**  
#                         &nbsp;&nbsp;&nbsp;&nbsp;📈 *Average CPI:* `{avg_project_cpi:.2f}`  
#                         &nbsp;&nbsp;&nbsp;&nbsp;🎯 *Average Preference Score:* `{avg_preference:.2f}`
#                         """, unsafe_allow_html=True)

#             for group_id in sorted(section_map[section][selected_project].keys()):
#                 st.markdown(f"**👥 Group {group_id}**")

#                 group_students = section_map[section][selected_project][group_id]
#                 avg_group_cpi = np.mean([s.cpi for s in group_students])
#                 min_avg_group_cpi = min(min_avg_group_cpi, avg_group_cpi)
#                 max_avg_group_cpi = max(max_avg_group_cpi, avg_group_cpi)
                
#                 st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp; 📈 *Average CPI:* `{avg_group_cpi:.2f}`")

#                 df = pd.DataFrame([{
#                     "Name": s.name,
#                     "Gender": s.gender,
#                     "Department": s.department,
#                     "Allocated preference": s.allocated_preference
#                 } for s in group_students])

#                 st.table(df)

#     min_cpi_placeholder.markdown(f'Minimum cpi across all groups: {min_avg_group_cpi:.2f}')
#     max_cpi_placeholder.markdown(f'Maximum cpi across all groups: {max_avg_group_cpi:.2f}')


# ###### Stats:

# def display_allocation_stats(students_data: List[allocated_student]):
#     st.markdown("## 📊 Allocation Statistics (Professor & Student View)")

#     # Organize data by group ID
    
#     section_map = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

#     for student in students_data:
#         section_map[student.section][student.project][student.group].append(student)
        
#     preference_scores_of_groups = []
#     gender_diversity_count = 0
#     department_diversity_count = 0
#     total_groups = 0

#     for projects in section_map.values():
#         for groups in projects.values():
#             for group_students in groups.values():
#                 total_groups += 1
#                 departments = set()
#                 preference_sum = 0
#                 female_present = False

#                 for student in group_students:
#                     departments.add(student.department)
#                     preference_sum += student.allocated_preference
#                     if student.gender.lower() == 'female':
#                         female_present = True

#                 avg_preference = preference_sum / len(group_students)
#                 preference_scores_of_groups.append(avg_preference)

#                 if female_present:
#                     gender_diversity_count += 1
#                 if len(departments) > 1:
#                     department_diversity_count += 1

#     dept_diversity = (department_diversity_count / total_groups) * 100 if total_groups > 0 else 0
#     gender_diversity = (gender_diversity_count / total_groups) * 100 if total_groups > 0 else 0

#     preference_scores_of_groups = np.array(preference_scores_of_groups)
#     pref_mean = np.mean(preference_scores_of_groups) if len(preference_scores_of_groups) > 0 else 0
#     pref_std = np.std(preference_scores_of_groups) if len(preference_scores_of_groups) > 0 else 0
#     pref_min = np.min(preference_scores_of_groups) if len(preference_scores_of_groups) > 0 else 0

#     st.markdown(f"""
#     - **Department Diversity:** {dept_diversity:.2f} %  
#     - **Gender Diversity:** {gender_diversity:.2f} %  
#     - **Average Preference Score:** {pref_mean:.2f}  
#     - **Preference Score Standard Deviation:** {pref_std:.2f}  
#     - **Minimum Preference Score:** {pref_min:.2f}  
#     """)


# if __name__ == "__main__":
#     st.set_page_config(page_title="Student Allocation Viewer", layout="wide")
#     st.title("📂 Import JSON or CSV File")
    
#     uploaded_file = st.file_uploader("Upload a JSON or CSV file containing student data (ensure it has the correct format): Please refer to README for more info on format)", type=["json","csv"])

#     if uploaded_file is not None:
#         try:
#             uploaded_file_name = uploaded_file.name.lower()
            
#             if uploaded_file_name.endswith(".json"):
#                 uploaded_file_data = json.load(uploaded_file)
#                 students_data = [allocated_student.model_validate(s) for s in uploaded_file_data]
#                 display_allocation_stats(students_data)
#                 display_allocation(students_data)
#             elif uploaded_file_name.endswith(".csv"):
#                 df = pd.read_csv(uploaded_file)
#                 uploaded_file_data = df.to_dict(orient='records')
#                 students_data = [allocated_student.model_validate(s) for s in uploaded_file_data]
#                 display_allocation_stats(students_data)
#                 display_allocation(students_data)
#             else:
#                 st.error("Unsupported file format. Please upload a .csv or .json")
    
#         except Exception as e:
#             st.error(f"❌ Failed to read file: {e}")
#     else:
#         st.info("Please upload a JSON or CSV file to proceed.")











import streamlit as st
import pandas as pd
import numpy as np
from collections import defaultdict
from utils import Group, Student, Project, allocated_student
from typing import List
import os
import copy
import json
import ast

#These must be hardcoded
project_names = {1:'theme 1: Food wastage mitigation', 2:'theme 2: Outdoor spaces improvement', 3:'theme 3: Improving lifes of labourers', 4:'theme 4: Solution for easy cleaning', 5:'theme 5: Automating watering of plants', 6:'theme 6: Wheelchair design improvement'}
section_names = {1:'S1: Mon 2PM-5PM', 3:'S3: Tue 2PM-5PM', 5:'S5: Thu 2PM-5PM', 7:'S7: Fri 2PM-5PM', 2:'S2: Mon 5:30PM-8:30PM', 4:'S4: Tue 5:30PM-8:30PM', 6:'S6: Thu 5:30PM-8:30PM', 8:'S8: Fri 5:30PM-8:30PM'}


def display_allocation(students_data: List[allocated_student]):
    st.title("Student Allocations by Section, Project, and Group")
    min_avg_group_cpi = 10
    max_avg_group_cpi = 0
    min_cpi_placeholder = st.empty()
    max_cpi_placeholder = st.empty()

    # Organize students by section → project → group
    section_map = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    student_lookup = copy.deepcopy(students_data)

    for student in students_data:
        section_map[student.section][student.project][student.group].append(student)

    # -------------------- Search Box --------------------
    search_name = st.text_input("🔍 Search student by name (partial allowed)").strip().lower()

    if search_name:
        matching_students = [s for s in student_lookup if search_name in s.name.lower()]

        if matching_students:
            options = [s.name for s in matching_students]
            selected_name = st.selectbox("Select a matching student", options)

            selected = next(s for s in matching_students if s.name == selected_name)
            st.success(f"📌 {selected_name} is in Section {section_names[selected.section]}, "
                       f"Project {project_names[selected.project]}, Group {selected.group}")
        else:
            st.warning("No matching student found.")

    # -------------------- Full Allocation Display --------------------
    for section in sorted(section_map):
        with st.expander(f"📘 Section {section_names[section]}", expanded=False):
            project_tabs = st.tabs([f"📁 Project {project_names[selected_project]}" for selected_project in sorted(section_map[section].keys())])
            for i,selected_project in enumerate(sorted(section_map[section].keys())):
                with project_tabs[i]:

            # for selected_project in sorted(section_map[section].keys()):
            #     with st.expander(f"📁 Project {project_names[selected_project]}", expanded=False):

            # selected_project = st.selectbox(
            #     f"Select a project in Section {section_names[section]}",
            #     project_list,
            #     key=f"select_project_section_{section}"
            # )
                    avg_project_cpi = np.mean([s.cpi for group_students in section_map[section][selected_project].values() for s in group_students ])
                    avg_preference = np.mean([s.allocated_preference for group_students in section_map[section][selected_project].values() for s in group_students])
            
                    st.markdown(f"### 📁 Project {project_names[selected_project]}")
                    st.markdown(f""" **📌 Project Overview**  
                                &nbsp;&nbsp;&nbsp;&nbsp;📈 *Average CPI:* `{avg_project_cpi:.2f}`  
                                &nbsp;&nbsp;&nbsp;&nbsp;🎯 *Average Preference Score:* `{avg_preference:.2f}`
                                """, unsafe_allow_html=True)

                    for group_id in sorted(section_map[section][selected_project].keys()):
                        st.markdown(f"**👥 Group {group_id}**")

                        group_students = section_map[section][selected_project][group_id]
                        avg_group_cpi = np.mean([s.cpi for s in group_students])
                        min_avg_group_cpi = min(min_avg_group_cpi, avg_group_cpi)
                        max_avg_group_cpi = max(max_avg_group_cpi, avg_group_cpi)
                        
                        st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp; 📈 *Average CPI:* `{avg_group_cpi:.2f}`")

                        # df = pd.DataFrame([{
                        #     "Name": s.name,
                        #     "Gender": s.gender,
                        #     "Department": s.department,
                        #     "Allocated preference": s.allocated_preference
                        # } for s in group_students])

                        # st.table(df)

                        rows = []
                        for s in group_students:    
                            highlighted = ", ".join(
                            f"<mark>{v}</mark>" if i==selected_project-1 else str(v)
                                for i,v in enumerate(s.preferences)
                            )
                            rows.append({
                                "Name": s.name,
                                "Gender": s.gender,
                                "Department": s.department,
                                "CPI:":s.cpi,
                                "Allocated preference": highlighted
                            })

                        # Convert to DataFrame
                        df = pd.DataFrame(rows)

                        # Render as HTML table manually
                        html = df.to_html(escape=False, index=False)
                        st.markdown(html, unsafe_allow_html=True)

    min_cpi_placeholder.markdown(f'Minimum cpi across all groups: {min_avg_group_cpi:.2f}')
    max_cpi_placeholder.markdown(f'Maximum cpi across all groups: {max_avg_group_cpi:.2f}')


###### Stats:

def display_allocation_stats(students_data: List[allocated_student]):
    st.markdown("## 📊 Allocation Statistics (Professor & Student View)")

    # Organize data by group ID
    
    section_map = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for student in students_data:
        section_map[student.section][student.project][student.group].append(student)
        
    preference_scores_of_groups = []
    gender_diversity_count = 0
    department_diversity_count = 0
    total_groups = 0

    for projects in section_map.values():
        for groups in projects.values():
            for group_students in groups.values():
                total_groups += 1
                departments = set()
                preference_sum = 0
                female_present = False

                for student in group_students:
                    departments.add(student.department)
                    preference_sum += student.allocated_preference
                    if student.gender.lower() == 'female':
                        female_present = True

                avg_preference = preference_sum / len(group_students)
                preference_scores_of_groups.append(avg_preference)

                if female_present:
                    gender_diversity_count += 1
                if len(departments) > 1:
                    department_diversity_count += 1

    dept_diversity = (department_diversity_count / total_groups) * 100 if total_groups > 0 else 0
    gender_diversity = (gender_diversity_count / total_groups) * 100 if total_groups > 0 else 0

    preference_scores_of_groups = np.array(preference_scores_of_groups)
    pref_mean = np.mean(preference_scores_of_groups) if len(preference_scores_of_groups) > 0 else 0
    pref_std = np.std(preference_scores_of_groups) if len(preference_scores_of_groups) > 0 else 0
    pref_min = np.min(preference_scores_of_groups) if len(preference_scores_of_groups) > 0 else 0

    st.markdown(f"""
    - **Department Diversity:** {dept_diversity:.2f} %  
    - **Gender Diversity:** {gender_diversity:.2f} %  
    - **Average Preference Score:** {pref_mean:.2f}  
    - **Preference Score Standard Deviation:** {pref_std:.2f}  
    - **Minimum Preference Score:** {pref_min:.2f}  
    """)


if __name__ == "__main__":
    st.set_page_config(page_title="Student Allocation Viewer", layout="wide")
    st.title("📂 Import JSON or CSV File")
    
    uploaded_file = st.file_uploader("Upload a JSON or CSV file containing student data (ensure it has the correct format): Please refer to README for more info on format)", type=["json","csv"])

    if uploaded_file is not None:
        try:
            uploaded_file_name = uploaded_file.name.lower()
            
            if uploaded_file_name.endswith(".json"):
                uploaded_file_data = json.load(uploaded_file)
                students_data=[]
                for s in uploaded_file_data:
                    s['preferences']= ast.literal_eval(s['preferences'])
                    students_data.append(allocated_student.model_validate(s))
                # students_data = [allocated_student.model_validate(s) for s in uploaded_file_data]
                display_allocation_stats(students_data)
                display_allocation(students_data)
            elif uploaded_file_name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
                uploaded_file_data = df.to_dict(orient='records')
                students_data=[]
                for s in uploaded_file_data:
                    s['preferences']= ast.literal_eval(s['preferences'])
                    students_data.append(allocated_student.model_validate(s))
                # students_data = [allocated_student.model_validate(s) for s in uploaded_file_data]
                display_allocation_stats(students_data)
                display_allocation(students_data)
            else:
                st.error("Unsupported file format. Please upload a .csv or .json")
    
        except Exception as e:
            st.error(f"❌ Failed to read file: {e}")
    else:
        st.info("Please upload a JSON or CSV file to proceed.")



