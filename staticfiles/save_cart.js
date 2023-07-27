// save_cart.js
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

        // Send the cart data to the server for saving
        fetch('/save_cart/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
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
