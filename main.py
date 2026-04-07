import random
from datetime import datetime, timedelta, UTC

import aeroparts_order_app as app

"""
Default library of parts, with all relevant parts

each part named for the type of item: A/B (plane), C/NC (certificate or no certificate), SL/NSL (shelf life or no shelf life)

description writes out the combination of variables
aircraft_type is either A320 or B737
requires_certificate is either True or False
shelf_life_days is either some number or None (meaning no shelf life)
hazmat is irrelevant for the current script so all false
"""
parts = {
  "A-C-SL": app.Part(
    part_no = "A-C-SL",
    description= "Plane A with certificate and shelf life", 
    aircraft_type = "A320", 
    requires_certificate = True, 
    shelf_life_days = 10, 
    hazmat = False, 
  ),
  "A-C-NSL": app.Part(
    part_no = "A-C-NSL",
    description= "Plane A with certificate and no shelf life", 
    aircraft_type = "A320", 
    requires_certificate = True, 
    shelf_life_days = None, 
    hazmat = False, 
  ),
  "A-NC-SL": app.Part(
    part_no = "A-NC-SL",
    description= "Plane A with shelf life and no certificate", 
    aircraft_type = "A320", 
    requires_certificate = False, 
    shelf_life_days = 10, 
    hazmat = False, 
  ),
  "A-NC-NSL": app.Part(
    part_no = "A-NC-NSL",
    description= "Plane A with no certificate and shelf life", 
    aircraft_type = "A320", 
    requires_certificate = False,
    shelf_life_days = None, 
    hazmat = False, 
  ),
  "B-C-SL": app.Part(
    part_no = "B-C-SL",
    description= "Plane B with certificate and shelf life", 
    aircraft_type = "B737", 
    requires_certificate = True,
    shelf_life_days = 10, 
    hazmat = False, 
  ),
  "B-C-NSL": app.Part(
    part_no = "B-C-NSL",
    description= "Plane B with certificate and no shelf life", 
    aircraft_type = "B737", 
    requires_certificate = True, 
    shelf_life_days = None, 
    hazmat = False, 
  ),
  "B-NC-SL": app.Part(
    part_no = "B-NC-SL",
    description= "Plane B with shelf life and no certificate", 
    aircraft_type = "B737", 
    requires_certificate = False, 
    shelf_life_days = 10, 
    hazmat = False, 
  ),
  "B-NC-NSL": app.Part(
    part_no = "B-NC-NSL",
    description= "Plane B with no certificate and shelf life", 
    aircraft_type = "B737", 
    requires_certificate = False, 
    shelf_life_days = None, 
    hazmat = False, 
  ),
} 

"""
Default list of StockItems that should cause no issues:
- item for each item in complete_parts
- all in warehouse AMS
- between 10 and 1000 on hand
- expiry date only if the item has shelf_life, and if so it's the maximum expiry date
"""
stock = []
for part in parts.values():
  stock_item = app.StockItem(
    part_no = part.part_no,
    warehouse= "AMS",
    on_hand = random.randint(10,1000),
    reserved = 0,
    safety_stock = 0,
    expires_on = datetime.now(UTC) + timedelta(days=part.shelf_life_days) if part.shelf_life_days else None
  )
  stock.append(stock_item)


"""
Returns list of SupplierOffers that should generally cause no issues:
- 2 items for each item in complete_parts
- a EUR and a USD version for each item
- unit price randomized between 1 and 1000
- lead_time randomized between 0 and 3 days
- all certified
"""
offers = []
for part in parts.values():
  supplier_offer_eur = app.SupplierOffer(
    supplier = "Some EUR supplier",
    part_no = part.part_no,
    unit_price = random.randint(100, 100000)/100,
    currency = "EUR",
    lead_time_days = random.randint(0,3),
    certified = True
  )
  supplier_offer_usd = app.SupplierOffer(
    supplier = "Some USD supplier",
    part_no = part.part_no,
    unit_price = random.randint(100, 100000)/100,
    currency = "USD",
    lead_time_days = random.randint(0,3),
    certified = True
  )
  offers.append(supplier_offer_eur)
  offers.append(supplier_offer_usd)



def get_user_input():
  """
  Asks the user for all relevant info in terminal. Doesn't verify any input.
  Creates an OrderRequest with the given input (and some default values) and returns it.

  For simplicity, the needed_by is calculated by asking the user in how many hours the part is needed.
  """
  part_no = ""
  keys = [key for key in parts.keys()]
  part_no = input(f"What part do you want to order? You can choose from: {keys} \n")

  aircraft_type = input("What plane is the part for? You can choose between A320 and B737 \n")

  quantity = int(input("How many of this item do you need? Please only enter a whole number \n"))

  priorities = [key for key in app.PRIORITY_SCORE.keys()]
  priority = input(f"What is the priority? You can choose from {priorities} \n").upper()

  needed_by = datetime.now(UTC) + timedelta(hours = int(input(f"In how many hours is the item needed? Please only enter a whole number \n")))

  request = app.OrderRequest(
    request_id=1,
    part_no=part_no,
    aircraft_type=aircraft_type,
    quantity=quantity,
    priority=priority,
    requested_by="main.py",
    needed_by=needed_by,
    cost_center="some cost center"
  )
  return request


def print_request_info(request):
  """
  Function to print the request info for troubleshooting. Not currently used.
  """
  print("--------------------------------------------------------------------------------")
  print(f"request_id: {request.request_id}")
  print(f"part_no: {request.part_no}")
  print(f"aircraft_type: {request.aircraft_type}")
  print(f"quantity: {request.quantity}")
  print(f"priority: {request.priority}")
  print(f"requested_by: {request.requested_by}")
  print(f"needed_by: {request.needed_by}")
  print(f"cost_center: {request.cost_center}")
  print("--------------------------------------------------------------------------------")


def print_order_info(response):
  """
  Function to print the final order info at the end of the process.
  """
  print("--------------------------------------------------------------------------------")
  print(f"order_id: {response.order_id}")
  print(f"source_type: {response.source_type}")
  print(f"source: {response.source}")
  print(f"quantity: {response.quantity}")
  print(f"eta: {response.eta}")
  print(f"total_cost_eur: {response.total_cost_eur}")
  print(f"notes: {response.notes}")
  print("--------------------------------------------------------------------------------")

order_request = get_user_input()

response = app.place_order(req=order_request, parts=parts, stock=stock, offers=offers)

print_order_info(response)

