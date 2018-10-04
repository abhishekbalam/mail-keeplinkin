import os
from flask import Flask, render_template, request, redirect, jsonify, abort
import requests
from flask_mail import Mail, Message
import db

app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.zoho.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ['zoho_username2']
app.config['MAIL_PASSWORD'] = os.environ['zoho_password2']
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

data1={
	"links":{
		"title":"Title",
		"description":"Subtitle",
		"url":"https://mail.keeplink.in/"
		}
	}

@app.route('/')	
def main():
	return render_template('index.html')

@app.route('/sent/')	
def sent():
	# return render_template('sent.html')
	links="ljdlkajsldkjalskdjlaksjdlkasd<br>dakshdksd<br>asldjkas"
	return render_template('email.html', subject="fsdfs", links=links)	

def verify(email):
	token="7996de2b-d743-4536-a107-5252fec5c828"
	url="https://api.trumail.io/v2/lookups/json?email="+email+"&token="+token
	print(url)
	data=requests.get(url).json()
	return data['deliverable']

@app.route('/send', methods = ['POST'])	
def send():
	data=request.form
	
	email=data['email'].strip()
	subject=data['subject'].strip()
	links=data['links'].strip()
	print(links)
	# links=links.replace('\n', '<br>')
	arr=links.split('\n')
	
	links="<ol>\n"
	
	for i in range(len(arr)):
		links="<li>"+arr(i)+"</li>"
	
	links=links+"<ol>"
	
	if(verify(email)==False):
		text="Invalid Email"
		return render_template('error.html', text=text, again=True)

	mail = Mail(app)
	msg = Message(subject, sender = ('Keeplink.in', 'mail@keeplink.in'), recipients = [email])
	msg.html = render_template('email.html', subject=subject, links=links) 
	test=mail.send(msg)
	
	print(test)
	return redirect("/sent/", code=302)

if __name__ == '__main__':
	app.jinja_env.auto_reload = True
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	# app.run(debug=True, port=4000)
	app.run(debug=True)