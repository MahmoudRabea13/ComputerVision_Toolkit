from flask import Flask, render_template , request , jsonify , json
from utalties.Filter import Filter
from utalties.Frequency import Frequency
from utalties.Histogram import Histogram
import numpy as np
import cv2
import os


app = Flask(__name__)
@app.route('/')
def main():
    return render_template('main.html')


@app.route('/filter' , methods = ['POST', 'GET'] )
def filter():
    if request.method == 'POST':
        img = request.files.get('original_img')
        name = './static/imgs/' + img.filename + '.jpg'
        img.save(name)
        os.remove("./static/imgs/noisy.jpg")
        print(img)
        return render_template('main.html')
    else:
        return render_template('main.html')

## Filter Tab ##
@app.route('/applyfilter' , methods =['POST','GET'])
def applyfilter():
    if request.method == 'POST':
        filtertype = request.json['type']
        kernal = request.json['kernalsize']
        raduis= request.json['raduissize']
        if os.path.exists("./static/imgs/noisy.jpg") != True:
            img = cv2.imread("./static/imgs/original_img.jpg",cv2.IMREAD_GRAYSCALE)
        else:
            img = cv2.imread("./static/imgs/noisy.jpg",cv2.IMREAD_GRAYSCALE)
        if filtertype == "gaussian-filter":
            new_img = Filter.gaussian_filter(Filter,img,int(kernal),1)
            Filter.display_image(Filter,new_img,'filtered_img')
        elif filtertype == "avg-filter":
            new_img = Filter.average_filter(Filter,image_data=img,filter_size=int(kernal))
            Filter.display_image(Filter,new_img,'filtered_img')
        elif filtertype == "mad-filter":
            new_img = Filter.median_filter(Filter,img,int(kernal))
            Filter.display_image(Filter,new_img,'filtered_img')
        elif filtertype == "hp-filter":
            new_img = Filter.low_high_pass(Filter,img,'high',int(raduis))
            Filter.display_image(Filter,new_img,'filtered_img')
        elif filtertype == "lp-filter":
            new_img = Filter.low_high_pass(Filter,img,'low',int(raduis))
            Filter.display_image(Filter,new_img,'filtered_img')
        print(filtertype)
        print(kernal)
        print(raduis)        
        return render_template("main.html")
    else:
        return render_template("main.html")

@app.route('/noise' , methods =['POST','GET'])
def noise():
    if request.method == 'POST':
        noiseType = request.json['type']
        print(noiseType)
        img = cv2.imread("./static/imgs/original_img.jpg",cv2.IMREAD_GRAYSCALE)
        if noiseType == "uniform-noise":
            new_img = Filter.noisy('uniform',img)
            Filter.display_image(Filter,new_img,'noisy')
        elif noiseType == "gaussian-noise":
            new_img = Filter.noisy('gaussian',img)
            Filter.display_image(Filter,new_img,'noisy')
        elif noiseType == "sp-noise":
            new_img = Filter.noisy('s&p',img)
            Filter.display_image(Filter,new_img,'noisy')
        return render_template("main.html")
    else:
        return render_template("main.html")
## End of Filter Tab ##
## Hybrid Tab ##
@app.route('/hybrid' , methods = ['POST', 'GET'] )
def hybrid():
    if request.method == 'POST':
        img1 = request.files.get('firstimg')
        img2 = request.files.get('secondimg')
        if img1 != None:
            name = './static/imgs/' + img1.filename + '.jpg'
            img1.save(name)
        if img2 != None:
            name = './static/imgs/' + img2.filename + '.jpg'
            img2.save(name)
        print(img1)
        print(img2)
        return render_template("main.html")
    else:
        return render_template("main.html")
