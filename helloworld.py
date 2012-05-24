#dhsfuture
#Ma Tang Hao 5C23
#An app that requires the CT or Promo result from the user, and output the admission Score and courses he can currently choose from
#09-05-2012
import cgi
import csv
import time
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class MainPage(webapp.RequestHandler):
	def get(self):
		#Welcome Page
		self.response.out.write('''
			<!DOCTYPE html>
			<html>
				<head>
					<title>Welcome!</title>
					<link type="text/css" rel="stylesheet" href="/stylesheets/style.css" />
					<link href='http://fonts.googleapis.com/css?family=Nunito:700' rel='stylesheet' type='text/css'>
					<link href='http://fonts.googleapis.com/css?family=Salsa' rel='stylesheet' type='text/css'>
				</head>
				<body>
					<center>
                    <div align="center" style="top: 50%;">
					<h2 style="font-family: 'Nunito', sans-serif;">WHERE IS MY FUTURE?</h2>
                    <img src="https://www.google.com/a/dhs.sg/images/logo.gif?alpha=1" />
                    </div>
                    <div align="center" class="border">
                    <ol>
                    	<li>1.The app is currently only open to those who chose <b>8</b> subjects.</li>
                        <br />
        				<li>2.All the course prerequisite is recorded according to the <b>90 percentile</b>.</li>
                        <br />
                        <li>3.Only courses from <b>NUS,NTU and SMU</b> are included in the App.</li>
                        <br />
                        <li>4.You can key in your Common Test or Promo result in the App</li>
                        <br />
                        <li>5.The App will calculate your Admission score and give <b>suggestions</b> for the future courses</li>
					</ol>
					</div>
					
					<form action="/input" method="post" >
						<b>Plz key in your dhsmail account:</b><input type="text" placeholder="E.g. koh.jingyu" name="name"></input><b>@dhs.sg</b>
						<br />
						<input type="submit" value="Enter your marks and predict your future!" style="background-color: rgb(255,255,0)">
					</form>
					
                    </center>
                    <center><footer>&copy;Ma Tang Hao <a href="mailto:"ma.tanghao@dhs.sg">Feedback</a></footer></center>
				</body>
			</html>
			''')

