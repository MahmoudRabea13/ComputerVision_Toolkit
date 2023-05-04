uploadcontour = document.getElementById('upload-contour')
let Contour_input = document.querySelector(".input-img-contour")
let Contour_output = document.querySelector(".output-img-contour")
let alpha =document.getElementById('alpha')
let beta = document.getElementById('beta')
let gamma = document.getElementById('gamma')


//############### Read the input img ###################//

uploadcontour.addEventListener('change' , (e) => {

    const reader4 = new FileReader();
    reader4.onload = (e) => {
    if (e.target){
        //upload input image
        let img = document.createElement("img");
        img.id = "img";
        img.src = e.target.result;
        $(document).ready(function(){
        //clean images
        Contour_input.innerHTML = " ";
        Contour_output.innerHTML = " ";
        //add 1st image 
        Contour_input.appendChild(img);

        $('.input-img-contour').Jcrop({
            boxWidth: 512,   //Maximum width you want for your bigger images
            boxHeight: 512,
            transparent: false, 
            onSelect: function(c){
                contourparameters = {
                    alpha:alpha.value,
                    beta:beta.value,
                    gamma:gamma.value,
                    height: c.h,
                    width: c.w,
                    x: c.x,
                    y: c.y,
                    x2: c.x2,
                    y2: c.y2
                }
                json_request(contourparameters,'/applycontour','outputcontour')
                console.log('what im doing')
            }
            

        })
        })
    }
    };
    //read the  1st img & send it >_<
    input_send =  e.target.files[0];
    reader4.readAsDataURL(input_send);
    imgToFlask("ContourInput",input_send,"ContourInput","/contour")

}); 


