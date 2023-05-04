
document.addEventListener("click", (e)=>{

    if(e.target.classList.contains("tab")){
        toggleClass(tabs, "active-tab")
        e.target.classList.add("active-tab")
        for(i = 0; i < tabsBodies.length; i++){
            tabsBodies[i].style.display = "none"
            if(tabsBodies[i].classList[1][2] == e.target.classList[1][3]){
                tabsBodies[i].style.display = "flex"
                console.log(tabsBodies[i].classList.value)
            }
        }
    }
});

function toggleClass(div, classname){
    for(i = 0; i < div.length; i++){
        div[i].classList.remove(classname)
    }
}


function json_request(data,route,state){
    var xhr=new XMLHttpRequest();
    xhr.open("POST",route , true);
    xhr.setRequestHeader('Content-Type', 'application/json');    
    xhr.send(JSON.stringify(data));
    xhr.onload = function (e) {
        if (xhr.readyState === 4 && xhr.status === 200) {
                if(state == 'input'){
                send_img('./static/imgs/original_img.jpg','input');
                }
                if(state == 'noise'){
                    send_img('./static/imgs/noisy.jpg','input');
                    console.log('wowowowo')    
                }
                if(state == 'output'){
                    send_img('./static/imgs/filtered_img.jpg','output');
                    
                }
                if(state == 'hybrid'){
                    send_img('./static/imgs/hybrid_img.jpg','hybrid');
                }
                if(state == 'edge'){
                    send_img('./static/imgs/outputedge.jpg','edge')
                }
                if(state == 'threshold'){
                    send_img('./static/imgs/threshold.jpg','edge')
                }
                if(state == 'inputhough'){
                    send_img('./static/imgs/HoughInput.jpg','inputhough');
                    }
                if(state == 'outputhough'){
                        send_img('./static/imgs/HoughOutput.jpg','outputhough');
                        
                    }
                if(state == 'inputcontour'){
                        send_img('./static/imgs/ContourInput.jpg','inputcontour');
                    }
                if(state == 'outputcontour'){
                        send_img('./static/imgs/ContourOutput.jpg','outputcontour')
                }
                if(state == 'harris'){
                    send_img('./static/imgs/output_harris.jpg','harris');
                }
                if(state == 'sift'){
                    send_img('./static/imgs/sift_img.jpg','sift');
                }
                if(state == 'ssd'){
                    send_img('./static/imgs/ssd_img.jpg','ssd');
                }
                if(state == 'segmentation'){
                    send_img('./static/imgs/segmented.jpg','segmentation');
                    
                }
                if(state == 'thresholdalgorithms'){
                    send_img('./static/imgs/Outputthreshold.jpg','thresholdalgorithms')
                }
            } else {
            console.log('err')
        }
    };
}


