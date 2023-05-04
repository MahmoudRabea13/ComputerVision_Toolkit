upload_ssd1 = document.getElementById('upload-ssd1')
upload_ssd2 = document.getElementById('upload-ssd2')
let firstImg_ssd = document.querySelector(".first-ssdimg")
let secondImg_ssd = document.querySelector(".second-ssdimg")
let ssdImg = document.querySelector('.ssd-img')

// ################ Read imgs ################## //

upload_ssd1.addEventListener('change' , (e) => {
    
    const reader2 = new FileReader();
    reader2.onload = (e) => {
    if (e.target){
        //upload first image
        let img = document.createElement("img");
        img.id = "img";
        img.src = e.target.result;
        //clean 1st image
        firstImg_ssd.innerHTML = " ";
        //add 1st image 
        firstImg_ssd.appendChild(img);
    }
    };
    //read the  1st img & send it >_<
    ssd1_send =  e.target.files[0];
    reader2.readAsDataURL(ssd1_send);
    imgToFlask("firstimg_ssd",ssd1_send,"firstimg_ssd","/ssd")
    }); 

upload_ssd2.addEventListener('change' , (e) => {

    const reader3 = new FileReader();
    reader3.onload = (e) => {
    if (e.target){
        //upload first image
        let img = document.createElement("img");
        img.id = "img";
        img.src = e.target.result;
        //clean 1st image
        secondImg_ssd.innerHTML = " ";
        //add 1st image 
        secondImg_ssd.appendChild(img);
    }
    };
    //read the  2nd img & send it >_<
    ssd2_send =  e.target.files[0];
    reader3.readAsDataURL(ssd2_send);
    imgToFlask("secondimg_ssd",ssd2_send,"secondimg_ssd","/ssd")
    }); 
//##########################################################///
document.getElementById('ssd').addEventListener('click', ()=>{
    data = {
        type: document.querySelector('input[name="choose_mode"]:checked').value,
        threshold: document.getElementById('threshold').value
    }
    json_request(data,'/applyssd','ssd')
}) 