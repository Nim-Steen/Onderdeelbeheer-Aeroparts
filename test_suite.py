"""
PREREQUISITE: typ het volgende in terminal: (dit hoeft alleen de eerste keer)
  pip install -U pytest

Om tests uit te voeren, typ het volgende in terminal: 
  python -m pytest

Om een specifieke test uit te voeren, typ je het nummer van de testcase hier: (maak er altijd 2 decimalen van, dus bijv '06' ipv '6')
  python -m pytest -k "[nummer]"
  Bijvoorbeeld: python -m pytest -k "06"

Om een test voor een specifiek test_criterium uit te voeren, typ het nummer van het criterium hier: (dit keer zonder de extra 0)
  python -m pytest -m criterium_[nummer]
  Bijvoorbeeld: python -m pytest -m "criterium_6"

Om alle tests voor een specifieke functie uit te voeren, typ de naam van de functie hierin:
  python -m pytest m method_[naam-van-functie]
  Bijvoorbeeld: python -m pytest -m "method_place_order"

Met 'or' en 'and' kun je meerdere voorwaarden aangeven en daardoor meer of minder tests uitvoeren:
  python -m pytest -k "06 or 14"
  voert testcase 6 en 14 uit ('bevat 06 of 14')

  python -m pytest -m "method_place_order and criterium_6"
  voert alleen tests uit die place_order testen voor criterium 6 (voldoet aan beide)

  python -m pytest -m "criterium_6 or criterium_7"
  voert alle tests uit voor criterium 6 en voor criterium 7

Dit kan verder gecombineerd met haakjes.
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

Voor verdere context in de log kun je print statements in je tests toevoegen, alles wat geprint wordt, zal in de log worden geschreven. 
"""

