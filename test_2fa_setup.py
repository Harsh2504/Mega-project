"""
Quick test to verify 2FA packages are installed correctly
Run this to check if pyotp and qrcode are working
"""

try:
    import pyotp
    print("✓ pyotp installed successfully")
    
    import qrcode
    print("✓ qrcode installed successfully")
    
    # Test TOTP generation
    secret = pyotp.random_base32()
    print(f"✓ Generated test secret: {secret}")
    
    totp = pyotp.TOTP(secret)
    code = totp.now()
    print(f"✓ Generated test code: {code}")
    
    # Test verification
    is_valid = totp.verify(code)
    print(f"✓ Code verification: {is_valid}")
    
    print("\n✅ All 2FA components are working correctly!")
    print("You can now use Two-Factor Authentication in your app.")
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Please run: pip install pyotp qrcode[pil]")
except Exception as e:
    print(f"❌ Error: {e}")
