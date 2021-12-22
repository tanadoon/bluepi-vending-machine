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
                'barcode_id': '001',
                'name': 'Pepsa non soda but za',
                'name_th': 'เป๊ปซ่า น้ำไม่อัดลมแต่เสือกซ่า',
                'price': 15,
                'stock': 200
            }, {
                'barcode_id': '002',
                'name': 'Cake Not Coke but Cake',
                'name_th': 'น้ำซ่าตราเค้ก',
                'price': 20,
                'stock': 2
            }, {
                'barcode_id': '003',
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

    def _create_change_coins_pool(self) -> list:
        return [[coin_value, self.reserved_change_coins.get(f'{coin_value}', 0) + self.input_coins.get(f'{coin_value}', 0)] for coin_value in self.accept_coin[::-1]]


    def calculate_change_coins(self, amount_change: int) -> dict:
        self.min_coin = float("inf")
        self.change_list = []
        self._do_calculate_minimum_coin_to_change(amount_change=amount_change, change_coins_pool=self._create_change_coins_pool())
        return {str(coin_value): self.change_list.count(coin_value) for coin_value in self.change_list}
    
    def _do_calculate_minimum_coin_to_change(self, amount_change: int, coin_count: int = 0, start: int = 0, coin_list: list = [], change_coins_pool: list = [[]]):
            if amount_change == 0 and self.min_coin > coin_count:
                self.change_list = coin_list
                self.min_coin = coin_count
            elif amount_change > 0:
                for i in range(start, len(change_coins_pool)):
                    if change_coins_pool[i][1] > 0:
                        change_coins_pool[i][1] -= 1
                        self._do_calculate_minimum_coin_to_change(
                            amount_change=amount_change - change_coins_pool[i][0], 
                            coin_count=coin_count + 1, 
                            start=i,
                            coin_list=coin_list + [change_coins_pool[i][0]],
                            change_coins_pool=change_coins_pool,
                        )
                        change_coins_pool[i][1] += 1
    
    def reset_input_coin(self) -> None:
        self.input_coins = self._init_input_coins()
    
    def update_reserved_change_coins(self, change_coins: dict, reset_input_coin_flag: bool = False) -> None:
        for coin_value in self.accept_coin:
            self.reserved_change_coins.update({
                f'{coin_value}': (self.reserved_change_coins.get(f'{coin_value}', 0) + self.input_coins.get(f'{coin_value}', 0)) - change_coins.get(f'{coin_value}', 0)
            })
        if reset_input_coin_flag:
            self.reset_input_coin()
    
    def update_product_stock_with_barcode_id(self, barcode_id: str, amount_change: int = -1) -> None:
        for product in self.product_list:
            if product.get('barcode_id') == barcode_id:
                product.update({
                    'stock': product.get('stock') + amount_change
                })