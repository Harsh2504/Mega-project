from bson import ObjectId
from flask import Flask, render_template, Markup, request, redirect, session, flash, url_for,send_from_directory, make_response
import pandas as pd
import secrets
import string
from datetime import datetime
import mysql.connector
import subprocess
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Connect to the MongoDB server and access the "Users" collection
# Connect to the MySQL server and access the "users" table


#import os
#import psycopg2
#
#conn = psycopg2.connect(os.environ["DATABASE_URL"])

#with conn.cursor() as cur:
#    cur.execute("SELECT now()")
#    res = cur.fetchall()
#    conn.commit()
#    print(res)



mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="",
      database="systemdb"
    )


post_value = None
did = None


@app.route('/', methods=['GET', 'POST'])
def login():
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="",
      database="systemdb"
    )

    global post_value
    global did
    session['logged_in'] = False  
    if request.method == 'POST':
        user=post_value
        email = request.form['email']
        password = request.form['pwd']
        if not email or not password:
            flash('Please enter credentials to login.', 'empty-error')
            return redirect('/')
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = mycursor.fetchone()

        if user is not None:
            session['logged_in'] = True
            session['username'] = email
            session['name'] = user[2]
            session['id']=user[0]
            post_value = session['post'] = user[7]
            did = session['did']= user[3]
            session['pre']=user[1]
            print(post_value)
            if post_value == 'Admin':
                 return redirect('/admin')
            else:
               return redirect('/divison') 
        else:
            flash('Invalid username or password. Please try again.', 'auth-error')
            return redirect('/')
    else:
        return render_template("login.html")


@app.route('/admin')
def home():
    global post_value
    if 'logged_in' in session and session['logged_in']:
        
        user=post_value
        mydb.commit()
        mycursor = mydb.cursor()
        sql = "SELECT s_time, e_time ,part,code FROM works WHERE work = 'feedback'"
        mycursor.execute(sql)
        result = mycursor.fetchone()





        if result:
        # Convert the date and time strings to datetime objects
            start_date_time_st = result[0]
            end_date_time_st = result[1]
            part_x = result[2]
            code1=result[3]
            try:
                start_date_time_x = start_date_time_st.isoformat()
                end_date_time_x = end_date_time_st.isoformat()
            except AttributeError:
            # Handle the exception here
                start_date_time_x = None
                end_date_time_x = None
        return render_template('admin.html',user=user,start_date_time_x=start_date_time_x,end_date_time_x=end_date_time_x,part_x=part_x,cod=code1)
        
    else:
        return redirect('/')
    
@app.route('/backup', methods=['POST'])
def backup():
    db_name = 'systemdb'
    file_name = db_name + '.sql'
   

    mydb = mysql.connector.connect(
         host="localhost",
         user="root",
         password=""
    )



   

    
    # Run mysqldump command to export database to file
    #subprocess.call(['D:\\xampp2\\mysql\\bin\\mysqldump', '-u', 'root', '--password=',"", '--databases',db_name, '--result-file=' + file_name])


    return redirect('/admin')


@app.route('/print1')
def print1():
    if 'logged_in' in session and session['logged_in']:
        table_html = request.args.get('table_html')
        print(table_html)
        table_html_safe = Markup(table_html)
        return render_template('print.html', table_html=table_html_safe)
    else:
        return redirect('/')

@app.route('/printt')
def printt():
    if 'logged_in' in session and session['logged_in']:
        table_html = request.args.get('table_html')
        print(table_html)
        table_html_safe = Markup(table_html)
        return render_template('printtrec.html', table_html=table_html_safe)
    else:
        return redirect('/')
    
@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    
    if request.method == 'POST':
    
        user=post_value
        if 'action' in request.form:
            if request.form['action'] == 'clear':
                # Clear the start and end date and time values from the database
                status = 'stop'
                mycursor = mydb.cursor()
               
                
                mycursor.execute("UPDATE works SET s_time = NULL, e_time = NULL ,status=%s  WHERE work = 'feedback'" ,(status,))
                mydb.commit()
                session.pop('start_date_time', None)
                session.pop('end_date_time', None)
                # Redirect to the same URL to show the student login page with default values
                return redirect('/admin')
            elif request.form['action'] == 'update':
                # Get the start and end date and time values from the form
                start_date_time_str = request.form['start_date_time']
                end_date_time_str = request.form['end_date_time']
                part_str = request.form['part']
                # Convert the date and time strings to datetime objects
                start_date_time = datetime.strptime(start_date_time_str, '%Y-%m-%dT%H:%M')
                end_date_time = datetime.strptime(end_date_time_str, '%Y-%m-%dT%H:%M')
                # Update the start and end date and time values in the database
                mycursor = mydb.cursor()
                status = 'start'
                sql = "UPDATE works SET s_time = %s, e_time = %s,status=%s,part=%s WHERE work = 'feedback'"
                val = (start_date_time, end_date_time,status,part_str)
                mycursor.execute(sql, val)
                mydb.commit()
                session['start_date_time'] = start_date_time.isoformat()
                session['end_date_time'] = end_date_time.isoformat()
                # Redirect to the same URL to show the student login page with updated values
                return redirect('/admin')
        else:
            # The action is not specified, so treat it as a regular submit
            # Get the start and end date and time values from the form
            start_date_time_str = request.form['start_date_time']
            end_date_time_str = request.form['end_date_time']
            part_str = request.form['part']
            # Convert the date and time strings to datetime objects
            start_date_time = datetime.strptime(start_date_time_str, '%Y-%m-%dT%H:%M')
            end_date_time = datetime.strptime(end_date_time_str, '%Y-%m-%dT%H:%M')
            alphabet = string.ascii_lowercase
            symbol = "&@#!"
            digits = string.digits

            while True:
                code = ''.join([secrets.choice(digits) if i == 2 or i == 5 else secrets.choice(symbol) if i == 3 else secrets.choice(alphabet) for i in range(7)])
                if sum(c.isdigit() for c in code) == 2 and sum(c in symbol for c in code) == 1:
                    code = code.capitalize()
                    break

            print(code)            
            # Update the start and end date and time values in the database
            mycursor = mydb.cursor()
            status = 'start'
            sql = "UPDATE works SET s_time = %s, e_time = %s,status=%s,part=%s,code=%s WHERE work = 'feedback'"
            val = (start_date_time, end_date_time,status,part_str,code)
            mycursor.execute(sql, val)
            mydb.commit()
            # Redirect to the same URL to show the student login page with updated values
            # Store the start and end date and time values in the session object
            session['start_date_time'] = start_date_time.isoformat()
            session['end_date_time'] = end_date_time.isoformat()
            # Redirect to the same URL to show the student login page with updated values

            
            return redirect('/admin')

    else:
        

            if 'st_logged_in' in session and session['st_logged_in']:  
                    mycursor = mydb.cursor()
                    mycursor.execute("SELECT * FROM class")
                    cls = mycursor.fetchall()
                    mycursor = mydb.cursor()
                    mycursor.execute("select id,dept_name from department")
                    dept = mycursor.fetchall()
                    mycursor = mydb.cursor()
                    mycursor.execute("select part from works WHERE work = 'feedback'")
                    part_x = mycursor.fetchone()
                    print("hahaha",part_x)
                    
                    return render_template('student_login.html',dept=dept,cls=cls,part_x=part_x)
            else:
                return render_template('codever.html')

@app.route('/student_verify')
def student_verify():
        mycursor = mydb.cursor()
        sql = "SELECT s_time, e_time FROM works WHERE work = 'feedback'"
        mycursor.execute(sql)
        result = mycursor.fetchone()
        if result:
        # Convert the date and time strings to datetime objects
            start_date_time_st = result[0]
            end_date_time_st = result[1]
            try:
                start_date_time_x = start_date_time_st.isoformat()
                end_date_time_x = end_date_time_st.isoformat()
            except AttributeError:
            # Handle the exception here
                start_date_time_x = None
                end_date_time_x = None
            if start_date_time_x and end_date_time_x:
                start_date_time = datetime.fromisoformat(start_date_time_x)
                end_date_time = datetime.fromisoformat(end_date_time_x)
                # Check if the current time is within the start and end date and time range
                current_time = datetime.now()
                if start_date_time <= current_time <= end_date_time:
                   
                    session['st_logged_in'] = False
                    flash('Enter Login Code above.', 'success')  
                    return render_template('codever.html')

        return render_template('error.html')
    
@app.route('/verify', methods=['POST'])
def verify():

    if request.method == 'POST':
        incod = request.form['cod']
        mycursor =mydb.cursor()
        mycursor.execute("Select code from works WHERE work = 'feedback'")
        dbcod=mycursor.fetchone()
        print("db",dbcod)
        if not incod :
              flash('Enter Login Code to Give Feedback.', 'success')
              return render_template('codever.html')
        else:      
            if incod == dbcod[0]:           
               
                session['st_logged_in'] = True     
                return redirect('/student_login')
            else:
                flash('Login Code is incorrect.', 'success')
                return render_template('codever.html')
        
