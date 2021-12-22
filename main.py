from vending_machine_service.service import VendingMachineService


def validate_input(input_value: str) -> bool:
    return input_value.isdigit()


def input_coin(vending_machine: VendingMachineService) -> dict:
    input_coin_dict = dict()
    while True:
        input_coin_value = input('Enter Coin Value: ').strip()
        if validate_input(input_coin_value) and vending_machine.validate_acceptable_coin(int(input_coin_value)):
            while True:
                input_coin_amount = input('Enter Coin Amount: ').strip()
                if validate_input(input_coin_amount):
                    input_coin_dict.update({
                        f'{input_coin_value}': int(input_coin_amount)
                    })
                    break
                else:
                    print('=== Invalid Input, please enter as a positive numeric. ===')
            continue_flag = input('Want to enter more coins? (y/n): ').strip().lower()
            if continue_flag in ('n', 'no', 'no.'):
                break
        else:
            print('=== Invalid Input, please enter as a numeric with these possible number 1, 5, 10. ===')
    print('====================')
    return input_coin_dict


def simplify_showing_product(product_list: list):
    for index, product in enumerate(product_list):
        print(f'Product#{index+1} : {product.get("name")}\tprice: {product.get("price")} baht.')
 

def select_product_from_purchaseable_product_list() -> dict:
    while True:
        select_product_index = input('What are you buying: ').strip()
        if validate_input(select_product_index) and int(select_product_index) <= len(purchaseable_product_list):
            return purchaseable_product_list[int(select_product_index)-1]
        else:
            print('=== please enter as numeric only within range of showing product ===')


if __name__ == '__main__':
    vending_machine = VendingMachineService()

    # State 1 Input coins
    input_dict = input_coin(vending_machine)

    # State 2 After finish input coin, update input coins to input list in machine
    vending_machine.update_input_state(input_dict)

    # State 3 Show money input as total input coin
    money_input = vending_machine.show_money_input()
    print(f'Input Money: {vending_machine.show_money_input()} baht.\n')

    # State 4 Show Product list if stock > 0 show else not
    purchaseable_product_list = vending_machine.list_purchaseable_products(money_input)
    print('Purchaseable Product List:')
    simplify_showing_product(purchaseable_product_list)

    # State 5 Buy 1 product
    selected_product = select_product_from_purchaseable_product_list()
    print(f'\nBuy Product: {selected_product.get("name")}')

    # State 6 change money from reserved change coins + input coins
    amount_changes = money_input - selected_product.get('price')
    print(f'Remaining Money: {amount_changes} baht.')
    change_coins = vending_machine.calculate_change_coins(amount_changes)

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
    vending_machine.update_product_stock_with_barcode_id(barcode_id=selected_product.get('barcode_id'))
