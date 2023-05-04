let tabs = document.getElementsByClassName("tab")
let tabsBodies = document.getElementsByClassName("tab-body")
let fTabFilters = document.getElementsByClassName("filter")
let fTabNoiseTypes = document.getElementsByClassName("noise-type")
let kernalSizeBox = document.querySelector(".kernal-size")
let radiusBox = document.querySelector(".radius")
let originalImg = document.querySelector(".original-img")
let filteredImg = document.querySelector('.filtered-img')
upload = document.getElementById("upload");

document.addEventListener("click", (e)=>{
// ################################################################################ //

    if(e.target.classList.contains("filter")){
        raduis_value = document.getElementById('raduis').value
        kernal_value = document.getElementById('kernal').value
        toggleClass(fTabFilters, "active-filter")
        e.target.classList.add("active-filter")
        filterType =e.target.classList[1]
        filteredImg.src = '/static/imgs/filtered_img.jpg';
        console.log(filteredImg.src)
        if(e.target.classList.contains("kernal")){
            filter = {
                type: filterType,
                raduissize:0,
                kernalsize: kernal_value
            }
            json_request(filter,'/applyfilter','output')
            kernalSizeBox.style.display = "flex"
            radiusBox.style.display = "none"
            console.log(filter)
        }else if(e.target.classList.contains("radius-filter")){
            filter = {
                type: filterType,
                raduissize: raduis_value,
                kernalsize: 0
            }
            json_request(filter,'/applyfilter','output')
            kernalSizeBox.style.display = "none"
            radiusBox.style.display = "flex"
            console.log(filter)
        }
    }

    // ################################################################################ //
    if(e.target.classList.contains("noise-type")){
        toggleClass(fTabNoiseTypes, "active-noise-type")
        noisetype = e.target.classList[1]
        e.target.classList.add("active-noise-type") 
        console.log(e.target.classList[1])
        noise = {
            type : noisetype,
        }
        json_request(noise,"/noise",'noise')
    }

})

// ################################################################################ //
// ################################################################################ //



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
        originalImg.innerHTML = " ";
        //add 1st image 
        originalImg.appendChild(img);
    }
    };
    //read the  1st img & send it >_<
    img1_send =  e.target.files[0];
    reader1.readAsDataURL(img1_send);
    imgToFlask("original_img",img1_send,"original_img","/filter")
    });

