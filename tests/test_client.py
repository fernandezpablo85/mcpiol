import pytest
from unittest.mock import patch, Mock
import httpx
import client
from datetime import datetime, timedelta


@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("IOL_USER", "test_user")
    monkeypatch.setenv("IOL_PASS", "test_pass")


@pytest.fixture
def mock_token_response():
    return {"access_token": "test_token", "token_type": "bearer", "expires_in": 3600}


@pytest.fixture
def mock_profile_response():
    return {
        "nombre": "Test",
        "apellido": "User",
        "numeroCuenta": "123456",
        "dni": "12345678",
        "cuitCuil": "20123456789",
        "perfilInversor": "Agresivo",
        "email": "test@example.com",
    }


@pytest.fixture
def mock_portfolio_response():
    return {
        "pais": "Argentina",
        "activos": [
            {
                "titulo": {
                    "simbolo": "GGAL",
                    "tipo": "ACCIONES",
                    "descripcion": "GRUPO FINANCIERO GALICIA",
                },
                "cantidad": 100,
                "ultimoPrecio": 250.5,
                "variacionDiaria": 1.5,
                "puntosVariacion": 2.0,
                "gananciaPorcentaje": 5.0,
                "gananciaDinero": 1000.0,
                "comprometido": 0,
                "ppc": 200.0,
                "valorizado": 25050.0,
            }
        ],
    }


@pytest.fixture
def mock_account_status_response():
    return {
        "cuentas": [
            {
                "numero": 123,
                "tipo": "Inversion_Argentina_Pesos",
                "moneda": "Peso_Argentino",
                "disponible": 1000.0,
                "comprometido": 0.0,
                "saldo": 1000.0,
                "titulosValorizados": 5000.0,
                "total": 6000.0,
                "margenDescubierto": 0.0,
                "estado": "Operable",
            }
        ],
        "estadisticas": [
            {"descripcion": "Operaciones del mes", "cantidad": 5, "volumen": 10000.0}
        ],
        "totalEnPesos": 6000.0,
    }


@pytest.fixture
def mock_performance_response():
    return [
        {
            "fecha": "2024-05-01",
            "apertura": 240.0,
            "maximo": 255.0,
            "minimo": 235.0,
            "cierre": 250.5,
            "volumen": 100000,
        },
        {
            "fecha": "2024-05-02",
            "apertura": 250.5,
            "maximo": 260.0,
            "minimo": 248.0,
            "cierre": 258.0,
            "volumen": 120000,
        }
    ]


@pytest.fixture
def mock_account_operations_response():
    return [
        {
            "numero": 123456,
            "tipo": "Compra",
            "estado": "Terminada",
            "fecha": "2024-05-01",
            "titulo": {
                "simbolo": "GGAL",
                "descripcion": "GRUPO FINANCIERO GALICIA"
            },
            "cantidad": 100,
            "precio": 250.5,
            "monto": 25050.0
        },
        {
            "numero": 123457,
            "tipo": "Venta",
            "estado": "Pendiente",
            "fecha": "2024-05-02",
            "titulo": {
                "simbolo": "YPF",
                "descripcion": "YPF S.A."
            },
            "cantidad": 50,
            "precio": 5000.0,
            "monto": 250000.0
        }
    ]


def test_get_auth_token(mock_env_vars, mock_token_response):
    with patch("httpx.post") as mock_post:
        mock_post.return_value.json.return_value = mock_token_response
        mock_post.return_value.raise_for_status = lambda: None

        token = client.get_auth_token()
        assert token == "test_token"
        mock_post.assert_called_once()


def test_get_profile_data(mock_env_vars, mock_token_response, mock_profile_response):
    with patch("httpx.post") as mock_post, patch("httpx.get") as mock_get:
        mock_post.return_value.json.return_value = mock_token_response
        mock_post.return_value.raise_for_status = lambda: None
        mock_get.return_value.json.return_value = mock_profile_response
        mock_get.return_value.raise_for_status = lambda: None

        profile = client.get_profile_data()
        assert profile["nombre"] == "Test"
        assert profile["apellido"] == "User"
        mock_get.assert_called_once()


def test_get_user_portfolio(
    mock_env_vars, mock_token_response, mock_portfolio_response
):
    with patch("httpx.post") as mock_post, patch("httpx.get") as mock_get:
        mock_post.return_value.json.return_value = mock_token_response
        mock_post.return_value.raise_for_status = lambda: None
        mock_get.return_value.json.return_value = mock_portfolio_response
        mock_get.return_value.raise_for_status = lambda: None

        portfolio = client.get_user_portfolio()
        assert portfolio["pais"] == "Argentina"
        assert len(portfolio["activos"]) == 1
        assert portfolio["activos"][0]["titulo"]["simbolo"] == "GGAL"
        mock_get.assert_called_once()


