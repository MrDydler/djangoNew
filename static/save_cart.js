document.addEventListener('DOMContentLoaded', function() {
    const saveButton = document.querySelector('.save-button');

    saveButton.addEventListener('click', function() {
        // Get all cart items
        const cartItems = document.querySelectorAll('.cart-item');

        // Create an array to store cart data
        const cartData = [];

        cartItems.forEach(function(item) {
            const productId = item.dataset.productId;
            const productName = item.querySelector('p').textContent;
            const productQuantity = parseInt(item.querySelector('.product-quantity').textContent);

            cartData.push({
                productId: productId,
                productName: productName,
                productQuantity: productQuantity
            });
        });

        // Get the CSRF token from the cookies
        const csrfToken = getCookie('csrftoken');
        console.log(cartData);
        // Send the cart data to the server for saving
        fetch('/save_cart/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken // Include the CSRF token in the request headers
            },
            body: JSON.stringify({ data: cartData })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Cart data saved successfully!');
            } else {
                alert('Error saving cart data.');
            }
        })
        .catch(error => {
            alert('An error occurred while saving cart data.');
            console.error(error);
        });
    });
});

// Function to get the CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if the cookie name matches the CSRF token name used by Django (default is 'csrftoken')
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
