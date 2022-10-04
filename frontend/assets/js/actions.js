
const start_button = document.getElementById('start');
const stop_button = document.getElementById('stop');
const capture_button = document.getElementById('capture');
const upload_button = document.getElementById('upload');
const recapture_button = document.getElementById('recapture');
const video_element = document.querySelector('video');
const canvas = document.querySelector('#canvas');
const context = canvas.getContext('2d');

const init = () => {
    start_button.addEventListener('click', start_button_action);
    stop_button.addEventListener('click', stop_button_action);
    capture_button.addEventListener('click', capture_button_action);
    upload_button.addEventListener('click', upload_button_action);
    recapture_button.addEventListener('click', function(){
        hide(upload_button)
        hide(recapture_button)
        show(video_element)
        hide(canvas)
        show(capture_button)
    });
    hide(canvas)
    

    hide(capture_button)
    hide(upload_button)
    hide(recapture_button)
    stop_button.setAttribute("disabled", "disabled");
    
}
const start_button_action = function() {
    show(capture_button)
    disable(start_button)
    enable(stop_button)
    hide(canvas)
    video_element.removeAttribute("style");
    hide(upload_button)
    hide(recapture_button)

    const constraints = {
        video: true
    };
    const handleSuccess = (stream) => {
        video_element.srcObject = stream;
    };
    const handleError = (error) => {
        console.log('navigator.getUserMedia error: ', error);
    };
    navigator.mediaDevices.getUserMedia(constraints).then(handleSuccess).catch(handleError);

    // do something
}
const stop_button_action = function() {
    enable(start_button)
    disable(stop_button)
    hide(capture_button)
    hide(upload_button)
    hide(recapture_button)

    video_element.srcObject.getTracks().forEach(track => track.stop());
    hide(video_element)
    hide(canvas)
    // do something
}
const capture_button_action = function() {
    
        // Draw the video frame to the canvas.
    context.drawImage(video_element, 0, 0, canvas.width, canvas.height);
    hide(video_element)
    show(canvas)
    hide(capture_button)
    show(upload_button)
    show(recapture_button)

    
    
    
    // do something
}
const upload_button_action = function() {
    url = "http://127.0.0.1:5000/save_image"
            
    const dataURL = canvas.toDataURL('image/png');
    const blobBin = atob(dataURL.split(',')[1]);
    const array = [];
    for (let i = 0; i < blobBin.length; i++) {
        array.push(blobBin.charCodeAt(i));
    }
    const file = new Blob([new Uint8Array(array)], { type: 'image/png' });
    const formData = new FormData();
    formData.append('file', file);

    document.querySelector(".loader").removeAttribute("style");
    fetch(url, {
        method: 'POST',
        body: formData
    }).then(response => response.json()).then(data => {
        console.log(data);
        show_faces(data);
    }).catch(error => {
        console.error(error);
    });
    // do something
}

const save_button_action = function() {
    // do something
}
const create_images = (data) => {

}

let hide = (object) => {
    object.setAttribute("style", "display: none;");
}
let show = (object) => {
    object.removeAttribute("style");
}
let disable = (object) => {
    object.setAttribute("disabled", "disabled");
}
let enable = (object) => {
    object.removeAttribute("disabled");
}
const show_faces = (data) => {
    faces = document.querySelector(".faces")
    faces.innerHTML = "";
    document.querySelector(".loader").setAttribute("style", "display: none;");
    data = data.faces;
    if(data.length == 0){
        faces.innerHTML = "No faces found";
        return
    }
    for (let i = 0; i < data.length; i++) {
        const face = document.createElement('div');
        face.setAttribute("class", "card");
        face.setAttribute("style", "width: 218px;margin: 6px;");
        const img = document.createElement('img');
        img.setAttribute("class", "card-img-top w-100 d-block");
        img.setAttribute("src", data[i]);
        img.setAttribute("width","150")
        img.setAttribute("height","200")
        face.appendChild(img);

        const cardBody = document.createElement('div');
        cardBody.setAttribute("class", "card-body");
        

        const nameInput = document.createElement('input');
        nameInput.setAttribute("class", "form-control");
        nameInput.setAttribute("type", "text");
        nameInput.setAttribute("placeholder", "Enter Name");
        nameInput.setAttribute("id", "name" + i);
        nameInput.setAttribute("name", "name" + i);

        const button = document.createElement('button');
        button.setAttribute("class", "btn btn-primary");
        button.setAttribute("id", "save" + i);
        button.setAttribute("type", "button");
        button.setAttribute("onclick", "save_name(this.id)");
        button.setAttribute("style", "margin-top: 10px;");
        button.innerText = "Register";
        
        cardBody.appendChild(nameInput);
        cardBody.appendChild(button);
        face.appendChild(cardBody);
        faces.appendChild(face);
    }
}

const save_name = (id) => {
    const name = document.querySelector('#' + id).previousElementSibling.value;
    const face = document.querySelector('#' + id).parentElement.parentElement;
    const img = face.querySelector('img').src;
    const url = "http://127.0.0.1:5000/register";
    
    const fd = new FormData();
    fd.append('name', name);
    fd.append('image', img);

    fetch(url, {
        method: 'POST',
        body: fd
    }).then(response => response.json()).then(data => {
        console.log(data);
        if (data.success) {
            document.querySelector('#' + id).innerHTML = "Saved";
            document.querySelector('#' + id).setAttribute("disabled", true);
        }
    }).catch(error => {
        console.error(error);
    });
}