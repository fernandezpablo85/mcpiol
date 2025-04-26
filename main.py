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
            f"""Operation Number: {op.get("numero")}
Type: {op.get("tipo")}
Date: {op.get("fecha")}
Status: {op.get("estado")}
Settlement: {op.get("liquidacion")}
Symbol: {op.get("simbolo")}
Quantity: {op.get("cantidad")}
Price: {op.get("precio")}
Total Amount: {op.get("monto")}
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
Number: {data.get("numero")}
Type: {data.get("tipo")}
Date: {data.get("fecha")}
Status: {data.get("estado")}
Settlement: {data.get("liquidacion")}
Symbol: {data.get("simbolo")}
Quantity: {data.get("cantidad")}
Price: {data.get("precio")}
Total Amount: {data.get("monto")}
Market: {data.get("mercado")}
Term: {data.get("plazo")}
Validity: {data.get("validez")}
Order Number: {data.get("numeroOrden")}
Currency: {data.get("moneda")}
"""


@mcp.tool()
async def get_account_status() -> str:
    """Get IOL (invertironline) account status and balances"""
    data = client.get_account_status()

    accounts = []
    for account in data["cuentas"]:
        accounts.append(
            f"""Account Number: {account.get("numero")}
Type: {account.get("tipo")}
Currency: {account.get("moneda")}
Available: {account.get("disponible")}
Committed: {account.get("comprometido")}
Balance: {account.get("saldo")}
Securities Value: {account.get("titulosValorizados")}
Total: {account.get("total")}
Overdraft Margin: {account.get("margenDescubierto")}
Status: {account.get("estado")}"""
        )

    stats = []
    for stat in data["estadisticas"]:
        if stat.get("descripcion"):  # Only add non-empty statistics
            stats.append(
                f"""Description: {stat.get("descripcion")}
Quantity: {stat.get("cantidad")}
Volume: {stat.get("volumen")}"""
            )

    result = "\n---\n".join(accounts)
    if stats:
        result += "\n\nStatistics:\n" + "\n---\n".join(stats)

    result += f"\n\nTotal in ARS: {data.get('totalEnPesos')}"

    return result


@mcp.tool()
async def get_quote(symbol: str, market: str = "bCBA") -> str:
    """
    Get current quote for a stock
    Args:
        symbol: The stock symbol (e.g., 'GGAL')
        market: Market identifier (default: 'bCBA' for Argentina)
    """
    data = client.get_stock_quote(symbol, market)
    return f"""Quote for {symbol}:
Last Price: {data.get("ultimoPrecio")}
Previous Close: {data.get("cierreAnterior")}
Opening: {data.get("apertura")}
Daily High: {data.get("maximo")}
Daily Low: {data.get("minimo")}
Volume: {data.get("volumenNominal")}
Amount Traded: {data.get("montoOperado")}
Date/Time: {data.get("fecha")}
Market: {data.get("mercado")}
Currency: {data.get("moneda")}
Daily Change: {data.get("variacionPorcentual")}%
Trades Count: {data.get("cantidadOperaciones")}
"""


@mcp.tool()
async def get_historical_data(symbol: str, start_date: str, end_date: str) -> str:
    """
    Get historical data for a stock
    Args:
        symbol: The stock symbol (e.g., 'GGAL')
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    """
    data = client.get_historical_data(
        symbol=symbol, start_date=start_date, end_date=end_date
    )
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
    return "\n---\n".join(result) if result else "No historical data found"


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
