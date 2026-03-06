"""
AI Negotiation Coach - Help farmers evaluate price offers and negotiate better deals.
"""

from decimal import Decimal
from typing import Dict, List, Tuple
import random


class NegotiationCoachService:
    """Service for analyzing price offers and providing negotiation guidance."""
    
    # Base market prices per quintal (100kg) for different crops
    BASE_MARKET_PRICES = {
        'Wheat': {'min': 2200, 'max': 2400, 'modal': 2300},
        'Rice': {'min': 2800, 'max': 3200, 'modal': 3000},
        'Cotton': {'min': 5800, 'max': 6200, 'modal': 6000},
        'Sugarcane': {'min': 350, 'max': 400, 'modal': 375},
        'Maize': {'min': 1800, 'max': 2000, 'modal': 1900},
        'Soybean': {'min': 4200, 'max': 4600, 'modal': 4400},
        'Groundnut': {'min': 5200, 'max': 5800, 'modal': 5500},
        'Potato': {'min': 1200, 'max': 1600, 'modal': 1400},
        'Tomato': {'min': 1500, 'max': 2500, 'modal': 2000},
        'Onion': {'min': 1000, 'max': 1800, 'modal': 1400},
    }
    
    def analyze_offer(self, crop_type: str, farmer_location: str, quantity: float, 
                     offered_price: float, nearby_market_prices: List[float] = None) -> Dict:
        """
        Analyze a price offer and provide negotiation guidance.
        
        Args:
            crop_type: Type of crop
            farmer_location: Farmer's location
            quantity: Quantity in quintals
            offered_price: Price offered by buyer (per quintal)
            nearby_market_prices: List of nearby mandi prices
        
        Returns:
            Dictionary with analysis results and negotiation advice
        """
        
        # Get fair price range
        fair_price_data = self._get_fair_price_range(crop_type, farmer_location)
        
        # Calculate nearby market average if provided
        nearby_avg = sum(nearby_market_prices) / len(nearby_market_prices) if nearby_market_prices else None
        
        # Analyze the offer
        analysis = self._analyze_price_offer(
            offered_price, 
            fair_price_data, 
            nearby_avg,
            quantity
        )
        
        # Generate negotiation strategy
        negotiation_advice = self._generate_negotiation_strategy(
            crop_type,
            offered_price,
            fair_price_data,
            analysis,
            farmer_location,
            quantity
        )
        
        return {
            'offer_analysis': analysis,
            'fair_price_range': fair_price_data,
            'negotiation_advice': negotiation_advice,
            'market_context': self._get_market_context(crop_type, farmer_location),
            'nearby_market_avg': nearby_avg
        }
    
    def _get_fair_price_range(self, crop_type: str, location: str) -> Dict:
        """Get fair price range for the crop based on market data."""
        base_prices = self.BASE_MARKET_PRICES.get(crop_type, {
            'min': 2000, 'max': 2500, 'modal': 2250
        })
        
        # Apply location-based adjustments (mock regional variations)
        location_multiplier = self._get_location_multiplier(location)
        
        return {
            'min_price': round(base_prices['min'] * location_multiplier, 2),
            'max_price': round(base_prices['max'] * location_multiplier, 2),
            'modal_price': round(base_prices['modal'] * location_multiplier, 2),
            'currency': 'INR',
            'unit': 'per quintal'
        }
    
    def _get_location_multiplier(self, location: str) -> float:
        """Get price multiplier based on location (mock regional variations)."""
        # Mock regional price variations
        location_lower = location.lower()
        
        if any(city in location_lower for city in ['mumbai', 'delhi', 'bangalore', 'chennai']):
            return 1.1  # Metro cities - 10% higher
        elif any(state in location_lower for state in ['punjab', 'haryana', 'uttar pradesh']):
            return 1.05  # Agricultural states - 5% higher
        elif any(region in location_lower for region in ['maharashtra', 'gujarat', 'rajasthan']):
            return 1.0  # Average prices
        else:
            return 0.95  # Other regions - 5% lower
    
    def _analyze_price_offer(self, offered_price: float, fair_price_data: Dict, 
                           nearby_avg: float, quantity: float) -> Dict:
        """Analyze the price offer against fair market prices."""
        modal_price = fair_price_data['modal_price']
        min_price = fair_price_data['min_price']
        max_price = fair_price_data['max_price']
        
        # Calculate price difference percentage
        price_diff_pct = ((offered_price - modal_price) / modal_price) * 100
        
        # Determine offer status
        if offered_price >= min_price and offered_price <= max_price:
            if offered_price >= modal_price * 0.95:
                status = "FAIR"
            else:
                status = "SLIGHTLY_UNDERPRICED"
        elif offered_price < min_price:
            status = "UNDERPRICED"
        else:
            status = "OVERPRICED"
        
        # Calculate potential profit loss
        profit_loss = (modal_price - offered_price) * quantity if offered_price < modal_price else 0
        
        return {
            'status': status,
            'offered_price': offered_price,
            'price_difference_percentage': round(price_diff_pct, 1),
            'potential_profit_loss': round(profit_loss, 2),
            'comparison_with_modal': round(offered_price - modal_price, 2),
            'comparison_with_nearby': round(offered_price - nearby_avg, 2) if nearby_avg else None
        }
    
    def _generate_negotiation_strategy(self, crop_type: str, offered_price: float, 
                                     fair_price_data: Dict, analysis: Dict, 
                                     location: str, quantity: float) -> Dict:
        """Generate AI-powered negotiation strategy and advice."""
        
        modal_price = fair_price_data['modal_price']
        status = analysis['status']
        
        # Calculate suggested negotiation price
        if status == "UNDERPRICED":
            suggested_price = min(modal_price * 1.02, fair_price_data['max_price'])
        elif status == "SLIGHTLY_UNDERPRICED":
            suggested_price = modal_price
        elif status == "FAIR":
            suggested_price = offered_price  # Accept the offer
        else:  # OVERPRICED
            suggested_price = offered_price  # Accept the generous offer
        
        # Generate AI explanation
        explanation = self._generate_ai_explanation(
            crop_type, offered_price, fair_price_data, analysis, location, quantity
        )
        
        # Generate negotiation tactics
        tactics = self._generate_negotiation_tactics(status, analysis, quantity)
        
        return {
            'suggested_price': round(suggested_price, 2),
            'negotiation_range': {
                'min_acceptable': round(fair_price_data['min_price'], 2),
                'target_price': round(suggested_price, 2),
                'max_realistic': round(fair_price_data['max_price'], 2)
            },
            'recommendation': self._get_recommendation_text(status),
            'explanation': explanation,
            'negotiation_tactics': tactics,
            'confidence_level': self._calculate_confidence_level(analysis, quantity)
        }
    
    def _generate_ai_explanation(self, crop_type: str, offered_price: float, 
                               fair_price_data: Dict, analysis: Dict, 
                               location: str, quantity: float) -> str:
        """Generate AI-powered explanation in farmer-friendly language."""
        
        status = analysis['status']
        modal_price = fair_price_data['modal_price']
        price_diff = analysis['price_difference_percentage']
        
        # Base explanation based on offer status
        if status == "UNDERPRICED":
            base_msg = f"The offered price of ₹{offered_price} per quintal is {abs(price_diff):.1f}% lower than the current market rate of ₹{modal_price}."
        elif status == "SLIGHTLY_UNDERPRICED":
            base_msg = f"The offered price of ₹{offered_price} per quintal is slightly below the market rate of ₹{modal_price}."
        elif status == "FAIR":
            base_msg = f"The offered price of ₹{offered_price} per quintal is fair and within the current market range."
        else:  # OVERPRICED
            base_msg = f"The offered price of ₹{offered_price} per quintal is {price_diff:.1f}% higher than the market rate - this is a good offer!"
        
        # Add market context
        market_context = self._get_market_reasoning(crop_type, location, quantity)
        
        # Add profit impact
        if analysis['potential_profit_loss'] > 0:
            profit_impact = f" Accepting this offer may reduce your total income by ₹{analysis['potential_profit_loss']:.0f}."
        else:
            profit_impact = ""
        
        return f"{base_msg} {market_context}{profit_impact}"
    
    def _get_market_reasoning(self, crop_type: str, location: str, quantity: float) -> str:
        """Generate market-based reasoning for the price analysis."""
        
        # Mock market conditions (in real implementation, this would use actual market data)
        market_conditions = [
            f"Current {crop_type.lower()} demand in {location} region is stable.",
            f"Recent mandi prices for {crop_type.lower()} have been consistent.",
            f"Quality {crop_type.lower()} is in good demand this season.",
            f"Transport costs to major markets from {location} are moderate."
        ]
        
        # Add quantity-based reasoning
        if quantity >= 100:
            market_conditions.append("Your large quantity gives you better negotiating power.")
        elif quantity >= 50:
            market_conditions.append("Your moderate quantity should attract serious buyers.")
        else:
            market_conditions.append("Consider combining with other farmers for better rates.")
        
        return random.choice(market_conditions)
    
    def _generate_negotiation_tactics(self, status: str, analysis: Dict, quantity: float) -> List[str]:
        """Generate specific negotiation tactics based on the situation."""
        
        tactics = []
        
        if status in ["UNDERPRICED", "SLIGHTLY_UNDERPRICED"]:
            tactics.extend([
                "Mention current mandi prices in nearby markets",
                "Highlight the quality of your produce",
                "Ask for a price closer to the market rate",
                "Be prepared to walk away if the price is too low"
            ])
            
            if quantity >= 50:
                tactics.append("Use your bulk quantity as leverage for better rates")
        
        elif status == "FAIR":
            tactics.extend([
                "The price is reasonable - you can accept",
                "Ask about payment terms and timing",
                "Confirm quality standards and grading"
            ])
        
        else:  # OVERPRICED
            tactics.extend([
                "This is an excellent offer - accept quickly",
                "Confirm all terms and conditions",
                "Ensure prompt payment arrangements"
            ])
        
        # Add general tactics
        tactics.extend([
            "Always negotiate politely and professionally",
            "Get all agreements in writing",
            "Check the buyer's reputation and payment history"
        ])
        
        return tactics[:5]  # Return top 5 tactics
    
    def _get_recommendation_text(self, status: str) -> str:
        """Get recommendation text based on offer status."""
        
        recommendations = {
            "UNDERPRICED": "NEGOTIATE HIGHER - The offer is below market rate",
            "SLIGHTLY_UNDERPRICED": "TRY TO NEGOTIATE - You can get a better price",
            "FAIR": "ACCEPTABLE OFFER - The price is reasonable",
            "OVERPRICED": "EXCELLENT OFFER - Accept this generous price"
        }
        
        return recommendations.get(status, "EVALUATE CAREFULLY")
    
    def _calculate_confidence_level(self, analysis: Dict, quantity: float) -> str:
        """Calculate confidence level for the analysis."""
        
        price_diff = abs(analysis['price_difference_percentage'])
        
        if price_diff <= 5:
            confidence = "HIGH"
        elif price_diff <= 15:
            confidence = "MEDIUM"
        else:
            confidence = "HIGH"  # Very clear under/overpricing
        
        return confidence
    
    def _get_market_context(self, crop_type: str, location: str) -> Dict:
        """Get additional market context information."""
        
        return {
            'seasonal_trend': 'Stable',
            'demand_level': 'Moderate to High',
            'supply_situation': 'Normal',
            'price_trend': 'Steady',
            'best_selling_period': self._get_best_selling_period(crop_type)
        }
    
    def _get_best_selling_period(self, crop_type: str) -> str:
        """Get the best selling period for the crop."""
        
        selling_periods = {
            'Wheat': 'April-May (Post Harvest)',
            'Rice': 'November-December (Post Harvest)',
            'Cotton': 'December-February',
            'Sugarcane': 'December-March',
            'Maize': 'February-March',
            'Soybean': 'October-November',
            'Groundnut': 'November-December',
            'Potato': 'February-April',
            'Tomato': 'Year-round with peak in winter',
            'Onion': 'March-May'
        }
        
        return selling_periods.get(crop_type, 'Consult local market calendar')