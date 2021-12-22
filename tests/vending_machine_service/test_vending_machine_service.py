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
