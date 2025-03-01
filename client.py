import os
import httpx
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

UA = "mcpiol/1.0"


def get_auth_token():
    user = os.getenv("IOL_USER")
    password = os.getenv("IOL_PASS")
    if not user or not password:
        raise ValueError("IOL_USER and IOL_PASS environment variables must be set")

    url = "https://api.invertironline.com/token"
    payload = {"username": user, "password": password, "grant_type": "password"}
    headers = {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": UA}

    response = httpx.post(url, data=payload, headers=headers)
    response.raise_for_status()
    return response.json().get("access_token")


def get_profile_data():
    token = get_auth_token()
    url = "https://api.invertironline.com/api/v2/datos-perfil"
    headers = {"Authorization": f"Bearer {token}", "User-Agent": UA}

    response = httpx.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def get_user_portfolio():
    token = get_auth_token()
    url = "https://api.invertironline.com/api/v2/portafolio/Argentina"
    headers = {"Authorization": f"Bearer {token}", "User-Agent": UA}

    response = httpx.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def get_last_week_performance(symbol: str):
    now = datetime.now()
    last_week = now - timedelta(days=7)
    now_iso = now.strftime("%Y-%m-%d")
    last_week_iso = last_week.strftime("%Y-%m-%d")
    url = f"https://api.invertironline.com/api/v2/bCBA/Titulos/{symbol}/Cotizacion/seriehistorica/{last_week_iso}/{now_iso}/ajustada"
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}", "User-Agent": UA}
    response = httpx.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def get_account_operations(
    start_date: str = None, end_date: str = None, status: str = None
):
    """
    Get account operations with optional filters.

    Args:
        start_date: Optional ISO format date (YYYY-MM-DD) to filter from
        end_date: Optional ISO format date (YYYY-MM-DD) to filter to
        status: Optional status filter ('pendientes', 'terminadas', 'canceladas')
    """
    token = get_auth_token()
    url = "https://api.invertironline.com/api/v2/operaciones"

    params = {}
    if start_date:
        params["fechaDesde"] = start_date
    if end_date:
        params["fechaHasta"] = end_date
    if status:
        params["estado"] = status

    headers = {"Authorization": f"Bearer {token}", "User-Agent": UA}

    response = httpx.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def get_operation_details(operation_number: int):
    """
    Get detailed information about a specific operation.

    Args:
        operation_number: The operation number to query
    """
    token = get_auth_token()
    url = f"https://api.invertironline.com/api/v2/operaciones/{operation_number}"
    headers = {"Authorization": f"Bearer {token}", "User-Agent": UA}

    response = httpx.get(url, headers=headers)
    response.raise_for_status()
    return response.json()
