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
}
