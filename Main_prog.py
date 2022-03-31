#code source 
import os
from functions import *

#Step 1
ROOT = 'courses'
CLASS_INFO_FILE = 'classInfo.csv'
CLASS_LIST_FILE = 'classList.csv'
ATTENDANCE_BB_FILE = 'attendance_BB.csv'
WARNING_PERC = 0.15
DISMISS_PERC = 0.25

#Step2 Get a List of Course Directory
#Step 3, 3.1, 3.2
course_dir = ListOfDir(ROOT)
print ("Courses directory : ", course_dir)
print ("---------------")
#Step 3.3
section_dir=[]
for course_d in course_dir:
    section_dir.append(ListOfDir(course_d))

print ("Sections directory : ", section_dir)
print ("---------------")

#Step 3.3.2, 3.3.2
for c in range(len(course_dir)):
    for s in range(len(section_dir[c])):
        
        classIpath1 = os.path.join(section_dir[c][s], CLASS_INFO_FILE)
        class_duration, session_per_semester=ClassInfo(classIpath1)
        

        classIpath2 = os.path.join(section_dir[c][s], CLASS_LIST_FILE) #Step 3.3.4, 3.3.5
        class_list=ClassListFile(classIpath2)
       
        
        CU_att_files_list=CUAttendanceFilesList(section_dir[c][s])#Step 3.3.6
       
        
        CU_Absance_No ,CU_Absance_Per,C_CU_Absance_Per,CU_Status = CU_data_process(class_list,CU_att_files_list,section_dir[c][s],class_duration,session_per_semester,DISMISS_PERC,WARNING_PERC)
        #Step 3.3.8, 3.3.9
        BB_Absance_No ,BB_Absance_Per,C_BB_Absance_Per,BB_Status = BB_data_process(class_list,ATTENDANCE_BB_FILE,section_dir[c][s],class_duration,session_per_semester,DISMISS_PERC,WARNING_PERC)

        ReportGenerator(ROOT,section_dir[c][s],class_list,CU_Absance_No ,CU_Absance_Per,C_CU_Absance_Per,CU_Status,BB_Absance_No ,BB_Absance_Per,C_BB_Absance_Per,BB_Status)
        
        

       
        
        
        

        


        


