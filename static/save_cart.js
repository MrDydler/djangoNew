function saveCart() {
    // Получаем все элементы корзины из контейнера user-cart
    const cartItems = document.querySelectorAll('.user-cart [data-product-id]');

    // Проверяем, пуста ли корзина
    if (cartItems.length === 0) {
        alert('Ваша корзина пуста. Добавьте товары перед сохранением корзины.');
        return;
    }

    // Создаем объект для хранения данных корзины (идентификатор продукта в качестве ключа, количество в качестве значения)
    const cartData = {};
    
    cartItems.forEach(function (item) {
        const productId = item.dataset.productId;
        const productQuantityElement = item.querySelector('.product-quantity-input');
        const productQuantity = productQuantityElement ? parseInt(productQuantityElement.value) : 0;
        cartData[productId] = productQuantity;
    });
    
    // Получаем CSRF-токен из куков
    const csrfToken = getCookie('csrftoken');

    // Отправляем данные корзины на сервер для сохранения
    axios
        .post('/save_cart/', JSON.stringify(cartData), {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
        })
        .then((response) => {
            if (!response.status === 200) {
                throw new Error('Ошибка сетевого запроса');
            }
            return response.data; // Читаем данные ответа
        })
        .then((data) => {
            // Обрабатываем ответ от сервера
            if (data.success) {
                alert('Данные корзины успешно сохранены!');
                // Перезагружаем страницу, чтобы обновить список корзин
                window.location.reload();
            } else {
                alert('Ошибка сохранения данных корзины.');
            }
        })
        .catch((error) => {
            alert('Произошла ошибка при сохранении данных корзины.');
            console.error(error);
        });
}

function showCart(cartId) {
    const cartProducts = document.getElementById(`cart-products-${cartId}`);
    
    // Проверяем текущее состояние отображения корзины
    if (cartProducts.style.display === 'block') {
        cartProducts.style.display = 'none';
    } else { 
        cartProducts.style.display = 'block';
    }
}

// Функция для получения CSRF-токена из куков
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Проверяем, соответствует ли имя куки имени CSRF-токена, используемого Django (по умолчанию - 'csrftoken')
            if (cookie.substring(0, name.length + 1) === name + '=') {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
