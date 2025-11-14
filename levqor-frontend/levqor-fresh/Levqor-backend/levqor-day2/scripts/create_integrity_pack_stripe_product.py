#!/usr/bin/env python3
"""
Create Stripe Product and Price for Integrity Pack
"""
import os
import requests

def create_integrity_pack_product():
    """Create Stripe product and price for Integrity Pack"""
    stripe_key = os.getenv("STRIPE_SECRET_KEY")
    
    if not stripe_key:
        print("❌ STRIPE_SECRET_KEY not found")
        return
    
    headers = {
        "Authorization": f"Bearer {stripe_key}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    # Create Product
    print("Creating Integrity Pack product...")
    product_data = {
        "name": "Integrity + Finalizer Pack",
        "description": "Enterprise-grade E2E verification, schema validation, and PDF evidence report. Run comprehensive integrity tests on your Levqor deployment.",
        "metadata[type]": "add_on",
        "metadata[category]": "enterprise",
    }
    
    product_response = requests.post(
        "https://api.stripe.com/v1/products",
        headers=headers,
        data=product_data
    )
    
    if product_response.status_code != 200:
        print(f"❌ Product creation failed: {product_response.text}")
        return
    
    product = product_response.json()
    product_id = product["id"]
    print(f"✅ Product created: {product_id}")
    
    # Create Price - One-time payment
    print("\nCreating one-time price...")
    price_data = {
        "product": product_id,
        "unit_amount": 4900,  # $49.00
        "currency": "usd",
        "billing_scheme": "per_unit",
        "metadata[type]": "one_time",
    }
    
    price_response = requests.post(
        "https://api.stripe.com/v1/prices",
        headers=headers,
        data=price_data
    )
    
    if price_response.status_code != 200:
        print(f"❌ Price creation failed: {price_response.text}")
        return
    
    price = price_response.json()
    price_id = price["id"]
    print(f"✅ Price created: {price_id}")
    
    # Create monthly subscription price option
    print("\nCreating monthly subscription price...")
    monthly_price_data = {
        "product": product_id,
        "unit_amount": 1900,  # $19/month
        "currency": "usd",
        "recurring[interval]": "month",
        "billing_scheme": "per_unit",
        "metadata[type]": "monthly_subscription",
    }
    
    monthly_price_response = requests.post(
        "https://api.stripe.com/v1/prices",
        headers=headers,
        data=monthly_price_data
    )
    
    if monthly_price_response.status_code != 200:
        print(f"❌ Monthly price creation failed: {monthly_price_response.text}")
        return
    
    monthly_price = monthly_price_response.json()
    monthly_price_id = monthly_price["id"]
    print(f"✅ Monthly price created: {monthly_price_id}")
    
    # Summary
    print("\n" + "="*60)
    print("📦 INTEGRITY PACK STRIPE PRODUCT CREATED")
    print("="*60)
    print(f"Product ID: {product_id}")
    print(f"One-time Price ID: {price_id} ($49.00)")
    print(f"Monthly Price ID: {monthly_price_id} ($19/month)")
    print("\nAdd these to your Replit Secrets:")
    print(f"STRIPE_PRICE_INTEGRITY_ONETIME={price_id}")
    print(f"STRIPE_PRICE_INTEGRITY_MONTHLY={monthly_price_id}")
    print("="*60)
    
    return {
        "product_id": product_id,
        "onetime_price_id": price_id,
        "monthly_price_id": monthly_price_id,
    }


if __name__ == "__main__":
    create_integrity_pack_product()
