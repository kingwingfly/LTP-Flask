from flask import Flask, render_template, request, redirect, url_for
from methods import dnnMethod, svmMethod, generate_lst
# from EventTriplesExtraction.triple_extraction import TripleExtractor
from EventTriplesExtraction.baidu_svo_extract import SVOParser
from EventTriplesExtraction.pattern_event_triples import ExtractEvent
from threading import Lock, Thread
from queue import Queue



app = Flask('Auto LTP')
methods_dict = {'DNN': dnnMethod, 'SVM': svmMethod}
triples_methods = {'LTP': 'TripleExtractor', 'Baidu DDParser': SVOParser, 'jieba': ExtractEvent}
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

@app.route('/Triples')
def Triples():
    return render_template('/Triples.html')


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

@app.route('/triplesResult', methods=['GET', 'POST'])
def triplesResult():
    if request.method == 'POST':
        cuda = request.form['cuda']
        method = request.form['method']
        dirpath = request.form['dirpath']
        print(cuda, method, dirpath)
        global queue
        thread2 = Thread(target=triplesWork, args=(cuda, method, dirpath, queue))
        thread2.start()
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
    queue.put(True)


def triplesWork(cuda, method, dirpath, queue):
    Method = triples_methods[method]
    extrator = Method()
    for content in generate_lst(dirpath):
        if method in ['LTP', 'Baidu DDParser']:
            svos = extrator.triples_main(content)
            # todo 对百度选用cuda
            print(svos)
        else:
            events, spos = extrator.phrase_ip(content)
            spos = [i for i in spos if i[0] and i[2]]
            for spo in spos:
                print(spo)
    queue.put(True)

if __name__ == '__main__':
    main()
