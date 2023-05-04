let EDModes = document.getElementsByClassName("edge-detection-type")
let TModes = document.getElementsByClassName("threshold-type")
uploadEdge = document.getElementById('upload-edge')
let outputEdge = document.querySelector(".tb4-selected-filter")
let inputEdge = document.querySelector(".tb4-original-filter")


document.addEventListener("click", (e)=>{
    if(e.target.classList.contains("edge-detection-type")){
        toggleClass(EDModes, "active-edge-detection")
        edgetype= e.target.classList[1]
        json_request(edgetype,'/edgetype','edge')
        e.target.classList.add("active-edge-detection") }
    })
document.addEventListener("click", (e)=>{
    if(e.target.classList.contains("threshold-type")){
        toggleClass(TModes, "active-threshold")
        threshold= e.target.classList[1]
        json_request(threshold,'/threshold','threshold')
        console.log(threshold)
        e.target.classList.add("active-threshold") }
    })
//################ upload img ##################///

uploadEdge.addEventListener('change' , (e) => {
    
    const reader5 = new FileReader();
    reader5.onload = (e) => {
    if (e.target){
        //upload input image
        let img = document.createElement("img");
        img.id = "img";
        img.src = e.target.result;
        //clean images
        inputEdge.innerHTML = " ";
        outputEdge.innerHTML = " ";
        //add 1st image 
        inputEdge.appendChild(img);
    }
    };
    //read the  1st img & send it >_<
    input_send =  e.target.files[0];
    reader5.readAsDataURL(input_send);
    imgToFlask("inputedge",input_send,"inputedge","/edge")
    
}); 

