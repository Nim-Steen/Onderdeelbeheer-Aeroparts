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

# A class to test the full system, so everything that happens when place_order is called
class TestClassSystem:
  pass
  # @pytest.fixture
  # def complete_stock():
  #   stock = [] # TODO insert List of app.StockItem with the items available in warehouses
  #   return stock
  
  # @pytest.fixture
  # def complete_offers():
  #   offers = [] # TODO insert List of app.SupplierOffer with the items that can be bought from suppliers
  #   return offers

  
  
  # def test_example(self, complete_parts, complete_stock, complete_offers):
  #   """
  #   Dit is een voorbeeld van een test van de functie place_order.
  #   Vul op de eerste regel de variabelen in van de OrderRequest die je wilt testen, de input.
  #   Maar eventueel een eigen parts/stock/offers lijst aan zoals relevant voor de test.
  #   Roep de functie place_order op, en sla deze op in een variabele (hier 'response').
  #   Schrijf een assert statement waar je de 'response' vergelijkt met de verwachte output.
  #   """
  #   request = app.OrderRequest("some id", "some no", "some type", 0, "prio", "requester", datetime.now(), "center") 

  #   response = app.place_order(request, complete_parts, complete_stock, complete_offers)
    
  #   assert "statement to test (probably from response?)" == "whatever you want to test"





# A class to test the method validate_request
class TestClassUnitValidateRequest:
  pass

  # def test_example(self, complete_parts):
  #   """
  #   Dit is een voorbeeld van een test van de functie validate_request.
  #   Vul op de eerste regel de variabelen in van de OrderRequest die je wilt testen, de input.
  #   Maar eventueel een eigen parts lijst aan zoals relevant voor de test.
  #   Roep de functie validate_request op, en sla deze op in een variabele (hier 'response').
  #   Schrijf een assert statement waar je de 'response' vergelijkt met de verwachte output.
  #   """
  #   request = app.OrderRequest("some id", "some no", "some type", 0, "prio", "requester", datetime.now(), "center")

  #   response = app.validate_request(request, complete_parts)

  #   assert "statement to test (probably from response?)" == "whatever you want to test"

  def test_case_12(self, complete_parts, basic_order_request):
    """
    Test changes the airplane_type of the basic order request to B737 to create an invalid order request as the part is for airplane_type A320
    It then checks all issues raised by validate_request and sets compatible to False if an issue contains "not compatible"
    Test passes if compatible has been set to False
    """
    basic_order_request.aircraft_type = "B737"
    response = app.validate_request(basic_order_request, complete_parts)

    compatible = True

    for issue in response:
      if "not compatible" in issue:
        compatible = False

    assert compatible == False

  def test_case_34(self, complete_parts, basic_order_request):
    """
    Test changes the requested quantity of the basic order request to -1, a negative number.
    It then checks whether the validate_request function returns any issues.
    Test passes if any issue has been raised.

    NOTE: Test currently passes because an erronous issue is raised (see test_case_12), will no longer pass when this is fixed.
    """
    basic_order_request.quantity = -1
    response = app.validate_request(basic_order_request, complete_parts)

    assert response

  def test_case_36(self, complete_parts, basic_order_request):
    """
    Test changes the requested quantity of the basic order request to 0.5, a fractional number.
    It then checks whether the validate_request function returns any issues.
    Test passes if any issue has been raised.

    NOTE: Test currently passes because an erronous issue is raised (see test_case_12), will no longer pass when this is fixed.
    """
    basic_order_request.quantity = 0.5
    response = app.validate_request(basic_order_request, complete_parts)

    assert response

  def test_case_38_and_42(self, complete_parts, basic_order_request):
    """
    Test checks whether the validate_request function returns any issues with the default parts and order request.
    Test passes if no issue has been raised.

    NOTE: Test currently fails because an erronous issue is raised (see test_case_12/test_case_40), will no longer fail when this is fixed.
    """
    response = app.validate_request(basic_order_request, complete_parts)

    assert not response

  def test_case_40(self, complete_parts, basic_order_request):
    """
    Test changes the airplane_type of the basic order request to B737 to create an invalid order request as the part is for airplane_type A320
    It then checks whether the validate_request function returns any issues.
    Test passes if any issue has been raised.
    """
    basic_order_request.aircraft_type = "B737"
    response = app.validate_request(basic_order_request, complete_parts)

    assert response