@app.route('/reload')
def reload():
        if 'logged_in' in session and session['logged_in']:
            alphabet = string.ascii_lowercase
            symbol = "&@#!"
            digits = string.digits

            while True:
                code = ''.join([secrets.choice(digits) if i == 2 or i == 5 else secrets.choice(symbol) if i == 3 else secrets.choice(alphabet) for i in range(7)])
                if sum(c.isdigit() for c in code) == 2 and sum(c in symbol for c in code) == 1:
                    code = code.capitalize()
                    break

            print(code)            
            # Update the start and end date and time values in the database
            mycursor = mydb.cursor()
           
            mycursor.execute("UPDATE works SET code=%s WHERE work = 'feedback'",(code,))
            mydb.commit()
            return redirect('/admin')




@app.route('/department')
def department():
    global post_value
    if 'logged_in' in session and session['logged_in']:
        user=post_value
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM department")
        depart = mycursor.fetchall()
      
      
      
       
        return render_template('department.html', depart=depart, user=user)
    else:
        return redirect('/')
    
@app.route('/class')
def class1():
    global post_value
    if 'logged_in' in session and session['logged_in']:
        user=post_value
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM class")
        cls = mycursor.fetchall()
        return render_template('class.html', cls=cls, user=user)
    else:
        return redirect('/')

@app.route('/divison')
def divison():
    global post_value 
    global did
    print(post_value) 
    print(did)
    if 'logged_in' in session and session['logged_in']:
        user=post_value
        
      #  dept = depart_collection.find()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM class")
        cls = mycursor.fetchall()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM department")
        dept = mycursor.fetchall()
        if post_value == 'Admin':
            cursor = mydb.cursor()
            cursor.execute("SELECT division.id as idd,department.dept_name as did,class.short as cn,division.division as dev from class,department,division WHERE division.cd_id=class.id AND division.dept_id=department.id")
            div = cursor.fetchall()
            cursor.close()
        else:
            cursor = mydb.cursor()
            cursor.execute("SELECT division.id as idd,department.dept_name as did,class.short as cn,division.division as dev from class,department,division WHERE division.cd_id=class.id AND division.dept_id=department.id and  department.id=%s", (did,))
            div = cursor.fetchall()
            cursor.close()
        return render_template('divison.html',div=div,cls=cls,dept=dept, user=user)
    else:
        return redirect('/')

@app.route('/batch')
def batch():
    global post_value 
    global did
    if 'logged_in' in session and session['logged_in']:
        user=post_value
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM class")
        cls = mycursor.fetchall()
        mycursor = mydb.cursor()
        mycursor.execute("select id,dept_name from department")
        dept = mycursor.fetchall()
        mycursor = mydb.cursor()
        #ex = 1
       # ex1= 4
        #mycursor.execute("select id,division from division where dept_id=%s and cd_id=%s",(ex,ex1))
       # div = mycursor.fetchall()
 

        if post_value == 'Admin':
            cursor = mydb.cursor()
            cursor.execute("SELECT batch.id as bati,batch.batch as bat,batch.div_id as divi,department.dept_name as dept,class.short as cls FROM department,class,batch WHERE batch.dept_id=department.id AND batch.cd_id=class.id")
            batch = cursor.fetchall()
            cursor.close()
        else:
            cursor = mydb.cursor()
            cursor.execute("SELECT batch.id as bati,batch.batch as bat,batch.div_id as divi,department.dept_name as dept,class.short as cls FROM department,class,batch WHERE batch.dept_id=department.id AND batch.cd_id=class.id and department.id=%s", (did,))
            batch = cursor.fetchall()
            cursor.close()
        
        # Create a list of batches with a new element to hold division data
        batch_list = []
        for row in batch:
            if row[2] == 0:
                batch_list.append((row[0], row[3], row[4], "--", row[1]))
            else:
                idd = row[2]
                cursor2 = mydb.cursor()
                cursor2.execute("SELECT division FROM division WHERE id=%s", (idd,))
                info2 = cursor2.fetchall()
                cursor2.close()
                for row1 in info2:
                    batch_list.append((row[0], row[3], row[4], row1[0], row[1]))
        
        return render_template('batch.html' , batch=batch_list , dept=dept ,cls=cls, user=user )
    else:
        return redirect('/')

@app.route('/faculty')
def faculty():
    global post_value 
    global did
    if 'logged_in' in session and session['logged_in']:
        user=post_value
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM department")
        dept = mycursor.fetchall()
        if post_value == 'Admin':
            cursor = mydb.cursor()
            cursor.execute("SELECT facility.id as fid,facility.pre as pref,facility.name as namef,facility.short as fshort,department.dept_s as dept_sf FROM department,facility WHERE facility.dept_id=department.id")
            fac = cursor.fetchall()
            cursor.close()
        else:
            cursor = mydb.cursor()
            cursor.execute("SELECT facility.id as fid,facility.pre as pref,facility.name as namef,facility.short as fshort,department.dept_s as dept_sf FROM department,facility WHERE facility.dept_id=department.id and department.id=%s" ,(did,))
            fac = cursor.fetchall()
            cursor.close()    
        return render_template('faculty.html', fac=fac , user=user ,dept=dept)
    else:
        return redirect('/')

@app.route('/subject')
def subject():
    global post_value 
    global did
    if 'logged_in' in session and session['logged_in']:
          
          user=post_value
          mycursor = mydb.cursor()
          mycursor.execute("SELECT * FROM class")
          cls = mycursor.fetchall()
          mycursor = mydb.cursor()
          mycursor.execute("SELECT * FROM department")
          dept = mycursor.fetchall()
          mycursor = mydb.cursor()
          mycursor.execute("SELECT * FROM semister")
          sem = mycursor.fetchall()
          if post_value == 'Admin':
            cursor = mydb.cursor()
            cursor.execute("SELECT subject.id as sid,subject.name as names,subject.name_s as sname,subject.sub_code as codes,class.short as classname,subject.sem as dsem,subject.th as th,subject.pr as pr,subject.tu as tu,department.dept_s as deptn from class,department,subject WHERE department.id=subject.dept_id AND class.id=subject.cd_id ")
            sub = cursor.fetchall()
            cursor.close()
          else:
            cursor = mydb.cursor()
            cursor.execute("SELECT subject.id as sid,subject.name as names,subject.name_s as sname,subject.sub_code as codes,class.short as classname,subject.sem as dsem,subject.th as th,subject.pr as pr,subject.tu as tu,department.dept_s as deptn from class,department,subject WHERE department.id=subject.dept_id AND class.id=subject.cd_id and department.id=%s" ,(did,))
            sub = cursor.fetchall()
            cursor.close()    
          return render_template('subject.html',sub=sub,user=user,cls=cls,dept=dept,sem=sem)
    else:
        return redirect('/')

@app.route('/student')
def student():
    global post_value
    if 'logged_in' in session and session['logged_in']:
        user=post_value
        return render_template('student.html', user=user)
    else:
        return redirect('/')

@app.route('/teaching_record')
def teaching():
    mydb = mysql.connector.connect(
       host="localhost",
      user="root",
      password="",
      database="systemdb"
    )
    global post_value 
    global did 
    if 'logged_in' in session and session['logged_in']:
          
          mycursor = mydb.cursor()
          mycursor.execute("SELECT * FROM class")
          cls = mycursor.fetchall()
          mycursor = mydb.cursor()
          mycursor.execute("select id,dept_name from department")
          dept = mycursor.fetchall()
          mycursor = mydb.cursor()
          mycursor.execute("select * from semister")
          seme = mycursor.fetchall()
          user=post_value
          if post_value == 'Admin':  
            cursor = mydb.cursor()
            cursor.execute("SELECT teaching_rec.id as tid,facility.pre as fpre,facility.name as fname,subject.name_s as sname,class.short as cls,teaching_rec.div_id as did,teaching_rec.bat_id as bid,teaching_rec.t_p as tp,department.dept_s as dept FROM teaching_rec,department,facility,class,subject where teaching_rec.dept_id=department.id AND teaching_rec.cd_id=class.id AND  teaching_rec.sub_id=subject.id AND teaching_rec.fac_id=facility.id")
            trec = cursor.fetchall()
          else: 
            cursor = mydb.cursor()
            cursor.execute("SELECT teaching_rec.id as tid,facility.pre as fpre,facility.name as fname,subject.name_s as sname,class.short as cls,teaching_rec.div_id as did,teaching_rec.bat_id as bid,teaching_rec.t_p as tp,department.dept_s as dept FROM teaching_rec,department,facility,class,subject where teaching_rec.dept_id=department.id AND teaching_rec.cd_id=class.id AND  teaching_rec.sub_id=subject.id AND teaching_rec.fac_id=facility.id and department.id=%s",(did,))
            trec = cursor.fetchall()



          trec_list = []
          for row in trec:
           if row[5] == 0:
              trec_list.append((row[0], row[1], row[2], row[3],row[4], "--", row[6],row[7],row[8]))
           else:
              idd = row[5]
              cursor2 = mydb.cursor()
              cursor2.execute("SELECT division FROM division WHERE id=%s", (idd,))
              info2 = cursor2.fetchall()
              cursor2.close()
              for row1 in info2:
                  trec_list.append((row[0], row[1], row[2], row[3],row[4], row1[0], row[6],row[7],row[8]))  
          trec_list_bat = []
          for rw in trec_list:
           if rw[6] == '0' :
            trec_list_bat.append((rw[0], rw[1], rw[2], rw[3], rw[4], rw[5], "--", rw[7], rw[8]))
           else:
              bid = rw[6].split(",")
         
              bath_info = []
             
              for i in range(1, len(bid)):
                idb = bid[i]
                cursor2 = mydb.cursor()
                cursor2.execute("select batch from batch where id=%s", (idb,))
                bati = cursor2.fetchall()
                bath_info.extend([x[0] for x in bati])
              trec_list_bat.append((rw[0], rw[1], rw[2], rw[3], rw[4], rw[5], ",".join(bath_info), rw[7], rw[8]))
          return render_template('teaching record.html', trec=trec_list_bat,user=user, dept=dept ,cls=cls,seme=seme)
    else:
        return redirect('/')
    

    