function send_img(path,state){
    checkIfImageExists(path, (exists) => {
    if (exists) {
        var timestamp = new Date().getTime();
        if(state == 'input'){
            original = document.createElement('img')
            original.src = path +'?t=' + timestamp;
            originalImg.innerHTML = " ";
            originalImg.appendChild(original);   
        }
        if(state == 'output'){
            filtered = document.createElement('img')
            filtered.src = path +'?t=' + timestamp;
            filteredImg.innerHTML = " ";
            filteredImg.appendChild(filtered);      
            }
        if(state == 'hybrid'){
            hybrid = document.createElement('img')
            hybrid.src = path +'?t=' + timestamp;
            hybridImg.innerHTML = " ";
            hybridImg.appendChild(hybrid); 
        }
        if(state == 'histogram'){
            histogram = document.createElement('img')
            histogram.src = path +'?t=' + timestamp;
            outputImg.innerHTML = " ";
            outputImg.appendChild(histogram); 
        }
        if(state == 'edge'){
            edge = document.createElement('img')
            edge.src = path +'?t=' + timestamp;
            outputEdge.innerHTML = " ";
            outputEdge.appendChild(edge);
        }
        if(state == 'threshold'){
            thresh = document.createElement('img')
            thresh.src = path +'?t=' + timestamp;
            outputEdge.innerHTML = " ";
            outputEdge.appendChild(edge);
        }
        if(state == 'inputhough'){
            original = document.createElement('img')
            original.src = path +'?t=' + timestamp;
            Hough_input.innerHTML = " ";
            Hough_input.appendChild(original);   
        }
        if(state == 'outputhough'){
            output = document.createElement('img')
            output.src = path +'?t=' + timestamp;
            Hough_output.innerHTML = " ";
            Hough_output.appendChild(output);      
            }
        if(state == 'outputcontour'){
            outputcontour = document.createElement('img')
            outputcontour.src = path +'?t=' + timestamp;
            Contour_output.innerHTML = " ";
            Contour_output.appendChild(outputcontour); 
        }
        if(state == 'harris'){
            harrisimg = document.createElement('img')
            harrisimg.src = path +'?t=' + timestamp;
            HarrisOutput.innerHTML = " ";
            HarrisOutput.appendChild(harrisimg);      
            }
        if(state == 'sift'){
            sift_img = document.createElement('img')
            sift_img.src = path +'?t=' + timestamp;
            siftImg.innerHTML = " ";
            siftImg.appendChild(sift_img);      
            }
        if(state == 'ssd'){
            ssd_img = document.createElement('img')
            ssd_img.src = path +'?t=' + timestamp;
            ssdImg.innerHTML = " ";
            ssdImg.appendChild(ssd_img);      
            }
            if(state == 'segmentation'){
                segmented = document.createElement('img')
                segmented.src = path +'?t=' + timestamp;
                SegmentedImg.innerHTML = " ";
                SegmentedImg.appendChild(segmented);      
                }
            if(state == 'thresholdalgorithms'){
                threshalgorithm = document.createElement('img')
                threshalgorithm.src = path +'?t=' + timestamp;
                outputThreshold.innerHTML = " ";
                outputThreshold.appendChild(threshalgorithm);
            }
    } else {
        console.log('Image does not exists.')
    }
});
}

function checkIfImageExists(url, callback) {
    const img = new Image();
    img.src = url;
    
    if (img.complete) {
        callback(true);
    } else {
        img.onload = () => {
        callback(true);
    };
        img.onerror = () => {
        callback(false);
        };
    }
};

function imgToFlask(name , data ,filename , route){
    var xhr=new XMLHttpRequest();
    var fd=new FormData();
    fd.append(name,data ,filename);
    xhr.onreadystatechange = function() {
        if (xhr.status == 200) {
            if(route == "/histogram"){
                send_img('./static/imgs/equalized_img.jpg','histogram');    
                RGB_Gray('./static/imgs/RGB_histogram.jpg',inputHist)
                RGB_Gray('./static/imgs/RGB_histogram_equalized.jpg',outputHist)
                console.log('Da histon!!!')
            }
            else{
                console.log("i've been sent")
            }
        }
        }; 
    xhr.open("POST",route,true);
    xhr.send(fd);
    console.log(fd)
};
/*Function for histogram 1st tab*/ 
function RGB_Gray(path,div){
    var timestamp = new Date().getTime();
    img = document.createElement('img')
    img.src = path +'?t=' + timestamp;
    div.innerHTML = " ";
    div.appendChild(img); 
}

/*Functions for segmentation 10th tab*/
function DisplaySegmentationParameters(seedpoint,rgthreshold,msbandwidth,numclusters,Maxiter){
    document.querySelector('.seedpoint-size').style.display= seedpoint;
    document.querySelector('.rgthreshold').style.display= rgthreshold;
    document.querySelector('.meanshift-bandwidth').style.display= msbandwidth;
    document.querySelector('.cluster').style.display= numclusters;
    document.querySelector('.Maxiter').style.display= Maxiter;
};

function segment(type,paramater1,parameter2,seedpoint,rgthreshold,msbandwidth,numclusters,Maxiter){
        value1= document.getElementById(paramater1).value
        value2= document.getElementById(parameter2).value
        DisplaySegmentationParameters(seedpoint,rgthreshold,msbandwidth,numclusters,Maxiter)
        segmentation = {
            type: type,
            parameter1:value1,
            parameter2: value2
        }
        json_request(segmentation,'/segmented','segmentation')
        console.log(segmentation)
    
}