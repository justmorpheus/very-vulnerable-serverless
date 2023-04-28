from flask import Flask, redirect, url_for, request, render_template, jsonify
import urllib.request
import subprocess
import json
import datetime as date
import re
import pickle
import base64

app = Flask(__name__)
app.secret_key = 'ThisisSuperFlagBySecurityDojo'

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

#Injection Vulnerability
@app.route('/welcome/<name>')
def success(name):
    return 'welcome %s' % name

#Injection Vulnerability
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['name']
        return redirect(url_for('success', name=user))
    else:
        user = request.args.get('name')
        return redirect(url_for('success', name=user))


#SSRF Vulnerability
@app.route('/redirect')
def web():
    try:
        site=request.args.get('url')
        response = urllib.request.urlopen(site)
        output=json.dumps(response.read().decode('utf-8'))
        return jsonify({"output": output}), 200
    except:
        return ("Error Ocurred")
#aws s3 ls

#Command Execution
@app.route('/date')
def command():
    try:
        cmd = request.args.get('exec')
        count = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        stdout, stderr = count.communicate()
        #print(stdout.decode())
        return jsonify({"output": stdout.decode()}), 200

    except:
        return ("Error Ocurred")

# ReDoS vulnerability demonstration route
@app.route('/redos')
def redos():
    try:
        # Get user-supplied string
        user_string = request.args.get('string')
        
        # Record start time
        start_time = date.datetime.now()

        # Use a maliciously-crafted regular expression that will take a long time to execute
        malicious_regex = "^(a+)+b$"
        
        # Record end time
        end_time = date.datetime.now()

        # Attempt to match the user-supplied string to the regular expression
        match = re.match(malicious_regex, user_string)
        if match:
            return "<html><body><p><h3 style='background-color:SpringGreen;'>String matches regex</p><p>Response time: {}</h3></p></body></html>".format(end_time - start_time)
        else:
            return "<html><body><p><h3 style='background-color:IndianRed;'>String does not match regex</p><p>Response time: {}</h3></p></body></html>".format(end_time - start_time)
    except:

        return ("Error Ocurred")

#Reference: https://github.com/CalfCrusher/Python-Pickle-RCE-Exploit
# Python deserialization vulnerability demonstration route - part_1
@app.route('/deserial', methods=['POST'])
def deserial():
    try:
        data = base64.urlsafe_b64decode(request.form['pickled'])
        pickle.loads(data)
        return 'pickled successfully', 200
    except Exception as e:
        return f'Error occurred while pickling: {e}', 500

# Python deserialization vulnerability demonstration route - part_2
#class AttackObject:
#    def __init__(self):
#        self.value = 'attack'


#@app.route('/attack', methods=['POST'])
#def attack():
    

    # Deserialize the user-supplied data
    #data = request.get_data()
    #print (data)
    #obj = pickle.loads(data)
    #print (obj)
    # Return a response based on the deserialized object
    #if obj == 'attack':
        #return 'Attack successful!'
    #elif isinstance(obj, AttackObject):
        #return 'Attack detected!'
    #else:
        #return 'Invalid input.'

