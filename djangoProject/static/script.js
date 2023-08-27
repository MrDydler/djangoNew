function toggleForm() { 
    var formContainer = document.getElementById('form-container');
    var overlay = document.getElementById('overlay');
    var formDisplay = getComputedStyle(formContainer).display;
    if (formDisplay === 'none') {
        formContainer.style.display = 'flex';
        overlay.style.display = 'flex';
    } else {
        formContainer.style.display = 'none';
        overlay.style.display = 'none'; 
        console.log("nOne")
    }
}

function toggleRegForm(){
    var regContainer = document.getElementById('reg-container');
    var overlay = document.getElementById('overlay');
    var overlayDisplay = getComputedStyle(overlay).display;
    var formDisplay = getComputedStyle(regContainer).display;
    if (formDisplay === 'none') {
        regContainer.style.display = 'flex';
        overlay.style.display = 'flex';
}
    else {
        regContainer.style.display = 'none';
        overlay.style.display = 'none';
    }
}

function registrationAccepted() {
    var formContainer = document.getElementById('form-container');
    var formDisplay = getComputedStyle(formContainer).display;
    if (formDisplay === 'none') {
        formContainer.style.display = 'flex';
    } else {
        formContainer.style.display = 'none';
    }
}

function showRegistrationForm(productId) {
    var overlay = document.getElementById("overlay");
    var registrationContainer = document.getElementById("registrationContainer");
    var registrationContainerDisplay = getComputedStyle(registrationContainer).display;
    var productInput = document.getElementById("product_id");
    if(registrationContainerDisplay === 'block') {
        overlay.style.display = "flex";
        }    else {
            overlay.style.display = "none";
        }
    console.log(overlay)
    

    registrationContainer.style.display = "block";
    productInput.value = productId;  // Set the value of the hidden input field to the product ID
    }

// Show success message if the flag is True
var successFlag = '{{ success }}';
if (successFlag === 'True') {
    var successMessage = document.getElementById('successMessage');
    successMessage.style.display = 'block';
}