@app.route('/hybridraduis' , methods = ['POST', 'GET'] )
def hybrid_raduis():
    if request.method == 'POST':
        raduis1 = request.json['img1_raduis']
        raduis2 = request.json['img2_raduis']
        print(raduis1)
        print(raduis2)
        img1 = cv2.imread('./static/imgs/firstimg.jpg',cv2.IMREAD_GRAYSCALE)
        img2 = cv2.imread('./static/imgs/secondimg.jpg',cv2.IMREAD_GRAYSCALE)
        img1 = Filter.low_high_pass(Filter,img1,'low',int(raduis1))
        img2 = Filter.low_high_pass(Filter,img2,'high',int(raduis2))
        new_img = img1+img2 
        Filter.display_image(Filter,new_img,'hybrid_img')
        return render_template("main.html")
    else:
        return render_template("main.html")
## End of Hybrid Tab ##
## Histogram Tab ##
@app.route('/histogram' , methods = ['POST', 'GET'] )
def histogram():
    if request.method == 'POST':
        img = request.files.get('inputimg')
        if img != None:
            name = './static/imgs/' + img.filename + '.jpg'
            img.save(name)
        print(img)
        read_img = cv2.imread('./static/imgs/inputimg.jpg')
        RGB_hist = Histogram.RGB_histogram(Histogram,read_img)
        Histogram.Plot_RGBHistogram(Histogram,RGB_hist,"./static/imgs/RGB_histogram.jpg")
        Gray_hist =Histogram.Gray_histogram_Compute(Histogram,read_img)
        Histogram.Gray_histogram_Plot(Histogram,Gray_hist,"./static/imgs/Gray_histogram.jpg")
        equalizedImg = Histogram.img_equalize(Histogram,read_img)
        Filter.display_image(Filter,equalizedImg,'equalized_img')
        RGB_equalized = Histogram.RGB_histogram(Histogram,equalizedImg)
        Histogram.Plot_RGBHistogram(Histogram,RGB_equalized,"./static/imgs/RGB_histogram_equalized.jpg")
        Gray_equalized =Histogram.Gray_histogram_Compute(Histogram,equalizedImg)
        Histogram.Gray_histogram_Plot(Histogram,Gray_equalized,"./static/imgs/Gray_histogram_equalized.jpg")
        return render_template("main.html")
    else:
        return render_template("main.html")
## End of Histogram Tab ##
## Edge Detection Tab ## 
@app.route('/edge' , methods = ['POST', 'GET'] )
def edge():
    if request.method == 'POST':
        img = request.files.get('inputedge')
        if img != None:
            name = './static/imgs/' + img.filename + '.jpg'
            img.save(name)
        print(img)
        return render_template("main.html")
    else:
        return render_template("main.html")
@app.route('/edgetype' , methods = ['POST', 'GET'] )
def edgetype():
    if request.method == 'POST':
        type = request.json
        print(type)
        img = cv2.imread('./static/imgs/inputedge.jpg',cv2.IMREAD_GRAYSCALE)
        new_img = Filter.edge_detection(Filter,img,str(type))
        new_img = new_img*150
        Filter.display_image(Filter,new_img,"outputedge")
        return render_template("main.html")
    else:
        return render_template("main.html")
@app.route('/threshold' , methods = ['POST', 'GET'] )
def threshold():
    if request.method == 'POST':
        type = request.json
        print(type)
        img = cv2.imread('./static/imgs/inputedge.jpg',cv2.IMREAD_GRAYSCALE)
        vv1 = Frequency.thres_finder(Frequency,img, thres=30, delta_T=1.0)
        # threshold the image
        if str(type) == 'localthreshold':
            local_thresh = Frequency.local_threshold(Frequency,img, 7)
            Filter.display_image(Filter,local_thresh,"threshold")
        if str(type) == 'globalthreshold':
            global_thresh = Frequency.global_threshold(Frequency,img, vv1, 255, 0)
            Filter.display_image(Filter,global_thresh,"threshold")
        return render_template("main.html")
    else:
        return render_template("main.html")
## End of Edge detection Tab ##



if __name__ == '__main__':
    app.run(debug=True)