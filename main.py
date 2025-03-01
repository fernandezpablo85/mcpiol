from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import client

# Initialize FastMCP server
mcp = FastMCP("iol")


@mcp.tool()
async def get_profile_data() -> str:
    """Get IOL (invertironline) profile data"""
    data = client.get_profile_data()
    return f"""Name: {data["nombre"]}
Last Name: {data["apellido"]}
Account Number: {data["numeroCuenta"]}
DNI: {data["dni"]}
CUIT/CUIL: {data["cuitCuil"]}
Investor Profile: {data["perfilInversor"]}
Email: {data["email"]}
"""


@mcp.tool()
async def get_portfolio() -> str:
    """Get IOL (invertironline) investment portfolio"""

    data = client.get_user_portfolio()["activos"]
    result = []
    for asset in data:
        result.append(
            f"""Asset: {asset["titulo"]["simbolo"]}
Type: {asset["titulo"]["tipo"]}
Description: {asset["titulo"]["descripcion"]}
Quantity: {asset["cantidad"]}
Last Price: {asset["ultimoPrecio"]}
Daily Variation: {asset["variacionDiaria"]}
Daily Variation Points: {asset["puntosVariacion"]}
Daily Variation (Percentage): {asset["gananciaPorcentaje"]}
Daily Variation (ARS): {asset["gananciaDinero"]}
Compromised: {asset["comprometido"]}
Average Purchase Price: {asset["ppc"]}
Total Valued: {asset["valorizado"]}
"""
        )
    return "\n---\n".join(result)


@mcp.tool()
def get_past_week_performance(stock_symbol: str) -> str:
    """Get past week performance of a stock"""
    data = client.get_last_week_performance(stock_symbol)
    result = []
    for day in data:
        result.append(
            f"""Date: {day["fechaHora"]}
Opening Price: {day["apertura"]}
Max Price: {day["maximo"]}
Min Price: {day["minimo"]}
Closing Price: {day["ultimoPrecio"]}
Variation: {day["variacion"]}
Volume: {day["volumenNominal"]}
Total Traded: {day["montoOperado"]}
"""
        )

    return "\n---\n".join(result)


@mcp.tool()
async def get_operations(
    start_date: str = None, end_date: str = None, status: str = None
) -> str:
    """
    Get IOL (invertironline) account operations with optional filters
    Args:
        start_date: Optional date in YYYY-MM-DD format to filter from
        end_date: Optional date in YYYY-MM-DD format to filter to
        status: Optional status ('pendientes', 'terminadas', 'canceladas')
    """
    data = client.get_account_operations(start_date, end_date, status)
    result = []
    for op in data:
        result.append(
            f"""Operation Number: {op.get('numero')}
Type: {op.get('tipo')}
Date: {op.get('fecha')}
Status: {op.get('estado')}
Settlement: {op.get('liquidacion')}
Symbol: {op.get('simbolo')}
Quantity: {op.get('cantidad')}
Price: {op.get('precio')}
Total Amount: {op.get('monto')}
"""
        )
    return "\n---\n".join(result) if result else "No operations found"


@mcp.tool()
async def get_operation_details(operation_number: int) -> str:
    """
    Get detailed information about a specific IOL operation
    Args:
        operation_number: The operation number to query
    """
    data = client.get_operation_details(operation_number)
    return f"""Operation Details:
Number: {data.get('numero')}
Type: {data.get('tipo')}
Date: {data.get('fecha')}
Status: {data.get('estado')}
Settlement: {data.get('liquidacion')}
Symbol: {data.get('simbolo')}
Quantity: {data.get('cantidad')}
Price: {data.get('precio')}
Total Amount: {data.get('monto')}
Market: {data.get('mercado')}
Term: {data.get('plazo')}
Validity: {data.get('validez')}
Order Number: {data.get('numeroOrden')}
Currency: {data.get('moneda')}
"""


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
