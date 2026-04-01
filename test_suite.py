"""
PREREQUISITE: typ het volgende in terminal: (dit hoeft alleen de eerste keer)
  pip install -U pytest

Om tests uit te voeren, typ het volgende in terminal: 
  python -m pytest

Om een specifieke test, of test class, uit te voeren, kun je een deel selecteren:
  python -m pytest test_suite.py::[naam van class]                              Voor de hele class
  python -m pytest test_suite.py::[naam van class]::[naam van test]             Voor een specifieke test

Bijvoorbeeld:
 python -m pytest pytest test_suite.py::TestClassSystem::test_case_46
______________________________________________________________________________________________________

In dit bestand staan tests (functies beginnende met 'test') verdeeld in test classes (classes beginnende met Test). 
In de basis is een test een functie met een 'assert' statement, en de test controleert of wat er bij assert staat klopt.
Bijvoorbeeld: 
  def test_kan_ik_rekenen():
    assert 1==1
zal goedgekeurd worden, maar
  def test_ik_kan_niet_rekenen():
    assert 1==2
zal falen.

In de testfunctie kun je andere functies aanroepen. In het bijzonder kun je functies uit het aeroparts script aanroepen. 
Ik heb dat script hier 'app' genoemd, dus je kunt bijvoorbeeld de place_order functie gebruiken door 'app.place_order' te typen (met de variabelen tussen haakjes)

Om de variabelen makkelijker te maken kunnen we ze van tevoren definiëren als fixture, door er @pytest.fixture voor te zetten.
Zo heb ik aan het begin 'complete_parts' gedefiniëerd met alle mogelijke parts. 
Deze kunnen dan in alle tests gebruikt worden door het als variabele aan te roepen, bijv:
  @pytest.fixture
  def input():
    return 1

  def test_ik_kan_weer_niet_rekenen(input):
  input == 2

Qua organisatie is nu mijn idee om een class te maken per functie die getest moet worden. 
Dan kan in de class de relevante variabelen al gedefiniëerd worden, en eventueel in de test zelf nog worden aangepast. 
Maar dit is pas een eerste opzet en misschien niet de beste manier om dit aan te pakken. 
"""

import aeroparts_order_app as app
from datetime import datetime, timedelta, UTC
import pytest
import random
import math


