// cart.js

// const cartProducts = document.getElementById('cartProducts');
// const shippingSelect = document.getElementById('shipping');
// const itemCountEl = document.getElementById('itemCount');
// const itemsTotalEl = document.getElementById('itemsTotal');
// const totalEl = document.getElementById('total');
//
// function updateSummary() {
//     let itemCount = 0;
//     let itemsTotal = 0;
//
//     document.querySelectorAll('.cart-row').forEach(row => {
//         const qty = parseInt(row.querySelector('.quantity').textContent);
//         const price = parseFloat(row.getAttribute('data-price'));
//         itemCount += qty;
//         itemsTotal += qty * price;
//         row.querySelector('.subtotal').textContent = `€${(qty * price).toFixed(2)}`;
//     });
//
//     const shipping = parseInt(shippingSelect.value);
//     itemCountEl.textContent = itemCount;
//     itemsTotalEl.textContent = `€${itemsTotal.toFixed(2)}`;
//     totalEl.textContent = `€${(itemsTotal + shipping).toFixed(2)}`;
// }
//
// cartProducts.addEventListener('click', e => {
//     if (e.target.classList.contains('increase')) {
//         const qtyEl = e.target.parentElement.querySelector('.quantity');
//         qtyEl.textContent = parseInt(qtyEl.textContent) + 1;
//         updateSummary();
//     }
//     if (e.target.classList.contains('decrease')) {
//         const qtyEl = e.target.parentElement.querySelector('.quantity');
//         let qty = parseInt(qtyEl.textContent);
//         if (qty > 1) {
//             qtyEl.textContent = qty - 1;
//             updateSummary();
//         }
//     }
//     if (e.target.classList.contains('remove-btn')) {
//         e.target.parentElement.remove();
//         updateSummary();
//     }
// });
//
// shippingSelect.addEventListener('change', updateSummary);
// updateSummary();