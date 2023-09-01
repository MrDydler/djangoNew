function buyProduct(productId) {
    console.log('buyProduct function called.');
    
    const quantity = parseInt(prompt('Введите количество:', '1'));

    console.log('Product ID:', productId);
    console.log('Quantity:', quantity)
    if (isNaN(quantity) || quantity <= 0) {
        alert('Invalid quantity.');
        return;
    }

    // Get the CSRF token from the cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === name + '=') {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrfToken = getCookie('csrftoken');

    // Include the CSRF token in the AJAX headers
    fetch('/add_to_cart/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json', // Specify JSON content type
        },
        body: JSON.stringify({
            product_id: productId,
            quantity: quantity,
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Product added to the cart.');
            // Update the cart contents on the page without a full reload
            const cartItem = document.querySelector(`[data-product-id="${productId}"]`);
            if (cartItem) {
                const productQuantityElement = cartItem.querySelector('.product-quantity');
                if (productQuantityElement) {
                    const newQuantity = parseInt(productQuantityElement.textContent) + quantity;
                    productQuantityElement.textContent = newQuantity;
                } else {
                    alert('Product quantity element not found in the cart item.');
                }
            } else {
                // If cart item not found, dynamically add it to the cart
                const cart = document.querySelector('.user-cart');
                const cartItemDiv = document.createElement('div');
                cartItemDiv.setAttribute('data-product-id', productId);
                cartItemDiv.classList.add('cart-item');
                cartItemDiv.innerHTML = `<p>${productId} - <span class="product-quantity">${quantity}</span></p>`;
                cart.appendChild(cartItemDiv);
            }
        } else {
            alert('Failed to add the product to the cart.');
        }
    })
    .catch(error => {
        alert('Failed to add the product to the cart.');
        console.error('Error:', error);
    });
}
