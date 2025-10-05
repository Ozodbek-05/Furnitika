document.addEventListener('DOMContentLoaded', function() {

    // ===== 🔐 Get CSRF token =====
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // ===== 🌍 Base URL (til prefiksini hisobga oladi) =====
    function getBaseUrl() {
        const lang = window.location.pathname.split('/')[1];
        if (['en', 'uz', 'ru'].includes(lang)) {
            return `/${lang}`;
        }
        return '';
    }

    // ===== 🛒 Update cart item quantity via AJAX =====
    function updateCartQuantity(productId, newQuantity, input) {
        const price = parseFloat(input.getAttribute('data-price'));
        const stock = parseInt(input.getAttribute('data-stock'));

        if (newQuantity > stock) {
            alert(`Only ${stock} items available in stock!`);
            return;
        }

        if (newQuantity < 1) {
            if (confirm('Remove this item from cart?')) {
                window.location.href = `${getBaseUrl()}/basket/remove/${productId}/`;
            }
            return;
        }

        const csrftoken = getCookie('csrftoken');

        fetch(`${getBaseUrl()}/basket/update/${productId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrftoken
            },
            body: `qty=${newQuantity}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const totalElement = document.getElementById(`total_${productId}`);
                if (totalElement) {
                    totalElement.textContent = `$ ${(price * newQuantity).toFixed(2)}`;
                }
                input.value = newQuantity;
                updateCartTotal();
            } else if (data.message) {
                alert(data.message);
            } else {
                alert('Something went wrong!');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to update cart');
        });
    }

    // ===== 💰 Update cart total price =====
    function updateCartTotal() {
        let total = 0;
        document.querySelectorAll('.quantity-input').forEach(input => {
            const quantity = parseInt(input.value) || 0;
            const price = parseFloat(input.getAttribute('data-price')) || 0;
            total += quantity * price;
        });

        const totalElement = document.getElementById('cart-total-price');
        const finalTotalElement = document.getElementById('final-total');

        if (totalElement) totalElement.textContent = `$ ${total.toFixed(2)}`;
        if (finalTotalElement) finalTotalElement.textContent = `$ ${total.toFixed(2)} (tax incl.)`;
    }

    // ===== 🧾 Product detail page price update =====
    const quantityInput = document.getElementById('quantity_wanted');
    const totalPriceElement = document.getElementById('total-price');

    if (quantityInput && totalPriceElement) {
        const basePrice = parseFloat(totalPriceElement.textContent.trim());
        const stockText = document.querySelector('.check')?.textContent.trim();
        const stockMatch = stockText?.match(/\((\d+)\)/);
        const maxStock = stockMatch ? parseInt(stockMatch[1]) : 999;

        function updatePrice() {
            const quantity = parseInt(quantityInput.value) || 1;
            totalPriceElement.textContent = (basePrice * quantity).toFixed(2);
        }

        quantityInput.addEventListener('input', function() {
            let value = parseInt(this.value);
            if (isNaN(value) || value < 1) value = 1;
            if (value > maxStock) {
                value = maxStock;
                alert(`Maximum ${maxStock} items available!`);
            }
            this.value = value;
            updatePrice();
        });
    }

    // ===== ➕ Plus and ➖ Minus button handlers =====
    document.querySelectorAll('.bootstrap-touchspin-up').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.getAttribute('data-product-id');

            // --- Cart page ---
            if (productId) {
                const input = document.getElementById(`quantity_${productId}`);
                if (input) {
                    let currentVal = parseInt(input.value) || 1;
                    updateCartQuantity(productId, currentVal + 1, input);
                }
            }
            // --- Product detail page ---
            else {
                const input = this.closest('.quantity').querySelector('input[name="qty"]');
                if (input) {
                    const stockText = document.querySelector('.check')?.textContent.trim();
                    const stockMatch = stockText?.match(/\((\d+)\)/);
                    const maxStock = stockMatch ? parseInt(stockMatch[1]) : 999;

                    let currentVal = parseInt(input.value) || 1;
                    if (currentVal < maxStock) {
                        input.value = currentVal + 1;

                        const totalPriceElement = document.getElementById('total-price');
                        if (totalPriceElement) {
                            const basePriceText = totalPriceElement.textContent.trim();
                            const basePrice = parseFloat(basePriceText) / currentVal;
                            totalPriceElement.textContent = (basePrice * (currentVal + 1)).toFixed(2);
                        }
                    } else {
                        alert(`Only ${maxStock} items available!`);
                    }
                }
            }
        });
    });

    document.querySelectorAll('.bootstrap-touchspin-down').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.getAttribute('data-product-id');

            // --- Cart page ---
            if (productId) {
                const input = document.getElementById(`quantity_${productId}`);
                if (input) {
                    let currentVal = parseInt(input.value) || 1;
                    updateCartQuantity(productId, currentVal - 1, input);
                }
            }
            // --- Product detail page ---
            else {
                const input = this.closest('.quantity').querySelector('input[name="qty"]');
                if (input) {
                    let currentVal = parseInt(input.value) || 1;
                    if (currentVal > 1) {
                        input.value = currentVal - 1;

                        const totalPriceElement = document.getElementById('total-price');
                        if (totalPriceElement) {
                            const basePriceText = totalPriceElement.textContent.trim();
                            const basePrice = parseFloat(basePriceText) / currentVal;
                            totalPriceElement.textContent = (basePrice * (currentVal - 1)).toFixed(2);
                        }
                    }
                }
            }
        });
    });
});
