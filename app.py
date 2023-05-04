from flask import Flask, render_template , request , jsonify , json
from utalties.Filter import Filter
from utalties.Frequency import Frequency
from utalties.Histogram import Histogram
from utalties.Hough import Hough
from utalties.contour import Contour
import numpy as np
import cv2
import os
from skimage.util import img_as_ubyte
from skimage import data, color
from skimage.draw import ellipse_perimeter


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
## Hough Tab ##

@app.route('/hough' , methods = ['POST', 'GET'] )
def hough():
    if request.method == 'POST':
        #to save imported image in hough tab
        img = request.files.get('HoughInput')
        name = './static/imgs/' + img.filename + '.jpg'
        img.save(name)

        # print(img)
        return render_template('main.html')
    else:
        return render_template('main.html')
@app.route('/shape' , methods =['POST','GET'])
def shape():
    if request.method == 'POST':
        shapetype = request.json['type']
        parameter1_val = request.json['parameter1val']
        parameter1_name = request.json['parameter1name']
        parameter2_val= request.json['parameter2val']
        parameter2_name= request.json['parameter2name']
        if shapetype == 'Circle-shape':
            img = './static/imgs/HoughInput.jpg'
            acc = Hough.accumulator_calc(img,int(parameter2_val),int(parameter1_val))
            circles = Hough.detect_circle(acc,int(parameter2_val),int(parameter1_val))
            imgr = cv2.imread(img)
            if len(circles) >1:
                Hough.draw_circles(circles,imgr)
        elif shapetype == 'Line-shape':
            img = './static/imgs/HoughInput.jpg'
            img = cv2.imread(img,cv2.IMREAD_GRAYSCALE)
            img = cv2.Canny(img,50,150)
            lines,img = Hough.hough_transform(img,int(parameter1_val),np.pi*2/180,int(parameter2_val))
            # print(lines)
            img = './static/imgs/HoughInput.jpg'
            imgr = cv2.imread(img)
            for line in lines:
                cv2.line(imgr,(int(line[0]),int(line[1])),(int(line[2]), int(line[3])), (0, 0, 255), 2)
                cv2.imwrite('./static/imgs/HoughOutput.jpg', imgr)
        elif shapetype == "Ellipse-shape":
            img = './static/imgs/HoughInput.jpg'
            img = cv2.imread(img,cv2.IMREAD_GRAYSCALE)
            edges = cv2.Canny(img, 50, 150)
            data = Hough.hough_ellipse(
                edges, accuracy=20, min_size=20, max_size=50)
            j = 0
            edges = color.gray2rgb(img_as_ubyte(edges))
            while j < len(data):
                best = list(data[j])
                yc, xc, a, b = (int(round(x)) for x in best[1:5])
                if a == 0 or b == 0:
                    j += 1
                    continue
                for x in range(len(data)):
                    if np.abs(data[x][1]-yc) <= 20 and np.abs(data[x][2]-xc) <= 20:
                        data[x][3] = data[x][4] = 0
                orientation = best[5]
                cy, cx = ellipse_perimeter(yc, xc, a, b, orientation)
                for i in range(len(cy)):
                    if cy[i] >= edges.shape[0]:
                        cy[i] = edges.shape[0]-1
                    if cx[i] >= edges.shape[1]:
                        cx[i] = edges.shape[1]-1
                    print(cy[i], cx[i])
                img[cy, cx] = (0, 0, 255)
                # Draw the edge (white) and the resulting ellipse (red)
                edges[cy, cx] = (250, 0, 0)
                j += 1
            cv2.imwrite('./static/imgs/HoughOutput.jpg', img)
            # print(data)
        print(shapetype)
        print(parameter1_name)
        print(parameter1_val)
        print(parameter2_name)
        print(parameter2_val)
        # parameter 1 , 2 vary according to the shape [line , circle , ellipse]
        return render_template("main.html")
    else:
        return render_template("main.html")
## End of Hough Tab ##
## Contour Tab ##
@app.route('/contour' , methods = ['POST', 'GET'] )
def contour():
    if request.method == 'POST':
        #to save imported image in contour tab
        img = request.files.get('ContourInput')
        name = './static/imgs/' + img.filename + '.jpg'
        img.save(name)
        print(img)
        return render_template('main.html')
    else:
        return render_template('main.html')

@app.route('/applycontour' , methods = ['POST', 'GET'] )
def apply_contour():
    if request.method == 'POST':
        alpha = request.json['alpha']
        beta = request.json['beta']
        gamma = request.json['gamma']
        x = request.json['x']
        y = request.json['y']
        h = request.json['height']
        w = request.json['width']
        Contour.apply_snake('./static/imgs/ContourInput.jpg',int(x),int(y),int(w),int(h),float(alpha),float(beta),float(gamma))
        print(alpha)
        print(beta)
        print(gamma)
        print(x)
        print(y)
        print(h)
        print(w) 
        #with each new selection , post request is initiated and u will have the updated data 
        #after handling , save output image as ContourOutput.jpg :)
        return render_template('main.html')
    else:
        return render_template('main.html')
## End of Contour Rab ##


if __name__ == '__main__':
    app.run(debug=True)