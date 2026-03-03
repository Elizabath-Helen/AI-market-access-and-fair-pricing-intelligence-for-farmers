"""
Tests for market_data app.
"""

from django.test import TestCase
from django.db import IntegrityError
from .models import Market, MarketPrice, TransportCost
from decimal import Decimal
from datetime import date


class MarketModelTests(TestCase):
    """Tests for the Market model."""

    def test_create_market(self):
        """Test creating a market with all required fields."""
        market = Market.objects.create(
            name="Test Mandi",
            location="28.6139,77.2090",
            mandi_code="DL001",
            region="Delhi",
            active=True
        )
        self.assertEqual(market.name, "Test Mandi")
        self.assertEqual(market.mandi_code, "DL001")
        self.assertEqual(market.region, "Delhi")
        self.assertTrue(market.active)

    def test_market_str_representation(self):
        """Test the string representation of a market."""
        market = Market.objects.create(
            name="Test Mandi",
            location="28.6139,77.2090",
            mandi_code="DL001",
            region="Delhi"
        )
        self.assertEqual(str(market), "Test Mandi (Delhi)")

    def test_mandi_code_unique_constraint(self):
        """Test that mandi_code must be unique."""
        Market.objects.create(
            name="Market 1",
            location="28.6139,77.2090",
            mandi_code="DL001",
            region="Delhi"
        )
        with self.assertRaises(IntegrityError):
            Market.objects.create(
                name="Market 2",
                location="28.7041,77.1025",
                mandi_code="DL001",  # Duplicate mandi_code
                region="Delhi"
            )

    def test_market_default_active_status(self):
        """Test that active defaults to True."""
        market = Market.objects.create(
            name="Test Mandi",
            location="28.6139,77.2090",
            mandi_code="DL001",
            region="Delhi"
        )
        self.assertTrue(market.active)


class MarketPriceModelTests(TestCase):
    """Tests for the MarketPrice model."""

    def setUp(self):
        """Set up test data."""
        self.market = Market.objects.create(
            name="Test Mandi",
            location="28.6139,77.2090",
            mandi_code="DL001",
            region="Delhi"
        )

    def test_create_market_price(self):
        """Test creating a market price with all required fields."""
        price = MarketPrice.objects.create(
            market=self.market,
            crop_type="Wheat",
            date=date(2024, 1, 15),
            min_price=Decimal("20.00"),
            max_price=Decimal("30.00"),
            modal_price=Decimal("25.00"),
            arrivals=1000,
            source="Agmarknet"
        )
        self.assertEqual(price.crop_type, "Wheat")
        self.assertEqual(price.min_price, Decimal("20.00"))
        self.assertEqual(price.max_price, Decimal("30.00"))
        self.assertEqual(price.modal_price, Decimal("25.00"))
        self.assertEqual(price.arrivals, 1000)

    def test_price_range_constraint_valid(self):
        """Test that valid price ranges are accepted (min <= modal <= max)."""
        price = MarketPrice.objects.create(
            market=self.market,
            crop_type="Wheat",
            date=date(2024, 1, 15),
            min_price=Decimal("20.00"),
            max_price=Decimal("30.00"),
            modal_price=Decimal("25.00"),
            arrivals=1000,
            source="Agmarknet"
        )
        self.assertIsNotNone(price.id)

    def test_price_range_constraint_equal_prices(self):
        """Test that equal prices are accepted (min = modal = max)."""
        price = MarketPrice.objects.create(
            market=self.market,
            crop_type="Wheat",
            date=date(2024, 1, 15),
            min_price=Decimal("25.00"),
            max_price=Decimal("25.00"),
            modal_price=Decimal("25.00"),
            arrivals=1000,
            source="Agmarknet"
        )
        self.assertIsNotNone(price.id)

    def test_price_range_constraint_modal_greater_than_max(self):
        """Test that modal_price > max_price violates constraint."""
        with self.assertRaises(IntegrityError):
            MarketPrice.objects.create(
                market=self.market,
                crop_type="Wheat",
                date=date(2024, 1, 15),
                min_price=Decimal("20.00"),
                max_price=Decimal("25.00"),
                modal_price=Decimal("30.00"),  # modal > max
                arrivals=1000,
                source="Agmarknet"
            )

    def test_price_range_constraint_min_greater_than_modal(self):
        """Test that min_price > modal_price violates constraint."""
        with self.assertRaises(IntegrityError):
            MarketPrice.objects.create(
                market=self.market,
                crop_type="Wheat",
                date=date(2024, 1, 15),
                min_price=Decimal("30.00"),  # min > modal
                max_price=Decimal("35.00"),
                modal_price=Decimal("25.00"),
                arrivals=1000,
                source="Agmarknet"
            )

    def test_market_price_str_representation(self):
        """Test the string representation of a market price."""
        price = MarketPrice.objects.create(
            market=self.market,
            crop_type="Wheat",
            date=date(2024, 1, 15),
            min_price=Decimal("20.00"),
            max_price=Decimal("30.00"),
            modal_price=Decimal("25.00"),
            arrivals=1000,
            source="Agmarknet"
        )
        self.assertEqual(str(price), "Wheat at Test Mandi on 2024-01-15")

    def test_market_price_ordering(self):
        """Test that market prices are ordered by date descending."""
        price1 = MarketPrice.objects.create(
            market=self.market,
            crop_type="Wheat",
            date=date(2024, 1, 15),
            min_price=Decimal("20.00"),
            max_price=Decimal("30.00"),
            modal_price=Decimal("25.00"),
            arrivals=1000,
            source="Agmarknet"
        )
        price2 = MarketPrice.objects.create(
            market=self.market,
            crop_type="Wheat",
            date=date(2024, 1, 20),
            min_price=Decimal("22.00"),
            max_price=Decimal("32.00"),
            modal_price=Decimal("27.00"),
            arrivals=1200,
            source="Agmarknet"
        )
        prices = list(MarketPrice.objects.all())
        self.assertEqual(prices[0].id, price2.id)  # Most recent first
        self.assertEqual(prices[1].id, price1.id)


