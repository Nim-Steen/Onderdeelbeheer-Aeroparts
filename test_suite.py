import aeroparts_order_app as app
from datetime import datetime

# insert str: app.Part dictionary with some possible parts, where the str is the part_no
# each part named for the type of item: A/B (plane), C/NC (certificate or no certificate), SL/NSL (shelf life or no shelf life)
parts = {
  "A-C-SL": app.Part(
    part_no = "A-C-SL",
    description= "Plane A with certificate and shelf life", # irrelevant in script
    aircraft_type = "A320",           # e.g. "A320", "B737" 
    requires_certificate = True,   # EASA Form 1 / FAA 8130-3 
    shelf_life_days = 10,  # None means no shelf life 
    hazmat = False, # irrelevant in script
  ),
  "A-C-NSL": app.Part(
    part_no = "A-C-NSL",
    description= "Plane A with certificate and no shelf life", # irrelevant in script
    aircraft_type = "A320",           # e.g. "A320", "B737" 
    requires_certificate = True,   # EASA Form 1 / FAA 8130-3 
    shelf_life_days = None,  # None means no shelf life 
    hazmat = False, # irrelevant in script
  ),
  "A-NC-SL": app.Part(
    part_no = "A-NC-SL",
    description= "Plane A with shelf life and no certificate", # irrelevant in script
    aircraft_type = "A320",           # e.g. "A320", "B737" 
    requires_certificate = False,   # EASA Form 1 / FAA 8130-3 
    shelf_life_days = 10,  # None means no shelf life 
    hazmat = False, # irrelevant in script
  ),
  "A-NC-NSL": app.Part(
    part_no = "4",
    description= "Plane A with no certificate and shelf life", # irrelevant in script
    aircraft_type = "A320",           # e.g. "A320", "B737" 
    requires_certificate = False,   # EASA Form 1 / FAA 8130-3 
    shelf_life_days = None,  # None means no shelf life 
    hazmat = False, # irrelevant in script
  ),
  "B-C-SL": app.Part(
    part_no = "B-C-SL",
    description= "Plane B with certificate and shelf life", # irrelevant in script
    aircraft_type = "B737",           # e.g. "A320", "B737" 
    requires_certificate = True,   # EASA Form 1 / FAA 8130-3 
    shelf_life_days = 10,  # None means no shelf life 
    hazmat = False, # irrelevant in script
  ),
  "B-C-NSL": app.Part(
    part_no = "B-C-NSL",
    description= "Plane B with certificate and no shelf life", # irrelevant in script
    aircraft_type = "B737",           # e.g. "A320", "B737" 
    requires_certificate = True,   # EASA Form 1 / FAA 8130-3 
    shelf_life_days = None,  # None means no shelf life 
    hazmat = False, # irrelevant in script
  ),
  "B-NC-SL": app.Part(
    part_no = "B-NC-SL",
    description= "Plane B with shelf life and no certificate", # irrelevant in script
    aircraft_type = "B737",           # e.g. "A320", "B737" 
    requires_certificate = False,   # EASA Form 1 / FAA 8130-3 
    shelf_life_days = 10,  # None means no shelf life 
    hazmat = False, # irrelevant in script
  ),
  "B-NC-NSL": app.Part(
    part_no = "B-NC-NSL",
    description= "Plane B with no certificate and shelf life", # irrelevant in script
    aircraft_type = "B737",           # e.g. "A320", "B737" 
    requires_certificate = False,   # EASA Form 1 / FAA 8130-3 
    shelf_life_days = None,  # None means no shelf life 
    hazmat = False, # irrelevant in script
  ),
} 

# A class to test the full system, so everything that happens when place_order is called
class TestClassSystem:
  stock = [] # insert List of app.StockItem with the items available in warehouses
  offers = [] # insert List of app.SupplierOffer with the items that can be bought from suppliers

  
  
  def test_example(self):
    request = app.OrderRequest("some id", "some no", "some type", 0, "prio", "requester", datetime.now(), "center") 
    # insert data in request for the tested order request
    # optionally change the self.parts/self.stock/self.offers for the specific test

    response = app.place_order(request, parts, self.stock, self.offers)
    
    assert "statement to test (probably from response?)" == "whatever you want to test"
    # test will pass if the 'assert' statement is correct, and fail otherwise





# A class to test the method validate_request
class TestClassUnitValidateRequest:
  pass

  def test_example(self):
    request = app.OrderRequest("some id", "some no", "some type", 0, "prio", "requester", datetime.now(), "center")
    # insert data in request for the tested order request
    # optionally change the self.parts for the specific test

    response = app.validate_request(request, parts)

    assert "statement to test (probably from response?)" == "whatever you want to test"
    # test will pass if the 'assert' statement is correct, and fail otherwise