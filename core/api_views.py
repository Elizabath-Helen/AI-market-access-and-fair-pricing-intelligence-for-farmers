"""
API views for the core app.
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import json
from decimal import Decimal

from .negotiation_coach import NegotiationCoachService


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def negotiation_advice_api(request):
    """
    API endpoint for negotiation advice.
    
    POST /api/negotiation-advice
    
    Request body:
    {
        "crop_type": "Wheat",
        "farmer_location": "Amritsar, Punjab",
        "quantity": 50.0,
        "offered_price": 2100.0,
        "nearby_market_prices": [2300, 2350, 2280]
    }
    
    Response:
    {
        "status": "success",
        "data": {
            "offer_analysis": {...},
            "fair_price_range": {...},
            "negotiation_advice": {...},
            "market_context": {...}
        }
    }
    """
    
    try:
        # Parse request data
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['crop_type', 'farmer_location', 'quantity', 'offered_price']
        for field in required_fields:
            if field not in data:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Missing required field: {field}'
                }, status=400)
        
        # Extract data
        crop_type = data['crop_type']
        farmer_location = data['farmer_location']
        quantity = float(data['quantity'])
        offered_price = float(data['offered_price'])
        nearby_market_prices = data.get('nearby_market_prices', [])
        
        # Validate data types and ranges
        if quantity <= 0:
            return JsonResponse({
                'status': 'error',
                'message': 'Quantity must be greater than 0'
            }, status=400)
        
        if offered_price <= 0:
            return JsonResponse({
                'status': 'error',
                'message': 'Offered price must be greater than 0'
            }, status=400)
        
        # Validate nearby market prices if provided
        if nearby_market_prices:
            try:
                nearby_market_prices = [float(price) for price in nearby_market_prices]
                if any(price <= 0 for price in nearby_market_prices):
                    return JsonResponse({
                        'status': 'error',
                        'message': 'All nearby market prices must be greater than 0'
                    }, status=400)
            except (ValueError, TypeError):
                return JsonResponse({
                    'status': 'error',
                    'message': 'Nearby market prices must be a list of numbers'
                }, status=400)
        
        # Use negotiation coach service
        coach = NegotiationCoachService()
        result = coach.analyze_offer(
            crop_type=crop_type,
            farmer_location=farmer_location,
            quantity=quantity,
            offered_price=offered_price,
            nearby_market_prices=nearby_market_prices
        )
        
        # Return successful response
        return JsonResponse({
            'status': 'success',
            'data': result
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON in request body'
        }, status=400)
    
    except ValueError as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Invalid data: {str(e)}'
        }, status=400)
    
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
def api_documentation(request):
    """
    API documentation endpoint.
    """
    
    documentation = {
        "title": "Farmer Market Advisor API",
        "version": "1.0.0",
        "description": "API for AI-powered negotiation advice for farmers",
        "endpoints": {
            "/api/negotiation-advice": {
                "method": "POST",
                "description": "Get negotiation advice for a price offer",
                "authentication": "Required (login)",
                "request_body": {
                    "crop_type": "string (required) - Type of crop (e.g., 'Wheat', 'Rice')",
                    "farmer_location": "string (required) - Farmer's location (e.g., 'Amritsar, Punjab')",
                    "quantity": "number (required) - Quantity in quintals",
                    "offered_price": "number (required) - Price offered by buyer per quintal",
                    "nearby_market_prices": "array (optional) - List of nearby mandi prices"
                },
                "response": {
                    "status": "string - 'success' or 'error'",
                    "data": {
                        "offer_analysis": {
                            "status": "string - 'FAIR', 'UNDERPRICED', 'SLIGHTLY_UNDERPRICED', or 'OVERPRICED'",
                            "offered_price": "number - The offered price",
                            "price_difference_percentage": "number - Percentage difference from market rate",
                            "potential_profit_loss": "number - Potential loss if offer is accepted"
                        },
                        "fair_price_range": {
                            "min_price": "number - Minimum fair price",
                            "max_price": "number - Maximum fair price",
                            "modal_price": "number - Market rate"
                        },
                        "negotiation_advice": {
                            "suggested_price": "number - Recommended negotiation price",
                            "recommendation": "string - Overall recommendation",
                            "explanation": "string - AI-generated explanation",
                            "negotiation_tactics": "array - List of negotiation tactics",
                            "confidence_level": "string - Confidence in the analysis"
                        },
                        "market_context": {
                            "seasonal_trend": "string - Current seasonal trend",
                            "demand_level": "string - Current demand level",
                            "supply_situation": "string - Current supply situation"
                        }
                    }
                },
                "example_request": {
                    "crop_type": "Wheat",
                    "farmer_location": "Amritsar, Punjab",
                    "quantity": 50.0,
                    "offered_price": 2100.0,
                    "nearby_market_prices": [2300, 2350, 2280]
                }
            }
        },
        "error_responses": {
            "400": "Bad Request - Invalid input data",
            "401": "Unauthorized - Authentication required",
            "500": "Internal Server Error"
        }
    }
    
    return JsonResponse(documentation, json_dumps_params={'indent': 2})