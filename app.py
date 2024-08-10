from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, linear_kernel
import mysql.connector
import re

app = Flask(__name__)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Sakshi@95",
  database="RESUME"
)

mycursor = mydb.cursor()

class TechnicalSkills:
    def __init__(self):
        self.df = pd.read_csv('technical skills.csv').dropna()
        # Create a TfidfVectorizer object
        self.tfidf = TfidfVectorizer(stop_words='english')

        # Fit and transform the 'Skills' column
        self.tfidf_matrix = self.tfidf.fit_transform(self.df['Skills'])

        # Calculate the cosine similarity between the skills
        self.cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)
        
    # Function to get the most similar skills for a given skill
    def get_similar_skills(self,skill):
        # Get the index of the given skill
        self.skill_index = self.df[self.df['Skills'] == skill].index[0]

        # Get the pairwise similarity scores of all skills with that skill
        self.similar_skills = list(enumerate(self.cosine_sim[self.skill_index]))

        # Sort the skills based on the similarity scores
        self.sorted_similar_skills = sorted(self.similar_skills, key=lambda x: x[1], reverse=True)

        # Get the scores of the 10 most similar skills
        self.sorted_similar_skills = self.sorted_similar_skills[2:15]

        # Get the skill names from the indices
        self.skill_list = [self.df['Skills'][i[0]] for i in self.sorted_similar_skills]
        self.skill_set = set(self.skill_list)
        self.skill_list = list(self.skill_set)
        return self.skill_list[:5]
    
    def get_course_skills(self, coursenm):
        self.skillsList = np.random.choice(self.df[self.df['Course']==coursenm]['Skills'].values,5)
        return self.skillsList
    
class SoftSkills:
    def __init__(self):
        self.ds = pd.read_csv('soft skills final.csv').dropna()
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.ds['Meaning'] = self.ds['Meaning'].fillna('')
        self.tfidfMatrix = self.tfidf.fit_transform(self.ds['Meaning'])
        #self.cosine_sin = linear_kernel(self.tfidfMatrix, self.tfidfMatrix)
        self.indices = pd.Series(self.ds.index, index=self.ds['Soft Skills']).drop_duplicates()
    
    def get_recommendation(self, title):
        cosine_sin = linear_kernel(self.tfidfMatrix, self.tfidfMatrix)
        idx = self.indices[title]
        simlarity = enumerate(cosine_sin[idx])
        simlarity = sorted(simlarity, key=lambda x:x[1], reverse=True)
        simlarity = simlarity[1:10]

        sin_index = [i[0] for i in simlarity]
        #print(self.ds_movies['original_title'].iloc[sin_index])
        return list(self.ds['Soft Skills'].iloc[sin_index])
    
    def getDefault(self):
        return list(self.ds['Soft Skills'].sample(n=5).values)
    
skill=[]

@app.route('/')
def home():
   return render_template('index1.html')


@app.route('/signup', methods=['POST','GET'])
def signup():
    mesage = ''
    if request.method == 'POST':
        userName = request.form['userName']
        ph = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        
        query = f"SELECT * FROM USERS WHERE email = '{email}'"
        mycursor.execute(query)
        account = mycursor.fetchone()
        if account:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not userName or not password or not email:
            mesage = 'Please fill out the form !'
        else:
            sql = f"INSERT INTO users (fullnm,phno,email,passwd) VALUES ('{userName}','{ph}', '{email}','{password}')"
            mycursor.execute(sql)
            mydb.commit()
            mesage = 'You have successfully registered !'
            return redirect(url_for('signin'))
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('signup.html', mesage = mesage)
    

@app.route('/signin', methods=['POST','GET'])
def signin():
    mesage = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        select_user_query = f"SELECT fullnm FROM USERS WHERE email = '{email}' AND passwd = '{password}'"
        mycursor.execute(select_user_query)
        user = mycursor.fetchone()
        if user:
            mesage = 'Logged in successfully !'
            return redirect(url_for('personal'))
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('signin.html', mesage = mesage)

@app.route('/personal', methods=['POST','GET'])
def personal():
    return render_template('personal.html')


@app.route('/person',methods = ['POST', 'GET'])
def person():
   return render_template('personal.html')

@app.route('/education',methods = ['POST', 'GET'])
def education():
   return render_template('education.html')

@app.route('/experiance',methods = ['POST', 'GET'])
def experiance():
   return render_template('experiance.html')


@app.route('/social',methods = ['POST', 'GET'])
def social():
   return render_template('social.html')


@app.route('/project',methods = ['POST', 'GET'])
def project():
   return render_template('project.html')

@app.route('/preview', methods=['POST','GET'])
def preview():
    return render_template('preview.html')

@app.route('/template1', methods=['POST','GET'])
def template1():
    return render_template('template1.html')

@app.route('/template2', methods=['POST','GET'])
def template2():
    return render_template('template2.html')

@app.route('/technical',methods = ['POST', 'GET'])
def technical():   
    if request.method == 'POST':
        selected = request.form.get('bank')
        sk = request.form['ip2']        
        skill.append(sk)
    
    l = TechnicalSkills()

    list1=[]
    slen = (skill.__len__())-1
    reg_indx=slen-1

    def getSkills(slen):
        if slen >= 0:
            try:
                return l.get_similar_skills(skill[slen])
            except:
                slen-=1
                return l.get_similar_skills(skill[slen])
            
        elif slen<0:
            return l.get_course_skills('Data Science')
        else:
            return ['Sakshi','Potdar']
    
    def regenerate(self):
        reglist=[]
        if (reg_indx)>0:
            reglist = l.get_course_skills(skill(reg_indx))
            slen-=1
        else:
            reglist = l.get_course_skills('Data science')
        return reglist
    '''
    if 'addskill' in request.form:
        return render_template('skills.html',skills = skill,rec_skills=getSkills(slen))
    
    elif 'regenrate' in request.form:
        return render_template('skills.html',skills = skill,rec_skills=getSkills(slen))
    else:
        return render_template('skills.html')
    '''
    return render_template('skills.html',skills = skill,rec_skills=getSkills(slen))

softskilllist=[]
@app.route('/softskill',methods = ['POST', 'GET'])
def softskill():   
    if request.method == 'POST':
        sk = request.form['inputskill']        
        softskilllist.append(sk)
    
    soskill = SoftSkills()

    list1=[]
    slen = (softskilllist.__len__())-1
    reg_indx=slen-1

    def getSkills(slen):
        if slen >= 0:
            try:
                return soskill.get_recommendation(softskilllist[slen])
            except:
                slen-=1
                return soskill.get_recommendation(softskilllist[slen])
            
        elif slen<0:
            return soskill.getDefault()
        else:
            return ['Sakshi','Potdar']
    
    
    return render_template('softskills.html',skills = softskilllist,soft_skills=getSkills(slen))


if __name__=='__main__':
    app.run(debug=True,port=8000)