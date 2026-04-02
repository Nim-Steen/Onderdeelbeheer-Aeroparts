"""
PREREQUISITE: typ het volgende in terminal: (dit hoeft alleen de eerste keer)
  pip install -U pytest

Om tests uit te voeren, typ het volgende in terminal: 
  python -m pytest
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
from datetime import datetime, timedelta
import pytest
import random


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
    needed_by = datetime.now() + timedelta(days=30),
    cost_center = "The cost center"
  )
  return request

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
      expires_on = datetime.now() + timedelta(days=part.shelf_life_days) if part.shelf_life_days else None
    )
    stock.append(stock_item)
  return stock
  
@pytest.fixture
def complete_offers(complete_parts):
  """
  Returns list of SupplierOffers that should generally cause no issues:
  - 2 items for each item in complete_parts
  - a EUR and a USD version for each item
  - unit price randomized between 1 and 1000
  - lead_time randomized between 0 and 3 days
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
  return offers

# A class to test the full system, so everything that happens when place_order is called
class TestClassSystem:  
  def test_example(self, complete_parts, complete_AMS_stock, complete_offers):
    """
    Dit is een voorbeeld van een test van de functie place_order.
    Vul op de eerste regel de variabelen in van de OrderRequest die je wilt testen, de input.
    Maar eventueel een eigen parts/stock/offers lijst aan zoals relevant voor de test.
    Roep de functie place_order op, en sla deze op in een variabele (hier 'response').
    Schrijf een assert statement waar je de 'response' vergelijkt met de verwachte output.
    """
    request = app.OrderRequest("some id", "some no", "some type", 0, "prio", "requester", datetime.now(), "center") 

    response = app.place_order(request, complete_parts, complete_AMS_stock, complete_offers)
    
    assert "statement to test (probably from response?)" == "whatever you want to test"





# A class to test the method validate_request
class TestClassUnitValidateRequest:
  def test_example(self, complete_parts):
    """
    Dit is een voorbeeld van een test van de functie validate_request.
    Vul op de eerste regel de variabelen in van de OrderRequest die je wilt testen, de input.
    Maar eventueel een eigen parts lijst aan zoals relevant voor de test.
    Roep de functie validate_request op, en sla deze op in een variabele (hier 'response').
    Schrijf een assert statement waar je de 'response' vergelijkt met de verwachte output.
    """
    request = app.OrderRequest("some id", "some no", "some type", 0, "prio", "requester", datetime.now(), "center")

    response = app.validate_request(request, complete_parts)

    assert "statement to test (probably from response?)" == "whatever you want to test"