class Input(webapp.RequestHandler):
  def post(self):
	#initialize input page
	comb=csv.reader(open('comb.csv'),delimiter=',')
	found=False
	subjectlist={'COMP':'Computing',' CSC':'CSC','CLL':'CLL','GSC':'GSC','ART':'Art','PHY':'Physics','MATH':'Maths','CHEM':'Chemistry','ECONS':'Economics','GEO':'Geography','BIO':'Biology','ELIT':'Literature','HIST':'History','FRENCH':'French','MUS':'Music'}
	#find the user in student name list
	for person in comb:
		if person[0]==self.request.get('name'):
			combination=person
			found=True
			break
	if found:
		#delete unncessary terms
		while '' in combination:combination.remove('')
		name=combination.pop(1)
		klass=combination.pop(1)
		try:
			combination.remove('H1CL')
		except:
			pass
		del combination[0]
		combination.remove('H1GP')
		#greeting!
		self.response.out.write('''
		<!DOCTYPE html>
		<html>
		<head>
			<link type="text/css" rel="stylesheet" href="/stylesheets/style.css" />
			<title>Where's My Future?</title>
			<link href='http://fonts.googleapis.com/css?family=Nunito:700' rel='stylesheet' type='text/css'>
			<link href='http://fonts.googleapis.com/css?family=Salsa' rel='stylesheet' type='text/css'>
			<script language=javascript>

			function check(){
			if((document.form.scoreGP.value== "")||(document.form.score1.value== "")||(document.form.score2.value== "")||(document.form.score3.value== "")||(document.form.score4.value== ""))
			{
				alert("Plz!Leave No Blank!");
				return false;
				}
		
			}
			</script>
		</head>
		<body>
			<div class="logo">
				<img src="https://www.google.com/a/dhs.sg/images/logo.gif?alpha=1">
			</div>
			<center>
			<h2 style="font-family: 'Nunito', sans-serif;">Hello, %s from %s!</h2>'''%(name,klass))
		#count how many subjects the user picked
		if len(combination)==4:
			combie=[]
			for subject in combination:
				combie.append([subject[:2],subject[2:]])
			#put the h1 subject at the last place if there is one
			for subject in combie:
				if subject[0]=='H1':
					combie[combie.index(subject)],combie[-1]=combie[-1],combie[combie.index(subject)]
					break
			self.response.out.write('''
			<div align="center" class="border">
			<form action="/analysis" name="form" method="post" >
				H1GP:<input type="text" name="scoreGP" style="width:60px" onKeyPress="if(event.keyCode!=46 && event.keyCode!=45 && (event.keyCode<48 || event.keyCode>57)) event.returnValue=false"></input><b>%</b>
				<br /><br />
				PW:
				<select name="scorePW">
					<option value="A">A</option>
					<option value="B">B</option>
					<option value="C">C</option>
					<option value="D">D</option>
					<option value="E">E</option>
					<option value="S">S</option>
					<option value="U">U</option>
				</select>
				<br /><br />''')
			for i in range(3):
				self.response.out.write('''
							<input type="text" name="subject%s" class="subject"  value="%s" readonly></input><b>:</b><input style="width:60px" type="text" name="score%s" onKeyPress="if(event.keyCode!=46 && event.keyCode!=45 && (event.keyCode<48 || event.keyCode>57)) event.returnValue=false"></input><b>%%</b>
								<br /><br />'''%((i+1),'H2 '+subjectlist[combie[i][1]],(i+1)))
			self.response.out.write(	
				'''<input type="text" name="h1h2" class="subject" value="%s" readonly></input><input type="text" name="subject4" class="subject" value="%s" readonly></input><b>:</b>
				<input type="text" style="width:60px" name="score4" onKeyPress="if(event.keyCode!=46 && event.keyCode!=45 && (event.keyCode<48 || event.keyCode>57)) event.returnValue=false"></input><b>%%</b>
				<br /><br />
				Anyway, choose your in your O-level Chinese grade?
				<br /><br />
				<select name="Chinesescore">
					<option value="A1">A1</option>
					<option value="A2">A2</option>
					<option value="B3">B3</option>
					<option value="B4">B4</option>
					<option value="C5">C5</option>
					<option value="D6">D6</option>
					<option value="D7">D7</option>
					<option value="E8">E8</option>
					<option value="E9">E9</option>
					<option value="F">F</option>
					<option value="U">U</option>
				</select>
				<br /><br />
				Did you pass your Sec4 EOY Maths1 AND Maths2?
				<br /><br />
				<select name="Maths">
					<option value="yes">Yes</option>
					<option value="no">No</option>
				</select>
				
				</div>
				<input type="submit" value="Calculate" onclick= "return   check() ">
					
			</form>
			</center>
			<center><footer>&copy;Ma Tang Hao <a href="mailto:"ma.tanghao@dhs.sg">Feedback</a></footer></center>
		</body>
	</html>
					
					'''%(combie[3][0],subjectlist[combie[3][1]]))
		else:
			self.response.out.write('''
			<center>
			<p>Sorry, this app is currently only available for students who picked seven subjects.</p>
			</center>

			<center><footer>&copy;Ma Tang Hao <a href="mailto:"ma.tanghao@dhs.sg">Feedback</a></footer></center>
			</body>
			</html>''')
	else:
		self.response.out.write('''
			<!DOCTYPE html>
			<html>
				<head>
					<title>Welcome!</title>
					<link type="text/css" rel="stylesheet" href="/stylesheets/style.css" />
					<link href='http://fonts.googleapis.com/css?family=Nunito:700' rel='stylesheet' type='text/css'>
					<link href='http://fonts.googleapis.com/css?family=Salsa' rel='stylesheet' type='text/css'>
				</head>
				<body>
					<center>
                    <div align="center" style="top: 50%;">
					<h2 style="font-family: 'Nunito', sans-serif;">WHERE IS MY FUTURE?</h2>
                    <img src="https://www.google.com/a/dhs.sg/images/logo.gif?alpha=1" />
                    </div>
                    <div align="center" class="border">
                    <ol>
                    	<li>1.The app is currently only open to those who chose <b>8</b> subjects.</li>
                        <br />
        				<li>2.All the course prerequisite is recorded according to the <b>90 percentile</b>.</li>
                        <br />
                        <li>3.Only courses from <b>NUS,NTU and SMU</b> are included in the App.</li>
                        <br />
                        <li>4.You can key in your Common Test or Promo result in the App</li>
                        <br />
                        <li>5.The App will calculate your Admission score and give <b>suggestions</b> for the future courses</li>
					</ol>
					</div>
					
					<form action="/input" method="post" >
						<b>Plz key in your dhsmail account:</b><input type="text"  name="name"></input><b>@dhs.sg</b>
						<br />
						<center><div style="color:red">this person is not from DHS senior high</div></center>
						<br />
						<input type="submit" value="Enter your marks and predict your future!" style="background-color: rgb(255,255,0)">
					</form>
					
                    </center>
                    <center><footer>&copy;Ma Tang Hao <a href="mailto:"ma.tanghao@dhs.sg">Feedback</a></footer></center>
				</body>
			</html>
			''')

