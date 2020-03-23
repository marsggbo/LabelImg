import glob
import os
import json

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

global HISTORY
global IT_IMGs

# IMGs = sorted(glob.glob('./static/data/*/*.jpg'))
classes = ['cyst',
           'Folliculitis',
           'Post_Inflammatory_Hyperpigmentation',
           'Skn_tag',
           'vitiligo']
IMGs = []
for c in classes:
    IMGs.extend(glob.glob(f'./static/data/{c}/*.jpg'))
IMGs = sorted(IMGs)
IT_IMGs = iter(IMGs)

with open('history.json', 'r') as f:
    HISTORY = json.load(f)


@app.route("/")
def main():
    try:
        name = next(IT_IMGs)
        while name in HISTORY:
            name = next(IT_IMGs)
        return render_template('index.html', name=name, history=list(HISTORY.items()))
    except (Exception, SystemExit, KeyboardInterrupt, GeneratorExit) as e:
    # except KeyboardInterrupt as e:
        print(str(e))
        with open('history.json', 'w') as f:
            json.dump(HISTORY, f, indent=4)
        return str(e)
    finally:
        print("Saving history ...")
        with open('history.json', 'w') as f:
            json.dump(HISTORY, f, indent=4)

@app.route("/getimage")
def getimage():
    name = next(IT_IMGs)
    return name

@app.route('/label', methods = ['POST', 'GET'])
def label():
    if request.method == 'POST':
        name = request.form['name']
        label = request.form['label']
        print(name, label)
        HISTORY[name] = label
        return redirect(url_for('main'))
    else:
        name = request.args.get('name')
        label = request.args.get('label')
        print(name, label)
        HISTORY[name] = label
        return redirect(url_for('main'))


if __name__ == '__main__':
    app.run(debug=True, port=6006)
