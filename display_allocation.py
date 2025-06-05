import streamlit as st
import pandas as pd
from collections import defaultdict
from utils import Group, Student, Project
from typing import List



def display_allocation(groups:List[Group]):

    # Organize students by section → project → group
    section_map = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for group in groups:
        section_map[group.section+1][group.projectCode+1][group.groupId+1] = group.students #note that I am doing +1 for groupId, section, project because they were zero indexed in code, but while displaying we want them to be 1 indexed

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