class Analysis(webapp.RequestHandler):
  def post(self):
	#check for correct input
	correct=True
	for element in ['scoreGP','score1','score2','score3','score4']:
		try:
			mark=float(self.request.get(element))
			if mark>100 or mark<0:
				correct=False
		except:
			correct=False
	if correct:
		#initialize
		subject=[]
		gradelist={'A':20,'B':17.5,'C':15,'D':12.5,'E':10,'S':5,'U':0}
		chineselist={'A1':10,'A2':10,'B3':8.75,'B4':7.5,'C5':6.25,'C6':5,'D7':2.5,'E8':3,'E9':0,'F':0,'U':0}
		grade=[['A',70],['B',60],['C',55],['D',50],['E',45],['S',40],['U',0]]
		subject.append(['PW',(self.request.get('scorePW')).encode('gbk')])
		subject.append(['GP',float(self.request.get('scoreGP'))])
		for i in range(4):
			subject.append([(self.request.get('subject%s'%(i+1))).encode('gbk'),float(self.request.get('score%s'%(i+1)))])
			
		for i in range(1,6):
			for j in range(7):
				if subject[i][1]>=grade[j][1]:
					subject[i][1]=grade[j][0]
					break	
		
		if self.request.get('h1h2')=='H1':
			s=0
			
			s=(gradelist[subject[0][1]]+gradelist[subject[1][1]]+gradelist[subject[5][1]])*0.5
			for i in range(2,5):
				s+=gradelist[subject[i][1]]
						
		else:
			s=0
			min=[999,0]
			for i in range(2,6):
				if gradelist[subject[i][1]]<min[0]:
					min[0]=gradelist[subject[i][1]]
					min[1]=i
			s=(gradelist[subject[0][1]]+gradelist[subject[1][1]])*0.5
			for i in range(2,6):
				if i==min[1]:
					s+=gradelist[subject[i][1]]*0.5
				else:
					s+=gradelist[subject[i][1]]
			switch=subject[min[1]]
			subject[min[1]]=subject[5]
			subject[5]=switch
			
			for element in subject[2:-1]:
                                if  'H2' == element[0][:2]:
                                        pass
                                else:
                                        
                                        element[0]='H2'+element[0]
                                
                        if 'H2' in subject[-1][0]:subject[-1][0]=subject[-1][0][2:]
                        
		if (s+chineselist[self.request.get('Chinesescore')])*0.9 >= s : 
			s=(s+chineselist[self.request.get('Chinesescore')])*0.9

		self.response.out.write('''
		<!DOCTYPE html>
					<html>
				<head>
					<link type="text/css" rel="stylesheet" href="/stylesheets/style.css" />
					<title>Admission Score: %s</title>
				</head>

			<body>
			<div class="logo">
					<img src="https://www.google.com/a/dhs.sg/images/logo.gif?alpha=1">
			</div>
			<center>
				<h3>Your subject combination is:</h3>
				<form style="width:270px" action='/future' method='post'>
				<div style="border:dotted">
				<b>H1 General Paper:</b><input class="score" type= 'text'   name='GPgrade' value='%s' readonly></input>
				<br />
				<b>H1 Project Work:</b><input class="score" type= 'text'   name='PWgrade' value='%s'   readonly></input>
				<br />
				<input class="subject" type= 'text'   name='subject1' value='%s'   readonly><b>:</b></input><input class="score" type= 'text'   name='grade1' value='%s'   readonly></input>
				<br />
				<input class="subject" type= 'text'   name='subject2' value='%s'   readonly><b>:</b></input><input class="score" type= 'text'   name='grade2' value='%s'   readonly></input>
				<br />
				<input class="subject" type= 'text'   name='subject3' value='%s'   readonly><b>:</b></input><input class="score" type= 'text'   name='grade3' value='%s'   readonly></input>
				<br />
				<input class="subject" type= 'text'   value='%s'   readonly><b>:</b></input><input class="score" type= 'text'   value='%s'   readonly></input>
				<input class="h1h2" type= 'hidden'   name='H1H2' value='%s'   readonly><input class="subject" type= 'hidden'   name='subject4' value='%s'   readonly></input><input class="score" type= 'hidden'   name='grade4' value='%s'   readonly></input>
				<br />
				<b>O-Level Chinese:</b></b><input class="score" type= 'text'   name='Chinesegrade' value='%s'   readonly></input>
				<br />
				<b>Pass in O-Level Mathematics</b><input style='border:0px;text-align:center;width:35px;background-color:transparent' type= 'text'   name='Maths' value='%s'   readonly>
				<br />
				<b>And your Admission Score is </b><input style='border:0px;text-align:center;width:35px;background-color:transparent' type= 'text'   name='score' value='%s'   readonly></input>
				<br />
				</div>
				<input type="submit" value="Where's my future?">
				
			</form>
			<input type="button" onClick="window.history.back()" value="I input my scores wrongly" style="background-color:#F30"></input>
			<br />
			<footer>&copy;Ma Tang Hao <a href="mailto:"ma.tanghao@dhs.sg">Feedback</a></footer>
			</center>
			</body>
			</html>'''%(s,subject[1][1],subject[0][1],subject[2][0],subject[2][1],subject[3][0],subject[3][1],subject[4][0],subject[4][1],(self.request.get('h1h2')+' '+subject[5][0]),subject[5][1],self.request.get('h1h2'),subject[5][0],subject[5][1],self.request.get('Chinesescore'),self.request.get('Maths'),s))
	else:
		self.response.out.write('''
		<!DOCTYPE html>
		<html>
		<head>
			<link type="text/css" rel="stylesheet" href="/stylesheets/style.css" />
			<title>OI!</title>
		</head>
		<body>
			<div class="logo">
				<img src="https://www.google.com/a/dhs.sg/images/logo.gif?alpha=1">
			</div>
			<center>
				<p>Plz!Enter your marks properly!Your mark should be real numbers between 0 and 100 (percentage)</p>
				<input type="button" onClick="window.history.back()" value="Re-input" style="background-color:#F30"></input>
			</center>
			<center><footer>&copy;Ma Tang Hao <a href="mailto:"ma.tanghao@dhs.sg">Feedback</a></footer></center>
		</body>
		</html>''')
			
    
