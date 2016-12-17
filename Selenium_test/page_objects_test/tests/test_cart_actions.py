import pytest
from .data_providers import valid_list_of_products


@pytest.mark.parametrize("valid_list_of_products", valid_list_of_products,
                         ids=[repr(x) for x in valid_list_of_products])
def test_cart_actions(app, valid_list_of_products):
    app.add_several_products_to_cart(valid_list_of_products)
    app.remove_objects_from_cart_one_by_one()