@app.route('/questions')
def questions():
    global post_value
    if 'logged_in' in session and session['logged_in']:
        mydb.commit()
        user=post_value
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM que")
        que = mycursor.fetchall()

        return render_template('questions.html',que=que, user=user)
    else:
        return redirect('/')
    
@app.route('/user')
def user():
    global post_value
    if 'logged_in' in session and session['logged_in']:
            user=post_value
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM department")
            departments = mycursor.fetchall()
       
            cursor = mydb.cursor()
            cursor.execute("SELECT users.id as idu,users.name as nameu,department.dept_s as named,users.email as emailu,users.post as postu,users.number as n1 from users,department WHERE department.id=users.dept_id;")
            users = cursor.fetchall()
            cursor.close()
            return render_template('user.html', users=users, departments=departments, user=user)
    
    else:
        return redirect('/') 

@app.route('/report')
def report():
    global post_value
    if 'logged_in' in session and session['logged_in']:
        user=post_value
        return render_template('report.html', user=user)
    else:
        return redirect('/')           

@app.route('/letter')
def letter():
    global post_value
    if 'logged_in' in session and session['logged_in']:
        user=post_value
        ##########Appreciation letter
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM department")
        departments = mycursor.fetchall()
        fin =[]
        for d in departments:
            dept = []
            did = d[0]
            dept.append(did)
            dept.append(d[1])
            mycursor.execute("SELECT DISTINCT(fac_id) as fid FROM teaching_rec where dept_id=%s ORDER by dept_id,fac_id",(did,))
            fac = mycursor.fetchall()
            fac1 =[]
            
            for f in fac:
                fid = f[0]
                teach=[]
                fnm=[]
              #  print("fid " , fid)
                mycursor.execute("select * from facility where id=%s",(fid,))
                facd = mycursor.fetchall()
                for fc in facd:
                    facnm = fc[1] + " " +fc[2]
                    facid = fc[0] 
                    fnm.append(facid)
                    fnm.append(facnm)
                
                mycursor.execute("select id from teaching_rec where dept_id=%s and fac_id=%s ORDER by dept_id,fac_id",(did,fid))
                teachd = mycursor.fetchall()
                #print(facnm," ",teachd)
                for t in teachd:
                    #print(t)
                    tid = t[0]
                   
                    mycursor.execute("select teach_id from sgp where teach_id=%s and avg>=7", (tid,))

                    ft = mycursor.fetchall()
                    
                    if ft:
                        teach.append(ft)
                #print(teach)
                fnm.append(teach)
                if teach:
                    fac1.append(fnm)
            dept.append(fac1)        
            #print(fac1)
            fin.append(dept)       
        #print(fin)


        ##########Suggestion letter
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM department")
        departments = mycursor.fetchall()
        fin1 =[]
        for d in departments:
            dept1 = []
            did = d[0]
            dept1.append(did)
            
            dept1.append(d[1])
            mycursor.execute("SELECT DISTINCT(fac_id) as fid FROM teaching_rec where dept_id=%s ORDER by dept_id,fac_id",(did,))
            fac = mycursor.fetchall()
            fac12 =[]
            
            for f in fac:
                fid = f[0]
                teach1=[]
                fnm1=[]
              #  print("fid " , fid)
                mycursor.execute("select * from facility where id=%s",(fid,))
                facd = mycursor.fetchall()
                for fc in facd:
                    facnm = fc[1] + " " +fc[2] 
                    facid = fc[0] 
                    fnm1.append(facid)
                    fnm1.append(facnm)
                    
                
                mycursor.execute("select id from teaching_rec where dept_id=%s and fac_id=%s ORDER by dept_id,fac_id",(did,fid))
                teachd = mycursor.fetchall()
                #print(facnm," ",teachd)
                for t in teachd:
                    #print(t)
                    tid = t[0]
                   
                    mycursor.execute("select teach_id from sgp where teach_id=%s and avg<7", (tid,))

                    ft = mycursor.fetchall()
                    
                    if ft:
                        teach1.append(ft)
                #print(teach)
                fnm1.append(teach1)
                if teach1:
                    fac12.append(fnm1)
            dept1.append(fac12)        
            #print(fac1)
            fin1.append(dept1)       
        #print(fin)
        return render_template('letter.html', user=user,final=fin,finalsl=fin1)
    else:
        return redirect('/') 


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect('/')

@app.route('/feedback', methods=['POST'])
def feedback():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM que")
    que_data = mycursor.fetchall()
    qnum = len(que_data)
   
    if request.method == 'POST':
        dept = request.form['dept']
        cls = request.form['cls']
        div = request.form['dfn']
        bat = request.form['batch']
        sem = request.form['semester']
        if cls == "4" and sem == "1":
            sem = "1"
        elif cls == "4" and sem == "2":
            sem = "2"
        elif cls == "5" and sem == "1":
            sem = "3"
        elif cls == "5" and sem == "2":
            sem = "4"
        elif cls == "6" and sem == "1":
            sem = "5"
        elif cls == "6" and sem == "2":
            sem = "6"
    
        did = dept
        cid = cls
        if  div == "0":
            ddid = "0"
        else:
            ddid = div
     
        bid = ',' + bat + ','   
        mydb.commit()
        cursor = mydb.cursor()
        print(did,"/",sem,"/",cid,"/",ddid,"/",bid)
        cursor.execute("SELECT facility.pre as fpre, facility.short as fname, subject.name_s as sname, teaching_rec.t_p as tp ,teaching_rec.id as tre FROM teaching_rec JOIN facility ON teaching_rec.fac_id = facility.id JOIN subject ON teaching_rec.sub_id = subject.id WHERE teaching_rec.dept_id=%s AND teaching_rec.sem=%s AND teaching_rec.cd_id=%s AND teaching_rec.div_id=%s AND teaching_rec.bat_id='0' OR teaching_rec.bat_id LIKE %s", (did, sem, cid, ddid, '%' + bid + '%'))
        
        records = cursor.fetchall()
        num = len(records)
        print("records num :",num )
        if num != 0:
            return render_template('feedback.html',que=que_data, fanum=num, qnum=qnum, fa=records, ddid=ddid,did=did,cid=cid)
        else:
            flash('There was no Feedback available for the options you selected.', 'success')
            return redirect("/student_login")


#database scene
@app.route('/get_admin_data')
def get_admin_data():
    _id = session['id']

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM department")
    dept_data = mycursor.fetchall()
    mycursor.close()  

    cur = mydb.cursor()
    cur.execute("SELECT * FROM users WHERE id=%s", (_id,))
    user_data = cur.fetchone()
  
  
    return render_template('admin_data.html', data=user_data, dept=dept_data )

@app.route('/set_admin_data', methods=['POST'])
def set_admin_data():
   # get the updated user data from the form
    session['pre']= pre = request.form.get('pre')
    session['name'] = name = request.form.get('name')
    email = request.form.get('email')
    num = request.form.get('num')
    password = request.form.get('password')

    _id = request.form.get('_id')

    # update the user data in the database
    cur = mydb.cursor()
    cur.execute(
        "UPDATE users SET pre=%s, name=%s, email=%s, number=%s, password=%s WHERE id=%s",
        (pre , name, email,num, password,  _id)
    )
    mydb.commit()
    cur.close()
    return redirect('/admin')
##########################user###########################
@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        num = request.form['num']
        post = request.form['post']
        dept = request.form['department']
        pre = request.form['pre']
        pswd = request.form['password']
        st = "active"
        
        if post == 'Admin':
            id = 0
        else:
            cursor = mydb.cursor()
            cursor.execute("SELECT id FROM department WHERE dept_name = %s", (dept,))
            row = cursor.fetchone()
            id = row[0]
        
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO users(pre, name, dept_id, email, number, post, status , password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (pre, name, id, email, num, post, st, pswd))
        mydb.commit()
        
        return redirect('/user')

@app.route('/delete_user/<id>', methods=['POST'])
def delete_user(id):
    mycursor = mydb.cursor()
    sql = "DELETE FROM users WHERE id = %s"
    val = (id,)
    mycursor.execute(sql, val)
    mydb.commit()
    flash('User deleted successfully.', 'success')
    return redirect('/user')

@app.route('/get_user_data', methods=['POST'])
def get_user_data():
    _id = request.form.get('_id')

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM department")
    dept_data = mycursor.fetchall()
    mycursor.close()  

    cur = mydb.cursor()
    cur.execute("SELECT * FROM users WHERE id=%s", (_id,))
    user_data = cur.fetchone()
  
  
    return render_template('user_data.html', data=user_data, dept=dept_data )


