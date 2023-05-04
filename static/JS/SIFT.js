upload_sift1 = document.getElementById('upload-img1-sift')
upload_sift2 = document.getElementById('upload-img2-sift')
let firstImgSift = document.querySelector(".first-img-sift")
let secondImgSift = document.querySelector(".second-img-sift")
let siftImg = document.querySelector('.sift-img')

// ################ Read imgs ################## //

upload_sift1.addEventListener('change' , (e) => {
    
    const reader2 = new FileReader();
    reader2.onload = (e) => {
    if (e.target){
        //upload first image
        let img = document.createElement("img");
        img.id = "img";
        img.src = e.target.result;
        //clean 1st image
        firstImgSift.innerHTML = " ";
        //add 1st image 
        firstImgSift.appendChild(img);
    }
    };
    //read the  1st img & send it >_<
    sift1_send =  e.target.files[0];
    reader2.readAsDataURL(sift1_send);
    imgToFlask("firstimg_sift",sift1_send,"firstimg_sift","/sift")
    }); 

upload_sift2.addEventListener('change' , (e) => {

    const reader3 = new FileReader();
    reader3.onload = (e) => {
    if (e.target){
        //upload first image
        let img = document.createElement("img");
        img.id = "img";
        img.src = e.target.result;
        //clean 1st image
        secondImgSift.innerHTML = " ";
        //add 1st image 
        secondImgSift.appendChild(img);
    }
    };
    //read the  2nd img & send it >_<
    sift2_send =  e.target.files[0];
    reader3.readAsDataURL(sift2_send);
    imgToFlask("secondimg_sift",sift2_send,"secondimg_sift","/sift")
    });
//##########################################################///
document.getElementById('sift').addEventListener('click', ()=>{
    data = {
        sift: "apply"
    }
    json_request(data,'/applysift','sift')
})