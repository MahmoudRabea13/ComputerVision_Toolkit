hybrid1 = document.getElementById('upload-hybrid1')
hybrid2 = document.getElementById('upload-hybrid2')
let firstImg = document.querySelector(".first-img")
let secondImg = document.querySelector(".second-img")
let hybridImg = document.querySelector('.hybrid-img')

// ################ Read imgs ################## //

hybrid1.addEventListener('change' , (e) => {
    
    const reader2 = new FileReader();
    reader2.onload = (e) => {
    if (e.target){
        //upload first image
        let img = document.createElement("img");
        img.id = "img";
        img.src = e.target.result;
        //clean 1st image
        firstImg.innerHTML = " ";
        //add 1st image 
        firstImg.appendChild(img);
    }
    };
    //read the  1st img & send it >_<
    hybrid1_send =  e.target.files[0];
    reader2.readAsDataURL(hybrid1_send);
    imgToFlask("firstimg",hybrid1_send,"firstimg","/hybrid")
    }); 

hybrid2.addEventListener('change' , (e) => {

    const reader3 = new FileReader();
    reader3.onload = (e) => {
    if (e.target){
        //upload first image
        let img = document.createElement("img");
        img.id = "img";
        img.src = e.target.result;
        //clean 1st image
        secondImg.innerHTML = " ";
        //add 1st image 
        secondImg.appendChild(img);
    }
    };
    //read the  2nd img & send it >_<
    hybrid2_send =  e.target.files[0];
    reader3.readAsDataURL(hybrid2_send);
    imgToFlask("secondimg",hybrid2_send,"secondimg","/hybrid")
    });
//##########################################################///


//####################### send raduis values ###########################//
document.getElementById('hybrid').addEventListener('click',(e) =>{
    raduis2_value = document.getElementById('raduis2').value
    raduis3_value = document.getElementById('raduis3').value
    values = {
        img1_raduis : raduis2_value,
        img2_raduis : raduis3_value
    };
    json_request(values,'/hybridraduis','hybrid')
})