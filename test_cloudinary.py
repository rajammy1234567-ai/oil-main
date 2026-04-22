import cloudinary
import cloudinary.api
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
env = environ.Env()
environ.Env.read_env(str(BASE_DIR / 'cattle' / '.env'))

def test_config(cn, ak, as_):
    cloudinary.config(
        cloud_name=cn,
        api_key=ak,
        api_secret=as_,
        secure=True
    )
    try:
        print(f"Testing Cloudinary (Cloud: {cn}, Secret starting with: {as_[:2]})...")
        result = cloudinary.api.ping()
        print("--- Connection Successful! ---")
        return True
    except Exception as e:
        print(f"--- Connection Failed: {str(e)} ---")
        return False

cloud = "dhjnveoxf"
key = "445972572321883"
secret1 = "y6h-5srcDUQ8-4dkx5BxHVGp40As"
secret2 = "6h-5srcDUQ8-4dkx5BxHVGp40As"

if not test_config(cloud, key, secret1):
    test_config(cloud, key, secret2)
