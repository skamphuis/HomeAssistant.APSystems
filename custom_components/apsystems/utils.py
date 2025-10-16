"""Utility functions for APSystems integration."""

import hashlib
import hmac
import time
import uuid
from typing import Any, Dict

import requests
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdfs.pbkdf2 import PBKDF2HMAC


class APSystemsAPI:
    """APSystems API client."""

    def __init__(self, app_id: str, app_secret: str):
        """Initialize the API client."""
        self.app_id = app_id
        self.app_secret = app_secret
        self.base_url = "https://api.apsystemsema.com:9282"

    def _generate_signature(self, method: str, path: str) -> Dict[str, str]:
        """Generate the signature for API requests."""
        timestamp = str(int(time.time() * 1000))
        nonce = str(uuid.uuid4()).replace("-", "")
        
        # Create the string to sign
        string_to_sign = f"{timestamp}/{nonce}/{self.app_id}/{path}/{method}/HmacSHA256"
        
        # Calculate HMAC-SHA256 signature
        signature = hmac.new(
            self.app_secret.encode("utf-8"),
            string_to_sign.encode("utf-8"),
            hashlib.sha256
        ).digest()
        
        import base64
        signature_b64 = base64.b64encode(signature).decode("utf-8")
        
        return {
            "X-CA-AppId": self.app_id,
            "X-CA-Timestamp": timestamp,
            "X-CA-Nonce": nonce,
            "X-CA-Signature-Method": "HmacSHA256",
            "X-CA-Signature": signature_b64,
        }

    def _make_request(self, method: str, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make an authenticated API request."""
        url = f"{self.base_url}{endpoint}"
        headers = self._generate_signature(method, endpoint)
        headers["Content-Type"] = "application/json"
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, params=params, timeout=30)
            else:
                response = requests.request(method, url, headers=headers, json=params, timeout=30)
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {e}")

    def get_system_details(self, system_id: str) -> Dict[str, Any]:
        """Get system details."""
        endpoint = f"/user/api/v2/systems/details/{system_id}"
        return self._make_request("GET", endpoint)

    def get_system_inverters(self, system_id: str) -> Dict[str, Any]:
        """Get system inverters."""
        endpoint = f"/user/api/v2/systems/{system_id}/devices/inverter"
        return self._make_request("GET", endpoint)

    def get_system_meters(self, system_id: str) -> Dict[str, Any]:
        """Get system meters."""
        endpoint = f"/user/api/v2/systems/{system_id}/devices/meter"
        return self._make_request("GET", endpoint)

    def get_system_summary_energy(self, system_id: str) -> Dict[str, Any]:
        """Get system summary energy."""
        endpoint = f"/user/api/v2/systems/{system_id}/energy/summary"
        return self._make_request("GET", endpoint)

    def get_system_energy_period(self, system_id: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """Get system energy for a period."""
        endpoint = f"/user/api/v2/systems/{system_id}/energy/period"
        params = {
            "start_date": start_date,
            "end_date": end_date,
        }
        return self._make_request("GET", endpoint, params)

    def get_ecu_summary_energy(self, system_id: str, ecu_id: str) -> Dict[str, Any]:
        """Get ECU summary energy."""
        endpoint = f"/user/api/v2/systems/{system_id}/devices/ecu/{ecu_id}/energy/summary"
        return self._make_request("GET", endpoint)

    def get_ecu_energy_period(self, system_id: str, ecu_id: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """Get ECU energy for a period."""
        endpoint = f"/user/api/v2/systems/{system_id}/devices/ecu/{ecu_id}/energy/period"
        params = {
            "start_date": start_date,
            "end_date": end_date,
        }
        return self._make_request("GET", endpoint, params)

    def get_inverter_summary_energy(self, system_id: str, inverter_id: str) -> Dict[str, Any]:
        """Get inverter summary energy."""
        endpoint = f"/user/api/v2/systems/{system_id}/devices/inverter/{inverter_id}/energy/summary"
        return self._make_request("GET", endpoint)

    def get_inverter_energy_period(self, system_id: str, inverter_id: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """Get inverter energy for a period."""
        endpoint = f"/user/api/v2/systems/{system_id}/devices/inverter/{inverter_id}/energy/period"
        params = {
            "start_date": start_date,
            "end_date": end_date,
        }
        return self._make_request("GET", endpoint, params)

    def get_inverter_energy_day(self, system_id: str, ecu_id: str, date: str, energy_level: str = "energy") -> Dict[str, Any]:
        """Get inverter energy for a specific day."""
        endpoint = f"/user/api/v2/systems/{system_id}/devices/inverter/batch/energy/{ecu_id}"
        params = {
            "energy_level": energy_level,
            "date_range": date,
        }
        return self._make_request("GET", endpoint, params)
