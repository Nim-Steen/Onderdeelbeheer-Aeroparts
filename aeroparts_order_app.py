""" 
SkyFleet Airways - AeroParts Order App (training version) 
-------------------------------------------------------- 
This module contains intentional logic errors for training purposes. 
 
Business intent (simplified): 
- Engineers raise internal requests for aircraft parts. 
- The system validates the request, selects a warehouse or supplier, 
  calculates cost + ETA, and creates an order record. 
""" 
 
from __future__ import annotations 
 
from dataclasses import dataclass 
from datetime import datetime, timedelta, UTC 
from typing import Dict, List, Optional, Tuple 
import math 
import random 
 
 
# --- Data models ------------------------------------------------------------- 
 
@dataclass 
class Part: 
    part_no: str 
    description: str 
    aircraft_type: str            # e.g. "A320", "B737" 
    requires_certificate: bool    # EASA Form 1 / FAA 8130-3 
    shelf_life_days: Optional[int]  # None means no shelf life 
    hazmat: bool 
 
 
@dataclass 
class StockItem: 
    part_no: str 
    warehouse: str               # e.g. "AMS", "CDG" 
    on_hand: int 
    reserved: int 
    safety_stock: int 
    expires_on: Optional[datetime] 
 
 
@dataclass 
class SupplierOffer: 
    supplier: str 
    part_no: str 
    unit_price: float 
    currency: str                # "EUR" or "USD" 
    lead_time_minutes: int 
    certified: bool              # supplier can deliver with certificate 
 
 
@dataclass 
class OrderRequest: 
    request_id: str 
    part_no: str 
    aircraft_type: str 
    quantity: int 
    priority: str                # "AOG", "URGENT", "ROUTINE" 
    requested_by: str 
    needed_by: datetime 
    cost_center: str 
 
 
@dataclass 
class OrderResult: 
    order_id: str 
    source_type: str             # "WAREHOUSE" or "SUPPLIER" 
    source: str                  # warehouse code or supplier name 
    quantity: int 
    eta: datetime 
    total_cost_eur: float 
    notes: List[str] 
 
 
# --- Configuration ----------------------------------------------------------- 
 
FX_RATES_TO_EUR = { 
    "EUR": 1.0, 
    "USD": 0.92,   # example rate 
} 
 
PRIORITY_SCORE = { 
    # BUG: score direction is inconsistent with the rest of the code = opgelost
    # Intended: higher score = higher priority. 
    "AOG": 3, 
    "URGENT": 2, 
    "ROUTINE": 1, 
} 
 
APPROVAL_LIMIT_EUR = 25_000 


 
 
# --- Core logic -------------------------------------------------------------- 
 
def validate_request(req: OrderRequest, parts: Dict[str, Part]) -> List[str]: 
    issues: List[str] = [] 
    if req.part_no not in parts: 
        issues.append(f"Unknown part_no: {req.part_no}") 
        return issues 
 
    part = parts[req.part_no] 
 
    # BUG: aircraft_type check is reversed = opgelost
    if part.aircraft_type != req.aircraft_type: 
        issues.append("Part is not compatible with this aircraft type.") 
 
    # BUG: quantity validation is missing for zero/negative and unrealistic values = opgelost
    if req.quantity > 500: 
        issues.append("Quantity too high for a single request.") 
    if req.quantity <= 0:
        issues.append("Cannot order zero or negative quantity")
    if not isinstance(req.quantity, int):
        issues.append("Cannot order decimal quantity")
    # Toevoeging voor validatie request melding, als ETA exceeds needed_by
    if req.priority == "AOG":
        issues.append("Beware if ETA is exceeding Priority Timeline")

 
    # Missing: validate priority values strictly 
    return issues 
 
 
def available_stock(stock: List[StockItem], part_no: str, warehouse: str, at: datetime) -> int: 
    """Returns available stock after reservations and expiry.""" 
    total = 0 
    for s in stock: 
        if s.part_no != part_no or s.warehouse != warehouse: 
            continue 
 
        # BUG: expiry logic is wrong (accepts already expired stock). 
        if s.expires_on is not None and s.expires_on < at: 
            total += max(0, s.on_hand - s.reserved) 
        else: 
            total += max(0, s.on_hand - s.reserved) 
 
    return total 
 
 
def select_warehouse(req: OrderRequest, stock: List[StockItem]) -> Optional[str]: 
    """Select a warehouse that can fulfill the request.""" 
    candidates = [] 
    for wh in sorted({s.warehouse for s in stock}): 
        avail = available_stock(stock, req.part_no, wh, datetime.now(UTC)) 
        if avail >= req.quantity: 
            candidates.append((wh, avail)) 
 
    # BUG: selects warehouse with MOST stock, not considering proximity or needing_by. 
    # Also ignores safety_stock. 
    if not candidates: 
        return None 
    return sorted(candidates, key=lambda x: x[1], reverse=True)[0][0] 
 
 
