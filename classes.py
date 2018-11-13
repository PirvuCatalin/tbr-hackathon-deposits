class Article:
    def __init__(self, code, pallet_quantity, single_unit_weight,
                 pallet_weight, single_unit_volume, pallet_volume):
        self.code = code
        self.pallet_quantity = pallet_quantity
        self.single_unit_weight = single_unit_weight
        self.pallet_weight = pallet_weight
        self.single_unit_volume = single_unit_volume
        self.pallet_volume = pallet_volume


class Stock:
    def __init__(self, code, stock_area_a, stock_area_b, stock_area_c):
        self.code = code
        self.stock_area_a = stock_area_a
        self.stock_area_b = stock_area_b
        self.stock_area_c = stock_area_c
        #D stock is infinite, no need to initialise it


class StockRule:
    def __init__(self, article_code, storage_area_code, min_quantity, max_quantity, max_capacity):
        self.article_code = article_code
        self.storage_area_code = storage_area_code
        self.min_quantity = min_quantity
        self.max_quantity = max_quantity
        self.max_capacity = max_capacity


class StorageArea:
    def __init__(self, code, area, capacity, max_weight, max_volume):
        self.code = code
        self.area = area
        self.capacity = capacity
        self.max_weight = max_weight
        self.max_volume = max_volume

#todo: activity
#network_transport o sa fie dictionar, cheie SOURCE:DESTINATION cu val TIMP