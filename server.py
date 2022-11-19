from flask import Flask, render_template, request, redirect, url_for
from methods import dnnMethod, svmMethod
from threading import Lock, Thread
from queue import Queue


app = Flask('Auto LTP')
methods_dict = {'DNN': dnnMethod, 'SVM': svmMethod}
queue = Queue()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/DNN')
def DNN():
    return render_template('DNN.html')


@app.route('/SVM')
def SVM():
    return render_template('SVM.html')


@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        method = request.form['method']
        dirpath = request.form['dirpath']
        tasks = request.form['tasks']
        print(method, dirpath, tasks)
        global queue
        thread1 = Thread(target=work, args=(method, dirpath, tasks, queue))
        thread1.start()
        return render_template('result.html')
    elif request.method == 'GET':
        lock = Lock()
        lock.acquire()
        flag = queue.get() if not queue.empty() else False
        lock.release()
        if flag:
            queue = Queue()
            return redirect(url_for('finish'))
        else:
            return render_template('result.html')


@app.route('/finish')
def finish():
    return render_template('finish.html')


def main():
    app.run(host='0.0.0.0', port=8848, debug=True)


def work(method, dirpath, tasks, queue):
    tasks = tasks.split(',')
    method = methods_dict[method]
    method(dirpath, tasks, queue)


if __name__ == '__main__':
    main()