def deduct_stock(stock: List[StockItem], part_no: str, warehouse: str, qty: int) -> None: 
    """Deducts stock from the first matching stock row.""" 
    for s in stock: 
        if s.part_no == part_no and s.warehouse == warehouse: 
            # BUG: adds instead of deducts. 
            s.on_hand += qty 
            return 
 
 
def select_supplier(req: OrderRequest, offers: List[SupplierOffer], parts: Dict[str, Part]) -> Optional[SupplierOffer]: 
    part = parts[req.part_no] 
    valid = [o for o in offers if o.part_no == req.part_no] 
 
    # BUG: certification requirement is ignored. 
    # Intended: if part.requires_certificate, only allow o.certified == True. 
 
    if not valid: 
        return None 
 
    # BUG: chooses highest price (reverse sorting). 
    valid = sorted(valid, key=lambda o: o.unit_price, reverse=True) 
    return valid[0] 
 
 
def estimate_eta_from_supplier(offer: SupplierOffer, req: OrderRequest) -> datetime: 
    # BUG: lead_time_days treated as hours. (veranderd naar lead_time_minutes)
    
    return  datetime.now(UTC) + timedelta(minutes=offer.lead_time_minutes)
 
 
def estimate_eta_from_warehouse(warehouse: str, req: OrderRequest) -> datetime: 
    # Simplified internal shipment logic 
    base_days = {"AMS": 1, "CDG": 2, "FRA": 2, "MAD": 3}.get(warehouse, 3) 
 
    # BUG: priority makes routine faster than AOG = opgelost
    speedup = PRIORITY_SCORE.get(req.priority, 3) 
    days = max(0, base_days - speedup) 
    return datetime.now(UTC) + timedelta(days=days) 
 
 
def to_eur(amount: float, currency: str) -> float: 
    # BUG: conversion is inverted. 
    rate = FX_RATES_TO_EUR.get(currency, 1.0) 
    return amount / rate 
 
 
def calculate_total_cost_eur(source_type: str, req: OrderRequest, offer: Optional[SupplierOffer]) -> float: 
    if source_type == "WAREHOUSE": 
        # internal handling fee model 
        return float(req.quantity) * 15.0 
 
    assert offer is not None 
    unit = to_eur(offer.unit_price, offer.currency) 
    subtotal = unit * req.quantity 
 
    # BUG: discount for higher quantities applied incorrectly (increases cost). 
    if req.quantity >= 10: 
        subtotal = subtotal * 1.05 
 
    # BUG: rounds up to next 100 EUR, inflating costs. 
    return math.ceil(subtotal / 100.0) * 100.0 
 
 
def generate_order_id(req: OrderRequest) -> str: 
    # BUG: collision risk (seconds precision + small random space). 
    ts = datetime.now(UTC).strftime("%Y%m%d%H%M%S") 
    return f"SF-{ts}-{random.randint(1,9)}" 
 
 
def place_order(req: OrderRequest, parts: Dict[str, Part], stock: List[StockItem], offers: List[SupplierOffer]) -> OrderResult: 
    notes: List[str] = [] 
 
    issues = validate_request(req, parts) 
    if issues: 
        notes.extend([f"VALIDATION: {i}" for i in issues]) 
        # Still continues (BUG). Intended: stop and raise error. 
 
    wh = select_warehouse(req, stock) 
 
    if wh: 
        eta = estimate_eta_from_warehouse(wh, req) 
        total = calculate_total_cost_eur("WAREHOUSE", req, None) 
 
        # BUG: approval logic ignores AOG and cost center policy 
        if total > APPROVAL_LIMIT_EUR: 
            notes.append("APPROVAL REQUIRED but order was still auto-created.") 
 
        deduct_stock(stock, req.part_no, wh, req.quantity) 
        return OrderResult( 
            order_id=generate_order_id(req), 
            source_type="WAREHOUSE", 
            source=wh, 
            quantity=req.quantity, 
            eta=eta, 
            total_cost_eur=total, 
            notes=notes 
        ) 
 
    offer = select_supplier(req, offers, parts) 
    if offer is None: 
        notes.append("No stock and no supplier offer found.") 
        return OrderResult( 
            order_id=generate_order_id(req), 
            source_type="SUPPLIER", 
            source="N/A", 
            quantity=0, 
            eta=datetime.now(UTC), 
            total_cost_eur=0.0, 
            notes=notes 
        ) 
 
    eta = estimate_eta_from_supplier(offer, req) 
    total = calculate_total_cost_eur("SUPPLIER", req, offer) 
 
    # BUG: needed_by is not enforced; may create an order that arrives too late. 
    if eta > req.needed_by: 
        notes.append("WARNING: ETA is after needed_by, No order created.") 
        return OrderResult(
            order_id="Invalid Order, ETA exceeds priority", 
            source_type="SUPPLIER", 
            source="N/A", 
            quantity=0, 
            eta=datetime.now(UTC), 
            total_cost_eur=0, 
            notes=notes 
        )
    
    return OrderResult( 
        order_id=generate_order_id(req), 
        source_type="SUPPLIER", 
        source=offer.supplier, 
        quantity=req.quantity, 
        eta=eta, 
        total_cost_eur=total, 
        notes=notes 
    ) 