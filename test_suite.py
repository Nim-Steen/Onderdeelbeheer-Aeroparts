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
from datetime import datetime
import pytest


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

  return parts

# A class to test the full system, so everything that happens when place_order is called
class TestClassSystem:

  @pytest.fixture
  def complete_stock():
    stock = [] # TODO insert List of app.StockItem with the items available in warehouses
    return stock
  
  @pytest.fixture
  def complete_offers():
    offers = [] # TODO insert List of app.SupplierOffer with the items that can be bought from suppliers
    return offers

  
  
  def test_example(self, complete_parts, complete_stock, complete_offers):
    request = app.OrderRequest("some id", "some no", "some type", 0, "prio", "requester", datetime.now(), "center") 
    # insert data in request for the tested order request
    # optionally change the parts/stock/offers for the specific test

    response = app.place_order(request, complete_parts, complete_stock, complete_offers)
    
    assert "statement to test (probably from response?)" == "whatever you want to test"





# A class to test the method validate_request
class TestClassUnitValidateRequest:
  pass

  def test_example(self, complete_parts):
    request = app.OrderRequest("some id", "some no", "some type", 0, "prio", "requester", datetime.now(), "center")
    # insert data in request for the tested order request
    # optionally change the parts for the specific test

    response = app.validate_request(request, complete_parts)

    assert "statement to test (probably from response?)" == "whatever you want to test"