def test_get_operation_details(mock_env_vars, mock_token_response):
    mock_operation = {
        "numero": 123456,
        "tipo": "Compra",
        "fecha": "2024-01-01",
        "estado": "Terminada",
        "simbolo": "GGAL",
        "cantidad": 100,
        "precio": 250.5,
        "monto": 25050.0,
    }

    with patch("httpx.post") as mock_post, patch("httpx.get") as mock_get:
        mock_post.return_value.json.return_value = mock_token_response
        mock_post.return_value.raise_for_status = lambda: None
        mock_get.return_value.json.return_value = mock_operation
        mock_get.return_value.raise_for_status = lambda: None

        operation = client.get_operation_details(123456)
        assert operation["numero"] == 123456
        assert operation["tipo"] == "Compra"
        mock_get.assert_called_once()


def test_api_error_handling(mock_env_vars, mock_token_response):
    with patch("httpx.post") as mock_post, patch("httpx.get") as mock_get:
        mock_post.return_value.json.return_value = mock_token_response
        mock_post.return_value.raise_for_status = lambda: None
        mock_get.side_effect = httpx.HTTPError("API Error")

        with pytest.raises(httpx.HTTPError):
            client.get_profile_data()


def test_get_account_status(
    mock_env_vars, mock_token_response, mock_account_status_response
):
    with patch("httpx.post") as mock_post, patch("httpx.get") as mock_get:
        mock_post.return_value.json.return_value = mock_token_response
        mock_post.return_value.raise_for_status = lambda: None
        mock_get.return_value.json.return_value = mock_account_status_response
        mock_get.return_value.raise_for_status = lambda: None

        status = client.get_account_status()
        assert len(status["cuentas"]) == 1
        assert status["cuentas"][0]["numero"] == 123
        assert status["cuentas"][0]["tipo"] == "Inversion_Argentina_Pesos"
        assert status["totalEnPesos"] == 6000.0
        mock_get.assert_called_once()


def test_get_last_week_performance(mock_env_vars, mock_token_response, mock_performance_response):
    with patch("httpx.post") as mock_post, patch("httpx.get") as mock_get, \
         patch("client.datetime") as mock_datetime:
        # Mock current date to ensure consistent test results
        mock_now = datetime(2024, 5, 10)
        mock_datetime.now.return_value = mock_now
        mock_datetime.datetime = datetime
        mock_datetime.timedelta = timedelta
        
        mock_post.return_value.json.return_value = mock_token_response
        mock_post.return_value.raise_for_status = lambda: None
        mock_get.return_value.json.return_value = mock_performance_response
        mock_get.return_value.raise_for_status = lambda: None
        
        performance = client.get_last_week_performance("GGAL")
        
        assert len(performance) == 2
        assert performance[0]["fecha"] == "2024-05-01"
        assert performance[0]["cierre"] == 250.5
        assert performance[1]["fecha"] == "2024-05-02"
        
        # Check that the URL was constructed with the correct date range
        mock_get.assert_called_once()
        call_args = mock_get.call_args[0][0]
        assert "2024-05-03/2024-05-10" in call_args
        assert "GGAL" in call_args


def test_get_account_operations_no_filters(mock_env_vars, mock_token_response, mock_account_operations_response):
    with patch("httpx.post") as mock_post, patch("httpx.get") as mock_get:
        mock_post.return_value.json.return_value = mock_token_response
        mock_post.return_value.raise_for_status = lambda: None
        mock_get.return_value.json.return_value = mock_account_operations_response
        mock_get.return_value.raise_for_status = lambda: None
        
        operations = client.get_account_operations()
        
        assert len(operations) == 2
        assert operations[0]["numero"] == 123456
        assert operations[0]["tipo"] == "Compra"
        assert operations[1]["numero"] == 123457
        
        mock_get.assert_called_once()
        # Verify no params were sent
        _, kwargs = mock_get.call_args
        assert "params" in kwargs
        assert kwargs["params"] == {}


def test_get_account_operations_with_filters(mock_env_vars, mock_token_response, mock_account_operations_response):
    with patch("httpx.post") as mock_post, patch("httpx.get") as mock_get:
        mock_post.return_value.json.return_value = mock_token_response
        mock_post.return_value.raise_for_status = lambda: None
        mock_get.return_value.json.return_value = mock_account_operations_response
        mock_get.return_value.raise_for_status = lambda: None
        
        # Test with all filters
        operations = client.get_account_operations(
            start_date="2024-05-01", 
            end_date="2024-05-10",
            status="terminadas"
        )
        
        assert len(operations) == 2
        
        # Verify correct params were sent
        _, kwargs = mock_get.call_args
        assert kwargs["params"]["fechaDesde"] == "2024-05-01"
        assert kwargs["params"]["fechaHasta"] == "2024-05-10"
        assert kwargs["params"]["estado"] == "terminadas"
