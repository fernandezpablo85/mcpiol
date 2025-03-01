# Invertir Online (IOL) API Client Implementation Guide

This guide provides comprehensive information for implementing a client for the Invertir Online (IOL) API v2.

## Table of Contents

- [Introduction](#introduction)
- [Authentication](#authentication)
- [Base URL](#base-url)
- [API Endpoints](#api-endpoints)
  - [Authentication](#authentication-endpoints)
  - [Account Management](#account-management)
  - [User Profile](#user-profile)
  - [Portfolio and Account Status](#portfolio-and-account-status)
  - [Trading Operations](#trading-operations)
  - [Financial Instruments](#financial-instruments)
  - [Mutual Funds (FCI)](#mutual-funds-fci)
  - [Bank Accounts](#bank-accounts)
  - [WebSocket](#websocket)
  - [Advisors](#advisors)
- [Request Examples](#request-examples)
- [Response Examples](#response-examples)
- [Implementation Best Practices](#implementation-best-practices)

## Introduction

IOL (Invertir Online) provides a REST API that allows developers to interact with the platform programmatically. The API enables actions such as retrieving account information, executing trades, and monitoring investments.

## Authentication

The API uses Bearer Token authentication. You need to:

1. Obtain a token via the authentication endpoint
2. Include the token in the Authorization header of all subsequent requests

```
Authorization: Bearer {your_token}
```

## Base URL

```
https://api.invertironline.com/api/v2
```

## API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | /token   | Obtain authentication token |

#### Example Request:

```curl
curl --location 'https://api.invertironline.com/api/v2/token' \
--header 'Content-Type: application/json' \
--data '{
  "username": "your_username",
  "password": "your_password"
}'
```

### Account Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | /apertura-cuenta | Create a user without a trading account |
| POST   | /apertura-cuenta/dni-frontal | Validate and save front DNI photo |
| POST   | /apertura-cuenta/dni-dorsal | Validate and save back DNI photo |
| POST   | /apertura-cuenta/selfie-neutral | Validate and save neutral selfie |
| POST   | /apertura-cuenta/selfie-sonriente | Validate and save smiling selfie |
| POST   | /apertura-cuenta/datos-personales | Submit essential personal data |
| POST   | /apertura-cuenta/datos-juridicos | Associate personal and legal data |
| POST   | /apertura-cuenta/generar-cuenta | Generate trading account number |
| GET    | /formulario-apertura-cuenta | Get account opening form |
| POST   | /aceptar-tyc | Accept terms and conditions |

### User Profile

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | /datos-perfil | Get authenticated user profile data |

#### Example Response:

```json
{
  "nombre": "Mi nombre",
  "apellido": "Mi apellido",
  "numeroCuenta": "123456",
  "dni": "2031546",
  "sexo": "Otro",
  "perfilInversor": "Nombre del perfil"
}
```

### Portfolio and Account Status

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | /estadocuenta | Get account status |
| GET    | /portafolio/:pais | Get portfolio by country |
| GET    | /clientes | Get clients list |

#### Example Response (estadocuenta):

```json
{
  "cuentas": [
    {
      "numero": 2,
      "tipo": "Inversion_Argentina_Pesos",
      "moneda": "Peso_Argentino",
      "disponible": 100,
      "comprometido": 0,
      "saldo": 200,
      "titulosValorizados": 0,
      "total": 200,
      "margenDescubierto": 0,
      "saldos": [
        {
          "liquidacion": "Inmediato",
          "saldo": 0,
          "comprometido": 0,
          "disponible": 0,
          "disponibleOperar": 0
        }
      ],
      "estado": "Operable"
    }
  ],
  "estadisticas": [
    {
      "descripcion": "",
      "cantidad": 0,
      "volumen": 0
    }
  ],
  "totalEnPesos": 200
}
```

#### Example Response (portafolio):

```json
{
  "pais": "Argentina",
  "activos": [
    {
      "cantidad": 0,
      "comprometido": 0,
      "puntosVariacion": 0,
      "variacionDiaria": 0,
      "ultimoPrecio": 0,
      "ppc": 0,
      "gananciaPorcentaje": 0,
      "gananciaDinero": 0,
      "valorizado": 0,
      "titulo": {
        "simbolo": "FMC",
        "descripcion": "",
        "pais": "Argentina",
        "mercado": "NYSE",
        "tipo": "ACCIONES",
        "plazo": "T0",
        "moneda": "Peso_Argentino"
      },
      "parking": {
        "disponibleInmediato": 0
      }
    }
  ]
}
```

### Trading Operations

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | /operaciones | Get operations |
| GET    | /operaciones/{numero} | Get operation by number |
| POST   | /operar/comprar | Execute buy operation |
| POST   | /operar/vender | Execute sell operation |
| DEL    | /micuenta/cancelar | Cancel operation |

### Financial Instruments

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | /titulos | Get securities list |
| GET    | /titulos/cotizacion | Get quote |
| GET    | /titulos/cotizacion/detalle | Get detailed quote |
| GET    | /titulos/panel-cotizaciones | Get quotes panel |
| GET    | /titulos/cotizacion/serie-historica | Get historical quotes |
| GET    | /{pais}/titulos/cotizacion | Get quotes by country |
| GET    | /titulos/opciones | Get options |

### Mutual Funds (FCI)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | /titulos/fci | Get mutual funds list |
| GET    | /titulos/administradoras/fci | Get fund administrators |
| GET    | /titulos/tipo-fondos | Get fund types |
| GET    | /titulos/administradoras/{administradora}/tipo-fondos | Get fund types by administrator |
| POST   | /operar/fci/suscripcion | Subscribe to a mutual fund |
| POST   | /operar/fci/rescate | Redeem from a mutual fund |
| POST   | /asesores/fci/suscribir | Advisor: subscribe to a mutual fund |
| POST   | /asesores/fci/rescatar | Advisor: redeem from a mutual fund |
| DEL    | /asesores/fci/cancelar | Advisor: cancel operation |

### Bank Accounts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | /cuentas-bancarias | Get client's bank accounts |
| POST   | /cuentas-bancarias | Add a bank account |
| DEL    | /cuentas-bancarias | Remove a bank account |
| POST   | /cuentas-bancarias/extraccion | Request withdrawal to bank account |
| DEL    | /cuentas-bancarias/extraccion | Cancel withdrawal request |
| POST   | /cuentas-bancarias/deposito | Report deposit |
| POST   | /cuentas-bancarias/movimientos | Query movements |

### WebSocket

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | /websocket/autenticacion | WebSocket authentication |
| GET    | /websocket/ping | WebSocket ping |
| GET    | /websocket/conexion | WebSocket connection |
| GET    | /websocket/movimientos | WebSocket movements |

### Advisors

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | /asesores/test-inversor/preguntas | Get investor test questions |
| POST   | /asesores/test-inversor/respuestas | Submit investor test answers |
| POST   | /asesores/movimiento/historico | Get advised client's historical movements |
| GET    | /asesores/operaciones | Get advised client's operations |
| GET    | /asesores/operaciones/{id}/componentes | Get components of a specific operation |
| GET    | /asesores/operaciones/{id}/boleto | Get transaction ticket |
| POST   | /asesores/operar/compra | Execute buy operation as advisor |
| POST   | /asesores/operar/venta | Execute sell operation as advisor |

## Request Examples

### Authenticating

```curl
curl --location 'https://api.invertironline.com/api/v2/token' \
--header 'Content-Type: application/json' \
--data '{
  "username": "your_username",
  "password": "your_password"
}'
```

### Getting Profile Data

```curl
curl --location 'https://api.invertironline.com/api/v2/datos-perfil' \
--header 'Authorization: Bearer YOUR_TOKEN'
```

### Getting Account Status

```curl
curl --location 'https://api.invertironline.com/api/v2/estadocuenta' \
--header 'Authorization: Bearer YOUR_TOKEN'
```

### Getting Portfolio (Argentina)

```curl
curl --location 'https://api.invertironline.com/api/v2/portafolio/Argentina' \
--header 'Authorization: Bearer YOUR_TOKEN'
```

### Executing a Buy Operation

```curl
curl --location 'https://api.invertironline.com/api/v2/operar/comprar' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer YOUR_TOKEN' \
--data '{
  "mercado": "BCBA",
  "simbolo": "GGAL",
  "cantidad": 100,
  "precio": 150.25,
  "plazo": "T2",
  "validez": "1d"
}'
```

## Implementation Best Practices

1. **Error Handling**: Always implement proper error handling in your client to deal with various HTTP status codes and API-specific error responses.

2. **Token Management**: Store and refresh your authentication token securely. Implement automatic token refresh when expired.

3. **Rate Limiting**: Be aware of possible rate limits on the API and implement appropriate backoff strategies.

4. **Data Validation**: Validate all data before sending it to the API to ensure it meets the required format and constraints.

5. **Connection Pooling**: For high-volume applications, use connection pooling to minimize connection overhead.

6. **Logging**: Implement comprehensive logging to help with debugging and monitoring of API interactions.

7. **WebSocket Connection**: For real-time updates, maintain a persistent WebSocket connection and implement reconnection logic.

8. **Security**: Store credentials and tokens securely, and consider using environment variables for sensitive information.

## Conclusion

This guide covers the basic information needed to implement a client for the IOL API. For more detailed information on each endpoint, refer to the official API documentation or contact IOL support.

Always test your implementation thoroughly in a staging environment before moving to production to ensure proper functionality and to avoid any unintended consequences in live trading environments.
