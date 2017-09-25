from flask import Flask
from model import *
from flask import render_template, request, url_for, redirect
import json
from flask import jsonify
app = Flask(__name__)
keyword = None

@app.route('/', methods=["GET","POST"])
def hello_world():
    #tasks = myTable().get_data()
    with open('/home/qialiu/PycharmProjects/untitled2/my_doc.json') as json_data:
        json_table = json.load(json_data)
    #return jsonify(tasks)
    #print tasks
        return render_template('index.html', result = json_table)

@app.route('/search', methods=["POST"])
def search():
    project = request.form['word']
    res = test(project)

    #print res
    return render_template('search.html', res = res, project= project)


def test(project):
    return project

if __name__ == '__main__':
    app.run(debug=True)
