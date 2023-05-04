let originalImgHarris = document.querySelector(".original-img-harris")
let HarrisOutput = document.querySelector('.harris-img');
upload = document.getElementById("upload3");
let harris = document.querySelector(".harrisrange")



////// Upload The img //////////
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
        originalImgHarris.innerHTML = " ";
        //add 1st image 
        originalImgHarris.appendChild(img);
    }
    };
    //read the  1st img & send it >_<
    img1_send =  e.target.files[0];
    reader1.readAsDataURL(img1_send);
    imgToFlask("input_harris",img1_send,"input_harris","/harris")
    
    harris.style.display = "flex";

});

document.getElementById('apply_harris').addEventListener('click', ()=>{
    range={
        harris:document.getElementById('harrisrange').value}
    console.log(range);
    json_request(range,'/applyharris','harris')
})

