import requests
import unittest
import random
import secrets
import string

# Function to generate a random name
def generate_random_name():
    return ''.join(random.choices(string.ascii_letters, k=10))  # 10 letters name

# Function to generate a random NIK (assuming numeric string of length 16)
def generate_random_nik():
    return ''.join(random.choices(string.digits, k=16))  # 16 digits NIK

# Function to generate a random phone number (assuming numeric string of length 10)
def generate_random_phone_number():
    return ''.join(random.choices(string.digits, k=10))  # 10 digits phone number

# Function to generate a random PIN (assuming numeric string of length 6)
def generate_random_pin():
    return ''.join(secrets.choice(string.digits) for _ in range(6))  # 6 digits PIN

class TestBankingAPI(unittest.TestCase):
    baseurl = 'http://localhost:8001/api/v1'
    no_hp = None
    pin = None
    no_rekening = None
    token = None

    @classmethod
    def setUpClass(cls):
        # REGISTER
        register_url = f'{cls.baseurl}/nasabah/daftar'
        register_data = {
            "nama": generate_random_name(),
            "nik": generate_random_nik(),
            "no_hp": generate_random_phone_number(),
            "pin": generate_random_pin()
        }
        cls.no_hp = register_data['no_hp']
        cls.pin = register_data['pin']
        response_register =  requests.post(register_url, json=register_data)
        resp_register_json = response_register.json()
        print('REGISTER:', resp_register_json)
        print('='*60)
        # LOGIN
        login_url = f'{cls.baseurl}/nasabah/login'
        login_data = {'no_hp': cls.no_hp, 'pin': cls.pin}
        response_login = requests.post(login_url, json=login_data)
        resp_login_json = response_login.json()
        print('LOGIN:', resp_login_json)
        print('='*60)
        cls.token = resp_login_json['result']['token']
        cls.no_rekening = resp_login_json['result']['no_rekening']

    def test_tabung_rekening_dikenali(self):
        url = f'{self.baseurl}/transaksi/tabung'
        data = {'no_rekening': self.no_rekening, 'nominal': 1000}
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.post(url, json=data, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('berhasil', response.json()['remark'].lower())
        print('TABUNG DIKENALI:', response.json())
        print('='*60)

    def test_tabung_rekening_tidak_dikenali(self):
        url = f'{self.baseurl}/transaksi/tabung'
        data = {'no_rekening': 'rekening_tidak_dikenali', 'nominal': 1000}
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.post(url, json=data, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('tidak dikenali', response.json()['remark'].lower())
        print('TABUNG TDK DIKENALI:', response.json())
        print('='*60)

    def test_tarik_saldo_kurang(self):
        url = f'{self.baseurl}/transaksi/tarik'
        data = {'no_rekening': self.no_rekening, 'nominal': 1000000}  # Asumsi saldo cukup
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.post(url, json=data, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('saldo anda kurang', response.json()['remark'].lower())
        print('TARIK SALDO KURANG:', response.json())
        print('='*60)

    def test_tarik_saldo_lebih(self):
        url = f'{self.baseurl}/transaksi/tarik'
        data = {'no_rekening': self.no_rekening, 'nominal': 500}  # Asumsi saldo tidak cukup
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.post(url, json=data, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('berhasil', response.json()['remark'].lower())
        print('TARIK SALDO LEBIH:', response.json())
        print('='*60)

if __name__ == '__main__':
    unittest.main()