@pytest.fixture
def complete_parts():
  """
  returns str: app.Part dictionary with some possible parts, where the str is the part_no. Covers every relevant combination of variables.

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
      shelf_life_days = 100, 
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
      shelf_life_days = 100, 
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
      shelf_life_days = 100, 
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
      shelf_life_days = 100, 
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
  return parts

@pytest.fixture
def basic_order_request():
  """
  Returns OrderRequest that should cause no issues:
  - Part and aircraft type correspond
  - Part doesnt need certificate and has no shelf life
  - Only 1 needed
  - routine priority
  - needed_by far in the future
  """
  request = app.OrderRequest(
    request_id = 1, 
    part_no = "A-NC-NSL", 
    aircraft_type="A320", 
    quantity = 1,
    priority = "ROUTINE",
    requested_by = "Mechanic",
    needed_by = datetime.now(UTC) + timedelta(days=30),
    cost_center = "The cost center"
  )
  return request

@pytest.fixture
def cert_request(basic_order_request):
  """
  Returns the basic_order_request above, but for the part that does need certification
  """
  basic_order_request.part_no = "A-C-NSL"
  return basic_order_request

@pytest.fixture
def low_needed_by_request(basic_order_request):
  """
  Returns the basic_order_request above, but with needed_by in 30 minutes
  """
  basic_order_request.needed_by = datetime.now(UTC) + timedelta(minutes = 30)
  return basic_order_request

@pytest.fixture
def shelf_life_request(basic_order_request):
  """
  Returns the basic_order_request above, but with an item with shelf life
  """
  basic_order_request.part_no = "A-NC-SL"
  return basic_order_request

@pytest.fixture
def incompatible_request(basic_order_request):
  """
  Returns the basic_order_request above, but for the other plane (incompatible with the part)
  """
  basic_order_request.aircraft_type = "B737"
  return basic_order_request

@pytest.fixture
def AOG_request(basic_order_request):
  """
  Returns the basic_order_request above, but with priority changed to "AOG"
  """
  basic_order_request.priority = "AOG"
  return basic_order_request

@pytest.fixture
def urgent_request(basic_order_request):
  """
  Returns the basic_order_request above, but with priority changed to "URGENT"
  """
  basic_order_request.priority = "URGENT"
  return basic_order_request

@pytest.fixture
def complete_AMS_stock(complete_parts):
  """
  Returns list of StockItems that should cause no issues:
  - item for each item in complete_parts
  - all in warehouse AMS
  - between 10 and 1000 on hand
  - expiry date only if the item has shelf_life, and if so it's the maximum expiry date
  """
  stock = []
  for part in complete_parts.values():
    stock_item = app.StockItem(
      part_no = part.part_no,
      warehouse= "AMS",
      on_hand = random.randint(10,1000),
      reserved = 0,
      safety_stock = 0,
      expires_on = datetime.now(UTC) + timedelta(days=part.shelf_life_days) if part.shelf_life_days else None
    )
    stock.append(stock_item)
  return stock

@pytest.fixture
def complete_expired_AMS_stock(complete_AMS_stock):
  """
  Returns default stock with expires_on set to yesterday
  """
  for stock in complete_AMS_stock:
    if stock.expires_on:
      stock.expires_on = datetime.now(UTC) - timedelta(days = 1)
  return complete_AMS_stock

@pytest.fixture
def no_AOG_AMS_stock(complete_AMS_stock, AOG_request):
  """
  Returns default stock with the items for AOG_request removed to force having no supply within AOG.
  """
  for stock_item in complete_AMS_stock:
      if (stock_item.part_no ==  AOG_request.part_no and 
          app.estimate_eta_from_warehouse(stock_item.warehouse, AOG_request) < datetime.now(UTC) + timedelta(hours = 1)):
        complete_AMS_stock.remove(stock_item)
  return complete_AMS_stock

@pytest.fixture
def no_urgent_AMS_stock(complete_AMS_stock, urgent_request):
  """
  Returns default stock with the items for urgent_request removed to force having no supply within urgent.
  """
  for stock_item in complete_AMS_stock:
      if (stock_item.part_no ==  urgent_request.part_no and 
          app.estimate_eta_from_warehouse(stock_item.warehouse, urgent_request) < datetime.now(UTC) + timedelta(days = 5)):
        complete_AMS_stock.remove(stock_item)
  return complete_AMS_stock
  
@pytest.fixture
def complete_offers(complete_parts):
  """
  Returns list of SupplierOffers that should generally cause no issues:
  - 2 items for each item in complete_parts
  - a EUR and a USD version for each item
  - unit price randomized between 1 and 1000
  - lead_time of 0 for EUR supplier, and 6 for USD supplier
  - all certified
  
  A lot here is randomized, make sure to change values or add a whole SupplierOffer if you need specific values
  """
  offers = []
  for part in complete_parts.values():
    supplier_offer_eur = app.SupplierOffer(
      supplier = "Some EUR supplier",
      part_no = part.part_no,
      unit_price = random.randint(100, 100000)/100,
      currency = "EUR",
      lead_time_days = 0,
      certified = True
    )
    supplier_offer_usd = app.SupplierOffer(
      supplier = "Some USD supplier",
      part_no = part.part_no,
      unit_price = random.randint(100, 100000)/100,
      currency = "USD",
      lead_time_days = 6,
      certified = True
    )
    offers.append(supplier_offer_eur)
    offers.append(supplier_offer_usd)
  return offers

@pytest.fixture
def complete_no_cert_offers(complete_offers):
  """
  Returns list of offers but with certified = False so it can't match the certification requirement
  """
  for supplier_offer in complete_offers:
    supplier_offer.certified = False
  return complete_offers

@pytest.fixture
def complete_no_AOG_offers(complete_offers):
  """
  Returns list of offers but with the lead_time_days increased so it can't match the AOG deadline
  """
  for supplier_offer in complete_offers:
    supplier_offer.lead_time_days = 4
  return complete_offers

@pytest.fixture
def complete_no_urgent_offers(complete_offers):
  """
  Returns list of offers but with the lead_time_days increased so it can't match the urgent deadline
  """
  for supplier_offer in complete_offers:
    supplier_offer.lead_time_days = 10
  return complete_offers

@pytest.fixture
def only_USD_offers(complete_offers):
  """
  Returns list of offers but with "EUR" offers removed
  """
  for supplier_offer in complete_offers:
    if supplier_offer == "EUR":
        complete_offers.remove(supplier_offer)
  return complete_offers



# A class to test the full system, so everything that happens when place_order is called
class TestClassSystem:
  def test_case_6(self, cert_request, complete_parts, complete_no_cert_offers):
    """
    Test calls the place_order function with a request requiring certification, a complete dictionary of parts, empty stock and offers without certification.
    It then checks all notes in the resulting OrderResult and sets certified to False if a note contains "certif" 
    (so it tests for "certified", "certification", "certificate", etc)

    Test passes if certified has been set to False
    """
    result = app.place_order(cert_request, complete_parts, [], complete_no_cert_offers)

    certified = True

    for note in result.notes:
      if "certif" in note:
        certified = False
        break
    
    assert not certified


  def test_case_9(self, low_needed_by_request, complete_parts, no_AOG_AMS_stock, complete_no_AOG_offers):
    """
    Test calls the place_order function with a request with 30 minute needed_by, a complete dictionary of parts, stock with ETA > 1hr and offers with lead_time of 4 days.
    It then checks all notes in the resulting OrderResult and sets in_time to False if a note contains "needed_by" 

    Test passes if in_time has been set to False
    """
    result = app.place_order(low_needed_by_request, complete_parts, no_AOG_AMS_stock, complete_no_AOG_offers)

    in_time = True

    for note in result.notes:
      if "needed_by" in note:
        in_time = False
        break

    assert not in_time

  def test_case_11(self, low_needed_by_request, complete_parts, complete_expired_AMS_stock):
    """
    Test calls the place_order function with a request for an item with shelf_life, a complete dictionary of parts, stock with only expired parts and no offers.
    It then checks all notes in the resulting OrderResult and sets expired to True if a note contains "expire" 

    Test passes if expired has been set to True
    """
    result = app.place_order(low_needed_by_request, complete_parts, complete_expired_AMS_stock, [])

    expired = False

    for note in result.notes:
      if "expire" in note:
        expired = True
        break

    assert expired


  def test_case_13(self, incompatible_request, complete_parts, complete_AMS_stock, complete_offers):
    """
    Test calls the place_order function with a request for an item for a different plane, a complete dictionary of parts, and complete stock and offers.
    It then checks all notes in the resulting OrderResult and sets compatible to False if a note contains "not compatible" 

    Test passes if compatible has been set to False
    """
    result = app.place_order(incompatible_request, complete_parts, complete_AMS_stock, complete_offers)

    compatible = True

    for note in result.notes:
      if "not compatible" in note:
        compatible = False
        break

    assert not compatible


  def test_case_24(self, basic_order_request, complete_parts, complete_AMS_stock):
    """
    Test notes the amount in stock of the requested item in the variable original_amount
    Then it runs the place_order function, and logs the stock of the requested item in the variable new_amount

    Test passes if the new_amount is equal to the original_amount minus the requested amount.
    """
    for item in complete_AMS_stock:
      if item.part_no == basic_order_request.part_no:
        original_amount = item.on_hand
        break

    app.place_order(basic_order_request, complete_parts, complete_AMS_stock, [])

    for item in complete_AMS_stock:
      if item.part_no == basic_order_request.part_no:
        new_amount = item.on_hand
        break
    
    assert new_amount == original_amount - basic_order_request.quantity



  def test_case_25(self, AOG_request, complete_parts, no_AOG_AMS_stock, complete_no_AOG_offers):
    """
    Test calls the place_order function with an AOG request, a complete dictionary of parts, and stock and offers that cannot meet the AOG-eta requirement.
    Test passes if no order is placed.
    """
    result = app.place_order(AOG_request, complete_parts, no_AOG_AMS_stock, complete_no_AOG_offers)

    assert not result


  def test_case_26(self, AOG_request, complete_parts, complete_AMS_stock, complete_no_AOG_offers):
    """
    Test calls the place_order function with an AOG request, a complete dictionary of parts, stock that can meet the AOG-eta requirement and offers that cannot.
    Test passes if the order placed has an eta within 1 hour.
    """
    result = app.place_order(AOG_request, complete_parts, complete_AMS_stock, complete_no_AOG_offers)

    assert result.eta < datetime.now(UTC) + timedelta(hours=1)


  def test_case_27(self, AOG_request, complete_parts, no_AOG_AMS_stock, complete_offers):
    """
    Test calls the place_order function with an AOG request, a complete dictionary of parts, offers that can meet the AOG-eta requirement and stock that cannot.
    Test passes if the order placed has an eta within 1 hour.

    Test currently passes/fails depending on the price of offers.
    """
    result = app.place_order(AOG_request, complete_parts, no_AOG_AMS_stock, complete_offers)

    assert result.eta < datetime.now(UTC) + timedelta(hours=1)


  def test_case_28(self, urgent_request, complete_parts, no_urgent_AMS_stock, complete_no_urgent_offers):
    """
    Test calls the place_order function with an urgent request, a complete dictionary of parts, and stock and offers that cannot meet the urgent-eta requirement.
    Test passes if no order is placed.
    """
    result = app.place_order(urgent_request, complete_parts, no_urgent_AMS_stock, complete_no_urgent_offers)

    assert not result


  def test_case_29(self, urgent_request, complete_parts, complete_AMS_stock, complete_no_urgent_offers):
    """
    Test calls the place_order function with an urgent request, a complete dictionary of parts, stock that can meet the urgent-eta requirement and offers that cannot.
    Test passes if the order placed has an eta within 5 days.
    """
    result = app.place_order(urgent_request, complete_parts, complete_AMS_stock, complete_no_urgent_offers)

    assert result.eta < datetime.now(UTC) + timedelta(days=5)


  def test_case_30(self, urgent_request, complete_parts, no_urgent_AMS_stock, complete_offers):
    """
    Test calls the place_order function with an urgent request, a complete dictionary of parts, offers that can meet the urgent-eta requirement and stock that cannot.
    Test passes if the order placed has an eta within 5 days.
    """
    result = app.place_order(urgent_request, complete_parts, no_urgent_AMS_stock, complete_offers)

    assert result.eta < datetime.now(UTC) + timedelta(days=5)
        

  def test_case_31(self, basic_order_request, complete_parts, no_urgent_AMS_stock, complete_no_urgent_offers):
    """
    Test calls the place_order function with a routine request, a complete dictionary of parts, and stock and offers that cannot meet the urgent-eta requirement.
    Test passes if an order is placed.
    """
    result = app.place_order(basic_order_request, complete_parts, no_urgent_AMS_stock, complete_no_urgent_offers)

    assert result


  def test_case_32(self, basic_order_request, complete_parts, complete_AMS_stock, complete_no_urgent_offers):
    """
    Test calls the place_order function with an routine request, a complete dictionary of parts, stock that can meet the urgent-eta requirement and offers that cannot.
    Test passes if an order is placed.
    """
    result = app.place_order(basic_order_request, complete_parts, complete_AMS_stock, complete_no_urgent_offers)

    assert result


  def test_case_33(self, basic_order_request, complete_parts, no_urgent_AMS_stock, complete_offers):
    """
    Test calls the place_order function with an routine request, a complete dictionary of parts, offers that can meet the urgent-eta requirement and stock that cannot.
    Test passes if an order is placed.
    """
    result = app.place_order(basic_order_request, complete_parts, no_urgent_AMS_stock, complete_offers)

    assert result


  def test_case_46(self, basic_order_request, complete_parts, only_USD_offers):
    """
    Test notes the cost of the item from the supplier and stores it as price_per_item
    Then it calculates the intended cost by multiplying by the exchange rate and the requested quantity
    Then it runs the place_order function.

    Test passes if the intended_cost is equal to the total_cost_eur in the result from place_order, both rounded to 3 decimals to avoid rounding errors
    """
    for item in only_USD_offers:
      if item.part_no == basic_order_request.part_no:
        price_per_item = item.unit_price
        break

    unit_cost_eur = price_per_item * app.FX_RATES_TO_EUR["USD"]
    intended_cost = unit_cost_eur * basic_order_request.quantity

    result = app.place_order(basic_order_request, complete_parts, [], only_USD_offers)

    assert round(result.total_cost_eur,3) == round(intended_cost, 3)




# A class to test the method validate_request
# class TestClassUnitValidateRequest:
#   def test_example(self, complete_parts):
#     """
#     Dit is een voorbeeld van een test van de functie validate_request.
#     Vul op de eerste regel de variabelen in van de OrderRequest die je wilt testen, de input.
#     Maar eventueel een eigen parts lijst aan zoals relevant voor de test.
#     Roep de functie validate_request op, en sla deze op in een variabele (hier 'response').
#     Schrijf een assert statement waar je de 'response' vergelijkt met de verwachte output.
#     """
#     request = app.OrderRequest("some id", "some no", "some type", 0, "prio", "requester", datetime.now(), "center")

#     response = app.validate_request(request, complete_parts)

#     assert "statement to test (probably from response?)" == "whatever you want to test"