@app.route('/set_data', methods=['POST'])
def set_data():
   # get the updated user data from the form
    pre = request.form.get('pre')
    name = request.form.get('name')
    email = request.form.get('email')
    num = request.form.get('num')
    password = request.form.get('password')
    access = request.form.get('access')
    department = request.form.get('department')
    _id = request.form.get('_id')

    # update the user data in the database
    cur = mydb.cursor()
    cur.execute(
        "UPDATE users SET pre=%s, name=%s, dept_id=%s, email=%s, number=%s, password=%s, post=%s WHERE id=%s",
        (pre , name, department , email,num, password, access, _id)
    )
    mydb.commit()
    cur.close()
    return redirect('/user')



##########################user end###########################   

##########################department###########################   
@app.route('/delete_dept/<id>', methods=['POST'])
def delete_dept(id):
    mycursor = mydb.cursor()
    sql = "DELETE FROM department WHERE id = %s"
    val = (id,)
    mycursor.execute(sql, val)
    mydb.commit()
    flash('Department deleted successfully.', 'success')
    return redirect('/department')

@app.route('/add_dept', methods=['POST'])
def add_dept():
    if request.method == 'POST':
     
        nm = request.form['deptnm']
        abbr = request.form['deptabbr']

        cursor = mydb.cursor()
        cursor.execute("INSERT INTO department(dept_name, dept_s) VALUES (%s, %s)", ( nm, abbr))
        mydb.commit()

        return redirect('/department')

@app.route('/get_dept_data', methods=['POST'])
def get_dept_data():
    _id = request.form.get('_id')
    cur = mydb.cursor()
    cur.execute("SELECT * FROM department WHERE id=%s", (_id,))
    dept_data = cur.fetchone()
    cur.close()
    return render_template('dept_data.html', data=dept_data)   

@app.route('/set_dept_data', methods=['POST'])
def set_dept_data():
    _id = request.form.get('_id')
    nm = request.form.get('deptnm')
    abbr = request.form.get('deptabbr')
    

    cur = mydb.cursor()
    cur.execute(
        "UPDATE department SET  dept_name=%s, dept_s=%s WHERE id=%s",
        (nm ,abbr, _id)
    )
    mydb.commit()
    cur.close()
    return redirect('/department')


 ##########################department end########################### 

 ##########################class ########################### 
@app.route('/get_cls_data', methods=['POST'])
def get_cls_data():
    _id = request.form.get('_id')
    cur = mydb.cursor()
    cur.execute("SELECT * FROM class WHERE id=%s", (_id,))
    cls_data = cur.fetchone()
    cur.close()
    return render_template('cls_data.html', data=cls_data)   

@app.route('/set_cls_data', methods=['POST'])
def set_cls_data():
    _id = request.form.get('_id')
   
    nm = request.form.get('clsnm')
    abbr = request.form.get('clsabbr')
    

    cur = mydb.cursor()
    cur.execute(
        "UPDATE class SET  class_name=%s, short=%s WHERE id=%s",
        (nm ,abbr, _id)
    )
    mydb.commit()
    cur.close()
    return redirect('/class')


    #return redirect(url_for('class1'))
 ##########################class end########################### 

  ##########################division########################### 

@app.route('/add_div', methods=['POST'])
def add_div():
    if request.method == 'POST':
        dept=request.form['deptnm']
        cls = request.form['clsnm']
        div = request.form['divnm']

        cursor = mydb.cursor()
        cursor.execute("SELECT id FROM department WHERE dept_name = %s", (dept,))
        row = cursor.fetchone()
        did = row[0]

        cursor = mydb.cursor()
        cursor.execute("SELECT id FROM class WHERE class_name = %s", (cls,))
        row = cursor.fetchone()
        cid = row[0]

        cursor = mydb.cursor()
        cursor.execute("INSERT INTO division(dept_id,cd_id,division) VALUES(%s,%s,%s)", ( did,cid,div))
        mydb.commit()
        cursor.close()
        return redirect('/divison')

@app.route('/delete_div/<_id>', methods=['POST'])

def delete_div(_id):
    mycursor = mydb.cursor()
    sql = "DELETE FROM division WHERE id = %s"
    val = (_id,)
    mycursor.execute(sql, val)
    mydb.commit()
    flash('Division deleted successfully.', 'success')
    return redirect('/divison')


@app.route('/get_div_data', methods=['POST'])
def get_div_data():
    _id = request.form.get('_id')
    did = request.form.get('did')

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM department")
    dept_data = mycursor.fetchall()
    mycursor.close()   
   
    mycursor1 = mydb.cursor()
    mycursor1.execute("SELECT * FROM class")
    cls_data = mycursor1.fetchall()
    mycursor1.close()  

    cur = mydb.cursor()
    cur.execute("SELECT * FROM division WHERE id=%s", (_id,))
    div_data = cur.fetchone()
    cur.close()
    return render_template('div_data.html', data=div_data , dept= dept_data ,cls=cls_data, did=did )   

@app.route('/set_div_data', methods=['POST'])
def set_div_data():
    _id = request.form.get('_id')
    dept = request.form.get('department')
    cd = request.form.get('class')
    div = request.form.get('division')
    print("row_id" , _id)
    print("dept_id" , dept)
    print("class", cd)
    cursor = mydb.cursor()
    cursor.execute("UPDATE division SET dept_id=%s, cd_id=%s, division=%s WHERE id=%s", (dept, cd, div, _id))
    mydb.commit()
    cursor.close()
    return redirect('/divison')

   ##########################division end########################### 

 ##########################batch ########################### 

@app.route('/get-divisions/<dept_id>/<cls_id>')
def get_divisions(dept_id, cls_id):
    cursor = mydb.cursor()
    cursor.execute('SELECT id, division FROM division WHERE dept_id=%s AND cd_id=%s', (dept_id, cls_id))
    div = cursor.fetchall()
    cursor.close()
    return render_template('batch.html', div=div)

@app.route('/add_batch', methods=['POST'])
def add_batch():
    if request.method == 'POST':
        dept=request.form['deptnm']
        cls = request.form['clsnm']
        div = request.form['divnm']
        batch = request.form['batch']

        cursor = mydb.cursor()
        cursor.execute("SELECT id FROM department WHERE id = %s", (dept,))
        row = cursor.fetchone()
        did = row[0]
        print(did)
        cursor = mydb.cursor()
        cursor.execute("SELECT id FROM class WHERE id = %s", (cls,))
        row = cursor.fetchone()
        cid = row[0]

        cursor = mydb.cursor()
        cursor.execute("SELECT id FROM division WHERE id = %s", (div,))
        row = cursor.fetchone()
        if row is None:
            vid = 0
        else:
            vid = row[0]

        cursor = mydb.cursor()
        query = "INSERT INTO batch(dept_id, cd_id, div_id, batch) VALUES (%s, %s, %s, %s)"
        values = (did, cid, vid, batch)
        cursor.execute(query, values)

        mydb.commit()
        cursor.close()
        return redirect('/batch')

@app.route('/delete_batch/<_id>', methods=['POST'])

def delete_batch(_id):
    mycursor = mydb.cursor()
    sql = "DELETE FROM batch WHERE id = %s"
    val = (_id,)
    mycursor.execute(sql, val)
    mydb.commit()
    flash('Batch deleted successfully.', 'success')
    return redirect('/batch')


@app.route('/get_batch_data', methods=['POST'])
def get_batch_data():
    _id = request.form.get('_id')
    did = request.form.get('did')

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM department")
    dept_data = mycursor.fetchall()
    mycursor.close()   
   
    mycursor1 = mydb.cursor()
    mycursor1.execute("SELECT * FROM class")
    cls_data = mycursor1.fetchall()
   
   

    cur = mydb.cursor()
    cur.execute("SELECT * FROM batch WHERE id=%s", (_id,))
    batch_data = cur.fetchone()
    dept_id=batch_data[1]
    cls_id=batch_data[2]
    cur.close()
    

    mycursor1 = mydb.cursor()
    mycursor1.execute('SELECT * FROM division WHERE dept_id=%s AND cd_id=%s', (dept_id, cls_id))
    div_data = mycursor1.fetchall()
    mycursor1.close()  
    return render_template('batch_data.html', data=batch_data , dept= dept_data ,cls=cls_data, div=div_data, did=did )   

@app.route('/set_batch_data', methods=['POST'])
def set_batch_data():
    _id = request.form.get('_id')
    dept = request.form.get('department')
    cd = request.form.get('class')
    div = request.form.get('division')
    bat = request.form.get('batch')
    print("row_id" , _id)
    print("dept_id" , dept)
    print("class", cd)
    print("batch", bat)
    cursor = mydb.cursor()
    cursor.execute("UPDATE batch SET dept_id=%s, cd_id=%s, div_id=%s , batch=%s WHERE id=%s", (dept, cd, div, bat,_id))
    mydb.commit()
    cursor.close()
    return redirect('/batch')

  ##########################batch end########################### 

##########################faculty########################### 
@app.route('/add_fac', methods=['POST'])
def add_fac():
    if request.method == 'POST':
        pre=request.form['pre']
        nm=request.form['name']
        init=request.form['init']
        dept=request.form['department']

        cursor = mydb.cursor()
        cursor.execute("INSERT INTO facility(pre,name,short,dept_id) VALUES(%s,%s,%s,%s)", (pre,nm,init,dept))
        mydb.commit()
        cursor.close()
        return redirect('/faculty')
    
@app.route('/delete_fac/<_id>', methods=['POST'])

def delete_fac(_id):
    mycursor = mydb.cursor()
    sql = "DELETE FROM facility WHERE id = %s"
    val = (_id,)
    mycursor.execute(sql, val)
    mydb.commit()
    flash('Faculty deleted successfully.', 'success')
    return redirect('/faculty')

