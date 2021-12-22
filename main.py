from vending_machine_service.service import VendingMachineService


# def validate_is_acceptable_coin(coin: int) -> bool:
#     if not coin: return False
#     try:
#         return int(coin) in accept_coin
#     except ValueError:
#         return False


# def list_available_product(input_money: int) -> list:
#     return [product for product in product_list if product.get('stock') > 0 and input_money > product.get('price')]


# def init_vending_machine():
#     pass


if __name__ == '__main__':
    vending_machine = VendingMachineService()
    print(vending_machine.available_coin)
    # # State 1 Input coin
    # print(f'Before re-balance: {available_coin}')
    # sample_input = {
    #     '1': 20,
    #     '2': 5,
    #     '5': 2,
    #     '10': 0
    # }

    # # State 2 After finish input coin, update available coin to available coin in machine
    # available_coin.update({
    #     '1': available_coin.get('1') + sample_input.get('1'),
    #     '5': available_coin.get('5') + sample_input.get('5'),
    #     '10': available_coin.get('10') + sample_input.get('10'),
    # })
    # print(f'After re-balance: {available_coin}')

    # # State 3 Show money input as total input coin
    # amount_money_input = sample_input.get('1') + sample_input.get('5') + sample_input.get('10')
    # print(f'Input Money: {amount_money_input}')

    # # State 4 Show Product list if stock > 0 show else not
    # sample_product_list = list_available_product(amount_money_input)
    # print(sample_product_list)

    # # State 5 Buy 1 product
    # mock_option = 1
    # print(f'Buy Product: {sample_product_list[mock_option].get("name_th")}')

    # # State 6 change money from available coin
    # change_amount = amount_money_input - sample_product_list[mock_option].get('price')
    # print(f'Remaining Money: {change_amount}')

    # # State 7 update product stock and available_coin in machine
    # # If not enough to change money return all input money

    
    # print('Input Your Coin Value ...')
    # value_coin = input()
    # print(validate_is_acceptable_coin(value_coin))
    # print('Input Your Coin Amount ...')
    # amount_coin = int(input())
    # print(amount_coin)