class Future(webapp.RequestHandler):
  def post(self):
		#initialize
		subject={}
		h2=''
		for i in range(3):
			h2+=(self.request.get('grade%s'%(i+1)))
		#sort
		h2 = "".join((lambda x:(x.sort(),x)[1])(list(h2)))
		
		subject['GP']=self.request.get('GPgrade')
		subject['PW']=self.request.get('PWgrade')
		subject['Chinese']=self.request.get('Chinesegrade')
		if self.request.get('Maths')=='yes':
			subject['OMaths']='D'
		else:
			subject['OMaths']='F'
		
		
		
		for i in range(3):
			subject[self.request.get('subject%s'%(i+1))]=self.request.get('grade%s'%(i+1))
		subject[self.request.get('H1H2')+self.request.get('subject4')]=self.request.get('grade4')
		score=self.request.get('score')
		
		start=-1
		requirement=csv.reader(open('requirement.csv'),delimiter=',')
		self.response.out.write('''
		<!DOCTYPE html>
			<html>
				<head>
					<title>Your Future is...</title>
					<link type="text/css" rel="stylesheet" href="/stylesheets/style.css" />
				</head>
				<body>
					<div class="logo">
						<img src="https://www.google.com/a/dhs.sg/images/logo.gif?alpha=1">
					</div>
					<center>
						<p>With your current result, here is the course you can ge into:</p>
						<div class="results">
			''')
		havefuture=False
		
		for course in requirement:
			if (float(course[0])<=float(score)) and (course[1]>=h2) and (course[2]>=self.request.get('grade4')):
				
				match=True
				pointer=3
				for i in course[4::2]:
					pointer+=2
					rlist=i.split('/')
					rgrade=course[pointer]
					subnotmatch=True
					for element in rlist:
						if subject.get(element)==None or subject.get(element)>rgrade:
							
							pass
						else:
							subnotmatch=False
							break
					if subnotmatch:
						match=False
						break
				if match:
					self.response.out.write('''<h5>%s</h5>'''%(course[3]))
					havefuture=True
		if not havefuture:
			self.response.out.write('''
										<p>You need to work harder!!</p>
									   <p>No Local University accepts this grade!</p>
									
									   
									   ''')
		self.response.out.write('''</div>
									<p>* Courses that require interview or test</p>
									<a href="http://www.nus.edu.sg/oam/apply/local/prerequisites/BYA-prerequisites.html"><b>NUS Prerequisites</b></a>
                                                                        <br />
									<a href="http://admissions.ntu.edu.sg/International/UndergraduateApplicants-backup/beforeapply/Pages/AdmissionRequirements.aspx#minimum"><b>NTU Prerequisites</b></a>
                                                                        <br />
									<a href="http://www.smu.edu.sg/admissions/pages/apply_to_smu/Apply-to-SMU.asp"><b>SMU Prerequisites</b></a>
									</center>
									
									<center><footer>&copy;Ma Tang Hao <a href="mailto:"ma.tanghao@dhs.sg">Feedback</a></footer></center>
									</body>
									</html>''')
							
			
		
		
		
			


          
		
application = webapp.WSGIApplication([
  ('/', MainPage),
  ('/input', Input),
  ('/analysis', Analysis),
  ('/future', Future)

], debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
