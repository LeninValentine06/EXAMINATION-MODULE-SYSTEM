import sys
import matplotlib.pyplot as plt
import mysql.connector

mycon = mysql.connector.connect(host='localhost', user='root', password='abhisek', database='exam')
mycur = mycon.cursor()

def Student_Profile():
    sql = "INSERT INTO student(adm_no, name, class, section) VALUES (%s, %s, %s, %s)"
    print('\nPLEASE PROVIDE THE REQUIRED INFORMATION\n')
    ad = input('\nENTER THE ADMISSION NUMBER TO REGISTER FOR EXAM:')
    nm = input('\nENTER THE STUDENT NAME:')
    cls = int(input('\nENTER THE CLASS(11/12):'))
    sec = input('\nENTER THE SECTION(A-D):')
    value = (ad, nm, cls, sec)
    try:
        mycur.execute(sql, value)
        print(nm, 'ADDED SUCCESSFULLY TO EXAM MODULE')
        mycon.commit()
    except mysql.connector.Error as err:
        print('UNABLE TO INSERT!!!!!', err)

def Edit_Profile():
    sql = "UPDATE student SET section=%s WHERE adm_no=%s"
    ph = input('\nENTER THE ADMISSION NUMBER WHOSE SECTION TO MODIFY:')
    nm = input('\nENTER THE NEW SECTION(A-D):')
    value = (nm, ph)
    try:
        mycur.execute(sql, value)
        mycon.commit()
        print('RECORD UPDATED SUCCESSFULLY')
    except mysql.connector.Error as err:
        print('UNABLE TO UPDATE SECTION!!!!', err)

def Remove_Profile():
    ph = input('\nENTER THE ADMISSION NUMBER TO DELETE:')
    sql = 'DELETE FROM student WHERE Adm_no=%s'
    value = (ph,)
    try:
        mycur.execute(sql, value)
        mycon.commit()
        print('RECORD DELETED SUCCESSFULLY')
    except mysql.connector.Error as err:
        mycon.rollback()
        print('UNABLE TO DELETE RECORD!!!', err)

def Record_Entry():
    sql = "INSERT INTO result(adm_no, exam_name, sub1, sub2, sub3, sub4, sub5, total, percentage, attendance, grade, remarks) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    print('\nPLEASE PROVIDE THE REQUIRED INFORMATION\n')
    ad = int(input('\nENTER THE ADMISSION NUMBER TO ENTER RECORD:'))
    nm = input('\nENTER THE EXAM NAME:')
    sub1 = int(input('ENTER MARKS IN SUBJECT 1(MAX:100):'))
    sub2 = int(input('ENTER MARKS IN SUBJECT 2(MAX:100):'))
    sub3 = int(input('ENTER MARKS IN SUBJECT 3(MAX:100):'))
    sub4 = int(input('ENTER MARKS IN SUBJECT 4(MAX:100):'))
    sub5 = int(input('ENTER MARKS IN SUBJECT 5(MAX:100):'))
    total = sub1 + sub2 + sub3 + sub4 + sub5
    per = total // 5
    wrkday = int(input('ENTER TOTAL NUMBER OF WORKING DAYS:'))
    present = int(input('ENTER NO OF DAYS PRESENT:'))
    att = present / wrkday * 100
    att = int(att)
    if per >= 90:
        g = 'A'
        rem = 'EXCELLENT PERFORMANCE!!'
    elif per >= 75 and per < 90:
        g = 'B'
        rem = 'VERY GOOD PERFORMANCE!!'
    elif per >= 55 and per <= 75:
        g = 'C'
        rem = 'SATISFACTORY PERFORMANCE!!'
    elif per >= 35 and per < 55:
        g = 'D'
        rem = 'AVERAGE PERFORMANCE!!'
    else:
        g = 'E'
        rem = 'SCOPE FOR IMPROVEMENT!!'
    value = (ad, nm, sub1, sub2, sub3, sub4, sub5, total, per, att, g, rem)
    try:
        mycur.execute(sql, value)
        print('RECORD ADDED SUCCESSFULLY TO EXAM MODULE')
        mycon.commit()
    except mysql.connector.Error as err:
        print('UNABLE TO INSERT!!!!!', err)

