MINI CHECKOUT TEST PLAN
 
 
1. OBJECTIVE
Verify that the checkout:
- calculates totals accurately
- validates user input
- prevents duplicate order submissions


2. SCOPE
In scope:
- product quantity management
- cart calculations
- customer name validation
- order placement and confirmation
- duplicate submission prevention
Out of scope:
- backend persistence
- payment processing
- coupons
- mobile-viewport testing
- browsers other than Chromium


3. ENVIRONMENT
- Windows
- Python 3.14.0
- pytest 9.2.0
- Playwright with Chromium
Command to run the tests:
python -m pytest tests -v
 
 
4. HOW THE PAGE BEHAVES
- Starts with Product A (Rs 500, qty 1) and Product B (Rs 300, qty 1)
- Starting order total is Rs 800
- The minus button is disabled at quantity 1
- Remove sets the quantity to 0 and the line total to Rs 0
- Total Items counts total quantity (A=3 and B=1 gives 4)
- After a successful order, the Place Order button is disabled and shows "Order Placed"
- The order reference looks like ORD- followed by 6 letters or digits


5. KEY RISKS (HIGHEST PRIORITY FIRST)
- R1 (High): duplicate orders from double-clicking
- R2 (High): incorrect order or line total
- R3 (High): empty cart checkout
- R4 (High): missing or whitespace-only name
- R5 (Medium): typed data lost after an error
- R6 (Medium): quantity going below the minimum


6. AUTOMATED TEST CASES (tests/checkout_test.py)
TC07 - Double-click Place Order
- Risk: R1
- Expected: one confirmation, one reference, button disabled
- Result: PASS
TC03 - Quantity change updates totals
- Risk: R2
- Expected: line and order totals are exact at each step
- Product A to 3: line Rs 1500, total Rs 1800
- Product A to 2: line Rs 1000, total Rs 1300
- Remove Product B: total Rs 1000
- Result: PASS
TC01 - Successful checkout
- Risk: R2
- Expected: confirmation, name, total Rs 800 and order reference shown
- Result: PASS
TC04 - Empty cart checkout
- Risk: R3
- Expected: message "Cart cannot be empty", no confirmation
- Result: PASS
TC02 - Missing customer name
- Risk: R4
- Expected: message "Please enter your name", no confirmation
- Result: PASS
TC05 - Name with spaces only
- Risk: R4
- Expected: message "Please enter your name", no confirmation
- Result: PASS
TC06 - Preserve name after validation error
- Risk: R5
- Expected: error shown, typed name stays in the field
- Result: PASS
TC08 - Quantity cannot go below minimum
- Risk: R6
- Expected: minus button disabled at 1
- Quantity stays 1, line stays Rs 500, total stays Rs 800
- Result: PASS
Overall result: 8 passed
Result: verification/automated_test_results.png
 
 
7. MANUAL TEST RESULTS
Empty cart checkout
- Steps: remove both products, enter a name, click Place Order
- Observed: validation shown correctly, typed name kept
- Result: PASS
Double-click Place Order
- Steps: enter a valid name, click Place Order twice quickly
- Observed: one confirmation, button locked
- Result: PASS

8. DEFECTS FOUND
No defects identified during testing.