class TransportCostModelTests(TestCase):
    """Tests for the TransportCost model."""

    def setUp(self):
        """Set up test data."""
        self.market = Market.objects.create(
            name="Test Mandi",
            location="28.6139,77.2090",
            mandi_code="DL001",
            region="Delhi"
        )

    def test_create_transport_cost(self):
        """Test creating a transport cost with all required fields."""
        transport = TransportCost.objects.create(
            from_location="Farmer Village",
            to_market=self.market,
            distance_km=Decimal("50.00"),
            cost_per_kg=Decimal("2.50")
        )
        self.assertEqual(transport.from_location, "Farmer Village")
        self.assertEqual(transport.to_market, self.market)
        self.assertEqual(transport.distance_km, Decimal("50.00"))
        self.assertEqual(transport.cost_per_kg, Decimal("2.50"))
        self.assertIsNotNone(transport.last_updated)

    def test_transport_cost_str_representation(self):
        """Test the string representation of a transport cost."""
        transport = TransportCost.objects.create(
            from_location="Farmer Village",
            to_market=self.market,
            distance_km=Decimal("50.00"),
            cost_per_kg=Decimal("2.50")
        )
        self.assertEqual(str(transport), "Farmer Village to Test Mandi: ₹2.50/kg")

    def test_distance_non_negative_constraint_valid(self):
        """Test that non-negative distance is accepted."""
        transport = TransportCost.objects.create(
            from_location="Farmer Village",
            to_market=self.market,
            distance_km=Decimal("0.00"),  # Zero is valid
            cost_per_kg=Decimal("2.50")
        )
        self.assertIsNotNone(transport.id)

    def test_distance_non_negative_constraint_violation(self):
        """Test that negative distance violates constraint."""
        with self.assertRaises(IntegrityError):
            TransportCost.objects.create(
                from_location="Farmer Village",
                to_market=self.market,
                distance_km=Decimal("-10.00"),  # Negative distance
                cost_per_kg=Decimal("2.50")
            )

    def test_cost_non_negative_constraint_valid(self):
        """Test that non-negative cost is accepted."""
        transport = TransportCost.objects.create(
            from_location="Farmer Village",
            to_market=self.market,
            distance_km=Decimal("50.00"),
            cost_per_kg=Decimal("0.00")  # Zero is valid
        )
        self.assertIsNotNone(transport.id)

    def test_cost_non_negative_constraint_violation(self):
        """Test that negative cost violates constraint."""
        with self.assertRaises(IntegrityError):
            TransportCost.objects.create(
                from_location="Farmer Village",
                to_market=self.market,
                distance_km=Decimal("50.00"),
                cost_per_kg=Decimal("-2.50")  # Negative cost
            )

    def test_unique_together_constraint(self):
        """Test that from_location and to_market combination must be unique."""
        TransportCost.objects.create(
            from_location="Farmer Village",
            to_market=self.market,
            distance_km=Decimal("50.00"),
            cost_per_kg=Decimal("2.50")
        )
        with self.assertRaises(IntegrityError):
            TransportCost.objects.create(
                from_location="Farmer Village",
                to_market=self.market,  # Duplicate combination
                distance_km=Decimal("60.00"),
                cost_per_kg=Decimal("3.00")
            )
