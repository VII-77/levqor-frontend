#!/usr/bin/env python3
"""
Setup Stripe Products for Developer Portal
Creates products and prices for Sandbox, Pro, and Enterprise tiers
"""
import os
import requests

def create_stripe_products():
    """Create Stripe products for developer tiers"""
    stripe_key = os.getenv("STRIPE_SECRET_KEY", "").strip()
    
    if not stripe_key:
        print("❌ STRIPE_SECRET_KEY not found in environment")
        return False
    
    headers = {
        "Authorization": f"Bearer {stripe_key}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    products_to_create = [
        {
            "name": "Levqor Developer - Pro",
            "description": "10,000 API calls per month with email support",
            "price": 1900,  # $19.00 in cents
            "interval": "month",
            "tier": "pro"
        },
        {
            "name": "Levqor Developer - Enterprise",
            "description": "Unlimited API calls with SLA and priority support",
            "price": 19900,  # $199.00 in cents
            "interval": "month",
            "tier": "enterprise"
        }
    ]
    
    created_products = {}
    
    for product_data in products_to_create:
        print(f"\n🔨 Creating product: {product_data['name']}")
        
        # Create product
        product_response = requests.post(
            "https://api.stripe.com/v1/products",
            headers=headers,
            data={
                "name": product_data["name"],
                "description": product_data["description"],
                "metadata[tier]": product_data["tier"]
            }
        )
        
        if product_response.status_code != 200:
            print(f"❌ Failed to create product: {product_response.text}")
            continue
        
        product = product_response.json()
        product_id = product["id"]
        print(f"✅ Product created: {product_id}")
        
        # Create price
        price_response = requests.post(
            "https://api.stripe.com/v1/prices",
            headers=headers,
            data={
                "product": product_id,
                "unit_amount": product_data["price"],
                "currency": "usd",
                "recurring[interval]": product_data["interval"],
                "metadata[tier]": product_data["tier"]
            }
        )
        
        if price_response.status_code != 200:
            print(f"❌ Failed to create price: {price_response.text}")
            continue
        
        price = price_response.json()
        price_id = price["id"]
        print(f"✅ Price created: {price_id}")
        
        created_products[product_data["tier"]] = {
            "product_id": product_id,
            "price_id": price_id,
            "amount": product_data["price"] / 100
        }
    
    # Print summary
    print("\n" + "="*70)
    print("📊 STRIPE DEVELOPER PRODUCTS CREATED")
    print("="*70)
    print("\nAdd these to your Replit Secrets:\n")
    
    if "pro" in created_products:
        print(f"STRIPE_PRICE_DEV_PRO={created_products['pro']['price_id']}")
    
    if "enterprise" in created_products:
        print(f"STRIPE_PRICE_DEV_ENTERPRISE={created_products['enterprise']['price_id']}")
    
    print("\n" + "="*70)
    
    return True

if __name__ == "__main__":
    print("🚀 Setting up Stripe products for Developer Portal...")
    create_stripe_products()
