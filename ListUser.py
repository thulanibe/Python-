import requests

url = 'https://xturf-api.ait-devel.com/api/v1/admin/wallet/transactions'

# Create a list to store user data dictionaries
user_data_list = []

for user_id in range(100, 125):
    user_data = {
        "transactionType": 24,
        "descriptionParams": {"date": "2023-08-08", "line_number": 1},
        "amount": 1000,
        "currency": "ZAR",
        "divisor": 1,
        "customer": user_id
    }
    user_data_list.append(user_data)

for user_data in user_data_list:
    response = requests.post(url, json=user_data)
    
    if response.status_code == 200:
        print(f"Transaction for customer {user_data['customer']} successful.")
    else:
        print(f"Transaction for customer {user_data['customer']} failed. Response: {response.text}")
