import streamlit as st
import pandas as pd
from collections import defaultdict
from utils import Group, Student, Project
from typing import List

class Student:
    def __init__(self, name, gender, department, section, project, group_id):
        self.name = name
        self.gender = gender
        self.department = department
        self.section = section
        self.project = project
        self.group_id = group_id

students = [
    Student("Alice", "F", "CSE", 1, 1, "G1"),
    Student("Bob", "M", "ECE", 1, 1, "G1"),
    Student("Clara", "F", "EEE", 1, 1, "G2"),
    Student("Dan", "M", "ME", 1, 1, "G2"),
    Student("Eva", "F", "CSE", 1, 2, "G3"),
    Student("Frank", "M", "CSE", 1, 2, "G3"),
    Student("Grace", "F", "ME", 2, 1, "G4"),
    Student("Henry", "M", "EEE", 2, 1, "G4"),
    Student("Ivy", "F", "ECE", 2, 1, "G5"),
    Student("Jack", "M", "CSE", 2, 1, "G5"),
    Student("Kelly", "F", "ME", 2, 2, "G6"),
    Student("Liam", "M", "EEE", 2, 2, "G6"),
]


def display_allocation(groups:List[Group]):

    # Organize students by section → project → group
    section_map = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for group in groups:
        for student in group:
            section_map[group.section][group.projectCode][group.groupId].append(student)

    st.set_page_config(page_title="Student Allocation Viewer", layout="wide")
    st.title("Student Allocations by Section, Project, and Group")

    # Loop over sections
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
                    "Allocated preference":s.preferences[group.projectCode]
                } for s in group_students])
                
                st.table(df)
