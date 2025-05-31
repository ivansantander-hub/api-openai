#!/usr/bin/env python3
"""
Script de debugging para Railway - Problema Error 307
"""

import requests
import os
import json
from urllib.parse import urljoin

def test_railway_auth():
    """Test específico para debugging del error 307 en Railway."""
    
    # Detectar si estamos en Railway o local
    railway_url = os.getenv('RAILWAY_STATIC_URL')
    if railway_url:
        base_url = f"https://{railway_url}"
        print(f"🚄 Testing Railway deployment: {base_url}")
    else:
        base_url = "http://localhost:8000"
        print(f"🏠 Testing local deployment: {base_url}")
    
    # Access key para testing
    access_key = os.getenv('ACCESS_KEY') or input("Enter ACCESS_KEY: ")
    
    print(f"\n🔍 Debugging authentication endpoints...")
    
    # Test diferentes variantes del endpoint auth
    auth_endpoints = [
        "/auth",
        "/auth/",
        "auth",
        "auth/"
    ]
    
    for endpoint in auth_endpoints:
        print(f"\n🧪 Testing endpoint: {endpoint}")
        url = urljoin(base_url, endpoint)
        print(f"Full URL: {url}")
        
        try:
            # Test con diferentes headers
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'User-Agent': 'Railway-Debug-Script/1.0'
            }
            
            data = {"access_key": access_key}
            
            response = requests.post(
                url, 
                json=data, 
                headers=headers,
                allow_redirects=False,  # No seguir redirects automáticamente
                timeout=10
            )
            
            print(f"Status Code: {response.status_code}")
            print(f"Headers: {dict(response.headers)}")
            
            if response.status_code in [307, 308]:
                print(f"🔄 REDIRECT DETECTED!")
                print(f"Location: {response.headers.get('Location', 'Not provided')}")
                
                # Intentar seguir el redirect manualmente
                if 'Location' in response.headers:
                    redirect_url = response.headers['Location']
                    print(f"Following redirect to: {redirect_url}")
                    
                    redirect_response = requests.post(
                        redirect_url,
                        json=data,
                        headers=headers,
                        timeout=10
                    )
                    print(f"Redirect result: {redirect_response.status_code}")
                    if redirect_response.ok:
                        print(f"✅ Success after redirect: {redirect_response.json()}")
            
            elif response.ok:
                print(f"✅ SUCCESS: {response.json()}")
                return True
            else:
                print(f"❌ FAILED: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"💥 ERROR: {e}")
    
    print(f"\n🔍 Testing health endpoint...")
    try:
        health_url = urljoin(base_url, "/health")
        health_response = requests.get(health_url, timeout=10)
        print(f"Health Status: {health_response.status_code}")
        if health_response.ok:
            print(f"✅ Health OK: {health_response.json()}")
        else:
            print(f"❌ Health Failed: {health_response.text}")
    except Exception as e:
        print(f"💥 Health Error: {e}")

    print(f"\n📊 Summary:")
    print(f"- Base URL: {base_url}")
    print(f"- Environment: {'Railway' if railway_url else 'Local'}")
    print(f"- ACCESS_KEY configured: {'Yes' if access_key else 'No'}")

if __name__ == "__main__":
    test_railway_auth() 