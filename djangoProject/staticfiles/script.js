function toggleForm() { 
    var formContainer = document.getElementById('form-container');
    var overlay = document.getElementById('overlay');
    var formDisplay = getComputedStyle(formContainer).display;
    if (formDisplay === 'none') {
        formContainer.style.display = 'flex';
        overlay.classList.remove('display');
    } else {
        formContainer.style.display = 'none';
        overlay.style.display = 'none'; 
        console.log("nOne")
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
    var productInput = document.getElementById("product_id");
            
    console.log(overlay)
    overlay.style.display = "flex";

    registrationContainer.style.display = "block";
    productInput.value = productId;  // скрытое поле product id для передачи айдишника продукта
}

// показ succes флага
var successFlag = '{{ success }}';
if (successFlag === 'True') {
    var successMessage = document.getElementById('successMessage');
    successMessage.style.display = 'block';
}
