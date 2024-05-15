from redistribution_method.constants import FIRST_INDEX, SECOND_INDEX


class TransferringElementToPlan:
    def __init__(
            self, sparse_matrix: list[list[int]],
            cost_matrix: list[list[int]],
            transportation_plan: list[list[int]],
            storages: list[int],
            shops: list[int],
            item_cors: list[int]
    ):
        self.sparse_matrix = sparse_matrix
        self.cost_matrix = cost_matrix
        self.transportation_plan = transportation_plan
        self.storages = storages
        self.shops = shops
        self.item_cors = item_cors
        self.storages_item = storages[item_cors[FIRST_INDEX]]
        self.shops_item = shops[item_cors[SECOND_INDEX]]
        self.ignoring_rows = []
        self.ignoring_columns = []

    def set_new_item_cors(self, item_cors: list[int]):
        self.item_cors = item_cors
        self.storages_item = self.storages[item_cors[FIRST_INDEX]]
        self.shops_item = self.shops[item_cors[SECOND_INDEX]]

    def calculate(self):
        self.comparing_items()

    def comparing_items(self):
        if self.shops_item > self.storages_item:
            self.transfer_storage_to_plan()
        elif self.shops_item == self.storages_item:
            self.transfer_shop_and_storage_to_plan()
        else:
            self.transfer_shop_to_plan()

    def transfer_storage_to_plan(self):
        self.transportation_plan[self.item_cors[FIRST_INDEX]][self.item_cors[SECOND_INDEX]] = self.storages_item
        self.shops[self.item_cors[SECOND_INDEX]] -= self.storages_item

        self.ignoring_rows.append(self.item_cors[FIRST_INDEX])

    def transfer_shop_and_storage_to_plan(self):
        self.transportation_plan[self.item_cors[FIRST_INDEX]][self.item_cors[SECOND_INDEX]] = self.storages_item

        self.ignoring_columns.append(self.item_cors[SECOND_INDEX])
        self.ignoring_rows.append(self.item_cors[FIRST_INDEX])

    def transfer_shop_to_plan(self):
        self.transportation_plan[self.item_cors[FIRST_INDEX]][self.item_cors[SECOND_INDEX]] = self.shops_item
        self.storages[self.item_cors[FIRST_INDEX]] -= self.shops_item

        self.ignoring_columns.append(self.item_cors[SECOND_INDEX])
