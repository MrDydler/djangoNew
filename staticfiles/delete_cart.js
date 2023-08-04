function deleteCart(cartId) {
    // Get the CSRF token from cookies
    const csrfToken = getCookie('csrftoken');

    // Send the cart ID to the server for deletion
    axios
        .post('/delete_cart/', { cart_id: cartId }, {
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
                alert('Cart deleted successfully!');
                // Remove the cart from the DOM
                const cartElement = document.getElementById(`cart-${cartId}`);
                if (cartElement) {
                    cartElement.remove();
                }
            } else {
                alert('Error deleting cart.');
            }
        })
        .catch((error) => {
            alert('An error occurred while deleting the cart.');
            console.error(error);
        });
}

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