import aeroparts_order_app as app
from datetime import datetime, timedelta, UTC
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
  - Between 1 and 9 needed
  - routine priority
  - needed_by far in the future
  """
  request = app.OrderRequest(
    request_id = 1, 
    part_no = "A-NC-NSL", 
    aircraft_type="A320", 
    quantity = random.randint(1,9),
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
def past_needed_by_request(AOG_request):
  """
  Returns the AOG_request above, but with needed_by 30 minutes ago
  """
  AOG_request.needed_by = datetime.now(UTC) - timedelta(minutes = 30)
  return AOG_request

@pytest.fixture
def urgent_request(basic_order_request):
  """
  Returns the basic_order_request above, but with priority changed to "URGENT"
  """
  basic_order_request.priority = "URGENT"
  return basic_order_request

@pytest.fixture
def negative_request(basic_order_request):
  """
  Returns the basic_order_request above, but with quantity changed to -1
  """
  basic_order_request.quantity = -1
  return basic_order_request

@pytest.fixture
def fractional_request(basic_order_request):
  """
  Returns the basic_order_request above, but with quantity changed to 0.5
  """
  basic_order_request.quantity = 0.5
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

@pytest.fixture
def only_EUR_offers(complete_offers):
  """
  Returns list of offers but with "USD" offers removed
  """
  for supplier_offer in complete_offers:
    if supplier_offer == "USD":
        complete_offers.remove(supplier_offer)
  return complete_offers



# A class to test the method generate_order_id
class TestsGenerateOrderId:
  @pytest.mark.criterium_23
  @pytest.mark.method_generate_order_id
  def test_case_50(self, basic_order_request):
    """
    Test creates up to 20 orders ids. 
    Each new order_id is checked against a list of order_ids, and added to the list if it's not yet in there.
    If the order_id is already in the list, duplicate_id is set to True and the loop ends.

    The test passes if duplicate_id is not set to True. 
    """
    print("Test criterium 23: Als veel items in dezelfde seconde worden besteld, hebben ze ieder een uniek ordernummer")
    order_ids = []
    duplicate_id = False
    for _ in range(20):
      result = app.generate_order_id(basic_order_request)
      if result not in order_ids:
        order_ids.append(result)
      else:
        duplicate_id = True
        break

    assert not duplicate_id



# A class to test the full system, so everything that happens when place_order is called
class TestClassSystem:
  @pytest.mark.criterium_3
  @pytest.mark.method_place_order
  def test_case_06(self, cert_request, complete_parts, complete_no_cert_offers):
    """
    Test calls the place_order function with a request requiring certification, a complete dictionary of parts, empty stock and offers without certification.
    It then checks all notes in the resulting OrderResult and sets certified to False if a note contains "certif" 
    (so it tests for "certified", "certification", "certificate", etc)

    Test passes if certified has been set to False
    """
    print("Test criterium 3: Als bij een order met certificering geen onderdeel met certificering beschikbaar is, krijgt de gebruiker hier melding van")
    result = app.place_order(cert_request, complete_parts, [], complete_no_cert_offers)

    certified = True

    for note in result.notes:
      if "certif" in note:
        certified = False
        break
    
    assert not certified


  @pytest.mark.criterium_4
  @pytest.mark.method_place_order
  def test_case_09(self, low_needed_by_request, complete_parts, no_AOG_AMS_stock, complete_no_AOG_offers):
    """
    Test calls the place_order function with a request with 30 minute needed_by, a complete dictionary of parts, stock with ETA > 1hr and offers with lead_time of 4 days.
    It then checks all notes in the resulting OrderResult and sets in_time to False if a note contains "needed_by" 

    Test passes if in_time has been set to False
    """
    print("Test criterium 4: Als bij een order met ETA geen onderdeel binnen de ETA beschikbaar is, krijgt de gebruiker hier melding van")

    result = app.place_order(low_needed_by_request, complete_parts, no_AOG_AMS_stock, complete_no_AOG_offers)

    in_time = True

    for note in result.notes:
      if "needed_by" in note:
        in_time = False
        break

    assert not in_time

  @pytest.mark.criterium_5
  @pytest.mark.method_place_order
  def test_case_11(self, low_needed_by_request, complete_parts, complete_expired_AMS_stock):
    """
    Test calls the place_order function with a request for an item with shelf_life, a complete dictionary of parts, stock with only expired parts and no offers.
    It then checks all notes in the resulting OrderResult and sets expired to True if a note contains "expire" 

    Test passes if expired has been set to True
    """
    print("Test criterium 5: Als bij een order met vervaldatum geen onderdeel binnen de vervaldatum beschikbaar is, krijgt de gebruiker hier melding van")
    result = app.place_order(low_needed_by_request, complete_parts, complete_expired_AMS_stock, [])

    expired = False

    for note in result.notes:
      if "expire" in note:
        expired = True
        break

    assert expired


  @pytest.mark.criterium_6
  @pytest.mark.method_place_order
  def test_case_13(self, incompatible_request, complete_parts, complete_AMS_stock, complete_offers):
    """
    Test calls the place_order function with a request for an item for a different plane, a complete dictionary of parts, and complete stock and offers.
    It then checks all notes in the resulting OrderResult and sets compatible to False if a note contains "not compatible" 

    Test passes if compatible has been set to False
    """
    print("test criterium 6: Als bij een order voor een vliegtuig geen onderdeel voor dat vliegtuig beschikbaar is, krijgt de gebruiker hier melding van")
    result = app.place_order(incompatible_request, complete_parts, complete_AMS_stock, complete_offers)

    compatible = True

    for note in result.notes:
      if "not compatible" in note:
        compatible = False
        break

    assert not compatible


  @pytest.mark.criterium_7
  @pytest.mark.method_place_order
  def test_case_14(self, basic_order_request, complete_parts, complete_AMS_stock, complete_offers):
    """
    Test calls the place_order function with a request for an item without issues, a complete dictionary of parts, and complete stock and offers.
    It then checks whether there are notes in the resulting OrderResult.

    Test passes if there are no notes.
    """
    print("Test criterium 7: Als een order zonder problemen kan worden uitgevoerd, krijgt de gebruiker geen errormelding")
    result = app.place_order(basic_order_request, complete_parts, complete_AMS_stock, complete_offers)

    assert not result.notes


  @pytest.mark.criterium_11
  @pytest.mark.method_place_order
  def test_case_20(self, basic_order_request, complete_parts, complete_offers):
    """
    Test calls the place_order function with a request for an item without issues, a complete dictionary of parts, complete offers (which contains 2 offers for the part) and empty stock.
    It then checks whether more than one option is returned.
    It assumes an array of options is returned and checks the length.

    Test passes if the result is an array and more than one option is returned.
    """
    print("Test criterium 11: Als een order niet door een warehouse kan worden vervuld, worden de verschillende goedgekeurde leveranciers met hun prijzen getoond.")
    result = app.place_order(basic_order_request, complete_parts, [], complete_offers)

    assert len(result) > 1


  @pytest.mark.criterium_12
  @pytest.mark.method_place_order
  def test_case_24(self, basic_order_request, complete_parts, complete_AMS_stock):
    """
    Test notes the amount in stock of the requested item in the variable original_amount
    Then it runs the place_order function, and logs the stock of the requested item in the variable new_amount

    Test passes if the new_amount is equal to the original_amount minus the requested amount.
    """
    print("Test criterium 12: Als een part uit een warehouse wordt gehaald, dan wordt de stock van dit item met de gevraagde hoeveelheid verlaagd bij dit warehouse.")
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


  @pytest.mark.criterium_13
  @pytest.mark.method_place_order
  def test_case_25(self, AOG_request, complete_parts, no_AOG_AMS_stock, complete_no_AOG_offers):
    """
    Test calls the place_order function with an AOG request, a complete dictionary of parts, and stock and offers that cannot meet the AOG-eta requirement.
    Test passes if no order is placed.
    """
    print("Test criterium 13: Wanneer een item met AOG-prioriteit wordt besteld, dan wordt alleen besteld wanneer het onderdeel binnen een uur leverbaar is")
    result = app.place_order(AOG_request, complete_parts, no_AOG_AMS_stock, complete_no_AOG_offers)

    assert not result


  @pytest.mark.criterium_13
  @pytest.mark.method_place_order
  def test_case_26(self, AOG_request, complete_parts, complete_AMS_stock, complete_no_AOG_offers):
    """
    Test calls the place_order function with an AOG request, a complete dictionary of parts, stock that can meet the AOG-eta requirement and offers that cannot.
    Test passes if the order placed has an eta within 1 hour.
    """
    print("Test criterium 13: Wanneer een item met AOG-prioriteit wordt besteld, dan wordt alleen besteld wanneer het onderdeel binnen een uur leverbaar is")
    result = app.place_order(AOG_request, complete_parts, complete_AMS_stock, complete_no_AOG_offers)

    assert result.eta < datetime.now(UTC) + timedelta(hours=1)


  @pytest.mark.criterium_13
  @pytest.mark.method_place_order
  def test_case_27(self, AOG_request, complete_parts, no_AOG_AMS_stock, complete_offers):
    """
    Test calls the place_order function with an AOG request, a complete dictionary of parts, offers that can meet the AOG-eta requirement and stock that cannot.
    Test passes if the order placed has an eta within 1 hour.

    Test currently passes/fails depending on the price of offers.
    """
    print("Test criterium 13: Wanneer een item met AOG-prioriteit wordt besteld, dan wordt alleen besteld wanneer het onderdeel binnen een uur leverbaar is")
    result = app.place_order(AOG_request, complete_parts, no_AOG_AMS_stock, complete_offers)

    assert result.eta < datetime.now(UTC) + timedelta(hours=1)


  @pytest.mark.criterium_14
  @pytest.mark.method_place_order
  def test_case_28(self, urgent_request, complete_parts, no_urgent_AMS_stock, complete_no_urgent_offers):
    """
    Test calls the place_order function with an urgent request, a complete dictionary of parts, and stock and offers that cannot meet the urgent-eta requirement.
    Test passes if no order is placed.
    """
    print("Test criterium 14: Wanneer een item met urgent-prioriteit wordt besteld, dan wordt alleen besteld wanneer het onderdeel binnen vijf dagen leverbaar is")
    result = app.place_order(urgent_request, complete_parts, no_urgent_AMS_stock, complete_no_urgent_offers)

    assert not result


  @pytest.mark.criterium_14
  @pytest.mark.method_place_order
  def test_case_29(self, urgent_request, complete_parts, complete_AMS_stock, complete_no_urgent_offers):
    """
    Test calls the place_order function with an urgent request, a complete dictionary of parts, stock that can meet the urgent-eta requirement and offers that cannot.
    Test passes if the order placed has an eta within 5 days.
    """
    print("Test criterium 14: Wanneer een item met urgent-prioriteit wordt besteld, dan wordt alleen besteld wanneer het onderdeel binnen vijf dagen leverbaar is")
    result = app.place_order(urgent_request, complete_parts, complete_AMS_stock, complete_no_urgent_offers)

    assert result.eta < datetime.now(UTC) + timedelta(days=5)


  @pytest.mark.criterium_14
  @pytest.mark.method_place_order
  def test_case_30(self, urgent_request, complete_parts, no_urgent_AMS_stock, complete_offers):
    """
    Test calls the place_order function with an urgent request, a complete dictionary of parts, offers that can meet the urgent-eta requirement and stock that cannot.
    Test passes if the order placed has an eta within 5 days.
    """
    print("Test criterium 14: Wanneer een item met urgent-prioriteit wordt besteld, dan wordt alleen besteld wanneer het onderdeel binnen vijf dagen leverbaar is")
    result = app.place_order(urgent_request, complete_parts, no_urgent_AMS_stock, complete_offers)

    assert result.eta < datetime.now(UTC) + timedelta(days=5)
        

  @pytest.mark.criterium_15
  @pytest.mark.method_place_order
  def test_case_31(self, basic_order_request, complete_parts, no_urgent_AMS_stock, complete_no_urgent_offers):
    """
    Test calls the place_order function with a routine request, a complete dictionary of parts, and stock and offers that cannot meet the urgent-eta requirement.
    Test passes if an order is placed.
    """
    print("Test criterium 15: Wanneer een item met routine-prioriteit wordt besteld, dan kan een part worden besteld dat niet binnen 5 dagen leverbaar is")
    result = app.place_order(basic_order_request, complete_parts, no_urgent_AMS_stock, complete_no_urgent_offers)

    assert result


  @pytest.mark.criterium_15
  @pytest.mark.method_place_order
  def test_case_32(self, basic_order_request, complete_parts, complete_AMS_stock, complete_no_urgent_offers):
    """
    Test calls the place_order function with an routine request, a complete dictionary of parts, stock that can meet the urgent-eta requirement and offers that cannot.
    Test passes if an order is placed.
    """
    print("Test criterium 15: Wanneer een item met routine-prioriteit wordt besteld, dan kan een part worden besteld dat niet binnen 5 dagen leverbaar is")
    result = app.place_order(basic_order_request, complete_parts, complete_AMS_stock, complete_no_urgent_offers)

    assert result


  @pytest.mark.criterium_15
  @pytest.mark.method_place_order
  def test_case_33(self, basic_order_request, complete_parts, no_urgent_AMS_stock, complete_offers):
    """
    Test calls the place_order function with an routine request, a complete dictionary of parts, offers that can meet the urgent-eta requirement and stock that cannot.
    Test passes if an order is placed.
    """
    print("Test criterium 15: Wanneer een item met routine-prioriteit wordt besteld, dan kan een part worden besteld dat niet binnen 5 dagen leverbaar is")
    result = app.place_order(basic_order_request, complete_parts, no_urgent_AMS_stock, complete_offers)

    assert result


  @pytest.mark.criterium_16
  @pytest.mark.method_place_order
  def test_case_35(self, negative_request, complete_parts, complete_AMS_stock, complete_offers):
    """
    Test calls the place_order function with a request with a negative quantity, a complete dictionary of parts, and a complete stock and offers.
    Test passes if any Exception is raised.
    """
    print("Test criterium 16: Wanneer een negatief aantal parts wordt besteld, runt het script niet")
    with pytest.raises(Exception):
      app.place_order(negative_request, complete_parts, complete_AMS_stock, complete_offers)


  @pytest.mark.criterium_17
  @pytest.mark.method_place_order
  def test_case_37(self, fractional_request, complete_parts, complete_AMS_stock, complete_offers):
    """
    Test calls the place_order function with a request with a fractional quantity, a complete dictionary of parts, and a complete stock and offers.
    Test passes if any Exception is raised.
    """
    print("Test criterium 17: Wanneer een niet-geheel aantal parts wordt besteld, runt het script niet")
    with pytest.raises(Exception):
      app.place_order(fractional_request, complete_parts, complete_AMS_stock, complete_offers)


  @pytest.mark.criterium_18
  @pytest.mark.criterium_20
  @pytest.mark.method_place_order
  def test_case_39(self, basic_order_request, complete_parts, complete_AMS_stock, complete_offers):
    """
    Test calls the place_order function with a request with a positive, whole quantity, a complete dictionary of parts, and a complete stock and offers.
    Test passes if an order is returned.
    """
    print("Test criterium 18: Wanneer een geheel, niet-negatief aantal parts wordt besteld, runt het script wel")
    result = app.place_order(basic_order_request, complete_parts, complete_AMS_stock, complete_offers)

    assert result


  @pytest.mark.criterium_19
  @pytest.mark.method_place_order
  def test_case_41(self, incompatible_request, complete_parts, complete_AMS_stock, complete_offers):
    """
    Test calls the place_order function with a request with an incompatible part, a complete dictionary of parts, and a complete stock and offers.
    Test passes if any Exception is raised.
    """
    print("Test criterium 19: Wanneer het gevraagde part van een order niet overeenkomt met het gevraagde vliegtuigtype, runt het script niet")
    with pytest.raises(Exception):
      app.place_order(incompatible_request, complete_parts, complete_AMS_stock, complete_offers)


  @pytest.mark.criterium_20
  @pytest.mark.method_place_order
  def test_case_43(self, basic_order_request, complete_parts, complete_AMS_stock, complete_offers):
    """
    Test calls the place_order function with a request with a compatible part, a complete dictionary of parts, and a complete stock and offers.
    Test passes if an order is returned.
    """
    print("Test criterium 20: Wanneer het gevraagde part van een order overeenkomt met het gevraagde vliegtuigtype, runt het script")
    result = app.place_order(basic_order_request, complete_parts, complete_AMS_stock, complete_offers)

    assert result


  @pytest.mark.criterium_21
  @pytest.mark.method_place_order
  def test_case_46(self, basic_order_request, complete_parts, only_USD_offers):
    """
    Test notes the cost of the item from the supplier and stores it as price_per_item
    Then it calculates the intended cost by multiplying by the exchange rate and the requested quantity
    Then it runs the place_order function.

    Test passes if the intended_cost is equal to the total_cost_eur in the result from place_order, both rounded to 3 decimals to avoid rounding errors
    """
    print("Test criterium 21: Wanneer een part in USD wordt besteld, wordt de prijs correct naar EUR converteerd")
    for item in only_USD_offers:
      if item.part_no == basic_order_request.part_no:
        price_per_item = item.unit_price
        break

    unit_cost_eur = price_per_item * app.FX_RATES_TO_EUR["USD"]
    intended_cost = unit_cost_eur * basic_order_request.quantity

    result = app.place_order(basic_order_request, complete_parts, [], only_USD_offers)

    assert round(result.total_cost_eur,3) == round(intended_cost, 3)


  @pytest.mark.criterium_22
  @pytest.mark.method_place_order
  def test_case_49(self, basic_order_request, complete_parts, only_EUR_offers):
    """
    Test notes the cost of the item from the supplier and stores it as price_per_item
    Then it calculates the intended cost by multiplying the price_per_item by the requested quantity
    Then it runs the place_order function.

    Test passes if the intended_cost is equal to the total_cost_eur in the result from place_order, both rounded to 3 decimals to avoid rounding errors
    """
    print("Test criterium 22: Wanneer een part in EUR wordt besteld, wordt de prijs niet geconverteerd")
    for item in only_EUR_offers:
      if item.part_no == basic_order_request.part_no:
        price_per_item = item.unit_price
        break

    intended_cost = price_per_item * basic_order_request.quantity

    result = app.place_order(basic_order_request, complete_parts, [], only_EUR_offers)

    assert round(result.total_cost_eur,3) == round(intended_cost, 3)

  
  @pytest.mark.criterium_23
  @pytest.mark.method_place_order
  def test_case_51(self, basic_order_request, complete_parts, complete_AMS_stock, complete_offers):
    """
    Test creates up to 20 orders. 
    After each order, the order_id is checked against a list of order_ids, and added to the list if it's not yet in there.
    If the order_id is already in the list, duplicate_id is set to True and the loop ends.

    The test passes if duplicate_id is not set to True. 
    """
    print("Test criterium 23: Als veel items in dezelfde seconde worden besteld, hebben ze ieder een uniek ordernummer")
    order_ids = []
    duplicate_id = False
    for _ in range(20):
      result = app.place_order(basic_order_request, complete_parts, complete_AMS_stock, complete_offers)
      if result.order_id not in order_ids:
        order_ids.append(result.order_id)
      else:
        duplicate_id = True
        break

    assert not duplicate_id


  @pytest.mark.criterium_24
  @pytest.mark.method_place_order
  def test_case_53(self, basic_order_request, complete_parts, complete_AMS_stock):
    """
    Test multiplies the requested quantity by the internal handling cost (15.0).
    Then it runs the place_order function with empty supplier list.

    Test passes if the intended_cost is equal to the total_cost_eur in the result from place_order, both rounded to 3 decimals.
    """
    print("Test criterium 24: De kosten van een part uit de warehouse wordt met 3 decimalen na de komma (of zoveel als relevant) weergegeven")
    intended_cost = basic_order_request.quantity * 15.0

    result = app.place_order(basic_order_request, complete_parts, complete_AMS_stock, [])

    assert round(result.total_cost_eur,3) == round(intended_cost, 3)


  @pytest.mark.criterium_25
  @pytest.mark.method_place_order
  def test_case_55(self, basic_order_request, complete_parts, complete_offers):
    """
    Test notes the cost of the item from each supplier and stores it as price_per_item
    Then it calculates the intended costs by multiplying the price_per_item by the requested quantity and rounding to 3 decimals
    Then it runs the place_order function.

    Test passes if the total_cost_eur in the result from place_order is any of the prices in intended_costs
    NOTE: This doesn't only test the rounding, it is also dependent on test cases 46 and 49
    """
    print("Test criterium 25: De kosten van een part van een supplier wordt met 3 decimalen na de komma weergegeven")
    price_per_item = []
    for item in complete_offers:
      if item.part_no == basic_order_request.part_no:
        price_per_item.append(item.unit_price)

    intended_cost = []
    for price in price_per_item:
      intended_cost.append(round(price * basic_order_request.quantity,3))

    result = app.place_order(basic_order_request, complete_parts, [], complete_offers)

    assert result.total_cost_eur in intended_cost


# A class to test the method validate_request
class TestClassUnitValidateRequest:
  @pytest.mark.criterium_6
  @pytest.mark.method_validate_request
  def test_case_12(self, complete_parts, basic_order_request):
    """
    Test changes the airplane_type of the basic order request to B737 to create an invalid order request as the part is for airplane_type A320
    It then checks all issues raised by validate_request and sets compatible to False if an issue contains "not compatible"
    Test passes if compatible has been set to False
    """
    print("Test criterium 6: Als bij een order voor een vliegtuig geen onderdeel voor dat vliegtuig beschikbaar is, krijgt de gebruiker hier melding van")
    basic_order_request.aircraft_type = "B737"
    response = app.validate_request(basic_order_request, complete_parts)

    compatible = True

    for issue in response:
      if "not compatible" in issue:
        compatible = False

    assert compatible == False


  @pytest.mark.criterium_16
  @pytest.mark.method_validate_request
  def test_case_34(self, complete_parts, basic_order_request):
    """
    Test changes the requested quantity of the basic order request to -1, a negative number.
    It then checks whether the validate_request function returns any issues.
    Test passes if any issue has been raised.

    NOTE: Test currently passes because an erronous issue is raised (see test_case_12), will no longer pass when this is fixed.
    """
    print("Test criterium 16: Wanneer een negatief aantal parts wordt besteld, runt het script niet")
    basic_order_request.quantity = -1
    response = app.validate_request(basic_order_request, complete_parts)

    assert response


  @pytest.mark.criterium_17
  @pytest.mark.method_validate_request
  def test_case_36(self, complete_parts, basic_order_request):
    """
    Test changes the requested quantity of the basic order request to 0.5, a fractional number.
    It then checks whether the validate_request function returns any issues.
    Test passes if any issue has been raised.

    NOTE: Test currently passes because an erronous issue is raised (see test_case_12), will no longer pass when this is fixed.
    """
    print("Test criterium 17: Wanneer een niet-geheel aantal parts wordt besteld, runt het script niet")
    basic_order_request.quantity = 0.5
    response = app.validate_request(basic_order_request, complete_parts)

    assert response


  @pytest.mark.criterium_18
  @pytest.mark.method_validate_request
  def test_case_38_and_42(self, complete_parts, basic_order_request):
    """
    Test checks whether the validate_request function returns any issues with the default parts and order request.
    Test passes if no issue has been raised.

    NOTE: Test currently fails because an erronous issue is raised (see test_case_12/test_case_40), will no longer fail when this is fixed.
    """
    print("Test criterium 18: Wanneer een geheel, niet-negatief aantal parts wordt besteld, runt het script wel\n" \
    "Test criterium 20: Wanneer het gevraagde part van een order overeenkomt met het gevraagde vliegtuigtype, runt het script")
    response = app.validate_request(basic_order_request, complete_parts)

    assert not response


  @pytest.mark.criterium_19
  @pytest.mark.method_validate_request
  def test_case_40(self, complete_parts, basic_order_request):
    """
    Test changes the airplane_type of the basic order request to B737 to create an invalid order request as the part is for airplane_type A320
    It then checks whether the validate_request function returns any issues.
    Test passes if any issue has been raised.
    """
    print("Test criterium 19: Wanneer het gevraagde part van een order niet overeenkomt met het gevraagde vliegtuigtype, runt het script niet")
    basic_order_request.aircraft_type = "B737"
    response = app.validate_request(basic_order_request, complete_parts)

    assert response


# A class to test the method to_eur
class TestClassUnitToEur:
  @pytest.mark.criterium_21
  @pytest.mark.method_to_eur
  def test_case_44(self):
    """
    Test calls the to_eur function with a random amount between 1 and 1000 and the currency USD.
    Test then compares the result to the intended result (amount * 0.92), each rounded to 3 decimals to avoid rounding errors
    Test passes if the result is equal to the amount * 0.92
    """
    print("Test criterium 21: Wanneer een part in USD wordt besteld, wordt de prijs correct naar EUR converteerd")
    amount = random.randint(1,100000)/100
    currency = "USD"
    converted_amount = app.to_eur(amount, currency)

    assert round(converted_amount, 3) == round(amount * 0.92, 3)


  @pytest.mark.criterium_22
  @pytest.mark.method_to_eur
  def test_case_47(self):
    """
    Test calls the to_eur function with a random amount between 1 and 1000 and the currency EUR.
    Test then compares the result to the intended result (amount), each rounded to 3 decimals to avoid rounding errors
    Test passes if the result is equal to the original amount. 
    """
    print("Test criterium 22: Wanneer een part in EUR wordt besteld, wordt de prijs niet geconverteerd")
    amount = random.randint(1,100000)/100
    currency = "EUR"
    converted_amount = app.to_eur(amount, currency)

    assert round(converted_amount, 3) == round(amount, 3)


# A class to test the method select_warehouse
class TestClassUnitSelectWarehouse:
  @pytest.mark.criterium_1
  @pytest.mark.method_select_warehouse
  def test_case_01(self, AOG_request, complete_AMS_stock):
    """
    Test calls the select_warehouse function with an AOG request and the regular AMS stock.
    Test passes if the function gives a result. 
    """
    print("Test criterium 1: Als bij een AOG-order de bestelling onder de ETA zit, wordt deze besteld")
    result = app.select_warehouse(AOG_request, complete_AMS_stock)

    assert result


  @pytest.mark.criterium_2
  @pytest.mark.method_select_warehouse
  def test_case_03(self, past_needed_by_request, complete_AMS_stock):
    """
    Test calls the select_warehouse function with an AOG request with past needed_by, and the regular AMS stock.
    Test passes if the function gives no result. 
    """
    print("Test criterium 2: Als bij een AOG-order de bestelling boven de ETA zit, wordt deze niet besteld")
    result = app.select_warehouse(past_needed_by_request, complete_AMS_stock)

    assert not result


  @pytest.mark.criterium_10
  @pytest.mark.method_select_warehouse
  def test_case_18(self, shelf_life_request, complete_expired_AMS_stock):
    """
    Test calls the select_warehouse function with an request with a shelf life, and expired AMS stock.
    Test passes if the function gives no result
    """
    print("Test criterium 10: Als een order een vervaldatum heeft, wordt er een onderdeel binnen de vervaldatum, of niks, besteld")
    result = app.select_warehouse(shelf_life_request, complete_expired_AMS_stock)

    assert not result


  @pytest.mark.criterium_10
  @pytest.mark.method_select_warehouse
  def test_case_19(self, shelf_life_request, complete_expired_AMS_stock):
    """
    Test calls the select_warehouse function with an request with a shelf life, and expired AMS stock, met 1 niet-expired part in de far stock.
    Test passes if the item from the far stock is chosen
    """
    print("Test criterium 10: Als een order een vervaldatum heeft, wordt er een onderdeel binnen de vervaldatum, of niks, besteld")
    far_item = app.StockItem(
      part_no = shelf_life_request.part_no,
      warehouse = "far", 
      on_hand = 10, 
      reserved = 0,
      safety_stock = 0,
      expires_on = datetime.now() + timedelta(days=100)
    )
    result = app.select_warehouse(shelf_life_request, complete_expired_AMS_stock)

    assert result == 'far'