"""Diagnostic script to check Square SDK installation."""
import sys

print("Python version:", sys.version)
print("\n" + "="*50)

# Check if square package exists
try:
    import square
    print("✓ 'square' package found")
    print(f"  Location: {square.__file__}")
    print(f"  Available attributes: {dir(square)}")

    # Check for Client
    if hasattr(square, 'Client'):
        print("✓ square.Client exists")
    else:
        print("✗ square.Client does NOT exist")

except ImportError as e:
    print(f"✗ Cannot import square: {e}")

print("\n" + "="*50)

# Check square.client module
try:
    import square.client
    print("✓ 'square.client' module found")
    print(f"  Available attributes: {dir(square.client)}")

    if hasattr(square.client, 'Client'):
        print("✓ square.client.Client exists")
    else:
        print("✗ square.client.Client does NOT exist")

except ImportError as e:
    print(f"✗ Cannot import square.client: {e}")

print("\n" + "="*50)

# Check installed package version
try:
    import pkg_resources
    version = pkg_resources.get_distribution('squareup').version
    print(f"✓ squareup package version: {version}")
except Exception as e:
    print(f"✗ Cannot get squareup version: {e}")

print("\n" + "="*50)
print("\nIf Client is not found, the Square SDK may not be properly installed.")
print("Try: pip uninstall squareup -y && pip install squareup")
