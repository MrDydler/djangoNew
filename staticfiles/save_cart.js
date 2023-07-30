function saveCart() {
    // Get all cart items from the user-cart container
    const cartItems = document.querySelectorAll('.user-cart [data-product-id]');

    // Check if the cart is empty
    if (cartItems.length === 0) {
        alert('Your cart is empty. Add products before saving the cart.');
        return;
    }

    // Create an object to store cart data (product ID as key, quantity as value)
    const cartData = {};
    let cartName = `Корзина ${document.querySelectorAll('.saved-cart-item').length + 1}`;

    cartItems.forEach(function (item) {
        const productId = item.dataset.productId;
        const productQuantityElement = item.querySelector('.product-quantity-input');
        const productQuantity = productQuantityElement ? parseInt(productQuantityElement.value) : 0;

        cartData[productId] = productQuantity;
    });

    // Get the CSRF token from cookies
    const csrfToken = getCookie('csrftoken');

    // Send the cart data to the server for saving
    axios
        .post('/save_cart/', JSON.stringify(cartData), {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
        })
        .then((response) => {
            if (!response.status === 200) {
                throw new Error('Network response was not ok');
            }
            return response.data; // Read the response data
        })
        .then((data) => {
            // Handle the response from the server
            if (data.success) {
                alert('Cart data saved successfully!');
                // ... (rest of the code remains the same)
            } else {
                alert('Error saving cart data.');
            }
        })
        .catch((error) => {
            alert('An error occurred while saving cart data.');
            console.error(error);
        });
}



// Function to get the CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if the cookie name matches the CSRF token name used by Django (default is 'csrftoken')
            if (cookie.substring(0, name.length + 1) === name + '=') {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
