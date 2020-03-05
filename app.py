from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def index():
    f = open("data/irrigation.conf")
    time_list = { 1: [], 2: [], 3: [], 4: []}

    for line in f:
        data = line.split(' ')
        time_list[int(data[0])].append(data[1] + ' - ' + data[2])
    f.close()
    print(time_list)
    return render_template('index.html', time_list=time_list)


@app.route('/start/<int:section>')
def start(section):

    return 'start: ' + str(section)


@app.route('/stop/<int:section>')
def stop(section):

    return 'start: ' + str(section)


if __name__ == '__main__':
    app.run()
