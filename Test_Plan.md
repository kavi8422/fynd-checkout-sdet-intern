E-Commerce Checkout Test Plan

Objective:
Verify that the checkout process works correctly, calculates totals accurately, validates user input, and prevents duplicate order submissions.

Scope:
- In Scope: Product quantity management, cart calculations, customer name validation, order placement, order confirmation, and duplicate submission prevention.
- Out of Scope: Backend persistence, payment processing, coupons, mobile-viewport testing, and browsers other than Chromium.

Key Risks:
1. Incorrect order total calculation
2. Empty cart checkout
3. Missing or whitespace-only customer name
4. Duplicate orders from double-clicking
5. Incorrect quantity handling

Automated Test Cases (tests/checkout_test.py):
- TC01 - Successful checkout: Confirmation and order reference displayed - PASS
- TC02 - Missing customer name: Validation message shown - PASS
- TC03 - Quantity change updates total: Line and order totals recalculate correctly - PASS
- TC04 - Empty cart checkout: Checkout blocked with empty cart message - PASS
- TC05 - Name with spaces only: Validation message shown - PASS
- TC06 - Preserve name after validation error: Previously entered name remains intact - PASS
- TC07 - Double-click Place Order: Only one confirmation generated - PASS
- TC08 - Quantity cannot go below minimum: Minus button stops at quantity 1 and never becomes negative - PASS

Verification Evidence:
verification/automated_test_results.png

Manual Test Cases:

MT01 - Empty Cart Checkout Validation
Precondition: Open index.html in a fresh browser tab.
Steps:
1. Click Remove on Product A.
2. Click Remove on Product B.
3. Type "Kavita Reddy" in the Customer Name field.
4. Click Place Order.
Expected Result: Error message "Cart cannot be empty" appears above the button, "Kavita Reddy" remains in the input box, and no order confirmation is shown.
Actual Result: Error message displayed clearly, customer name remained intact, and checkout was blocked.
Status: PASS

MT02 - Rapid Double-Click Protection
Precondition: Refresh index.html so both products are back in the cart.
Steps:
1. Type "Kavita Reddy" in the Customer Name field.
2. Rapidly double-click the Place Order button.
Expected Result: Only one order confirmation card and one ORD-XXXXXX reference are generated, and the button disables with text "Order Placed".
Actual Result: Single confirmation card and order reference displayed; button locked immediately.
Status: PASS

MT03 - Whitespace-Only Name Validation
Precondition: Refresh index.html.
Steps:
1. Type three spaces ("   ") into the Customer Name field.
2. Click Place Order.
Expected Result: Error message "Please enter your name" appears above the button and no order confirmation is shown.
Actual Result: Validation error displayed and checkout was blocked.
Status: PASS

Defects Found:
No defects identified during testing.