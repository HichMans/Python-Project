
#hwHelper

import os
import pathlib
#(Function 1): Returning a list of  directory 
def ListOfDir(dir_path):
    course_list_file = os.listdir(dir_path)
    course_list_d=[]
    for course in course_list_file:
        coursepath = os.path.join(dir_path, course)
       
        if os.path.isdir(coursepath):
            course_list_d.append(coursepath)
    return course_list_d

# Function (2): Access the file ‘CLASS_INFO_FILE’
# Returning: Class duration & Number of Sessions per semester
def ClassInfo(classIpath):
    thefile = open(classIpath, 'r')
    line1 = thefile.readline()
    line2 = thefile.readline().rstrip('\n')
    infoList = line2.split(',')
    class_duration = infoList[-2]
    session_per_semester = infoList[-1]
    thefile.close()
    return class_duration, session_per_semester

# Funcnction (3): Get a list of class ‘class_list’
def ClassListFile(classLpath):
    thefile = open(classLpath, 'r')
    names = thefile.readlines()
    class_list = []
    for i in range(len(names)):
            eachname = names[i].rstrip('\n')
            class_list.append(eachname)
    del class_list[0]
    thefile.close()
    return class_list 
#Funcntion (4): Get a list of CU attendance files ‘CU_att_files_list’ for this section
# by providing ‘section_dir’
# Returning a list of CU attendance files
def CUAttendanceFilesList(sectionpath):
    CU_att_files_list = os.listdir(sectionpath)
    CU_att_files_list.remove('classInfo.csv')
    CU_att_files_list.remove('classList.csv')
    CU_att_files_list.remove('attendance_BB.csv')
    return CU_att_files_list

#Funcntion (5) : Get data from CU_attendance_files_list

def CU_data_process(classlist,CUattfileslist,section_dir,Classduration,
SessionPerSemester,DISMISSPERC,WARNINGPERC):
    CUAbsanceNo=[0]*len(classlist)
    CUAbsancePer = [0]*len(classlist)
    C_CUAbsancePer=[0]*len(classlist)
    CUStatus=['']*len(classlist)
    sessionPerSemester=int(SessionPerSemester)
    classduration=int(Classduration)
    allowed_missed_time=classduration-classduration*0.25
    for l_file in CUattfileslist:#Step 3.3.7
        filepath = os.path.join(section_dir, l_file)
        thefile = open(filepath)
        line = thefile.readlines()
        NBline= len(line)-1
        file = open(filepath, 'r')
        line1 = file.readline()
        
        attendance=[]
        for i in range(NBline):
            line2 = file.readline().rstrip('\n')
            record = line2.split(',')
            del record[0]
            del record[2]
            del record[3]
            del record[4]
            del record[2]
            if record[1] == "Participant":
                
                attendance.append(record[0])
            
            time=record[2].split(':')
            hour=int(time[0])*60
            minute=int(time[1])
            total_hour=hour+minute
            
            for username in classlist:
                if (username==record[0] and total_hour<=allowed_missed_time):
                    CUAbsanceNo[classlist.index(username)]+=1

    
        for username in classlist:
            if username not in attendance:
                CUAbsanceNo[classlist.index(username)]+=1
        thefile.close()  
    for username in classlist:
        CAP=CUAbsanceNo[classlist.index(username)]/len(CUattfileslist)*100
        CUAbsancePer[classlist.index(username)]= round(CAP,2)
        C_CAP=(CUAbsanceNo[classlist.index(username)]/sessionPerSemester)*100
        C_CUAbsancePer[classlist.index(username)]= round(C_CAP,2)
        if C_CUAbsancePer[classlist.index(username)]>(DISMISSPERC*100):
            CUStatus[classlist.index(username)]="Dismissed"
        else:
            if (C_CUAbsancePer[classlist.index(username)]<(DISMISSPERC*100)) and  (C_CUAbsancePer[classlist.index(username)]>(WARNINGPERC*100)):
                CUStatus[classlist.index(username)]="Warning"
            else:
                CUStatus[classlist.index(username)]="OK"


    return  CUAbsanceNo ,CUAbsancePer,C_CUAbsancePer,CUStatus



#Funcntion (6) : Get data from BB_attendance_file
def BB_data_process (classlist,ATTENDANCEBBFILE,section_dir,Classduration,
SessionPerSemester,DISMISSPERC,WARNINGPERC):
    BBAbsanceNo =[0]*len(classlist)
    BBAbsancePer=[0]*len(classlist)
    CBBAbsancePer=[0]*len(classlist)
    BBStatus=['']*len(classlist)
    sessionPerSemester=int(SessionPerSemester)

    filepath = os.path.join(section_dir, ATTENDANCEBBFILE)
    thefile = open(filepath)
    line = thefile.readlines()
    NBline= len(line)-1
    
    file = open(filepath, 'r')
    line1 = file.readline()
    for i in range(NBline):
            line2 = file.readline().rstrip('\n')
            record = line2.split(',')
            del record [0]
                                                
            for username in classlist:
                if username==record[0] :
                    BBAbsancePer[classlist.index(username)]=100-float(record[-1])
                    if record[-2] =='':
                        BBAbsanceNo[classlist.index(username)]=0
                    else:
                        BBAbsanceNo[classlist.index(username)]=int(record[-2])
                    
                    CBB=  ( BBAbsanceNo[classlist.index(username)] /sessionPerSemester )*100
                    CBBAbsancePer[classlist.index(username)]=CBB
                    
                    if CBBAbsancePer[classlist.index(username)]>(DISMISSPERC*100):
                        BBStatus[classlist.index(username)]="Dismissed"
                    else:
                        if (CBBAbsancePer[classlist.index(username)]<(DISMISSPERC*100)) and  (CBBAbsancePer[classlist.index(username)]>(WARNINGPERC*100)):
                            BBStatus[classlist.index(username)]="Warning"
                        else:
                            BBStatus[classlist.index(username)]="OK"

    

    thefile.close()
    return BBAbsanceNo ,BBAbsancePer,CBBAbsancePer,BBStatus

# Function (7) : Create  the report
def ReportGenerator (root,section_dir,class_list,CU_Absance_No 
,CU_Absance_Per,C_CU_Absance_Per,CU_Status,BB_Absance_No 
,BB_Absance_Per,C_BB_Absance_Per,BB_Status):
    
    paths = pathlib.PurePath(section_dir)
    sectionN=paths.name
    courseN=paths.parent.name
    ReportName="BBvsCUReport_"+courseN+"_"+sectionN+".txt"
    
    filepath = os.path.join(root,courseN,ReportName )
    
    
    f= open(filepath, "w") 
        
    f.writelines("Username\tCU_AbsanceNo\tBB_Absance No\tCU_Absance% \tBB_Absance%  \tC_CU_Absance%\tCU_Status \tC_BB_Absance%\tBB_Status ")
    f.writelines("\n")
    for i in range (len(class_list)):
        
        
        to_write2= '{0}\t{1}\t\t{2}\t\t{3}\t\t{4:3.2f}\t\t{5:3.2f}\t\t{6:9s}\t{7:3.2f}\t\t{8}'.format(class_list[i],CU_Absance_No[i]
        ,BB_Absance_No[i],CU_Absance_Per[i]
        ,BB_Absance_Per[i],C_CU_Absance_Per[i],CU_Status[i],C_BB_Absance_Per[i],BB_Status[i])
        f.writelines(to_write2)
        
        f.writelines("\n")
        
    f.close()
