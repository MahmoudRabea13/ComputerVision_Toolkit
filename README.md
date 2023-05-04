<div id = 'top'></div>

# ComputerVision_Toolkit 💻
### Web-based app that implements computer vision concepts.
_______________________________________________________________
## <p align='left'>Contents:</p>

* [Overview](#overview)
* [Requirements](#requirements)
* Project description
    * [Task1](#task1)
    * [Task2](#task2)
    * [Task3](#task3)
    * [Task4](#task4)
* <p><a href="#members">Team meambers</a></p>

Overview
============

This project was done on 4 stages each with its own features as follows: 
### 1. Task 1: 
- Add different noise types and apply different filtering methods.
- Do histogram equalization and normalization to both RGB & Gray image histograms.
- Hybrid image.
- Apply different Edge detection techniques.
### 2. Task 2:
- Hough Transform.
- Snake active image contouring.
### 3. Task 3:
- Harris corner detection.
- SIFT Matching.
- sum of differences SSD.
### 4. Task 4:
- Diferent Segmentation techniques.
- Different Thresholding algorithms *Local&Global*

Requirements
============
```
Flask==2.2.2

matplotlib==3.6.1
numpy==1.22.4
opencv_python==4.6.0.66
scipy==1.10.1

```
```
Front-end => vanillaJS, CSS and HTML
Back-end => Flask
```

Task1
============
1. Apply image Filters: [Median](https://en.wikipedia.org/wiki/Median_filter#:~:text=The%20median%20filter%20is%20a,edge%20detection%20on%20an%20image) , [Gaussian](https://en.wikipedia.org/wiki/Gaussian_filter#:~:text=In%20electronics%20and%20signal%20processing,would%20have%20infinite%20impulse%20response) , [Averaging](https://en.wikipedia.org/wiki/Geometric_mean_filter) , [Low-pass](https://www.l3harrisgeospatial.com/docs/lowpassfilter.html#:~:text=A%20low%20pass%20filter%20is,reducing%20the%20high%20frequency%20information) and [High-pass](https://www.l3harrisgeospatial.com/docs/highpassfilter.html#:~:text=A%20high%20pass%20filter%20is,reducing%20the%20low%20frequency%20information) 
2. Add different noise to the image: [Uniform](https://en.wikipedia.org/wiki/Image_noise#Quantization_noise_(uniform_noise)) , [Gaussian](https://en.wikipedia.org/wiki/Image_noise#Gaussian_noise) and [Salt-Pepper](https://en.wikipedia.org/wiki/Image_noise#Salt-and-pepper_noise)    
3. Apply histogram Equalization and view RGB & Gray histogram 
4. apply Low & High pass filters to two images and show their [Hybrid image](https://en.wikipedia.org/wiki/Hybrid_image)
5. apply different Edge detection methods: [Sobel](https://homepages.inf.ed.ac.uk/rbf/HIPR2/sobel.htm) , [Canny](https://homepages.inf.ed.ac.uk/rbf/HIPR2/canny.htm) , [Roberts](https://homepages.inf.ed.ac.uk/rbf/HIPR2/roberts.htm) , [Prewitt](https://homepages.inf.ed.ac.uk/rbf/HIPR2/prewitt.htm)
6. Apply Local & Global Thresholding 

| `Median filter` | ![alt text](https://github.com/MahmoudRabea13/ComputerVision_Toolkit/blob/main/snaps/medianF.jpg) |
| --- | --- |
| `Gaussian filter` | ![alt text](https://github.com/MahmoudRabea13/ComputerVision_Toolkit/blob/main/snaps/gaussianF.jpg) |
| `Averaging filter` | ![alt text](https://github.com/MahmoudRabea13/ComputerVision_Toolkit/blob/main/snaps/averagingF.jpg) |
| `Low pass filter` | ![alt text](https://github.com/MahmoudRabea13/ComputerVision_Toolkit/blob/main/snaps/lowpassF.jpg) |
| `High pass filter` | ![alt text](https://github.com/MahmoudRabea13/ComputerVision_Toolkit/blob/main/snaps/highpassF.jpg) |
| `S&P Noise` | ![alt text](https://github.com/MahmoudRabea13/ComputerVision_Toolkit/blob/main/snaps/s%26pN.jpg) |
| `Hybrid` | ![alt text](https://github.com/MahmoudRabea13/ComputerVision_Toolkit/blob/main/snaps/hybrid.jpg) |
| `Sobel edge detection` | ![alt text](https://github.com/MahmoudRabea13/ComputerVision_Toolkit/blob/main/snaps/sobel.jpg) |
| `Canny edge detection`| ![alt text](https://github.com/MahmoudRabea13/ComputerVision_Toolkit/blob/main/snaps/canny.jpg) |
| `Roperts edge detection` | ![alt text](https://github.com/MahmoudRabea13/ComputerVision_Toolkit/blob/main/snaps/roberts.jpg) |
| `Prewitt edge detection` | ![alt text](https://github.com/MahmoudRabea13/ComputerVision_Toolkit/blob/main/snaps/prewitt.jpg) |
| `Local thresholding` | ![alt text](https://github.com/MahmoudRabea13/ComputerVision_Toolkit/blob/main/snaps/localthreshold.jpg) |
| `Global thresholding` | ![alt text](https://github.com/MahmoudRabea13/ComputerVision_Toolkit/blob/main/snaps/globalthreshold.jpg) |
| `Histogram` | ![alt text](https://github.com/MahmoudRabea13/ComputerVision_Toolkit/blob/main/snaps/Tab2_RGB.jpg) |

Task2
============
1. Apply [Hough Transform](https://en.wikipedia.org/wiki/Hough_transform#:~:text=The%20Hough%20transform%20is%20a,shapes%20by%20a%20voting%20procedure.) *lines,circles & ellipses*
2. Apply [active Snake contouring](https://en.wikipedia.org/wiki/Active_contour_model)    

| `Line` | ![alt text](https://github.com/MahmoudRabea13/ComputerVision_Toolkit/blob/main/snaps/houghlines.jpg) |
| --- | --- |
| `Circle` | ![alt text](https://github.com/MahmoudRabea13/ComputerVision_Toolkit/blob/main/snaps/CircleHough.jpg) |
| `Ellipse` | ![alt text](https://github.com/MahmoudRabea13/ComputerVision_Toolkit/blob/main/snaps/Houghellipse2.jpg) |
| `Snake contour` | ![alt text](https://github.com/MahmoudRabea13/ComputerVision_Toolkit/blob/main/snaps/contouroutput.jpg) |

Task3
============
1. [Harris corner detection](https://en.wikipedia.org/wiki/Harris_corner_detector#:~:text=The%20Harris%20corner%20detector%20is,improvement%20of%20Moravec's%20corner%20detector.) 
2. [SIFT](https://www.sciencedirect.com/topics/computer-science/scale-invariant-feature-transform#:~:text=Scale%2DInvariant%20Feature%20Transform%20(SIFT)%E2%80%94SIFT%20is%20an,Keypoints%20Detection%2C%20and%20Feature%20Description.)
3. [SSD](https://en.wikipedia.org/wiki/Sum_of_absolute_differences#:~:text=In%20digital%20image%20processing%2C%20the,block%20being%20used%20for%20comparison.) 

| `Harris` | ![alt text](https://github.com/MahmoudRabea13/ComputerVision_Toolkit/blob/main/snaps/harris.jpg) |
| --- | --- |
| `SIFT` | ![alt text](https://github.com/MahmoudRabea13/ComputerVision_Toolkit/blob/main/snaps/sift.jpg) |
| `SSD` | ![alt text](https://github.com/MahmoudRabea13/ComputerVision_Toolkit/blob/main/snaps/ssd.jpg) |

Task4
============
1. Apply [Kmeans](https://www.geeksforgeeks.org/image-segmentation-using-k-means-clustering/), [Mean shift](https://towardsdatascience.com/understanding-mean-shift-clustering-and-implementation-with-python-6d5809a2ac40#:~:text=Mean%20shift%20is%20an%20unsupervised,clusters%20in%20the%20feature%20space.),[Region Growing](https://en.wikipedia.org/wiki/Region_growing#:~:text=Region%20growing%20is%20a%20simple,selection%20of%20initial%20seed%20points.) and [Agglomerative](https://ieeexplore.ieee.org/document/1044838/) Segmentation techniques
2. Apply [Otsu](https://en.wikipedia.org/wiki/Otsu%27s_method) , [Spectral](https://medium.com/abraia/hyperspectral-image-classification-with-python-7dce4ebcda0a) and [Optimal](https://www.researchgate.net/publication/32973889_Optimal_thresholding_for_image_segmentation) Thresholding  

| `K-means` | ![alt text](https://github.com/MahmoudRabea13/ComputerVision_Toolkit/blob/main/snaps/Kmean.jpg) |
| --- | --- |
| `Mean shift` | ![alt text](https://github.com/MahmoudRabea13/ComputerVision_Toolkit/blob/main/snaps/Mean%20Shift.jpg) |
| `Region Growing` | ![alt text](https://github.com/MahmoudRabea13/ComputerVision_Toolkit/blob/main/snaps/RegionGrowing.jpg) |
| `Agglomerative` | ![alt text](https://github.com/MahmoudRabea13/ComputerVision_Toolkit/blob/main/snaps/aggo.jpg) |
| `Ostu` | ![alt text](https://github.com/MahmoudRabea13/ComputerVision_Toolkit/blob/main/snaps/otsuglobal.png) |
| `Spectral` | ![alt text](https://github.com/MahmoudRabea13/ComputerVision_Toolkit/blob/main/snaps/spectralglobal.png) |
| `Optimal` | ![alt text](https://github.com/MahmoudRabea13/ComputerVision_Toolkit/blob/main/snaps/optimalglobal.png) |

_____________________
<div id='members'>
   
### Task Submitted by 3rd year SBME2024 students 💉:
* [Ahemd Hassan](https://github.com/ahmedhassan187) 
* [Dina khalid](https://github.com/dina-khalid) 
* [Abdelrahman Yasser](https://github.com/Abdelrhman012)
* [Mohammed Nasser](https://github.com/MohamedNasser8) 
* [Mahmoud Rabea](https://github.com/MahmoudRabea13) 

</div>

<p align="right"><a href="#top">back to top</a></p>

