from unittest.mock import MagicMock

import pytest

from vending_machine_service.service import VendingMachineService


@pytest.fixture
def vending_machine_service_obj():
    vending_machine_service: VendingMachineService = VendingMachineService()
    return vending_machine_service


def test_update_input_state(vending_machine_service_obj):
    sample_input = {
        '1': 10,
        '5': 2,
        '10': 0
    }
    expected_result = {
        '1': 10,
        '5': 2,
        '10': 0
    }

    vending_machine_service_obj.update_input_state(sample_input)
    result = vending_machine_service_obj.input_coins

    assert result.get('1') == expected_result.get('1')
    assert result.get('5') == expected_result.get('5')
    assert result.get('10') == expected_result.get('10')


def test_show_money_input_valid_case(vending_machine_service_obj):
    test_input_1 = {
        '1': 10,
        '5': 1
    }
    test_input_2 = {
        '1': 20,
        '5': 0,
        '10': 5
    }

    expected_result = 15
    expected_result_2 = 70
    vending_machine_service_obj.update_input_state(test_input_1)
    result = vending_machine_service_obj.show_money_input()
    vending_machine_service_obj.update_input_state(test_input_2)
    result_2 = vending_machine_service_obj.show_money_input()
    
    assert result == expected_result
    assert result_2 == expected_result_2


def test_show_money_input_invalid_case(vending_machine_service_obj):
    test_input_1 = {
        '1': '10'
    }
    test_input_2 = {
        '1': '1d'
    }
    expected_result = 0

    vending_machine_service_obj.update_input_state(test_input_1)
    result = vending_machine_service_obj.show_money_input()
    vending_machine_service_obj.update_input_state(test_input_2)
    result_2 = vending_machine_service_obj.show_money_input()

    assert result == expected_result
    assert result_2 == expected_result


def test_list_purchaseable_products_valid_case(vending_machine_service_obj):
    test_product_list = [
        {
            'name': 'test_product_001',
            'price': 15,
            'stock': 10
        }, {
            'name': 'test_product_002',
            'price': 20,
            'stock': 0
        }, {
            'name': 'test_product_003',
            'price': 5,
            'stock': 2
        }
    ]

    test_input_money_1 = 20
    test_input_money_2 = 7

    expected_result_1 = [
        {
            'name': 'test_product_001',
            'price': 15,
            'stock': 10
        }, {
            'name': 'test_product_003',
            'price': 5,
            'stock': 2
        }
    ]
    expected_result_2 = [
        {
            'name': 'test_product_003',
            'price': 5,
            'stock': 2
        }
    ]
    vending_machine_service_obj._update_product_list(test_product_list)
    result = vending_machine_service_obj.list_purchaseable_products(test_input_money_1)
    result_2 = vending_machine_service_obj.list_purchaseable_products(test_input_money_2)
    
    assert result == expected_result_1
    assert result_2 == expected_result_2


def test_list_purchaseable_products_invalid_case(vending_machine_service_obj):
    test_product_list = [
        {
            'name': 'test_product_001',
            'price': 15,
            'stock': 10
        }, {
            'name': 'test_product_002',
            'price': 20,
            'stock': 0
        }, {
            'name': 'test_product_003',
            'price': 5,
            'stock': 2
        }
    ]

    test_input_money_1 = None
    test_input_money_2 = '1'
    test_input_money_3 = 1.0

    expected_result = []

    vending_machine_service_obj._update_product_list(test_product_list)
    result = vending_machine_service_obj.list_purchaseable_products(test_input_money_1)
    result_2 = vending_machine_service_obj.list_purchaseable_products(test_input_money_2)
    result_3 = vending_machine_service_obj.list_purchaseable_products(test_input_money_3)
    
    assert result == expected_result
    assert result_2 == expected_result
    assert result_3 == expected_result