@app.route('/get_fac_data', methods=['POST'])
def get_fac_data():
    _id = request.form.get('_id')
    did = request.form.get('did')

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM department")
    dept_data = mycursor.fetchall()
    mycursor.close()   
   
    mycursor1 = mydb.cursor()
    mycursor1.execute("SELECT * FROM class")
    cls_data = mycursor1.fetchall()
    mycursor1.close()  

    cur = mydb.cursor()
    cur.execute("SELECT * FROM facility WHERE id=%s", (_id,))
    fac_data = cur.fetchone()
    cur.close()
    return render_template('fac_data.html', data=fac_data , dept= dept_data ,cls=cls_data, did=did )   

@app.route('/set_fac_data', methods=['POST'])
def set_fac_data():
    _id = request.form.get('_id')
    dept = request.form.get('department')
    pre = request.form.get('pre')
    nm = request.form.get('name')
    init = request.form.get('init')
   
    cursor = mydb.cursor()
    cursor.execute("UPDATE facility SET pre=%s, name=%s, short=%s, dept_id=%s WHERE id=%s", (pre, nm, init, dept, _id))
    mydb.commit()
    cursor.close()
    return redirect('/faculty')

@app.route('/download_file')
def download_file():
    return send_from_directory('static/files', 'faculty.xlsx', as_attachment=True)

@app.route('/up_fac', methods=['POST'])
def up_fac():
    if request.method == 'POST':
      # Get the uploaded Excel file and read it using Pandas
        excel_file = request.files['file']
        df = pd.read_excel(excel_file)
        dept_id = request.form['department']
        cursor = mydb.cursor()
        for index, row in df.iterrows():
             pre = row['pre']
             name = row['name']
             short = row['short']
             query = "INSERT INTO facility (pre, name, short, dept_id) VALUES (%s, %s, %s, %s)"
             values = (pre, name, short, dept_id)
             cursor.execute(query, values)
        mydb.commit()
        cursor.close()
       
        
        return redirect('/faculty')

##########################faculty end########################### 

##########################ques###########################

@app.route('/delete_que/<id>', methods=['POST'])
def delete_que(id):
    mycursor = mydb.cursor()
    sql = "DELETE FROM que WHERE id = %s"
    val = (id,)
    mycursor.execute(sql, val)
    mydb.commit()
    flash('Question deleted successfully.', 'success')
    return redirect('/questions')

@app.route('/add_que', methods=['POST'])
def add_que():
    if request.method == 'POST':
     
        ques = request.form['ques']
        o1 = request.form['o1']
        o2 = request.form['o2']
        o3 = request.form['o3']
        o4 = request.form['o4']
      
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO que(ques, o1, o2, o3 ,o4) VALUES (%s, %s, %s, %s, %s)", ( ques, o1, o2, o3, o4))
        mydb.commit()

        return redirect('/questions')

##########################ques end###########################



##########################subject###########################
@app.route('/add_sub', methods=['POST'])
def add_sub():
    if request.method == 'POST':
        nm=request.form['subname']
        init=request.form['subinit']
        cd=request.form['subcd']
        cl=request.form['clsnm']
        sem=request.form['semister']
        th1 = 'y' if request.form.get('th') else 'n'
        pr1 = 'y' if request.form.get('pra') else 'n'
        tu1 = 'y' if request.form.get('tu') else 'n'
        dept=request.form['department']

        cursor = mydb.cursor()
        cursor.execute("insert into subject(dept_id,cd_id,name,name_s,sub_code,th,pr,tu,sem) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)", (dept,cl,nm,init,cd,th1,pr1,tu1,sem))
        mydb.commit()
        cursor.close()
        return redirect('/subject')
    
@app.route('/delete_sub/<_id>', methods=['POST'])
def delete_sub(_id):
    mycursor = mydb.cursor()
    sql = "DELETE FROM subject WHERE id = %s"
    val = (_id,)
    mycursor.execute(sql, val)
    mydb.commit()
    flash('Faculty deleted successfully.', 'success')
    return redirect('/subject')

@app.route('/download_sub_file')
def download_sub_file():
    return send_from_directory('static/files', 'subject.xlsx', as_attachment=True)


@app.route('/up_sub', methods=['POST'])
def up_sub():
    if request.method == 'POST':
        # Get the uploaded Excel file and read it using Pandas
        excel_file = request.files['file']
        df = pd.read_excel(excel_file)
        dept_id = request.form['department']
        cursor = mydb.cursor()
        for index, row in df.iterrows():
            Subject_Name = row['Subject_Name']
            Subject_Code = row['Subject_Code']
            Abrrevation = row['Abrrevation']
            Class = row['Class']
            Semester = row['Semester']
            th1 = row['TH']
            pr1 = row['PR']
            tut1 = row['TUT']

            mycursor = mydb.cursor()
            mycursor.execute("SELECT id FROM class WHERE short=%s", (Class,))
            cls = mycursor.fetchall()
            query = "INSERT INTO subject(dept_id, cd_id, name, name_s, sub_code, th, pr, tu, sem) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (dept_id, cls[0][0], Subject_Name, Abrrevation, Subject_Code, th1, pr1, tut1, Semester)
            cursor.execute(query, values)
        mydb.commit()
        cursor.close()
 
        return redirect('/subject')
    
@app.route('/get_sub_data', methods=['POST'])
def get_sub_data():
    _id = request.form.get('_id')
    did = request.form.get('did')

    cur = mydb.cursor()
    cur.execute("SELECT * FROM subject WHERE id=%s", (_id,))
    sub_data = cur.fetchone()
    cur.close()
    return render_template('sub_data.html', data=sub_data , did=did )   

@app.route('/set_sub_data', methods=['POST'])
def set_sub_data():
    _id = request.form.get('_id')
   
    nm = request.form.get('name')
    init = request.form.get('init')
    cd = request.form.get('cd')
   
    cursor = mydb.cursor()
    cursor.execute("UPDATE subject SET name=%s, name_s=%s, sub_code=%s WHERE id=%s", ( nm, init, cd, _id))
    mydb.commit()
    cursor.close()
    return redirect('/subject')

##########################subject end###########################


########################teaching record end###########################

import json

@app.route('/get-divisionstrec/<dept>/<cls>')
def get_divisionstrec(dept, cls):
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="",
      database="systemdb"
    )
    cursor2 = mydb.cursor()
    cursor2.execute('SELECT id, division FROM division WHERE dept_id=%s AND cd_id=%s', (dept, cls))
    div1 = cursor2.fetchall()

    cursor2.close()
    return json.dumps(div1)

@app.route('/get-faculties/<deptId>')
def get_faculties(deptId):
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="",
      database="systemdb"
    )
    cursor = mydb.cursor()
    cursor.execute('SELECT id, name FROM facility WHERE dept_id=%s', (deptId,))
    faculties = cursor.fetchall()
    cursor.close()
    return json.dumps(faculties)

@app.route('/get-subjects/<deptId>/<st>')
def get_subjects(deptId ,st):
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="",
      database="systemdb"
    )
    thx='y'
    
    cursor1 = mydb.cursor()
    
    if st == '1':
        cursor1.execute('select name,sub_code,id from subject where dept_id=%s AND th=%s', (deptId,thx,))
    elif st == '2':
        cursor1.execute('select name,sub_code,id from subject where dept_id=%s AND pr=%s', (deptId,thx,))
    else:
       cursor1.execute('select name,sub_code,id from subject where dept_id=%s AND tu=%s', (deptId,thx,))
    
    subjects = cursor1.fetchall()
    
    return json.dumps(subjects)

@app.route('/get-batches/<dept>/<cls>/<dfn>')
def get_batches(dept, cls, dfn):
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="",
      database="systemdb"
    )
    if dfn == '':
        dfn1=0
    else:
        dfn1=dfn
    print(dfn1)    
    cursor3 = mydb.cursor()
    cursor3.execute('SELECT id, batch FROM batch WHERE dept_id=%s AND cd_id=%s AND div_id=%s', (dept, cls, dfn1,))
    batches = cursor3.fetchall()
    cursor3.close()
    return json.dumps(batches)

@app.route('/delete_trec/<_id>', methods=['POST'])
def delete_trec(_id):
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="",
      database="systemdb"
    )
    mycursor = mydb.cursor()
    sql = "DELETE FROM teaching_rec WHERE id = %s"
    val = (_id,)
    mycursor.execute(sql, val)
    mydb.commit()
    flash('Teaching record deleted successfully.', 'success')
    return redirect('/teaching_record')


@app.route('/add_trec', methods=['POST'])
def add_trec():
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="",
      database="systemdb"
    )
    if request.method == 'POST':
        dept=request.form['dept']
        cls=request.form['cls']
        sem=request.form['sem']
        div=request.form['dfn']
        tp=request.form['tp']
        sub=request.form['sub']
        fac=request.form['fac']
     
        
        
    
        if tp == '1':
            st = 'theory'
        elif tp == '2':
               st = 'practical'  
        else :
               st = 'tutorial'  

    if div == '':
        ddid = 0
    else:
        ddid = div
    
    if st == 'theory':
        selected_batch = request.form['batch']
        bid1 = selected_batch
        print('theory',bid1)
    else:
        selected_batches = request.form.getlist('batch')
        bid1 = "," + ",".join(selected_batches) + ","
        print('other',bid1)

        
    cursor = mydb.cursor()
    cursor.execute("insert into teaching_rec(sem,dept_id,fac_id,cd_id,div_id,sub_id,t_p,bat_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", (sem,dept,fac,cls,ddid,sub,st,bid1))
    print(bid1)   
    mydb.commit()
   
    return redirect('/teaching_record')
