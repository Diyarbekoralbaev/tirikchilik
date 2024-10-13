# Tirikchilik

[![PyPI version](https://img.shields.io/pypi/v/)](https://pypi.org/project/tirikchilik/)
[![Python Versions](https://img.shields.io/pypi/pyversions/tirikchilik.svg)](https://pypi.org/project/tirikchilik/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![PyPI Downloads](https://img.shields.io/pypi/dm/tirikchilik)
<p align="center">
  <a href="https://tirikchilik.uz/araltech">
    <img src="https://camo.githubusercontent.com/ed28339e5a5786534715b1c0c885271437761fc91af84d5dc5bbc2c71e307a02/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f546972696b6368696c696b2d6666646430303f7374796c653d666f722d7468652d6261646765" alt="Donate with Tirikchilik">
  </a>
</p>

Tirikchilik is an unofficial Python library for interacting with the Tirikchilik payment API. It provides a simple and
efficient way to create payments, check payment statuses, and handle various payment-related operations.

**Note:** This is an unofficial API wrapper and is not affiliated with or endorsed by Tirikchilik. Use at your own risk.

## Features

- Easy-to-use interface for creating payments
- Automatic project ID retrieval by project name
- Robust error handling for various API responses
- Retry mechanism for failed requests
- Type hinting for better code completion and error detection
- Customizable session management

## Installation

You can install Tirikchilik using pip:

```bash
pip install tirikchilik
```

## Quick Start

Here's a simple example to get you started with Tirikchilik:

```python
from tirikchilik import Tirikchilik

# Initialize the Tirikchilik client
client = Tirikchilik("MyProject")

# Create a payment
try:
    payment_response = client.create_payment(
        amount=1000,
        donater="John Doe",
        notes="Donation for Project X",
        card_number="1234567890123456",
        expiry="12/25"
    )

    # Get payment ID and checkout URL
    payment_id = payment_response['data']['payId']
    checkout_url = payment_response['data']['checkoutUrl']

    print(f"Payment ID: {payment_id}")
    print(f"Checkout URL: {checkout_url}")

    # Check payment status
    status_response = client.get_payment_status(payment_id)
    print(f"Payment status: {status_response['data']}")

except Exception as e:
    print(f"Error: {str(e)}")
```

## Advanced Usage

### Error Handling

Tirikchilik provides custom exceptions for different error scenarios:

```python
from tirikchilik import Tirikchilik, CardNotFoundError, PaymentNotFoundError, UserNotFoundError, PaymentError

client = Tirikchilik("MyProject")

try:
    payment = client.create_payment(...)
except CardNotFoundError as e:
    print(f"Card not found: {e}")
except PaymentNotFoundError as e:
    print(f"Payment not found: {e}")
except UserNotFoundError as e:
    print(f"User not found: {e}")
except PaymentError as e:
    print(f"General payment error: {e}")
```

## API Reference

### `Tirikchilik(project_name: str)`

Initialize a Tirikchilik client.

- `project_name`: The name of the project to use for payments.

### `create_payment(amount: int, donater: str, notes: str, card_number: str, expiry: str) -> Dict[str, Any]`

Create a new payment.

- `amount`: The payment amount in cents.
- `donater`: The name of the person making the donation.
- `notes`: Additional notes for the payment.
- `card_number`: The card number to use for the payment.
- `expiry`: The expiry date of the card in the format "YYMM". Example if the expiry date is December 2025, you should
  set "2512".

Returns a dictionary with the payment details. Example:

```python
{
    'data': {
        'payId': 'ecdd416a-1bba-4047-9ebb-808b24424487',
        'checkoutUrl': 'https://checkout.multicard.uz/8ba58fb9-7b33-11ef-bfaa-00875680eaf6',
        'donateAmount': 500000,
        'commissionAmount': 26326,
        'totalAmount': 526512
    },
    'success': True,
    'error': None
}   
```

- `payId`: The ID of the payment.
- `checkoutUrl`: The URL to redirect the user to complete the payment.
- `donateAmount`: The amount donated by the user. Remember you should increase amount to x100. For example, if you want
  to donate 5000 UZS, you should set 5000 * 100 = 500000.
- `commissionAmount`: The commission amount calculated by the system.
- `totalAmount`: The total amount to be paid by the user.

### `get_payment_status(payment_id: int) -> Dict[str, Any]`

Get the status of a payment.

- `payment_id`: The ID of the payment to check.

Returns a dictionary with the payment status. Example if the payment is successful:

```python
{
    'data': 'Paid',
    'success': True,
    'error': None
}
```

Or if payment is in draft (not paid) status:

```python
{
    'data': 'Draft',
    'success': True,
    'error': None
}
```

## Dependencies

Tirikchilik depends on the following packages:

- requests (~2.32.3)
- urllib3 (~2.2.3)

These dependencies will be automatically installed when you install Tirikchilik.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Support

If you like this project, please consider supporting it by making a donation:
<p align="center">
  <a href="https://tirikchilik.uz/araltech">
    <img src="https://camo.githubusercontent.com/ed28339e5a5786534715b1c0c885271437761fc91af84d5dc5bbc2c71e307a02/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f546972696b6368696c696b2d6666646430303f7374796c653d666f722d7468652d6261646765" alt="Donate with Tirikchilik">
  </a>
</p>

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/Diyarbekoralbaev/tirikchilik/LICENSE)
file for details.

## Disclaimer

This is an unofficial API wrapper for Tirikchilik. It is not affiliated with, endorsed, or supported by Tirikchilik. Use
this library at your own risk. The authors and contributors are not responsible for any misuse or damage caused by this
software.

## Acknowledgments

- Built with love for the Python community
- Inspired by modern Python API clients
