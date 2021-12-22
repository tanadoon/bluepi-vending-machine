class VendingMachineService:
    def __init__(self):
        self.accept_coin = [1, 5, 10]
        self.reserved_change_coins = self._init_reserved_change_coins()
        self.product_list = self._init_product_list()
        self.input_coins = self._init_input_coins()
    
    def _init_reserved_change_coins(self):
        return {
            '1': 10,
            '5': 2,
            '10': 2
        }

    def _init_input_coins(self):
        return {
            '1': 0,
            '5': 0,
            '10': 0,
        }

    def _init_product_list(self):
        return [
            {
                'name': 'Pepsa non soda but za',
                'name_th': 'เป๊ปซ่า น้ำไม่อัดลมแต่เสือกซ่า',
                'price': 15,
                'stock': 200
            }, {
                'name': 'Cake Not Coke but Cake',
                'name_th': 'น้ำซ่าตราเค้ก',
                'price': 20,
                'stock': 2
            }, {
                'name': 'Peach Soda',
                'name_th': 'น้ำซ่า 0 แคล รสพีช',
                'price': 10,
                'stock': 0
            },
        ]

    def update_input_state(self, input_coins_dict: dict) -> None:
        self.input_coins = input_coins_dict

    def show_money_input(self):
        total = 0
        for coin in self.accept_coin:
            total += coin*self.input_coins.get(f'{coin}')

        return total
    
    def list_purchaseable_products(self, total_money) -> list:
        # result_list = []
        # for product in self.product_list:
        #     if product.get('stock') > 0 and total_money > product.get('price'):
        #         result_list.append(product)

        return [product for product in self.product_list if product.get('stock') > 0 and total_money > product.get('price')]

    def change_coins(self, amount_change: int):
        def _calculte_minimum_coin_to_change(amount_change: int = amount_change, coin_count: int = 0, coin_list: list = []):
            if amount_change == 0 and self.min_coin > coin_count:
                self.change_list = coin_list
                self.min_coin = coin_count
            elif amount_change > 0:
                for coin_value in self.accept_coin[::-1]:
                    if self.reserved_change_coins.get(f'{coin_value}') > 0:
                        self.reserved_change_coins.update({
                            f'{coin_value}': self.reserved_change_coins.get(f'{coin_value}') - 1
                        })
                        _calculte_minimum_coin_to_change(amount_change-coin_value, coin_count+1, coin_list+[coin_value])
                        self.reserved_change_coins.update({
                            f'{coin_value}': self.reserved_change_coins.get(f'{coin_value}') + 1
                        })

        self.min_coin = float("inf")
        self.change_list = []
        _calculte_minimum_coin_to_change()
        return {str(coin_value): self.change_list.count(coin_value) for coin_value in self.change_list}