##########################teaching record end###########################



##########################student login ###########################
@app.route('/get-divisionssl/<dept>/<cls>')
def get_divisionssl(dept, cls):
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="",
      database="systemdb"
    )
    cursor2 = mydb.cursor()
    cursor2.execute('SELECT id, division FROM division WHERE dept_id=%s AND cd_id=%s', (dept, cls))
    div1 = cursor2.fetchall()

    cursor2.close()
    return json.dumps(div1)



@app.route('/get-batchessl/<dept>/<cls>/<dfn>')
def get_batchessl(dept, cls, dfn):
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="",
      database="systemdb"
    )
    if dfn == '':
        dfn1=0
    else:
        dfn1=dfn
    print(dfn1)    
    cursor3 = mydb.cursor()
    cursor3.execute('SELECT id, batch FROM batch WHERE dept_id=%s AND cd_id=%s AND div_id=%s', (dept, cls, dfn1,))
    batches = cursor3.fetchall()
    cursor3.close()
    return json.dumps(batches)
##########################student login end###########################

##########################feedback###########################

@app.route('/add_feed', methods=['POST'])
def add_feed():

    if request.method == 'POST':
     mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="",
      database="systemdb"
    )
     num = int(request.form['fanum'])
     quesnum = int(request.form['qnum'])
     dept = request.form['dept_id']
     cls = request.form['cls_id']
     div = request.form['div_id']
     com = request.form['co']
     fac = [None] * (num+1)
     q1 = [[None for i in range(num+1)] for j in range(quesnum+1)]
     avg = [None] * (num+1)
     fact = []
     for i in range(num):
         id = "fa" + str(i+1)
         fact.append(request.form[id])
     for j in range(num):
         for i in range(quesnum):
             fd = "q" + str(i+1) + "f" + str(j+1)
             if request.form[fd] == "A":
                 q1[i][j] = 10
             elif request.form[fd] == "B":
                 q1[i][j] = 7.5
             elif request.form[fd] == "C":
                 q1[i][j] = 5
             elif request.form[fd] == "D":
                 q1[i][j] = 2.5
     # create a list of column names q1, q2, q3, ...
     column_names = ['q' + str(i+1)  for i in range(quesnum)]
     
     for j in range(num):
         for i in range(quesnum):
             print(q1[i][j], end=",")
         avg[j] = sum([x for row in q1[:quesnum] for x in [row[j]] if x is not None])/quesnum
         print("<br>" + str(avg[j]) + "<br>")
         
         cursor = mydb.cursor()
         facs = fact[j]
         print(facs)
     
         # if column does not exist in feedbackr table, create new column
         for column in column_names:
             try:
                 cursor.execute("ALTER TABLE feedbacknew ADD COLUMN " + column + " FLOAT")
             except mysql.connector.errors.ProgrammingError as e:
                 # catch the exception and do nothing, as the column may already exist
                 pass
             
         # build a dictionary of values to be inserted
         values = {'teach_id': facs, 'avg': avg[j]}
         for i in range(quesnum):
             # assign value to corresponding key in dictionary
             values[column_names[i]] = q1[i][j]
     
         # build the query string with dynamic column names and placeholders
         query_string = "INSERT INTO feedbacknew(teach_id," + ",".join(column_names) + ",avg) VALUES(" + ",".join(['%s' for i in range(quesnum+2)]) + ")"
         # get the values in correct order to match the placeholders in query string
         query_values = [values[column] for column in ['teach_id'] + column_names + ['avg']]
         cursor.execute(query_string, tuple(query_values))
         mydb.commit()
             
    cursor =  mydb.cursor() 
    cursor.execute("insert into comments(com,dept_id,cd_id,div_id) values(%s,%s,%s,%s)",(com,dept,cls,div))
    mydb.commit()
    print("successful")
         
   
    return redirect('/thankyou')


@app.route('/thankyou')
def thankyou():
    # Disable browser caching for the response
    if 'st_logged_in' in session and session['st_logged_in']:
        session['st_logged_in'] = False 
        return render_template('thankyou.html')
    else:
         return redirect('/student_verify')
#########################feedback end ###########################
@app.route('/showreport', methods=['POST'])
def showreport():
    global post_value
    if 'logged_in' in session and session['logged_in']:
        user = post_value
        mydb.commit()
        #mycursor = mydb.cursor()
       # mycursor.execute("SELECT * FROM department")
        #dept_data = mycursor.fetchall()

        #cursor = mydb.cursor()

        # SQL query to create the view
        #create_view_query = "CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `sgp` AS select `feedbacknew`.`teach_id` AS `teach_id`,avg(`feedbacknew`.`q1`) AS `q1`,avg(`feedbacknew`.`q2`) AS `q2`,avg(`feedbacknew`.`q3`) AS `q3`,avg(`feedbacknew`.`q4`) AS `q4`,avg(`feedbacknew`.`q5`) AS `q5`,avg(`feedbacknew`.`q6`) AS `q6`,avg(`feedbacknew`.`q7`) AS `q7`,avg(`feedbacknew`.`q8`) AS `q8`,avg(`feedbacknew`.`q9`) AS `q9`,avg(`feedbacknew`.`q10`) AS `q10`,avg(`feedbacknew`.`avg`) AS `avg` from `feedbacknew` group by `feedbacknew`.`teach_id` ;"

        #cursor.execute(create_view_query)

        #mydb.commit()


       # report_data = []
        #for dept in dept_data:
        #     did = dept[0]
         #    mycursor.execute("SELECT fac_id, pre, short FROM teaching_rec, facility WHERE teaching_rec.fac_id=facility.id AND teaching_rec.dept_id=%s ORDER BY teaching_rec.dept_id, teaching_rec.fac_id", (did,))
        #     faculty_data = mycursor.fetchall()
        #     dept_faculties = set()  # use a set instead of a list
        #     for fac in faculty_data:
         #       fname = fac[1] + ' ' + fac[2]
        #        dept_faculties.add(fname)  # use add() instead of append()
        #     report_data.append((dept[1], list(dept_faculties)))  # convert set back to list

        #mycursor.close()
        cursor = mydb.cursor()
        cursor.execute("select id,dept_name from department")
        dept= cursor.fetchall()
        final = []
        
        for d in dept:
            # create a new dept_list for each department
            
          
            # add the department name to the list
            
            
            did = d[0]
            cursor.execute("select * from facility where dept_id=%s", (did,))
            fac = cursor.fetchall()
            
            for f in fac:
                dept_list = []
                dept_list.append(d[1])
                facnm = f[1] + " " + f[2]
                dept_list.append(facnm)
        
                fac_id = f[0]
                query1 = '''
                SELECT 
                c.short, CASE
                        WHEN tr.div_id = 0 THEN '--'
                        ELSE dv.division
                    END AS division,
                    s.name_s,
                    tr.t_p, 
                ROUND(sgp.q1, 2) as q1, ROUND(sgp.q2, 2) as q2, ROUND(sgp.q3, 2) as q3, 
                ROUND(sgp.q4, 2) as q4, ROUND(sgp.q5, 2) as q5, ROUND(sgp.q6, 2) as q6, 
                ROUND(sgp.q7, 2) as q7, ROUND(sgp.q8, 2) as q8, ROUND(sgp.q9, 2) as q9, 
                ROUND(sgp.q10, 2) as q10, ROUND(sgp.avg, 2) as avg
                FROM 
                    teaching_rec tr
                    JOIN sgp ON tr.id = sgp.teach_id
                    JOIN class c ON tr.cd_id = c.id
                    JOIN subject s ON tr.sub_id = s.id
                    LEFT JOIN division dv ON tr.div_id = dv.id
                WHERE 
                    tr.fac_id = %s
                    ''' 
                values = (fac_id,)
                cursor.execute(query1,values)
                tr=cursor.fetchall()
                
                tr_list= []
                for t in tr:
                    trec=t[0],t[1],t[2],t[3]," feedback: ",t[4],t[5],t[6],t[7],t[8],t[9],t[10],t[11],t[12],t[13]," avg: ",t[14]
                    tr_list.append(trec)
                
                # add the tr_list to dept_list
                dept_list.append(tr_list)   
                
                final.append(dept_list)   
            # add the dept_list to final
            print(final)   
                
       

        cursor = mydb.cursor()
        query = '''
    SELECT d.dept_name, f.name,  c.short, dv.division, s.name_s , tr.t_p, 
ROUND(sgp.q1, 2) as q1, ROUND(sgp.q2, 2) as q2, ROUND(sgp.q3, 2) as q3, 
ROUND(sgp.q4, 2) as q4, ROUND(sgp.q5, 2) as q5, ROUND(sgp.q6, 2) as q6, 
ROUND(sgp.q7, 2) as q7, ROUND(sgp.q8, 2) as q8, ROUND(sgp.q9, 2) as q9, 
ROUND(sgp.q10, 2) as q10, ROUND(sgp.avg, 2) as avg
FROM teaching_rec tr
JOIN facility f ON tr.fac_id = f.id
JOIN department d ON tr.dept_id = d.id
JOIN class c ON tr.cd_id = c.id
LEFT JOIN division dv ON tr.div_id = dv.id
JOIN subject s ON tr.sub_id = s.id
JOIN sgp ON tr.id = sgp.teach_id
GROUP BY f.name
ORDER BY d.dept_name, f.name, c.short, dv.division, s.name_s
    '''
        cursor.execute(query)
        
        report_data = cursor.fetchall()  
        #print(report_data)
        now = datetime.now()
        current_month = now.strftime("%B")
        current_year = now.strftime("%Y")
        c_month = int(datetime.now().strftime("%m"))
        if 7 <= c_month <= 9:
            academic_year = f"{datetime.now().year}-{str(datetime.now().year + 1)[2:]}"
        else:
            academic_year = f"{datetime.now().year - 1}-{str(datetime.now().year)[2:]}"
        return render_template('allreport.html', user=user, rows=report_data ,final=final, current_month=current_month, current_year=current_year,ay=academic_year)
    else:
        return redirect('/')

