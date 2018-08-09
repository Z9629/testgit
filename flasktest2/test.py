from flask import Flask,request,render_template
import os
app = Flask(__name__)
@app.route('/',methods=['GET','POST'])
def home():
    path = '/'
    all_file = os.listdir(path)
    return render_template('hello.html',all_file = all_file)

if __name__ == '__main__':
    app.run()



