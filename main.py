from vending_machine_service.service import VendingMachineService


# def validate_is_acceptable_coin(coin: int) -> bool:
#     if not coin: return False
#     try:
#         return int(coin) in accept_coin
#     except ValueError:
#         return False


def simplify_showing_product(product_list: list):
    for index, product in enumerate(product_list):
        print(f'Product#{index+1} : {product.get("name")}\tprice: {product.get("price")} baht.')


if __name__ == '__main__':
    vending_machine = VendingMachineService()

    # State 1 Input coins
    print(f'Before re-balance: \n reserved_change_coins: {vending_machine.reserved_change_coins} \n input_coins: {vending_machine.input_coins}\n')
    sample_input = {
        '1': 20,
        '5': 2,
        '10': 0
    }

    # State 2 After finish input coin, update input coins to input list in machine
    vending_machine.update_input_state(sample_input)
    print(f'After Input coins: \n reserved_change_coins: {vending_machine.reserved_change_coins} \n input_coins: {vending_machine.input_coins}\n')

    # # State 3 Show money input as total input coin
    money_input = vending_machine.show_money_input()
    print(f'Input Money: {vending_machine.show_money_input()} baht.\n')

    # # State 4 Show Product list if stock > 0 show else not
    purchaseable_product_list = vending_machine.list_purchaseable_products(money_input)
    print('Purchaseable Product List:')
    simplify_showing_product(purchaseable_product_list)

    # # State 5 Buy 1 product
    mock_option = 1
    print(f'\nBuy Product: {purchaseable_product_list[mock_option].get("name")}')

    # State 6 change money from reserved change coins + input coins
    amount_changes = money_input - purchaseable_product_list[mock_option].get('price')
    print(f'Remaining Money: {amount_changes} baht.')
    change_coins = vending_machine.calculte_change_coins(amount_changes)

    # State 7 check from change_coins if empty it mean vending machine coins is not enough to change user just cancel order and return all input coins if not return as cahnge coins dict
    if change_coins:
        print(f'Change Coins: {change_coins}\n')
        vending_machine.update_reserved_change_coins(change_coins=change_coins, reset_input_coin_flag=True)
    else:
        print(f'Not enough coins to change cancelled order and return input coins : {vending_machine.input_coins}\n')
        vending_machine.reset_input_coin()
    
    # State 8 Re-balance reserved change coins in machine and reset input coins
    print(f'After re-balance: \n reserved_change_coins: {vending_machine.reserved_change_coins} \n input_coins: {vending_machine.input_coins}\n')
    
    # State 9 update product stock 
    vending_machine.update_product_stock_with_barcode_id(barcode_id=purchaseable_product_list[mock_option].get('barcode_id'))
    
    # print('Input Your Coin Value ...')
    # value_coin = input()
    # print(validate_is_acceptable_coin(value_coin))
    # print('Input Your Coin Amount ...')
    # amount_coin = int(input())
    # print(amount_coin)

