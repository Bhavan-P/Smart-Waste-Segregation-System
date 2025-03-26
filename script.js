// 🎥 Start the Camera
const cameraFeed = document.getElementById("cameraFeed");
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        cameraFeed.srcObject = stream;
    })
    .catch(error => {
        console.error("Camera access denied:", error);
    });

// 📸 Capture Image & Send to Backend for AI Classification
function captureImage() {
    const video = document.getElementById("cameraFeed");
    const canvas = document.getElementById("capturedImage");
    const context = canvas.getContext("2d");

    // Set canvas size to match video feed
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    // Draw video frame onto canvas
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert to Blob and send to backend
    canvas.toBlob(blob => {
        const formData = new FormData();
        formData.append("image", blob, "captured.jpg");

        fetch("http://127.0.0.1:5000/classify", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("wasteType").innerText = `${data.label} (${data.category})`;
        })
        .catch(error => console.error("Error:", error));
    }, "image/jpeg");
}

// 🔑 Login & Developer Actions
function showLogin() { document.getElementById("loginPopup").style.display = "block"; }
function loginUser() { alert("Login Successful!"); closePopup(); }
function showDevelopers() { 
    let devPopup = document.getElementById("developersPopup");
    devPopup.style.display = "block"; 
    devPopup.style.zIndex = "1001"; // Keeps it above other elements
}
function closePopup() { document.querySelectorAll('.popup').forEach(popup => popup.style.display = "none"); }
