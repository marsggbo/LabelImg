import glob
import os
import json

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

global HISTORY
global IT_IMGs

patients = sorted(os.listdir('./static/NCP/'), key=lambda x:int(x.split('/')[-1]))
slices = {}
for patient in patients:
    patient_path = f"./static/NCP/{patient}"
    for scan in sorted(os.listdir(patient_path), key=lambda x:int(x.split('/')[-1])):
        scan_path = f"{patient_path}/{scan}"
        imgs = []
        for img in sorted(os.listdir(scan_path), key=lambda x:int(x.split('/')[-1].split('.')[0])):
            imgs.append(f"{scan_path}/{img}")
        slices[scan_path] = imgs

global index
global path_imgs

index = 0
path_imgs = list(slices.items())

@app.route("/")
def main():
    try:
        data = path_imgs[index]
        path, images = data
        return render_template('index.html', path=path, images=images, num=len(images), index=index)
    except (Exception, SystemExit, KeyboardInterrupt, GeneratorExit) as e:
        print(str(e))

@app.route("/getimage")
def getimage():
    name = next(path_imgs)
    return name

@app.route('/label', methods = ['POST', 'GET'])
def label():
    global index
    if request.method == 'POST':
        specify_index = request.form['idx']
        label = request.form['label']
        if label == 'pre':
            index -= 1
        elif label == 'next':
            index += 1
        if index < 0: index = len(path_imgs) - 1
        if index > len(path_imgs) - 1: index = 0
        if specify_index:
            index = int(specify_index)
        print(index, label)
        return redirect(url_for('main'))
    else:
        label = request.args.get('label')
        if label == 'pre':
            index -= 1
        elif label == 'next':
            index += 1
        if index < 0: index = len(path_imgs) - 1
        if index > len(path_imgs) - 1: index = 0
        print(label)
        return redirect(url_for('main'))


if __name__ == '__main__':
    app.run(debug=True, port=6006)