def Report_Card():
    ad = int(input('\nENTER THE ADMISSION NUMBER TO SEARCH:'))
    sql1 = 'SELECT * FROM student WHERE adm_no=%s'
    value = (ad,)
    mycur.execute(sql1, value)
    rec1 = mycur.fetchone()
    if rec1 is not None:
        adm, name, cls, sec = rec1
        sql2 = 'SELECT * FROM result WHERE adm_no=%s'
        mycur.execute(sql2, value)
        rec2 = mycur.fetchone()
        if rec2 is not None:
            adm, exname, sub1, sub2, sub3, sub4, sub5, total, per, att, g, rem = rec2
            print(f'\n\n--------REPORT CARD OF {name}----------\n\n')
            print(f'\nCLASS-{cls} SECTION-{sec}\n')
            print('\n------------------------------\n')
            print(f'\nRESULT OF {exname}\n')
            print('\n------------------------------\n')
            subjects = {
                'A': ['English', 'History', 'Pol.Sc', 'Economics', 'Geography'],
                'B': ['English', 'Accountancy', 'B.Studies', 'Economics', 'Info.Practices'],
                'C': ['English', 'Physics', 'Computer Sc.', 'Chemistry', 'Mathematics'],
                'D': ['English', 'Physics', 'Biology', 'Chemistry', 'Mathematics']
            }
            sub = subjects[sec]
            print('\n'.join([f'\n {sub[i]} : {rec2[i + 2]}' for i in range(5)]))
            print(f'\n TOTAL      : {total}')
            print(f'\n PERCENTAGE : {per}')
            print(f'\n ATTENDANCE : {att}%')
            print(f'\n GRADE      : {g}')
            print(f'\n REMAKS     : {rem}')
        else:
            print('NO RECORD FOUND')
    else:
        print('WRONG ADMISSION NUMBER GIVEN!!!!!!')


def Remove_Record():
    ph = input('\nENTER THE ADMISSION NUMBER TO DELETE RECORD:')
    sql = 'DELETE FROM result WHERE adm_no=%s'
    value = (ph,)
    try:
        mycur.execute(sql, value)
        mycon.commit()
        print('RECORD DELETED SUCCESSFULLY')
    except mysql.connector.Error as err:
        mycon.rollback()
        print('UNABLE TO DELETE RECORD!!!', err)

def Graph():
    ad = int(input('\nENTER THE ADMISSION NUMBER TO SEARCH:'))
    sql1 = 'SELECT * FROM result WHERE adm_no=%s'
    value = (ad,)
    mycur.execute(sql1, value)
    T = mycur.fetchone()
    sql2 = 'SELECT section FROM student WHERE adm_no=%s'
    mycur.execute(sql2, value)
    s = mycur.fetchone()
    L = [T[2], T[3], T[4], T[5], T[6]]
    sec = s[0] if s else None

    if sec in ('A', 'B', 'C', 'D') and T:
        subjects = {
            'A': ['English', 'History', 'Pol.Sc', 'Economics', 'Geography'],
            'B': ['English', 'Accountancy', 'B.Studies', 'Economics', 'Info.Practices'],
            'C': ['English', 'Physics', 'Computer Sc.', 'Chemistry', 'Mathematics'],
            'D': ['English', 'Physics', 'Biology', 'Chemistry', 'Mathematics']
        }
        sub = subjects[sec]
        clr = ('red', 'green', 'blue', 'orange', 'brown')

        plt.bar(sub, L, color=clr)
        plt.xlabel('Subjects')
        plt.ylabel('Marks')
        plt.title('Marks Analysis')
        plt.show()
    else:
        print('Invalid admission number or missing data.')

def Close():
    print('\nTHANK YOU FOR USING THE APPLICATION')
    sys.exit()

print('-----------WELCOME TO EXAMINATION MODULE  SYSTEM FOR CLASS-XI & XII-------------\n\n')
while True:
    print('\n\nPRESS 1 TO CREATE A STUDENT PROFILE')
    print('PRESS 2 TO EDIT A STUDENT PROFILE')
    print('PRESS 3 TO DELETE A STUDENT PROFILE')
    print('PRESS 4 FOR MARKS AND ATTENDANCE ENTRY')
    print('PRESS 5 TO GENERATE REPORT CARD')
    print('PRESS 6 TO DELETE MARKS DETAILS')
    print('PRESS 7 TO PRODUCE A GRAPH PERFORMANCE')
    print('PRESS 8 TO CLOSE THE APPLICATION')
    choice = int(input('ENTER YOUR CHOICE : '))
    if choice == 1:
        Student_Profile()
    elif choice == 2:
        Edit_Profile()
    elif choice == 3:
        Remove_Profile()
    elif choice == 4:
        Record_Entry()
    elif choice == 5:
        Report_Card()
    elif choice == 6:
        Remove_Record()
    elif choice == 7:
        Graph()
    elif choice == 8:
        Close()