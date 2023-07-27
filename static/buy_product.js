// buy_product.js
function buyProduct(productId, productName, event) {
    event.preventDefault();
    console.log('buyProduct function called.');

    // Get the shopping cart element
    const shoppingCart = document.querySelector('.user-cart');

    // Check if the product is already in the cart based on the product ID
    const existingProduct = Array.from(shoppingCart.children).find(item => item.dataset.productId === productId);

    if (existingProduct) {
        // If the product already exists, update its quantity
        const productQuantityElement = existingProduct.querySelector('.product-quantity');
        if (productQuantityElement) {
            const currentQuantity = parseInt(productQuantityElement.textContent);
            productQuantityElement.textContent = currentQuantity + 1;
            alert('Product quantity updated in the cart.');
        }
    } else {
        // If the product is not in the cart, create a new entry
        const productDiv = document.createElement('div');
        productDiv.dataset.productId = productId;
        productDiv.textContent = productName;

        // Create a delete button for the product
        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Удалить';
        deleteButton.onclick = function() {
            shoppingCart.removeChild(productDiv);
            alert('Product removed from the cart.');
        };

        // Append the product div and delete button to the shopping cart
        productDiv.appendChild(deleteButton);
        shoppingCart.appendChild(productDiv);

        alert('Product added to the cart.');
    }
}