@app.route('/showcomments', methods=['POST'])
def showcomments():
    global post_value
    if 'logged_in' in session and session['logged_in']:
        mydb.commit()


        cursor = mydb.cursor()
        cursor.execute("select id,dept_name from department")
        dept= cursor.fetchall()
        finalcom = []
        for d in dept:
            
            did = d[0]
            cursor = mydb.cursor()
            cursor.execute("select id,short from class")
            cls= cursor.fetchall()
            
            for c in cls:
                deptlist =[]
                deptlist.append(d[1])
               # print(d)
                cid=c[0]
                #print(c)
                deptlist.append(c[1])
                cursor = mydb.cursor()
                cursor.execute("select id,division from division where dept_id=%s and cd_id= %s",(did,cid))
                div= cursor.fetchall()
                print(div)
                if not div:
                    divi = "None"
                    deptlist.append(divi)
                    
                    #print(ddid)
                    cursor = mydb.cursor()
                    cursor.execute("select * from comments where dept_id=%s and cd_id = %s ",(did,cid))
                    com = cursor.fetchall()
                    comment = []
                    if not com:
                            comment.append("There are no comments available yet!!!!")
                            deptlist.append(comment)
                    else:    
                        for co in com:
                            comment.append(co[1])
                                #print("Comments: " , co[1])
                        deptlist.append(comment)
                else:    
                    for dv in div :
                        deptlist.append(dv[1])
                        ddid = dv[0]
                        #print(ddid)
                        cursor = mydb.cursor()
                        cursor.execute("select * from comments where div_id=%s",(ddid,))
                        com = cursor.fetchall()
                        comment = []
                        if not com:
                            comment.append("There are no comments available yet!!!!")
                            deptlist.append(comment)
                        else:    
                            for co in com:
                                 comment.append(co[1])
                                 #print("Comments: " , co[1])
                            deptlist.append(comment)
                finalcom.append(deptlist)
        #print(finalcom)                 
        return render_template('comments.html', com=finalcom)
    else:
        return redirect('/')


#####################Letter codes###############################

@app.route('/letdown', methods=['POST'])
def letdown ():
    global post_value
    if 'logged_in' in session and session['logged_in']:
        import datetime
        if request.method == 'POST':
            did=request.form['depart']
            fid = request.form['facid']


            cursor = mydb.cursor()
            cursor.execute("SELECT dept_name FROM department WHERE id = %s", (did,))
            row = cursor.fetchall()
            deptnm=row[0]
            mycursor = mydb.cursor()
            mycursor.execute("select * from facility where id=%s",(fid,))
            facd = mycursor.fetchall()
            for fc in facd:
                facnm = fc[1] + " " +fc[2]
                facnms = fc[1] + " " + fc[3]
            mycursor.execute("select id from teaching_rec where dept_id=%s and fac_id=%s ORDER by dept_id,fac_id",(did,fid))
            teachd = mycursor.fetchall()
            #print(facnm," ",teachd)
            ctid = []
            for t in teachd:
                #print(t)
                tid = t[0]
                   
                mycursor.execute("select teach_id ,avg from sgp where teach_id=%s and avg>=7", (tid,))

                fteach = mycursor.fetchall()
                if fteach:
                    ctid.append(fteach[0])
                    
                
          
            trec_list = []
            res =[]
            rem=[]  
            for x in ctid:
                   xid = x[0]
                
                   mycursor.execute("SELECT teaching_rec.id as tid,facility.pre as fpre,facility.name as fname,subject.name_s as sname,class.short as cls,teaching_rec.div_id as did,teaching_rec.bat_id as bid,teaching_rec.t_p as tp,department.dept_s as dept,subject.name as aname FROM teaching_rec,department,facility,class,subject where teaching_rec.dept_id=department.id AND teaching_rec.cd_id=class.id AND  teaching_rec.sub_id=subject.id AND teaching_rec.fac_id=facility.id AND teaching_rec.id = %s",(xid,))
                   trec = mycursor.fetchall()
                  
                        
                   #Excellent , good ,average 

                   for row in trec:
                       
                        
                        if str(row[5]) == "0":
                            
                            if row[7]=="theory":
                                trec_list.append((row[0], row[1], row[2], row[3],row[4],"no division", row[6],"TH",row[8],row[9]))
                            elif row[7]=="practical":
                                trec_list.append((row[0], row[1], row[2], row[3],row[4],"no division", row[6],"PR",row[8],row[9]))
                            else:
                                trec_list.append((row[0], row[1], row[2], row[3],row[4],"no division", row[6],"TH",row[8],row[9]))
                        else:
                            idd = row[5]
                            cursor2 = mydb.cursor()
                            cursor2.execute("SELECT division FROM division WHERE id=%s", (idd,))
                            info2 = cursor2.fetchall()
                            cursor2.close()
                            for row1 in info2:
                                if row[7]=="theory":
                                    trec_list.append((row[0], row[1], row[2], row[3],row[4],row1[0], row[6],"TH",row[8],row[9]))
                                elif row[7]=="practical":
                                    trec_list.append((row[0], row[1], row[2], row[3],row[4],row1[0], row[6],"PR",row[8],row[9]))
                                else:
                                    trec_list.append((row[0], row[1], row[2], row[3],row[4],row1[0], row[6],"TH",row[8],row[9]))
                              
                        mycursor.execute("select avg from sgp where teach_id=%s", (row[0],))
                        a = mycursor.fetchone()            
                        avg = a[0] * 10
                        print("average",avg)
                        result = "{:.2f}".format(avg)
                        res.append(result)
                        numeric_result = float(result)
                        if numeric_result > 90:
                             remark = "Excellent"
                        elif numeric_result <= 90 and numeric_result>80:
                              remark = "Good"
                        elif numeric_result <= 80 and numeric_result>=70:
                             remark ="Average"
                        else:
                              remark ="Poor"  
                        rem.append(remark)
                        print("result1: " , res)
                        new_list = []
                        i=0
                        for tup in trec_list:
                             new_tup = tup + (res[i], rem[i])
                             new_list.append(new_tup)
                             i+=1
                        # print("ddid it work",trec)
                        
            print(new_list)       
            today = datetime.datetime.now().strftime("%d/%m/%Y")
            now =  datetime.datetime.now()
            current_month = now.strftime("%B")
            current_year = now.strftime("%Y")
            c_month = int( datetime.datetime.now().strftime("%m"))
            if 7 <= c_month <= 9:
                academic_year = f"{ datetime.datetime.now().year}-{str( datetime.datetime.now().year + 1)[2:]}"
            else:
                academic_year = f"{ datetime.datetime.now().year - 1}-{str( datetime.datetime.now().year)[2:]}"
            return render_template('letdown.html',deptnm=deptnm,today=today,facnm=facnm,tinfo=new_list,ay=academic_year,facnms=facnms)
            
    else:
        return redirect('/')



