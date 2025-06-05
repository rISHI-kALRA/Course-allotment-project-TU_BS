import pandas as pd
student_df = pd.read_csv('students_data.csv')
for idx,row in student_df.iloc[:10].iterrows():
    print(idx)