import pytest
from item import Item

def test_item_init():
    item = Item("Apple", "Fruit", 1.5, 6)
    assert item.name == "Apple"
    assert item.category == "Fruit"
    assert item.price == 1.5
    assert item.quantity == 6


@pytest.mark.parametrize("price, quantity, expected_exception", [
    (-1, 3, ValueError),
    (0, 3, ValueError),
    (3, -1, ValueError),
    (3, 0, ValueError),
])
def test_invalid_price_and_quantity(price, quantity, expected_exception):
    with pytest.raises(expected_exception):
        Item(name="Apple", category="Fruit", price=price, quantity=quantity)


@pytest.mark.parametrize("price, quantity", [
    (1.3, 4),
    (1.9, 8),
    (10.0, 5),
])
def test_valid_price_and_quantity(price, quantity):
    item = Item(name="Apple", category="Fruit", price=price, quantity=quantity)
    assert item.price == price
    assert item.quantity == quantity
    assert item.name == "Apple"
    assert item.category == "Fruit"

@pytest.mark.parametrize("name, category, expected_exception" , [
    ("", "", ValueError),
    (" ", " ", ValueError),
])
def test_invalid_name_and_category(name, category, expected_exception):
    with pytest.raises(expected_exception):
        Item(name, category, 1.5, 3)


