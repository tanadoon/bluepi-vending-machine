from unittest.mock import MagicMock

import pytest

from vending_machine_service.service import VendingMachineService


@pytest.fixture
def vending_machine_service_obj():
    vending_machine_service: VendingMachineService = VendingMachineService()
    return vending_machine_service


def test_update_input_state(vending_machine_service_obj):
    test_input = {
        '1': 10,
        '5': 2,
        '10': 0
    }
    expected_result = {
        '1': 10,
        '5': 2,
        '10': 0
    }

    vending_machine_service_obj.update_input_state(test_input)
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


def test_create_change_coins_pool_valid_case(vending_machine_service_obj):
    test_input_coin = {
        '1': 10,
        '5': 2,
        '10': 0
    }
    test_input_coin_2 = {
        '5': 2,
        '10': 0
    }

    expected_default_result =  [[10,2], [5,2], [1, 10]]
    expected_result = [[10,2], [5,4], [1, 20]]
    expected_result_2 = [[10,2], [5,4], [1, 10]]
    
    default_result = vending_machine_service_obj._create_change_coins_pool()
    vending_machine_service_obj.update_input_state(test_input_coin)
    result = vending_machine_service_obj._create_change_coins_pool()
    vending_machine_service_obj.update_input_state(test_input_coin_2)
    result_2 = vending_machine_service_obj._create_change_coins_pool()
    
    assert default_result == expected_default_result
    assert result == expected_result
    assert result_2 == expected_result_2


def test_create_change_coins_pool_invalid_case(vending_machine_service_obj):
    test_input_coin = {
        '1': '10',
        '5': None,
        '10': 5.5
    }

    expected_default_result =  [[10,2], [5,2], [1, 10]]
    
    vending_machine_service_obj.update_input_state(test_input_coin)
    result = vending_machine_service_obj._create_change_coins_pool()
    
    assert result == expected_default_result


def test_calculate_change_coins_valid_case_with_no_input_coins(vending_machine_service_obj):
    test_change_amount = 32
    test_change_amount_2 = 12
    test_not_enough_change = 9999

    expected_result = {'10': 2, '5': 2, '1': 2}
    expected_result_2 = {'10': 1, '1': 2}
    expected_result_3 = {}

    result = vending_machine_service_obj.calculate_change_coins(test_change_amount)
    result_2 = vending_machine_service_obj.calculate_change_coins(test_change_amount_2)
    result_3 = vending_machine_service_obj.calculate_change_coins(test_not_enough_change)

    assert result == expected_result
    assert result_2 == expected_result_2
    assert result_3 == expected_result_3


def test_calculate_change_coins_valid_case_with_valid_input_coins(vending_machine_service_obj):
    test_change_amount = 40
    test_change_amount_2 = 39
    test_not_enough_change = 9999

    test_input_coin = {
        '10': 2
    }

    expected_result = {'10': 4}
    expected_result_2 = {'10': 3, '5': 1, '1': 4}
    expected_result_3 = {}

    vending_machine_service_obj.update_input_state(test_input_coin)
    result = vending_machine_service_obj.calculate_change_coins(test_change_amount)
    result_2 = vending_machine_service_obj.calculate_change_coins(test_change_amount_2)
    result_3 = vending_machine_service_obj.calculate_change_coins(test_not_enough_change)

    assert result == expected_result
    assert result_2 == expected_result_2
    assert result_3 == expected_result_3


def test_calculate_change_coins_valid_case_with_invalid_input_coins(vending_machine_service_obj):
    test_change_amount = 40
    test_not_enough_change = 9999

    test_input_coin = {
        '10': '2'
    }

    expected_result = {'10': 2, '5': 2, '1': 10}
    expected_result_2 = {}

    vending_machine_service_obj.update_input_state(test_input_coin)
    result = vending_machine_service_obj.calculate_change_coins(test_change_amount)
    result_2 = vending_machine_service_obj.calculate_change_coins(test_not_enough_change)

    assert result == expected_result
    assert result_2 == expected_result_2


def test_calculate_change_coins_valid_case_with_invalid_change_amount(vending_machine_service_obj):
    test_change_amount = '40'
    test_change_amount_2 = None
    test_change_amount_3 = 40.5


    expected_result = {}

    result = vending_machine_service_obj.calculate_change_coins(test_change_amount)
    result_2 = vending_machine_service_obj.calculate_change_coins(test_change_amount_2)
    result_3 = vending_machine_service_obj.calculate_change_coins(test_change_amount_3)

    assert result == expected_result
    assert result_2 == expected_result
    assert result_3 == expected_result


