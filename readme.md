# Mini Checkout - SDET Intern Hackathon Submission

A simple checkout page built with HTML, CSS, and JavaScript, tested with automated Playwright and pytest browser tests.

## Project Files
- `index.html`, `style.css`, `app.js` - The checkout page
- `tests/checkout_test.py` - 8 automated browser tests (TC01 to TC08)
- `Test_Plan.md` - Test plan, manual test results, and defects
- `verification/automated_test_results.png` - Screenshot of the passing test run
- `requirements.txt` - Python packages needed for the tests

## What the Page Does
- Shows two products with line totals, total items, and order total
- Quantity buttons: `+`, `-`, and `Remove` (the `-` button stops at quantity 1)
- Blocks checkout for an empty cart, a blank name, or a name with only spaces
- Keeps the typed name after a validation error
- Prevents duplicate orders on a double-click of **Place Order**

## How to Run the Page
Open `index.html` in any browser. No backend or build step is needed.

## How to Run the Tests (Windows PowerShell)
Run these commands one by one:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install chromium
python -m pytest tests/checkout_test.py -v
