uploadThreshold = document.getElementById('upload-threshold')
let outputThreshold = document.querySelector(".tb2-output-img")
let inputThreshold = document.querySelector(".tb2-input-img")

//################ upload img ##################///

uploadThreshold.addEventListener('change' , (e) => {
    
    const reader5 = new FileReader();
    reader5.onload = (e) => {
    if (e.target){
        //upload input image
        let img = document.createElement("img");
        img.id = "img";
        img.src = e.target.result;
        //clean images
        inputThreshold.innerHTML = " ";
        outputThreshold.innerHTML = " ";
        //add 1st image 
        inputThreshold.appendChild(img);
    }
    };
    //read the  1st img & send it >_<
    input_send =  e.target.files[0];
    reader5.readAsDataURL(input_send);
    imgToFlask("thresholdalgorithms_input",input_send,"thresholdalgorithms_input","/thresholdalgorithms")
    
}); 


document.getElementById('apply-threshold').addEventListener('click',()=>{
    ThresholdType=document.querySelector('input[name="threshold"]:checked').value
    AlgorithmType=document.querySelector('input[name="Algorithm"]:checked').value
    WindowSize=document.getElementById('window').value
    applythreshold={
        type: ThresholdType,
        algorithm: AlgorithmType,
        window: WindowSize
    }
    if(ThresholdType=='global'){
        applythreshold['window']=0
    }
    json_request(applythreshold,'/applythreshold','thresholdalgorithms')
});

document.addEventListener("click", (e)=>{
    if(e.target.classList.contains("localcheck")){
        document.getElementById('window-size').style.display='flex';
        document.getElementById('defaultlocal').style.display='flex';
    }
    
    if(e.target.classList.contains("globalcheck")){
        document.getElementById('window-size').style.display='none';
        document.getElementById('defaultlocal').style.display='none';
    }
    });