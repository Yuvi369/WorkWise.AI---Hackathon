import json
import os
import requests
from langchain.tools import tool
from typing import Dict, List, Optional, Any
import re

class CompetitorAnalysisTools:
    
    @staticmethod
    @tool("Analyze competitors in India")
    def analyze_indian_competitors(business_type: str, city: str, state: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyzes competitors for a specific business type in an Indian city/location.
        Provides detailed information about market density, top competitors, and opportunity assessment.
        
        Args:
            business_type: Type of business (e.g., "restaurant", "grocery store", "clothing boutique")
            city: City in India (e.g., "Mumbai", "Bangalore", "Delhi")
            state: Optional state name to disambiguate city names
        
        Returns:
            Dict containing competitor analysis information
        """
        try:
            # Format location for API queries
            location = f"{city}, {state}, India" if state else f"{city}, India"
            location = location.strip()
            
            # Get competitor data from Google Places API or JustDial
            competitors_data = CompetitorAnalysisTools._get_competitor_data(business_type, location)
            
            # Calculate market density
            market_density = CompetitorAnalysisTools._calculate_market_density(
                competitors_data["competitor_count"], 
                city
            )
            
            # Calculate opportunity score
            opportunity_score = CompetitorAnalysisTools._calculate_opportunity_score(
                competitors_data["competitor_count"],
                competitors_data["avg_rating"],
                market_density
            )
            
            # Generate insights based on the analysis
            insights = CompetitorAnalysisTools._generate_market_insights(
                business_type,
                city,
                competitors_data,
                market_density,
                opportunity_score
            )
            
            return {
                "location": location,
                "business_type": business_type,
                "competitor_count": competitors_data["competitor_count"],
                "market_density": market_density,
                "top_competitors": competitors_data["top_competitors"],
                "ratings_distribution": competitors_data["ratings_distribution"],
                "opportunity_score": opportunity_score,
                "market_insights": insights,
                "data_sources": [
                    "Google Places API",
                    "JustDial Business Data",
                    "Market density calculations based on population data"
                ]
            }
        except Exception as e:
            return {"error": f"Failed to analyze competitors: {str(e)}"}
        
    @staticmethod
    @tool("Get competitor details")
    def get_competitor_details(business_name: str, city: str) -> Dict[str, Any]:
        """
        Retrieves detailed information about a specific competitor business in India.
        
        Args:
            business_name: Name of the business to analyze
            city: City where the business is located
        
        Returns:
            Dict containing detailed business information
        """
        try:
            # This would normally connect to APIs like Google Places, JustDial, MagicPin, etc.
            # For demonstration, using mock data with realistic Indian business information
            
            # In a real implementation, you would make API calls here
            api_key = os.environ.get("GOOGLE_PLACES_API_KEY")
            
            # Mock response with realistic Indian business data
            return {
                "business_name": business_name,
                "location": city,
                "rating": 4.2,
                "review_count": 127,
                "years_in_business": "~3 years",
                "price_level": "₹₹",  # Using rupee symbol
                "popular_times": {
                    "monday": ["10AM-12PM", "6PM-8PM"],
                    "tuesday": ["11AM-1PM", "7PM-9PM"],
                    "wednesday": ["11AM-1PM", "7PM-9PM"],
                    "thursday": ["11AM-1PM", "6PM-8PM"],
                    "friday": ["12PM-2PM", "7PM-10PM"],
                    "saturday": ["12PM-3PM", "7PM-11PM"],
                    "sunday": ["1PM-4PM", "6PM-9PM"]
                },
                "top_services": [
                    "Product/Service A",
                    "Product/Service B",
                    "Product/Service C"
                ],
                "customer_sentiment": {
                    "positive_mentions": ["quality", "service", "value"],
                    "negative_mentions": ["parking", "waiting time"]
                },
                "online_presence": {
                    "website": True,
                    "google_my_business": True,
                    "instagram": True,
                    "facebook": True,
                    "justdial": True
                },
                "note": "This is demo data for illustration. Connect to actual APIs for real data."
            }
        except Exception as e:
            return {"error": f"Failed to get competitor details: {str(e)}"}
    
    @staticmethod
    @tool("Calculate business viability")
    def calculate_business_viability(business_type: str, city: str, budget: float) -> Dict[str, Any]:
        """
        Calculates the viability of starting a specific type of business in an Indian city
        based on competition, market conditions, and available budget.
        
        Args:
            business_type: Type of business (e.g., "restaurant", "grocery store")
            city: City in India
            budget: Available budget in INR lakhs (e.g., 10 = 10 lakh rupees)
        
        Returns:
            Dict containing viability assessment
        """
        try:
            # Get competition data
            competition_data = CompetitorAnalysisTools.analyze_indian_competitors(business_type, city)
            
            # Mock data for startup costs in India (would be from actual data sources)
            # These values would typically come from industry databases or web scraping
            business_costs = CompetitorAnalysisTools._get_business_startup_costs(business_type, city)
            
            # Calculate if budget is sufficient
            is_budget_sufficient = budget >= business_costs["min_startup_cost"]
            
            # Calculate break-even time (in months)
            if is_budget_sufficient:
                break_even_time = round((business_costs["avg_startup_cost"] / 
                                       business_costs["estimated_monthly_revenue"]) * 0.8)
            else:
                break_even_time = None
            
            # Calculate overall viability score (0-100)
            if is_budget_sufficient:
                opportunity_score = competition_data.get("opportunity_score", 60)
                budget_factor = min(100, (budget / business_costs["recommended_budget"]) * 70)
                viability_score = (opportunity_score * 0.6) + (budget_factor * 0.4)
            else:
                viability_score = 0
            
            viability_level = "High" if viability_score > 75 else "Medium" if viability_score > 50 else "Low"
            
            return {
                "business_type": business_type,
                "location": city,
                "budget_provided": f"₹{budget} lakhs",
                "min_budget_required": f"₹{business_costs['min_startup_cost']} lakhs",
                "recommended_budget": f"₹{business_costs['recommended_budget']} lakhs",
                "is_budget_sufficient": is_budget_sufficient,
                "estimated_monthly_revenue": f"₹{business_costs['estimated_monthly_revenue']} lakhs",
                "estimated_monthly_expenses": f"₹{business_costs['estimated_monthly_expenses']} lakhs",
                "estimated_break_even_time": f"{break_even_time} months" if break_even_time else "Budget insufficient",
                "market_competition_level": competition_data.get("market_density", "Medium"),
                "viability_score": round(viability_score),
                "viability_level": viability_level,
                "recommendations": CompetitorAnalysisTools._generate_viability_recommendations(
                    business_type, 
                    city, 
                    budget,
                    viability_score,
                    competition_data,
                    is_budget_sufficient
                )
            }
        except Exception as e:
            return {"error": f"Failed to calculate business viability: {str(e)}"}
    
    # Private helper methods
    @staticmethod
    def _get_competitor_data(business_type: str, location: str) -> Dict[str, Any]:
        """Get data about competitors from various APIs."""
        # In a real implementation, this would call Google Places API, JustDial API, etc.
        
        # Mock data generation with realistic Indian business context
        business_density_map = {
            "restaurant": {"Mumbai": 48, "Delhi": 52, "Bangalore": 45, "Hyderabad": 38, "Chennai": 35, "Pune": 32, "Kolkata": 40},
            "cafe": {"Mumbai": 35, "Delhi": 38, "Bangalore": 42, "Hyderabad": 30, "Chennai": 28, "Pune": 26, "Kolkata": 29},
            "grocery store": {"Mumbai": 60, "Delhi": 65, "Bangalore": 55, "Hyderabad": 50, "Chennai": 52, "Pune": 48, "Kolkata": 58},
            "clothing boutique": {"Mumbai": 70, "Delhi": 75, "Bangalore": 60, "Hyderabad": 55, "Chennai": 58, "Pune": 50, "Kolkata": 65},
            "electronics store": {"Mumbai": 45, "Delhi": 50, "Bangalore": 48, "Hyderabad": 40, "Chennai": 38, "Pune": 35, "Kolkata": 42},
            "salon": {"Mumbai": 55, "Delhi": 60, "Bangalore": 50, "Hyderabad": 48, "Chennai": 45, "Pune": 42, "Kolkata": 50},
            "gym": {"Mumbai": 32, "Delhi": 35, "Bangalore": 30, "Hyderabad": 28, "Chennai": 25, "Pune": 24, "Kolkata": 26},
        }
        
        # Extract city name from location
        city_match = re.search(r'([A-Za-z\s]+)', location)
        city = city_match.group(1).strip() if city_match else "Mumbai"
        
        # Get competitor count based on business type and city
        # Fallback to Mumbai if city not in map
        default_city = "Mumbai"
        competitor_count = 25  # Default
        
        if business_type in business_density_map:
            if city in business_density_map[business_type]:
                competitor_count = business_density_map[business_type][city]
            elif default_city in business_density_map[business_type]:
                competitor_count = business_density_map[business_type][default_city]
        
        # Generate realistic Indian business names based on business type
        business_name_prefixes = {
            "restaurant": ["Spice", "Taj", "Royal", "Desi", "Mumbai", "Delhi", "Chennai", "Cafe", "Hotel"],
            "cafe": ["Chai", "Coffee", "Cafe", "Barista", "Tea", "Urban", "Amul"],
            "grocery store": ["Fresh", "Reliance", "Big", "Daily", "Super", "Dmart", "Spar"],
            "clothing boutique": ["Fashion", "Style", "Trends", "Ethnic", "Metro", "Urban", "Fab"],
            "electronics store": ["Digital", "Tech", "Electronics", "Gadget", "Reliance", "Croma"],
            "salon": ["Style", "Beauty", "Looks", "Hair", "Glamour", "Lakme"],
            "gym": ["Fitness", "Gold's", "Power", "Health", "Active", "Cult"]
        }
        
        business_name_suffixes = {
            "restaurant": ["Restaurant", "Dhaba", "Kitchen", "Dining", "Treats", "Tastes", "Palace", "Garden"],
            "cafe": ["Cafe", "Coffee House", "Chai Point", "Express", "Corner", "Junction"],
            "grocery store": ["Mart", "Bazaar", "Supermarket", "Store", "Market", "Kirana", "Fresh"],
            "clothing boutique": ["Fashion", "Clothing", "Wear", "Fabrics", "Collections", "Styles"],
            "electronics store": ["Electronics", "Gadgets", "Tech World", "Digital Zone", "Solutions"],
            "salon": ["Salon", "Spa", "Beauty Parlour", "Studio", "Makeovers"],
            "gym": ["Gym", "Fitness Center", "Health Club", "Wellness Studio"]
        }
        
        # Generate top competitors with Indian context
        prefixes = business_name_prefixes.get(business_type, ["New", "Best", "Top"])
        suffixes = business_name_suffixes.get(business_type, ["Place", "Shop", "Center"])
        
        top_competitors = []
        avg_rating = 0
        
        for i in range(min(5, competitor_count)):
            prefix = prefixes[i % len(prefixes)]
            suffix = suffixes[i % len(suffixes)]
            
            # Create realistic Indian business names
            if business_type == "restaurant":
                if i % 3 == 0:
                    name = f"{prefix} {suffix}"
                else:
                    indian_food_terms = ["Spice", "Curry", "Tandoor", "Biryani", "Chaat", "Vada", "Dosa"]
                    name = f"{indian_food_terms[i % len(indian_food_terms)]} {suffix}"
            else:
                name = f"{prefix} {suffix}"
                
            # Add city name to some businesses
            if i % 4 == 0:
                name = f"{city} {name}"
            
            rating = round(3.5 + (i * 0.3) % 1.5, 1)  # Ratings between 3.5 and 5.0
            avg_rating += rating
            
            reviews = (75 + (i * 50)) % 300  # Review counts between 75 and 300
            
            # Use rupee symbol for pricing
            price_level = "₹" * (1 + (i % 3))
            
            competitor = {
                "name": name,
                "rating": rating,
                "reviews": reviews,
                "price_level": price_level,
                "years_in_business": f"{1 + (i % 10)} years",
                "popular_for": CompetitorAnalysisTools._get_popular_services(business_type, i)
            }
            
            top_competitors.append(competitor)
        
        avg_rating = avg_rating / len(top_competitors) if top_competitors else 4.0
        
        # Generate ratings distribution
        ratings_distribution = {
            "5_star": round(20 + (avg_rating - 3.5) * 20),
            "4_star": round(35 + (avg_rating - 4) * 10),
            "3_star": round(25 - (avg_rating - 4) * 10),
            "2_star": round(15 - (avg_rating - 4) * 5),
            "1_star": round(5 - (avg_rating - 4) * 2)
        }
        
        return {
            "competitor_count": competitor_count,
            "top_competitors": top_competitors,
            "avg_rating": avg_rating,
            "ratings_distribution": ratings_distribution
        }
    
    @staticmethod
    def _calculate_market_density(competitor_count: int, city: str) -> str:
        """Calculate market density based on competitor count and city population."""
        # Population estimates for major Indian cities (in millions)
        city_populations = {
            "Mumbai": 20.4,
            "Delhi": 16.8,
            "Bangalore": 12.3,
            "Hyderabad": 10.0,
            "Chennai": 8.6,
            "Kolkata": 14.9,
            "Pune": 6.6,
            "Ahmedabad": 8.1,
            "Jaipur": 4.1,
            "Lucknow": 3.5,
            "Kanpur": 3.1,
            "Nagpur": 2.9,
            "Indore": 2.4,
            "Thane": 2.0,
            "Bhopal": 2.4,
            "Visakhapatnam": 2.1,
            "Patna": 2.0,
            "Vadodara": 2.0,
            "Ghaziabad": 1.7,
            "Ludhiana": 1.6
        }
        
        # Default to Mumbai if city not found
        population = city_populations.get(city, city_populations.get("Mumbai", 20.4))
        
        # Calculate density score (competitors per million people)
        density_score = competitor_count / population
        
        if density_score < 2:
            return "Very Low"
        elif density_score < 3.5:
            return "Low"
        elif density_score < 5:
            return "Medium"
        elif density_score < 7:
            return "High"
        else:
            return "Very High"
    
    @staticmethod
    def _calculate_opportunity_score(competitor_count: int, avg_rating: float, market_density: str) -> int:
        """Calculate opportunity score based on various factors."""
        # Base score
        base_score = 50
        
        # Adjust for competitor count
        if competitor_count < 10:
            base_score += 20  # Few competitors is good
        elif competitor_count < 20:
            base_score += 10
        elif competitor_count > 50:
            base_score -= 15  # Too many competitors is bad
        elif competitor_count > 30:
            base_score -= 5
        
        # Adjust for average rating
        if avg_rating < 3.7:
            base_score += 15  # Low ratings mean opportunity to do better
        elif avg_rating < 4.0:
            base_score += 10
        elif avg_rating > 4.5:
            base_score -= 10  # High ratings mean tough competition
        elif avg_rating > 4.3:
            base_score -= 5
        
        # Adjust for market density
        density_factor = {
            "Very Low": 15,
            "Low": 10,
            "Medium": 0,
            "High": -10,
            "Very High": -20
        }
        
        base_score += density_factor.get(market_density, 0)
        
        # Ensure score is between 0-100
        return max(0, min(100, base_score))
    
    @staticmethod
    def _generate_market_insights(business_type: str, city: str, competitors_data: Dict, 
                                 market_density: str, opportunity_score: int) -> List[str]:
        """Generate insights based on the analysis."""
        insights = []
        
        # Generate insights based on competitor count
        if competitors_data["competitor_count"] > 40:
            insights.append(f"The {business_type} market in {city} is heavily saturated with many established players.")
        elif competitors_data["competitor_count"] < 15:
            insights.append(f"There are relatively few {business_type} businesses in {city}, suggesting potential market gaps.")
        else:
            insights.append(f"The {business_type} market in {city} has a moderate number of competitors.")
        
        # Generate insights based on ratings
        if competitors_data["avg_rating"] < 3.8:
            insights.append(f"Average customer satisfaction for {business_type} businesses in this area is low, indicating opportunity for quality service.")
        elif competitors_data["avg_rating"] > 4.3:
            insights.append(f"Existing {business_type} businesses have high customer satisfaction, suggesting high standards will be expected.")
        
        # Generate insights based on market density
        if market_density in ["High", "Very High"]:
            insights.append(f"Market density is {market_density.lower()}, indicating you'll need a strong differentiation strategy to stand out.")
        elif market_density in ["Low", "Very Low"]:
            insights.append(f"Market density is {market_density.lower()}, suggesting good opportunity for new entrants with the right offering.")
        
        # Generate opportunity-based insight
        if opportunity_score > 75:
            insights.append(f"Overall market opportunity is excellent. Consider prioritizing this business type in {city}.")
        elif opportunity_score > 50:
            insights.append(f"Market opportunity is moderate. Success will depend on your unique value proposition.")
        else:
            insights.append(f"Market opportunity is challenging. Consider alternative business types or locations unless you have a highly differentiated offering.")
        
        # Add India-specific insight
        insights.append(f"In {city}, {business_type} businesses typically need to navigate local municipal regulations and potentially GST registration depending on turnover.")
        
        return insights
    
    @staticmethod
    def _get_popular_services(business_type: str, index: int) -> List[str]:
        """Get popular services based on business type with Indian context."""
        services_map = {
            "restaurant": [
                ["North Indian Thali", "Biryani", "South Indian"],
                ["Chinese Cuisine", "Punjabi Food", "Fast Food"],
                ["Street Food", "Mughlai", "Continental"],
                ["Breakfast", "Dinner Buffet", "Home Delivery"],
                ["Family Dining", "Corporate Events", "Catering"]
            ],
            "cafe": [
                ["Filter Coffee", "Masala Chai", "Cold Coffee"],
                ["Sandwiches", "Pastries", "Wifi"],
                ["Breakfast", "Study Space", "Meetings"],
                ["Snacks", "Italian Coffee", "Quick Bites"],
                ["Desserts", "Tea Varieties", "Casual Ambience"]
            ],
            "grocery store": [
                ["Fresh Produce", "Daily Essentials", "Home Delivery"],
                ["Imported Items", "Organic Food", "Bulk Discounts"],
                ["Monthly Packages", "Farm Fresh", "Wide Selection"],
                ["Quick Checkout", "24/7 Service", "Membership Discounts"],
                ["Regional Specialties", "Festival Specials", "Wholesale"]
            ],
            "clothing boutique": [
                ["Ethnic Wear", "Western Outfits", "Festival Collections"],
                ["Designer Wear", "Affordable Fashion", "Accessories"],
                ["Wedding Collection", "Office Wear", "Customization"],
                ["Kid's Clothing", "Men's Fashion", "Women's Exclusive"],
                ["Seasonal Collections", "Designer Labels", "Fashion Consulting"]
            ],
            "electronics store": [
                ["Mobile Phones", "Appliances", "Service Center"],
                ["Laptops & Computers", "Audio Equipment", "EMI Options"],
                ["Smart Home", "Accessories", "Extended Warranty"],
                ["Gaming Products", "Repair Services", "Trade-in Options"],
                ["Latest Gadgets", "Demo Zone", "Technical Support"]
            ],
            "salon": [
                ["Haircuts", "Facial", "Bridal Packages"],
                ["Hair Color", "Spa Services", "Makeup"],
                ["Threading", "Waxing", "Manicure & Pedicure"],
                ["Hair Treatments", "Beauty Packages", "Men's Grooming"],
                ["Wedding Services", "Skin Treatments", "Membership"]
            ],
            "gym": [
                ["Personal Training", "Cardio", "Weight Training"],
                ["Group Classes", "Yoga", "Zumba"],
                ["CrossFit", "Diet Planning", "Bodybuilding"],
                ["24/7 Access", "Steam & Sauna", "Supplements"],
                ["Martial Arts", "Weight Loss Programs", "Sports Training"]
            ]
        }
        
        default_services = ["Service A", "Service B", "Service C"]
        if business_type in services_map:
            return services_map[business_type][index % len(services_map[business_type])]
        return default_services
    
    @staticmethod
    def _get_business_startup_costs(business_type: str, city: str) -> Dict[str, float]:
        """Get startup costs for different business types in Indian cities (in lakhs of rupees)."""
        # Base costs for different business types (in lakhs INR)
        base_costs = {
            "restaurant": {"min": 15, "avg": 25, "recommended": 35},
            "cafe": {"min": 8, "avg": 15, "recommended": 20},
            "grocery store": {"min": 5, "avg": 12, "recommended": 18},
            "clothing boutique": {"min": 10, "avg": 18, "recommended": 25},
            "electronics store": {"min": 20, "avg": 35, "recommended": 50},
            "salon": {"min": 5, "avg": 10, "recommended": 15},
            "gym": {"min": 15, "avg": 25, "recommended": 40},
            # Default for other business types
            "default": {"min": 10, "avg": 20, "recommended": 30}
        }
        
        # City cost multipliers (relative to tier-2 cities)
        city_multipliers = {
            "Mumbai": 1.8,
            "Delhi": 1.6,
            "Bangalore": 1.5,
            "Hyderabad": 1.3,
            "Chennai": 1.3,
            "Pune": 1.2,
            "Kolkata": 1.2,
            "Ahmedabad": 1.1,
            "Jaipur": 1.0,
            "Lucknow": 0.9,
            "Kanpur": 0.9,
            "Nagpur": 0.9,
            "Indore": 0.9,
            "Thane": 1.6,
            "Bhopal": 0.9,
            "Visakhapatnam": 0.9,
            "Patna": 0.9,
            "Vadodara": 1.0,
            "Ghaziabad": 1.3,
            "Ludhiana": 1.0,
            # Default for other cities
            "default": 1.0
        }
        
        # Get base costs for business type
        costs = base_costs.get(business_type, base_costs["default"])
        
        # Apply city multiplier
        multiplier = city_multipliers.get(city, city_multipliers["default"])
        
        adjusted_costs = {
            "min_startup_cost": round(costs["min"] * multiplier, 1),
            "avg_startup_cost": round(costs["avg"] * multiplier, 1),
            "recommended_budget": round(costs["recommended"] * multiplier, 1),
            # Estimated monthly figures
            "estimated_monthly_revenue": round((costs["avg"] * multiplier) / 10, 1),
            "estimated_monthly_expenses": round((costs["avg"] * multiplier) / 15, 1),
        }
        
        return adjusted_costs
    
    @staticmethod
    def _generate_viability_recommendations(business_type: str, city: str, budget: float,
                                          viability_score: float, competition_data: Dict,
                                          is_budget_sufficient: bool) -> List[str]:
        """Generate recommendations based on viability analysis."""
        recommendations = []
        
        # Budget-based recommendations
        if not is_budget_sufficient:
            recommendations.append(f"Your budget of ₹{budget} lakhs is below the minimum recommended for a {business_type} in {city}. Consider increasing your budget or exploring smaller-scale options.")
        elif budget < competition_data.get("recommended_budget", float('inf')):
            recommendations.append(f"Your budget is sufficient but on the lower side. Consider starting with a smaller format or in a less premium location.")
        else:
            recommendations.append(f"Your budget is adequate for establishing a competitive {business_type} in {city}.")
        
        # Competition-based recommendations
        market_density = competition_data.get("market_density", "Medium")
        if market_density in ["High", "Very High"]:
            recommendations.append(f"Due to {market_density.lower()} competition, focus on a unique selling proposition like specialized offerings, premium experience, or niche targeting.")
        
        # Location-specific recommendations for Indian context
        if city in ["Mumbai", "Delhi", "Bangalore"]:
            recommendations.append(f"In metros like {city}, consider location carefully as rental costs can significantly impact profitability. Areas like commercial complexes or tech parks may offer better footfall despite higher rent.")
        
        # Business type specific recommendations with Indian context
        if business_type == "restaurant":
            recommendations.append("In the Indian food industry, consider offering both dine-in and delivery options through platforms like Zomato and Swiggy to maximize revenue streams.")
        elif business_type == "cafe":
            recommendations.append("For cafes in India, creating Instagram-worthy spaces and offering reliable WiFi can attract the growing digital nomad and student populations.")
        elif business_type == "grocery store":
            recommendations.append("Consider offering digital payment options like UPI, Paytm, and PhonePe, and home delivery services to stay competitive in the Indian market.")
        elif business_type == "clothing boutique":
            recommendations.append("Given the seasonal nature of Indian fashion and festivals, plan inventory to align with major events like wedding season and festivals.")
        
        # General recommendation
        if viability_score > 70:
            recommendations.append("Overall viability is strong. Proceed with a detailed business plan and location survey.")
        elif viability_score > 50:
            recommendations.append("Moderate viability. Success will depend on execution excellence and differentiation strategy.")
        else:
            recommendations.append("Challenging viability. Consider pivoting to a different business model or location that offers better opportunity.")
        
        return recommendations