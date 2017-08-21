# -*- coding: utf-8 -*-
#!/usr/bin/env python


import json

import validictory
from flask import Flask, request, abort, make_response

import Network

import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-p", help="listen port", type=int, default=1111) 
#parser.add_argument("-f", help="listen port", type=str, default='../config/radiant.cfg') 
args = parser.parse_args()

app = Flask(__name__)
#app.config.from_pyfile('radiant.cfg')
#app.config.from_pyfile(args.f)


def build_task(parameters):
    task = parameters.to_dict()
    depth = task.get("depth", None)
    if depth is not None:
        try:
            task['depth'] = float(int(depth))
        except ValueError:
            task['depth'] = 5.0
    else:
        task['depth'] = 5.0
    
    probability = task.get("probability", None)
    if probability is not None:
        probability = probability.lower()
        if probability in ('true', 't', 'yes', 'y', '1'):
            task["probability"] = True
        elif probability in ('false', 'f', 'no', 'n', '0'):
            task["probability"] = False
        else:
            abort(400, "Invalid value for boolean parameter probability")
    query = task.get("query", None)
    if query is not None:
        query = query.lower()
        task['query'] = query
        
    return task


@app.route("/network", methods=["GET", "POST"])
def query_network():
    if request.method == "GET":
        task = build_task(request.args)
    elif request.method == "POST":
        task = request.get_json(silent=True, force=True)
        if task is None:
            task = build_task(request.form)
    else:
        abort(400, "Unsupported request method")

    schema = {
        "type": "object",
        "properties": {
            "query": {"type": "string"},
        },
    }
    try:
        validictory.validate(task, schema)
    except ValueError as e:
        abort(400, e)


    app.logger.info("Received new task [{}]".format(request.method))

    
    global SNet
    Q_result = SNet.query(task['query'])
    try:
        if task['probability']:
            #Q_result['probability'] = SNet.page_rank(task['query'],depth=task['depth'])
            Q_result['probability'] = SNet.get_page_rank(task['query'])
    except:
        pass
    #result = translator.translate(strategy, task)
    
    
    

    result = json.dumps(Q_result, encoding='utf-8', ensure_ascii=False, indent=4)
    callback = task.get('jsoncallback', None)
    result = '%s(%s)' % (callback, result) if callback is not None else result

    response = make_response(result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    #response.headers.add('Access-Control-Allow-Methods','GET, POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Methods','*')
    response.headers.add('Access-Control-Allow-Headers','Origin, Content-Type, X-Auth-Token')
    response.headers['Content-Type'] = 'text/json;charset=utf-8'
    
    response.headers.add('Content-Type', 'application/javascript')

    return response


if __name__ == "__main__":
    global SNet
    SNet = Network.SNetwork("Network.p")
    app.run(host="0.0.0.0", port=args.p)
