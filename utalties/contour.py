import numpy as np
import cv2
import math
class Contour():
    def snake(img,x,y,alpha = 0.001,beta = 0.4,gamma = 100,
                sigma = 20, iterations =500):
        """
        The snake algorithm to segment image
        Parameters
        ------
        img : ndarray
            input image

        ------
        x,y : ndarry
            X-coordinate and Y-coordinate of the initial contour
        alpha,beta: number
            The set of parameters of internal energy
        gamma : number
            Parameter cotrolling the external engery
        sigma : number
            Standard deviation
        iterations : number
            The number of iteration
        """

        # compute the matrix
        N = np.size(x)
        a = gamma*(2*alpha+6*beta)+1
        b = gamma*(-alpha-4*beta)
        c = gamma*beta
        p = np.zeros((N,N))
        p[0] = np.c_[a,b,c,np.zeros((1,N-5)),c,b]
        for i in range(N):
            p[i] = np.roll(p[0],i)
        p = np.linalg.inv(p)
        # filter the image
        smoothed = cv2.GaussianBlur((img-img.min()) / (img.max()-img.min()),(89,89),sigma)
        giy,gix  = np.gradient(smoothed)
        gmi = (gix**2+giy**2)**0.5
        gmi = (gmi - gmi.min()) / (gmi.max() - gmi.min())
        Iy,Ix = np.gradient(gmi)

        # avoid the curvature evolve to the outside of the image
        def fmax(x,y):
            x[x < 0] = 0
            y[y < 0] = 0
            x[x > img.shape[1]-1] = img.shape[1]-1
            y[y > img.shape[0]-1] = img.shape[0]-1
            return y.round().astype(int),x.round().astype(int)
        for i in range(iterations):
            fex = Ix[fmax(x,y)]
            fey = Iy[fmax(x,y)]
            x = np.dot(p,x + gamma*fex)
            y = np.dot(p,y + gamma*fey)
        return x,y

    def apply_snake(img,x,y,width,height,alpha,beta,gamma):
        # Load the image and define the initial contour points
        img = cv2.imread(img, 0)
        draw_image = img
        t = np.linspace(0,2*np.pi,60,endpoint = True)
        # x_0 = 350+250*np.sin(t)
        # y_0 = 330+250*np.cos(t)
        # get circle contour arount the image using img shape
        x_0 = x+width/2+width/2*np.sin(t)
        y_0 = y+height/2+height/2*np.cos(t)
        # x_0 = img.shape[1]/2+img.shape[1]/2*np.sin(t)
        # y_0 = img.shape[0]/2+img.shape[0]/2*np.cos(t)
        img = cv2.Canny(img, 50, 150, apertureSize=3)

        # Run the snake algorithm using a greedy algorithm
        updated_contour = Contour.snake(img, x_0,y_0,alpha=alpha,beta=beta,gamma=gamma)
        # convert updated_contour to array of tuple
        updated_contour = np.array([updated_contour[0], updated_contour[1]]).T
        # update onture to array of int
        updated_contour = updated_contour.astype(int)
        print(updated_contour)
        # Display the result
        result = cv2.cvtColor(draw_image, cv2.COLOR_GRAY2RGB)
        for i in range(len(updated_contour)):
            cv2.circle(result,(updated_contour[i][0],updated_contour[i][1]) ,radius=1,color=(50,100,200),thickness=2)
            cv2.circle(result,(int(x_0[i]),int(y_0[i])) ,radius=1,color=(50,200,100),thickness=2)
        # write the output image
        cv2.imwrite('./static/imgs/ContourOutput.jpg',result)
    def freeman_chain_code(contour):
        chain_code = []
        # line interpolate each 2 contour points
        for i in range(len(contour)):
            if i == len(contour)-1:
                break
            else:
                x1 = contour[i][0]
                y1 = contour[i][1]
                x2 = contour[i+1][0]
                y2 = contour[i+1][1]
                if x1 == x2:
                    if y1 > y2:
                        for j in range(y2, y1):
                            chain_code.append(2)
                    else:
                        for j in range(y1, y2):
                            chain_code.append(6)
                elif y1 == y2:
                    if x1 > x2:
                        for j in range(x2, x1):
                            chain_code.append(0)
                    else:
                        for j in range(x1, x2):
                            chain_code.append(4)
                elif x1 > x2 and y1 > y2:
                    for j in range(x2, x1):
                        chain_code.append(1)
                elif x1 < x2 and y1 > y2:
                    for j in range(y2, y1):
                        chain_code.append(3)
                elif x1 < x2 and y1 < y2:
                    for j in range(x1, x2):
                        chain_code.append(5)
                elif x1 > x2 and y1 < y2:
                    for j in range(y1, y2):
                        chain_code.append(7)

        return chain_code

    def calculate_perimeter(chain_code):
        """
        Calculates the perimeter of a closed contour represented by a chain code.
        """
        perimeter = 0
        for i in range(len(chain_code)):
            if chain_code[i] in [0, 2, 4, 6]:
                perimeter += 1
            elif chain_code[i] in [1, 3, 5, 7]:
                perimeter += math.sqrt(2)
        return perimeter

    def calculate_area(chain_code):
        """
        Calculates the area of a closed contour represented by a chain code.
        """
        area = 0
        x, y = 0, 0
        for i in range(len(chain_code)):
            if chain_code[i] == 0:
                x += 1
            elif chain_code[i] == 1:
                x += 1
                y -= 1
            elif chain_code[i] == 2:
                y -= 1
            elif chain_code[i] == 3:
                x -= 1
                y -= 1
            elif chain_code[i] == 4:
                x -= 1
            elif chain_code[i] == 5:
                x -= 1
                y += 1
            elif chain_code[i] == 6:
                y += 1
            elif chain_code[i] == 7:
                x += 1
                y += 1
            if i == len(chain_code) - 1:
                area += x * y
            else:
                next_x, next_y = x, y
                if chain_code[i+1] == 0:
                    next_x += 1
                elif chain_code[i+1] == 1:
                    next_x += 1
                    next_y -= 1
                elif chain_code[i+1] == 2:
                    next_y -= 1
                elif chain_code[i+1] == 3:
                    next_x -= 1
                    next_y -= 1
                elif chain_code[i+1] == 4:
                    next_x -= 1
                elif chain_code[i+1] == 5:
                    next_x -= 1
                    next_y += 1
                elif chain_code[i+1] == 6:
                    next_y += 1
                elif chain_code[i+1] == 7:
                    next_x += 1
                    next_y += 1
                area += x * next_y - next_x * y
                x, y = next_x, next_y
        return abs(area) / 2
    # apply_snake()