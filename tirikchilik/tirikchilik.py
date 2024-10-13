import json
from typing import Dict, Any
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class Tirikchilik:
    def __init__(self, project_name: str):
        self.base_url = 'https://api.tirikchilik.uz/api/ProjectPay'
        self.user_url = 'https://api.tirikchilik.uz/api/User'
        self.session = self._create_session()
        self.project_id = self._get_project_by_name(project_name)

    def _create_session(self):
        session = requests.Session()
        retries = Retry(total=3, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retries, pool_connections=10, pool_maxsize=10)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def _make_request(self, method: str, url: str, payload: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Make HTTP request and handle response
        """
        try:
            kwargs = {
                'timeout': (3.05, 10),  # (connect timeout, read timeout)
                'headers': {'Content-Type': 'application/json'}
            }

            if method.lower() == 'post':
                response = self.session.post(url, json=payload, **kwargs)
            elif method.lower() == 'get':
                response = self.session.get(url, **kwargs)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            data = response.json()

            if data.get('success'):
                return data
            else:
                self._handle_error(data.get('error', {}))

        except requests.RequestException as e:
            raise PaymentError(f"Request failed: {str(e)}")

    def _handle_error(self, error: Dict[str, Any]):
        """
        Handle API errors
        """
        code = error.get('code')
        message = error.get('message', {}).get('en', 'Unknown error')
        description = error.get('description', '')
        if code == "ERROR_INTERNAL" and "ERROR_CARD_NOT_FOUND" == str(json.loads(description).get('error').get('code')):
            details = json.loads(description).get('error', {}).get('details', '')
            raise CardNotFoundError(details, code, description)
        elif code == "ERROR_NOT_FOUND":
            raise PaymentNotFoundError(message, code, description)
        else:
            raise PaymentError(message, code, description)

    def _get_project_by_name(self, name: str) -> int:
        """
        Get project ID by name
        """
        url = f'{self.user_url}/GetByName?userName={name}'
        response = self._make_request('get', url)

        if response['success'] and response['data']:
            return response['data']['donateId']
        else:
            raise UserNotFoundError(f"User '{name}' not found")

    def create_payment(self, amount: int, donater: str, notes: str, card_number: str, expiry: str) -> Dict[str, Any]:
        """
        Create payment
        :param amount: int - amount of payment
        :param card_number: str - card number
        :param expiry: str - expiry date of card
        :param donater: str - name of donater (optional)
        :param notes: str - notes for payment (optional)
        :return: dict example: {'data': {'payId': 'ecdd416a-1bba-4047-9ebb-808b24424487', 'checkoutUrl': 'https://checkout.multicard.uz/8ba58fb9-7b33-11ef-bfaa-00505680eaf6', 'donateAmount': 500186, 'commissionAmount': 26326, 'totalAmount': 526512}, 'success': True, 'error': None}
        """
        url = f'{self.base_url}/Create'
        payload = {
            "projectId": self.project_id,
            "amount": int(amount),
            "source": "",
            "donater": donater,
            "notes": notes,
            "card": {
                "pan": str(card_number),
                "expiry": str(expiry)
            }
        }

        return self._make_request('post', url, payload)

    def get_payment_status(self, payment_id: int) -> Dict[str, Any]:
        """
        Get payment status
        :param payment_id: int - payment id
        :return: dict example: {'data': 'Paid', 'success': True, 'error': None}
        """
        url = f'{self.base_url}/Status?payId={payment_id}'
        return self._make_request('get', url)


class PaymentError(Exception):
    def __init__(self, message: str, code: str = None, description: str = None):
        self.code = code
        self.message = message
        self.description = description
        super().__init__(f"PaymentError. Code: {self.code}. Message: {self.message}. Description: {self.description}")


class CardNotFoundError(PaymentError):
    pass


class PaymentNotFoundError(PaymentError):
    pass

class UserNotFoundError(PaymentError):
    pass