<<<<<<< HEAD
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
=======
buy_product.js
function buyProduct(productId, productName, event, saveCart = false) {
    event.preventDefault();
    console.log('buyProduct function called.');

    // Get the shopping cart element
    const shoppingCart = document.querySelector('.user-cart');

    // Check if the product is already in the cart based on the product ID
    const existingProduct = Array.from(shoppingCart.children).find(item => item.dataset.productId === productId);

    if (existingProduct) {
        // If the product already exists, update its quantity
        const productQuantityElement = existingProduct.querySelector('.product-quantity');
        const currentQuantity = parseInt(productQuantityElement.textContent);
        const quantityInput = prompt(`Enter the quantity of ${productName} you want to add:`, currentQuantity);

        if (quantityInput !== null) {
            const newQuantity = parseInt(quantityInput);
            productQuantityElement.textContent = newQuantity;
            alert('Product quantity updated in the cart.');
        }
    } else {
        // If the product is not in the cart, create a new entry
        const productDiv = document.createElement('div');
        productDiv.dataset.productId = productId;
        productDiv.textContent = productName;

        // Create a quantity input field
        const quantityInput = document.createElement('input');
        quantityInput.type = 'number';
        quantityInput.value = '1';
        quantityInput.min = '1';
        quantityInput.classList.add('product-quantity-input');
        productDiv.appendChild(quantityInput);

        // Create a delete button for the product
        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Удалить';
        deleteButton.onclick = function () {
            shoppingCart.removeChild(productDiv);
            alert('Продукт удален из корзины.');
        };

        // Append the product div and delete button to the shopping cart
        productDiv.appendChild(deleteButton);
        shoppingCart.appendChild(productDiv);

        alert('Продукт добавлен в корзину.');

        // If saveCart is true, call the saveCart function to save the cart
        if (saveCart) {
            saveCart();
        }
    }
}


function buyInCart() {
    // Trigger the "Buy in cart" functionality by clicking the "Buy in cart" button
    document.querySelector('.buy-in-cart-button').click();
>>>>>>> b5b69d5ebaa383dfce01b65de7d0cb7f0b09e35e
}
