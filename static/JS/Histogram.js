uploadHist = document.getElementById('upload-histogram')
let inputImg = document.querySelector(".input-img")
let outputImg = document.querySelector(".output-img")
let inputHist = document.querySelector('.input-hist')
let outputHist = document.querySelector('.output-hist')
let colorMode = document.getElementsByClassName("mode")


//############### Read the input img ###################//

uploadHist.addEventListener('change' , (e) => {
    
    const reader4 = new FileReader();
    reader4.onload = (e) => {
    if (e.target){
        //upload input image
        let img = document.createElement("img");
        img.id = "img";
        img.src = e.target.result;
        //clean images
        inputImg.innerHTML = " ";
        outputImg.innerHTML = " ";
        inputHist.innerHTML = " ";
        outputHist.innerHTML = " ";
        //add 1st image 
        inputImg.appendChild(img);
    }
    };
    //read the  1st img & send it >_<
    input_send =  e.target.files[0];
    reader4.readAsDataURL(input_send);
    imgToFlask("inputimg",input_send,"inputimg","/histogram")
    
}); 

// ################# toggle gray_RGB ##############//
document.getElementById('gray').addEventListener('click',(e)=>{
    RGB_Gray('./static/imgs/Gray_histogram.jpg',inputHist)
    RGB_Gray('/static/imgs/Gray_histogram_equalized.jpg',outputHist)
    
})
document.getElementById('rgb').addEventListener('click',(e)=>{
    RGB_Gray('./static/imgs/RGB_histogram.jpg',inputHist)
    RGB_Gray('./static/imgs/RGB_histogram_equalized.jpg',outputHist)
})

document.addEventListener("click", (e)=>{
    if(e.target.classList.contains("mode")){
        toggleClass(colorMode, "active-mode")
        e.target.classList.add("active-mode") }
    })