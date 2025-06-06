import streamlit as st
import pandas as pd
from collections import defaultdict
from utils import Group, Student, Project
from typing import List
import os
import copy


def display_allocation(students_data: pd.DataFrame):
    st.set_page_config(page_title="Student Allocation Viewer", layout="wide")
    st.title("Student Allocations by Section, Project, and Group")

    # Organize students by section → project → group
    section_map = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    student_lookup = copy.deepcopy(students_data)

    for student in students_data.itertuples():
        section_map[student.section][student.project][student.group].append(student)

    # -------------------- Search Box --------------------
    search_name = st.text_input("🔍 Search student by name (partial allowed)").strip().lower()

    if search_name:
        matching_students = [s for _,s in student_lookup.iterrows() if search_name in s["name"].lower()]

        if matching_students:
            options = [s["name"] for s in matching_students]
            selected_name = st.selectbox("Select a matching student", options)

            selected = next(s for s in matching_students if s["name"] == selected_name)
            st.success(f"📌 {selected_name} is in Section {selected['section']}, "
                       f"Project {selected['project']}, Group {selected['group']}")
        else:
            st.warning("No matching student found.")

    # -------------------- Full Allocation Display --------------------
    for section in sorted(section_map):
        with st.expander(f"📘 Section {section}", expanded=False):
            project_list = sorted(section_map[section].keys())

            selected_project = st.selectbox(
                f"Select a project in Section {section}",
                project_list,
                key=f"select_project_section_{section}"
            )

            st.markdown(f"### 📁 Project {selected_project}")

            for group_id in sorted(section_map[section][selected_project].keys()):
                st.markdown(f"**👥 Group {group_id}**")

                group_students = section_map[section][selected_project][group_id]

                df = pd.DataFrame([{
                    "Name": s.name,
                    "Gender": s.gender,
                    "Department": s.department,
                    "Allocated preference": s.allocated_preference
                } for s in group_students])

                st.table(df)


if __name__=="__main__":
    if not os.path.exists('allocated_students_data.csv'):
        raise FileNotFoundError("The file 'allocated_students_data.csv' does not exist. Maybe run the main.py file first")
    students_data = pd.read_csv('allocated_students_data.csv')
    display_allocation(students_data)