@app.route('/letsf', methods=['POST'])
def letsf ():
    global post_value
    if 'logged_in' in session and session['logged_in']:
        import datetime
        if request.method == 'POST':
            mydb.commit()
            did=request.form['depart']
            fid = request.form['facid']
            cursor = mydb.cursor()
            wid = 1
            cursor.execute("SELECT part FROM works WHERE id = %s", (wid,))
            part = cursor.fetchone()

            cursor = mydb.cursor()
            cursor.execute("SELECT dept_name FROM department WHERE id = %s", (did,))
            row = cursor.fetchall()
            deptnm=row[0]
            mycursor = mydb.cursor()
            mycursor.execute("select * from facility where id=%s",(fid,))
            facd = mycursor.fetchall()
            for fc in facd:
                facnm = fc[1] + " " +fc[3]
            today = datetime.datetime.now().strftime("%d/%m/%Y")
            now =  datetime.datetime.now()
            current_month = now.strftime("%B")
            current_year = now.strftime("%Y")
            c_month = int( datetime.datetime.now().strftime("%m"))
            if 7 <= c_month <= 9:
                academic_year = f"{ datetime.datetime.now().year}-{str( datetime.datetime.now().year + 1)[2:]}"
            else:
                academic_year = f"{ datetime.datetime.now().year - 1}-{str( datetime.datetime.now().year)[2:]}"

        cursor = mydb.cursor()
        cursor.execute("select id,dept_name from department")
        dept= cursor.fetchall()
        final = []

        dept_list = []
        dept_list.append("sgp")
        facnm2 = "sgp"
        dept_list.append(facnm2)
        
        fac_id = fid
        query1 = '''
                SELECT 
                c.short, CASE
                        WHEN tr.div_id = 0 THEN '--'
                        ELSE dv.division
                    END AS division,
                    s.name_s,
                    tr.t_p, 
                ROUND(sgp.q1, 2) as q1, ROUND(sgp.q2, 2) as q2, ROUND(sgp.q3, 2) as q3, 
                ROUND(sgp.q4, 2) as q4, ROUND(sgp.q5, 2) as q5, ROUND(sgp.q6, 2) as q6, 
                ROUND(sgp.q7, 2) as q7, ROUND(sgp.q8, 2) as q8, ROUND(sgp.q9, 2) as q9, 
                ROUND(sgp.q10, 2) as q10, ROUND(sgp.avg, 2) as avg
                FROM 
                    teaching_rec tr
                    JOIN sgp ON tr.id = sgp.teach_id
                    JOIN class c ON tr.cd_id = c.id
                    JOIN subject s ON tr.sub_id = s.id
                    LEFT JOIN division dv ON tr.div_id = dv.id
                WHERE 
                    tr.fac_id = %s and sgp.avg<7
                    ''' 
        values = (fac_id,)
        cursor.execute(query1,values)
        tr=cursor.fetchall()
                
        tr_list= []
        for t in tr:
                trec=t[0],t[1],t[2],t[3]," feedback: ",t[4],t[5],t[6],t[7],t[8],t[9],t[10],t[11],t[12],t[13]," avg: ",t[14]
                tr_list.append(trec)
                
                # add the tr_list to dept_list
        dept_list.append(tr_list)   
                
        final.append(dept_list)   
            # add the dept_list to final
        print(final) 
                

        mycursor= mydb.cursor()
        mycursor.execute("select ques from que")
        questions = mycursor.fetchall()            
        return render_template('letsf.html',deptnm=deptnm,facnm=facnm,ay=academic_year,part=part,today=today,final=final , que =questions)
            
    else:
        return redirect('/')
    

@app.route('/letc', methods=['POST'])
def letc ():
    global post_value 
  
    if 'logged_in' in session and session['logged_in']:
        import datetime
        mydb.commit()
        if request.method == 'POST':
           
            did=request.form['depart']
            fid = request.form['facid']
            cursor = mydb.cursor()
            wid = 1
            cursor.execute("SELECT part FROM works WHERE id = %s", (wid,))
            part = cursor.fetchone()
            print(part[0],"aaaaaaaaaa")
            partq =part[0]
            if partq == 1:
                prt = "I"
                evod ="ODD"
            else:
                prt = "II"
                evod ="EVEN"      

            cursor = mydb.cursor()
            cursor.execute("SELECT dept_name FROM department WHERE id = %s", (did,))
            row = cursor.fetchall()
            deptnm=row[0]
            mycursor = mydb.cursor()
            mycursor.execute("select * from facility where id=%s",(fid,))
            facd = mycursor.fetchall()
            for fc in facd:
                facnm = fc[1] + " " +fc[2]
                facnms = fc[1] + " " + fc[3]
            mycursor.execute("select id from teaching_rec where dept_id=%s and fac_id=%s ORDER by dept_id,fac_id",(did,fid))
            teachd = mycursor.fetchall()
            #print(facnm," ",teachd)
            ctid = []
            for t in teachd:
                #print(t)
                tid = t[0]
                   
                mycursor.execute("select teach_id ,avg from sgp where teach_id=%s and avg<7", (tid,))

                fteach = mycursor.fetchall()
                if fteach:
                    ctid.append(fteach[0])
                    
                
          
            trec_list = []
            res =[]
            rem=[]  
            for x in ctid:
                   xid = x[0]
                
                   mycursor.execute("SELECT teaching_rec.id as tid,facility.pre as fpre,facility.name as fname,subject.name_s as sname,class.short as cls,teaching_rec.div_id as did,teaching_rec.bat_id as bid,teaching_rec.t_p as tp,department.dept_s as dept,subject.name as aname FROM teaching_rec,department,facility,class,subject where teaching_rec.dept_id=department.id AND teaching_rec.cd_id=class.id AND  teaching_rec.sub_id=subject.id AND teaching_rec.fac_id=facility.id AND teaching_rec.id = %s",(xid,))
                   trec = mycursor.fetchall()
                  
                        
                   #Excellent , good ,average 

                   for row in trec:
                       
                        
                        if str(row[5]) == "0":
                            
                            if row[7]=="theory":
                                trec_list.append((row[0], row[1], row[2], row[3],row[4],"no division", row[6],"TH",row[8],row[9]))
                            elif row[7]=="practical":
                                trec_list.append((row[0], row[1], row[2], row[3],row[4],"no division", row[6],"PR",row[8],row[9]))
                            else:
                                trec_list.append((row[0], row[1], row[2], row[3],row[4],"no division", row[6],"TH",row[8],row[9]))
                        else:
                            idd = row[5]
                            cursor2 = mydb.cursor()
                            cursor2.execute("SELECT division FROM division WHERE id=%s", (idd,))
                            info2 = cursor2.fetchall()
                            cursor2.close()
                            for row1 in info2:
                                if row[7]=="theory":
                                    trec_list.append((row[0], row[1], row[2], row[3],row[4],row1[0], row[6],"TH",row[8],row[9]))
                                elif row[7]=="practical":
                                    trec_list.append((row[0], row[1], row[2], row[3],row[4],row1[0], row[6],"PR",row[8],row[9]))
                                else:
                                    trec_list.append((row[0], row[1], row[2], row[3],row[4],row1[0], row[6],"TH",row[8],row[9]))
                              
                        mycursor.execute("select avg from sgp where teach_id=%s", (row[0],))
                        a = mycursor.fetchone()            
                        avg = a[0] * 10
                        print("average",avg)
                        result = "{:.2f}".format(avg)
                        res.append(result)
                        numeric_result = float(result)
                        if numeric_result > 90:
                             remark = "Excellent"
                        elif numeric_result <= 90 and numeric_result>80:
                              remark = "Good"
                        elif numeric_result <= 80 and numeric_result>=70:
                             remark ="Average"
                        else:
                              remark ="POOR"  
                        rem.append(remark)
                        print("result1: " , res)
                        new_list = []
                        i=0
                        for tup in trec_list:
                             new_tup = tup + (res[i], rem[i])
                             new_list.append(new_tup)
                             i+=1
                        # print("ddid it work",trec)
                        
            print(new_list)       
            today = datetime.datetime.now().strftime("%d/%m/%Y")
            now =  datetime.datetime.now()
            current_month = now.strftime("%B")
            current_year = now.strftime("%Y")
            c_month = int( datetime.datetime.now().strftime("%m"))
            if 7 <= c_month <= 9:
                academic_year = f"{ datetime.datetime.now().year}-{str( datetime.datetime.now().year + 1)[2:]}"
            else:
                academic_year = f"{ datetime.datetime.now().year - 1}-{str( datetime.datetime.now().year)[2:]}"  
            return render_template('letc.html',deptnm=deptnm,facnm=facnm,ay=academic_year,today=today,prt=prt,evod=evod,tinfo=new_list,facnms=facnms)
            
    else:
        return redirect('/')
      
#####################Delete databse codes###############################

@app.route('/deldivbtr')
def deldivbtr():
    global post_value
    if 'logged_in' in session and session['logged_in']:
        mycursor = mydb.cursor()
        mycursor.execute("DELETE FROM division")
        mydb.commit()
        mycursor = mydb.cursor()
        mycursor.execute("Delete From teaching_rec")
        mydb.commit()
        mycursor = mydb.cursor()
        mycursor.execute("Delete From batch")
        flash('Division , Batch and Teaching_record Data Deleted Successfully.', 'success1')
        mydb.commit()
        return redirect('/admin')
    else:
        return redirect('/')

@app.route('/delfeedcom')
def delfeedcom():
    global post_value
    if 'logged_in' in session and session['logged_in']:
        mydb.commit()
        mycursor = mydb.cursor()
        mycursor.execute("DELETE FROM feedbacknew")
        mydb.commit()
        mycursor = mydb.cursor()
        mycursor.execute("Delete From comments")
        mydb.commit()
        flash('Feedback and Comments Data Deleted Successfully.', 'success')
        mydb.commit()
        return redirect('/admin')
    else:
        return redirect('/')
    
@app.route('/delfacd')
def delfacd():
    global post_value
    if 'logged_in' in session and session['logged_in']:
        mydb.commit()
        mycursor = mydb.cursor()
        mycursor.execute("DELETE FROM facility")
        flash('Faculty Data Deleted Successfully.', 'success2')
        mydb.commit()
        return redirect('/admin')
    else:
        return redirect('/')    
    
@app.route('/delsubd')
def delsubd():
    global post_value
    if 'logged_in' in session and session['logged_in']:
        mydb.commit()
        mycursor = mydb.cursor()
        mycursor.execute("DELETE FROM subject")
        flash('Subject Data Deleted Successfully .', 'success3')
        mydb.commit()
        return redirect('/admin')
    else:
        return redirect('/')      













#if __name__ == "__main__":
 #   app.run(debug=True, port=8000)
import os

port = int(os.environ.get('PORT', 8000)) # default port is 5000
app.run(host='0.0.0.0', port=port)
