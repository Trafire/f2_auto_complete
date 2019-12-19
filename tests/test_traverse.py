import pytest
from parse import dates
from navigation import traverse


class TestTraverse():
    system = 'f2_canada_real'
    from_date = dates.menu_date('19/12/19')
    to_date = dates.menu_date('31/12/19')

    def test_to_main_menu(self):
        return traverse.main_menu(TestTraverse.system)


    # stock tests
    def test_main_menu_stock(self):
        return traverse.main_menu_stock(TestTraverse.system)

    def test_main_menu_stock_stock_per_location(self):
        return traverse.main_menu_stock_stock_per_location(TestTraverse.system)

   
    def test_main_menu_stock_stock_per_location_edit_stock(self):
        return traverse.main_menu_stock_stock_per_location_edit_stock(TestTraverse.system)

    def test_main_menu_stock_stock_per_location_edit_stock_date(self):
        return traverse.main_menu_stock_stock_per_location_edit_stock_date(TestTraverse.system, TestTraverse.from_date,
                                                                           TestTraverse.to_date)

    def test_main_menu_stock_stock_per_location_edit_stock_date_flowers(self):
        return traverse.main_menu_stock_stock_per_location_edit_stock_date_flowers(TestTraverse.system,
                                                                                   TestTraverse.from_date,
                                                                                   TestTraverse.to_date)

    def test_main_menu_purchase(self):
        return traverse.main_menu_purchase(TestTraverse.system)
    
    ##purchase tests

    def test_main_menu_purchase(self):
        return traverse.main_menu_purchase(TestTraverse.system)

    def test_main_menu_purchase_default(self):
        return traverse.main_menu_purchase_default(TestTraverse.system)

    def test_main_menu_purchase_default_purchase_distribute(self):
        return traverse.main_menu_purchase_default_purchase_distribute(TestTraverse.system)
    

    def test_main_menu_purchase_default_purchase_distribute_flowers(self):
        return traverse.main_menu_purchase_default_purchase_distribute_flowers(TestTraverse.system)
    
    def test_main_menu_purchase_default_purchase_distribute_flowers_purchase(self):
        return traverse.main_menu_purchase_default_purchase_distribute_flowers_purchase(TestTraverse.system,TestTraverse.from_date)
    

    def test_main_menu_purchase_default_input_purchases(self):
        return traverse.main_menu_purchase_default_input_purchases(TestTraverse.system)
   
    def test_main_menu_purchase_default_input_purchases_flowers(self):
        return traverse.main_menu_purchase_default_input_purchases_flowers(TestTraverse.system)
    
    def test_main_menu_purchase_default_input_purchases(self):
        return traverse.main_menu_purchase_default_input_purchases(TestTraverse.system)
    

    def test_main_menu_purchase_default_input_purchases_flowers(self):
        return traverse.main_menu_purchase_default_input_purchases_flowers(TestTraverse.system)

    def test_main_menu_purchase_default_input_purchases_flowers_date(self):
        return traverse.main_menu_purchase_default_input_purchases_flowers_date(TestTraverse.system,
                                                                                TestTraverse.from_date)
