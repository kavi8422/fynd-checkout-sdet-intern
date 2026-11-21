const state = {
  products: {
    a: { name: "Product A", price: 500, qty: 1 },
    b: { name: "Product B", price: 300, qty: 1 }
  },
  isOrderPlaced: false
};

// DOM references
const qtyAEl = document.getElementById("qty-a");
const qtyBEl = document.getElementById("qty-b");
const lineTotalAEl = document.getElementById("line-total-a");
const lineTotalBEl = document.getElementById("line-total-b");
const totalItemsEl = document.getElementById("total-items");
const orderTotalEl = document.getElementById("order-total");

const decABtn = document.getElementById("dec-a");
const incABtn = document.getElementById("inc-a");
const removeABtn = document.getElementById("remove-a");

const decBBtn = document.getElementById("dec-b");
const incBBtn = document.getElementById("inc-b");
const removeBBtn = document.getElementById("remove-b");

const form = document.getElementById("checkout-form");
const nameInput = document.getElementById("customer-name");
const errorEl = document.getElementById("validation-error");
const placeOrderBtn = document.getElementById("place-order-btn");

const confirmationEl = document.getElementById("order-confirmation");
const orderRefEl = document.getElementById("order-ref");
const confirmedNameEl = document.getElementById("confirmed-name");
const confirmedTotalEl = document.getElementById("confirmed-total");

function formatINR(amount) {
  return `₹${amount}`;
}

function generateOrderRef() {
  const chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
  let code = "";
  for (let i = 0; i < 6; i++) {
    code += chars[Math.floor(Math.random() * chars.length)];
  }
  return `ORD-${code}`;
}

function render() {
  const { a, b } = state.products;
  const lineA = a.price * a.qty;
  const lineB = b.price * b.qty;
  const totalItems = a.qty + b.qty;
  const orderTotal = lineA + lineB;

  qtyAEl.textContent = String(a.qty);
  qtyBEl.textContent = String(b.qty);
  lineTotalAEl.textContent = formatINR(lineA);
  lineTotalBEl.textContent = formatINR(lineB);
  totalItemsEl.textContent = String(totalItems);
  orderTotalEl.textContent = formatINR(orderTotal);

  // '-' stops at quantity 1 (disabled when qty <= 1); Remove sets qty to 0
  decABtn.disabled = state.isOrderPlaced || a.qty <= 1;
  incABtn.disabled = state.isOrderPlaced;
  removeABtn.disabled = state.isOrderPlaced;
  removeABtn.textContent = a.qty > 0 ? "Remove" : "Add";
  removeABtn.classList.toggle("is-add", a.qty === 0);

  decBBtn.disabled = state.isOrderPlaced || b.qty <= 1;
  incBBtn.disabled = state.isOrderPlaced;
  removeBBtn.disabled = state.isOrderPlaced;
  removeBBtn.textContent = b.qty > 0 ? "Remove" : "Add";
  removeBBtn.classList.toggle("is-add", b.qty === 0);
}

function showError(message, highlightInput = false) {
  errorEl.textContent = `⚠ ${message}`;
  nameInput.classList.toggle("input-error", highlightInput);
}

function clearError() {
  errorEl.textContent = "";
  nameInput.classList.remove("input-error");
}

function increaseQty(key) {
  if (state.isOrderPlaced) return;
  state.products[key].qty += 1;
  clearError();
  render();
}

function decreaseQty(key) {
  if (state.isOrderPlaced) return;
  const product = state.products[key];
  if (product.qty > 1) {
    product.qty -= 1;
    clearError();
    render();
  }
}

function toggleRemove(key) {
  if (state.isOrderPlaced) return;
  const product = state.products[key];
  product.qty = product.qty > 0 ? 0 : 1;
  clearError();
  render();
}

// Cart listeners
incABtn.addEventListener("click", () => increaseQty("a"));
decABtn.addEventListener("click", () => decreaseQty("a"));
removeABtn.addEventListener("click", () => toggleRemove("a"));

incBBtn.addEventListener("click", () => increaseQty("b"));
decBBtn.addEventListener("click", () => decreaseQty("b"));
removeBBtn.addEventListener("click", () => toggleRemove("b"));

nameInput.addEventListener("input", () => {
  if (errorEl.textContent) clearError();
});

// Form submit & double-click guard
form.addEventListener("submit", (event) => {
  event.preventDefault();

  // Ignore any click after the first successful order
  if (state.isOrderPlaced) return;

  const totalItems = state.products.a.qty + state.products.b.qty;
  const customerName = nameInput.value.trim();

  // Empty cart validation (preserves typed name)
  if (totalItems === 0) {
    showError("Cart cannot be empty", false);
    return;
  }

  // Blank or whitespace-only name validation (preserves typed input)
  if (!customerName) {
    showError("Please enter your name", true);
    nameInput.focus();
    return;
  }

  // Lock immediately to prevent duplicate confirmations
  state.isOrderPlaced = true;
  clearError();

  placeOrderBtn.disabled = true;
  placeOrderBtn.textContent = "✓ Order Placed";
  nameInput.disabled = true;
  render();

  const orderTotal =
    state.products.a.price * state.products.a.qty +
    state.products.b.price * state.products.b.qty;

  orderRefEl.textContent = generateOrderRef();
  confirmedNameEl.textContent = customerName;
  confirmedTotalEl.textContent = formatINR(orderTotal);
  confirmationEl.hidden = false;
});

render();