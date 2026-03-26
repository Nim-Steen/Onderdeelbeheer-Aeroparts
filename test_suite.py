import aeroparts_order_app as app
from datetime import datetime

# A class to test the full system, so everything that happens when place_order is called
class TestClassSystem:
  parts = {} # insert str: app.Part dictionary with some possible parts, where the str is the part_no
  stock = [] # insert List of app.StockItem with the items available in warehouses
  offers = [] # insert List of app.SupplierOffer with the items that can be bought from suppliers

  def example_test(self):
    request = app.OrderRequest("some id", "some no", "some type", 0, "prio", "requester", datetime.now(), "center") 
    # insert data in request for the tested order request
    # optionally change the self.parts/self.stock/self.offers for the specific test

    response = app.place_order(request, self.parts, self.stock, self.offers)
    
    assert "statement to test (probably from response?)" == "whatever you want to test"
    # test will pass if the 'assert' statement is correct, and fail otherwise





# A class to test the method validate_request
class TestClassUnitValidateRequest:
  parts = {} # insert str: app.Part dictionary with some possible parts, where the str is the part_no

  def example_test(self):
    request = app.OrderRequest("some id", "some no", "some type", 0, "prio", "requester", datetime.now(), "center")
    # insert data in request for the tested order request
    # optionally change the self.parts for the specific test

    response = app.validate_request(request, self.parts)

    assert "statement to test (probably from response?)" == "whatever you want to test"
    # test will pass if the 'assert' statement is correct, and fail otherwise