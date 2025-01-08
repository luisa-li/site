from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime, timezone
import os

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def get_access_key(service_name: str) -> str:

    response = (
        supabase.table("api-keys")
        .select("access_key", "updated_at")
        .eq("service", service_name)
        .execute()
    )
    if response.data:
        return response.data[0]["access_key"], response.data[0]["updated_at"]
    else:
        print(f"No access key found for service '{service_name}'")
        return None


def update_access_key(service_name: str, new_access_token: str) -> None:

    existing_key, _ = get_access_key(service_name)
    if existing_key:
        updated_at = datetime.now(timezone.utc).isoformat()
        supabase.table("api-keys").update(
            {
                "access_key": new_access_token,
                "updated_at": updated_at,
            }
        ).eq("service", service_name).execute()
    else:
        supabase.table("api-keys").insert(
            {
                "service": service_name,
                "access_key": new_access_token,
            }
        ).execute()
