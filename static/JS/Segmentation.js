let fTabSegmentation = document.getElementsByClassName("segment")
let UnSegmentedImg = document.querySelector(".unsegmented-img")
let SegmentedImg = document.querySelector('.segmented-img')
uploadSegmented = document.getElementById("uploadsegmented");



document.addEventListener("click", (e)=>{
    if(e.target.classList.contains("segment")){
        toggleClass(fTabSegmentation, "active-segment")
        e.target.classList.add("active-segment")
        SegmentationType =e.target.classList[1]
        console.log(SegmentationType)
        if(e.target.classList.contains(SegmentationType)){
        if (SegmentationType == 'region-growing'){
            segment(SegmentationType,'seedpoint','rgthreshold','flex','flex','none','none','none')
        }
        if (SegmentationType == 'agglomerative'){
            segment(SegmentationType,'cluster','Maxiter','none','none','none','flex','none')
        }
        if (SegmentationType == 'mean-shift'){
            segment(SegmentationType,'meanshift-bandwidth','Maxiter','none','none','flex','none','none')
        }
        if (SegmentationType == 'k-means'){
            segment(SegmentationType,'cluster','Maxiter','none','none','none','flex','flex')
        }
    }
}
})

//############################################## upload img ############### //
uploadSegmented.addEventListener('change' , (e) => {
    console.log(e)
    const reader1 = new FileReader();
    reader1.onload = (e) => {
    if (e.target){
        //upload first image
        let img = document.createElement("img");
        img.id = "img";
        img.src = e.target.result;
        //clean 1st image
        UnSegmentedImg.innerHTML = " ";
        //add 1st image 
        UnSegmentedImg.appendChild(img);
    }
    };
    //read the  1st img & send it >_<
    img1_send =  e.target.files[0];
    reader1.readAsDataURL(img1_send);
    imgToFlask("unsegmented",img1_send,"unsegmented","/unsegmented")
    });
