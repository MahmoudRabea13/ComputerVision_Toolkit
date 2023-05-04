let shapes = document.getElementsByClassName("shape")
let parameter1 = document.querySelector(".parameter1-size")
let parameter2 = document.querySelector(".parameter2")
let Hough_input = document.querySelector(".inputhough-img")
let Hough_output = document.querySelector('.outputhough-img')
upload = document.getElementById("upload2");

document.addEventListener("click", (e)=>{

// ###############################send shape type and its parameters########################################## //

    if(e.target.classList.contains("shape")){
        parameter2_value = document.getElementById('parameter2').value
        parameter1_value = document.getElementById('parameter1').value
        toggleClass(shapes, "active-shape")
        e.target.classList.add("active-shape")
        shapeType =e.target.classList[1]

            shape = {
                type: shapeType,
                parameter1name: document.getElementById('parameter1-title').innerHTML,
                parameter1val: parameter1_value,
                parameter2name: document.getElementById('parameter2-title').innerHTML,
                parameter2val: parameter2_value
            }
            json_request(shape,'/shape','outputhough')
            parameter1.style.display = "flex"
            parameter2.style.display = "flex"
            console.log(shape)
        
    }

}) 



//############################################## upload img ############### //

upload.addEventListener('change' , (e) => {
    console.log(e)
    const reader1 = new FileReader();
    reader1.onload = (e) => {
    if (e.target){
        //upload first image
        let img = document.createElement("img");
        img.id = "img";
        img.src = e.target.result;
        //clean 1st image
        Hough_input.innerHTML = " ";
        //add 1st image 
        Hough_input.appendChild(img);
    }
    };
    //read the  1st img & send it >_<
    img1_send =  e.target.files[0];
    reader1.readAsDataURL(img1_send);
    imgToFlask("HoughInput",img1_send,"HoughInput","/hough")
    });



///////###################### Toggle parameters ###################///
document.getElementById('line').addEventListener('click',()=>{
    document.getElementById('parameter1-title').innerHTML ='Roh';
    document.getElementById('parameter2-title').innerHTML ='threshold';
})
document.getElementById('circle').addEventListener('click',()=>{
    document.getElementById('parameter1-title').innerHTML ='R_max';
    document.getElementById('parameter2-title').innerHTML ='R_min';
})
document.getElementById('ellipse').addEventListener('click',()=>{
    document.getElementById('parameter1-title').innerHTML ='R';
    document.getElementById('parameter2-title').innerHTML ='r';
})