def test_reset_input_coin(vending_machine_service_obj):
    test_input_coin = {
        '1': 100,
        '5': 100,
        '10': 100,
    }

    expected_result = {
        '1': 0,
        '5': 0,
        '10': 0,
    }

    vending_machine_service_obj.update_input_state(test_input_coin)
    vending_machine_service_obj.reset_input_coin()
    
    assert vending_machine_service_obj.input_coins == expected_result


def test_validate_acceptable_coin(vending_machine_service_obj):
    test_coin_1 = 1
    test_coin_2 = 2
    test_coin_3 = 5
    test_coin_4 = 10
    test_coin_5 = '10'
    test_coin_6 = None
    test_coin_7 = 5.0
    test_coin_8 = 5.9

    assert vending_machine_service_obj.validate_acceptable_coin(test_coin_1)
    assert not vending_machine_service_obj.validate_acceptable_coin(test_coin_2)
    assert vending_machine_service_obj.validate_acceptable_coin(test_coin_3)
    assert vending_machine_service_obj.validate_acceptable_coin(test_coin_4)
    assert not vending_machine_service_obj.validate_acceptable_coin(test_coin_5)
    assert not vending_machine_service_obj.validate_acceptable_coin(test_coin_6)
    assert vending_machine_service_obj.validate_acceptable_coin(test_coin_7)
    assert not vending_machine_service_obj.validate_acceptable_coin(test_coin_8)


def test_update_product_list_valid_case(vending_machine_service_obj):
    test_product_list = [
        {
            'name': 'test_product_001',
            'price': 15,
            'stock': 10
        }
    ]

    expected_result = [
        {
            'name': 'test_product_001',
            'price': 15,
            'stock': 10
        }
    ]

    vending_machine_service_obj._update_product_list(test_product_list)
    
    assert vending_machine_service_obj.product_list == expected_result


def test_update_product_list_invalid_case(vending_machine_service_obj):
    test_product_list = []
    test_product_list_2 = None

    expected_result = vending_machine_service_obj._init_product_list()

    vending_machine_service_obj._update_product_list(test_product_list)
    assert vending_machine_service_obj.product_list == expected_result
    vending_machine_service_obj._update_product_list(test_product_list_2)
    assert vending_machine_service_obj.product_list == expected_result


def test_reset_product_list(vending_machine_service_obj):
    test_product_list = [
        {
            'name': 'test_product_001',
            'price': 15,
            'stock': 10
        }
    ]

    expected_result = vending_machine_service_obj._init_product_list()

    vending_machine_service_obj._update_product_list(test_product_list)
    vending_machine_service_obj._reset_product_list()
    
    assert vending_machine_service_obj.product_list == expected_result


def test_ensure_value(vending_machine_service_obj):
    test_element = 1
    test_element_2 = '1'
    test_element_3 = 1.5
    test_element_4 = None

    test_check_type = int
    test_default_return_value = 0
    
    expected_result = 1
    expected_result_2 = 0

    assert vending_machine_service_obj._ensure_value(test_element, test_check_type, test_default_return_value) == expected_result
    assert vending_machine_service_obj._ensure_value(test_element_2, test_check_type, test_default_return_value) == expected_result_2
    assert vending_machine_service_obj._ensure_value(test_element_3, test_check_type, test_default_return_value) == expected_result_2
    assert vending_machine_service_obj._ensure_value(test_element_4, test_check_type, test_default_return_value) == expected_result_2


def test_update_reserved_change_coins_with_reset_input_case(vending_machine_service_obj):
    test_input_coin = {'1': 10, '5': 2, '10': 0}
    test_change_coin = {'1': 2}
    test_reset_flag = True

    expected_reserved_change_coins = {'1': 18, '5': 4, '10': 2}
    expected_input_coin = vending_machine_service_obj._init_input_coins()

    vending_machine_service_obj.update_input_state(test_input_coin)
    vending_machine_service_obj.update_reserved_change_coins(test_change_coin, test_reset_flag)

    assert vending_machine_service_obj.reserved_change_coins == expected_reserved_change_coins
    assert vending_machine_service_obj.input_coins == expected_input_coin


def test_update_reserved_change_coins_with_no_reset_input_case(vending_machine_service_obj):
    test_input_coin = {'1': 10, '5': 2, '10': 0}
    test_change_coin = {'1': 2}
    test_reset_flag = False

    expected_reserved_change_coins = {'1': 18, '5': 4, '10': 2}
    expected_input_coin = test_input_coin

    vending_machine_service_obj.update_input_state(test_input_coin)
    vending_machine_service_obj.update_reserved_change_coins(test_change_coin, test_reset_flag)

    assert vending_machine_service_obj.reserved_change_coins == expected_reserved_change_coins
    assert vending_machine_service_obj.input_coins == expected_input_coin
