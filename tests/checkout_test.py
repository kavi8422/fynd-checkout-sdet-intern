import re
from pathlib import Path
import pytest
from playwright.sync_api import Page, expect

APP_URL = Path(__file__).resolve().parent.parent.joinpath("index.html").as_uri()


@pytest.fixture(autouse=True)
def open_clean_checkout(page: Page):
    """Start every test from a fresh, clean page state."""
    page.goto(APP_URL)
    expect(page.get_by_role("heading", name="MINI CHECKOUT")).to_be_visible()


def test_tc01_successful_checkout(page: Page):
    """TC01: Valid customer name and items produce confirmation and order reference."""
    page.get_by_test_id("customer-name").fill("Kavita Reddy")
    page.get_by_test_id("place-order-btn").click()

    confirmation = page.get_by_test_id("order-confirmation")
    expect(confirmation).to_be_visible()
    expect(confirmation).to_contain_text("Order Successful")
    expect(page.get_by_test_id("confirmed-name")).to_have_text("Kavita Reddy")
    expect(page.get_by_test_id("confirmed-total")).to_have_text("₹800")
    expect(page.get_by_test_id("order-ref")).to_have_text(re.compile(r"^ORD-[A-Z0-9]{6}$"))


def test_tc02_missing_name_validation(page: Page):
    """TC02: Empty customer name blocks checkout and shows validation message."""
    page.get_by_test_id("place-order-btn").click()

    error_el = page.get_by_test_id("validation-error")
    expect(error_el).to_be_visible()
    # FIX 2: Assert message text without coupling to the ⚠ icon
    expect(error_el).to_contain_text("Please enter your name")
    expect(page.get_by_test_id("order-confirmation")).to_be_hidden()


def test_tc03_quantity_change_updates_totals(page: Page):
    """TC03: Increasing, decreasing, and removing items updates line and order totals."""
    expect(page.get_by_test_id("total-items")).to_have_text("2")
    expect(page.get_by_test_id("order-total")).to_have_text("₹800")

    # Increase Product A to 3 (₹1500) -> Order Total = ₹1800
    page.get_by_test_id("inc-a").click()
    page.get_by_test_id("inc-a").click()
    expect(page.get_by_test_id("qty-a")).to_have_text("3")
    expect(page.get_by_test_id("line-total-a")).to_have_text("₹1500")
    expect(page.get_by_test_id("total-items")).to_have_text("4")
    expect(page.get_by_test_id("order-total")).to_have_text("₹1800")

    # Decrease Product A to 2 (₹1000) -> Order Total = ₹1300
    page.get_by_test_id("dec-a").click()
    expect(page.get_by_test_id("qty-a")).to_have_text("2")
    expect(page.get_by_test_id("line-total-a")).to_have_text("₹1000")
    expect(page.get_by_test_id("total-items")).to_have_text("3")
    expect(page.get_by_test_id("order-total")).to_have_text("₹1300")

    # FIX 4: Actually remove Product B and verify totals drop to ₹1000 / 2 items
    page.get_by_test_id("remove-b").click()
    expect(page.get_by_test_id("qty-b")).to_have_text("0")
    expect(page.get_by_test_id("line-total-b")).to_have_text("₹0")
    expect(page.get_by_test_id("total-items")).to_have_text("2")
    expect(page.get_by_test_id("order-total")).to_have_text("₹1000")


def test_tc04_empty_cart_blocks_checkout(page: Page):
    """TC04: Removing all items blocks checkout with an empty cart message."""
    page.get_by_test_id("remove-a").click()
    page.get_by_test_id("remove-b").click()
    page.get_by_test_id("customer-name").fill("Kavita Reddy")
    page.get_by_test_id("place-order-btn").click()

    error_el = page.get_by_test_id("validation-error")
    expect(error_el).to_be_visible()
    # FIX 2: Assert message text without coupling to the ⚠ icon
    expect(error_el).to_contain_text("Cart cannot be empty")
    expect(page.get_by_test_id("order-confirmation")).to_be_hidden()


def test_tc05_name_with_only_spaces(page: Page):
    """TC05: Whitespace-only customer name is rejected."""
    page.get_by_test_id("customer-name").fill("   ")
    page.get_by_test_id("place-order-btn").click()

    error_el = page.get_by_test_id("validation-error")
    expect(error_el).to_be_visible()
    # FIX 2: Assert message text without coupling to the ⚠ icon
    expect(error_el).to_contain_text("Please enter your name")
    expect(page.get_by_test_id("order-confirmation")).to_be_hidden()


def test_tc06_preserve_customer_input_after_validation_error(page: Page):
    """TC06: Typed customer name is preserved when another validation error occurs."""
    name_input = page.get_by_test_id("customer-name")
    name_input.fill("Kavita Reddy")

    # Trigger empty-cart validation error
    page.get_by_test_id("remove-a").click()
    page.get_by_test_id("remove-b").click()
    page.get_by_test_id("place-order-btn").click()

    # FIX 2: Assert message text without coupling to the ⚠ icon
    expect(page.get_by_test_id("validation-error")).to_contain_text("Cart cannot be empty")
    expect(name_input).to_have_value("Kavita Reddy")


def test_tc07_double_click_protection(page: Page):
    """TC07: Rapid double-click generates only one visible confirmation and one reference."""
    page.get_by_test_id("customer-name").fill("Kavita Reddy")
    place_order_btn = page.get_by_test_id("place-order-btn")

    # FIX 1: Use a real rapid double-click and count only visible confirmations
    place_order_btn.dblclick()

    expect(place_order_btn).to_be_disabled()
    expect(place_order_btn).to_have_text("✓ Order Placed")
    expect(page.locator('[data-testid="order-confirmation"]:visible')).to_have_count(1)
    expect(page.get_by_test_id("order-ref")).to_have_text(re.compile(r"^ORD-[A-Z0-9]{6}$"))


def test_tc08_quantity_cannot_go_below_minimum(page: Page):
    """TC08: Clicking '-' at minimum quantity 1 keeps quantity at 1 and total unchanged."""
    dec_a = page.get_by_test_id("dec-a")

    # FIX 3: Focus strictly on the minimum-quantity rule ('-' stops at 1)
    expect(dec_a).to_be_disabled()
    dec_a.click(force=True)
    dec_a.click(force=True)

    expect(page.get_by_test_id("qty-a")).to_have_text("1")
    expect(page.get_by_test_id("line-total-a")).to_have_text("₹500")
    expect(page.get_by_test_id("order-total")).to_have_text("₹800")