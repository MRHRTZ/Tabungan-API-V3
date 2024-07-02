from model.nasabah import Nasabah 
from datastore.nasabah import NasabahData 
from script.utils import (
    generateLog, LogLevel, setSuccess, 
    setError, setFailed, 
    encrypt_string, verify_encrypt,
    encode_jwt,
    get_random, RandomType
)

class NasabahApp:
    def __init__(self):
        self.nasabah_data = NasabahData()

    def daftar_nasabah(self, data):
        try:
            response = setSuccess("", "Berhasil mendaftarkan nasabah!")
            
            if data.nama in [None, "", 0]:
                response = setFailed('field nama masih kosong!')
                return response
            elif data.nik in [None, "", 0]:
                response = setFailed('field nik masih kosong!')
                return response
            elif data.no_hp in [None, "", 0]:
                response = setFailed('field no_hp masih kosong!')
                return response
            
            count_nik = self.nasabah_data.get_nik_count(data.nik)
            if count_nik != 0:
                response = setFailed('(999) NIK telah terdaftar.')
                return response

            count_phone = self.nasabah_data.get_phone_count(data.no_hp)
            if count_phone != 0:
                response = setFailed('(999) No Hp telah terdaftar.')
                return response

            next_acc_no = self.nasabah_data.get_next_account_no()
            if not next_acc_no:
                response = setFailed('(999) Gagal mendapatkan no rekening.')
                return response

            account_no = int(get_random(RandomType.INTEGER, 5)) + int(next_acc_no)
            account_no = get_random(RandomType.INTEGER, 4) + str(account_no).zfill(10)

            newNasabah = {}
            newNasabah['no_rekening'] = account_no
            newNasabah['nama'] = data.nama.upper()
            newNasabah['nik'] = data.nik
            newNasabah['no_hp'] = data.no_hp
            newNasabah['pin'] = encrypt_string(data.pin)

            nasabah = Nasabah(**newNasabah)
            self.nasabah_data.create_nasabah(nasabah)

            response['result'] = {'account_no':account_no}

            return response

        except Exception as e:
            return setError("(99) Gagal mendaftar!")
        # --
    # --
    
    def login(self, data):
        try:
            response = setSuccess("", "Berhasil login!")
            
            if data.no_hp in [None, "", 0]:
                response = setFailed('field no_hp masih kosong!')
                return response
            elif data.pin in [None, "", 0]:
                response = setFailed('field pin masih kosong!')
                return response
            
            nasabah = self.nasabah_data.get_nasabah_by_phone(data.no_hp)
            if not nasabah:
                response = setFailed('(999) Nasabah tidak terdaftar.')
                return response

            verify_pin = verify_encrypt(data.pin, nasabah['pin'])
            if not verify_pin:
                response = setFailed('(999) PIN Salah.')
                return response

            token = encode_jwt({
                'no_rekening': nasabah['no_rekening'],
                'pin': nasabah['pin']
            })
            response['result'] = {
                'no_rekening': nasabah['no_rekening'],
                'token': token
            }

            return response

        except Exception as e:
            return setError("(99) Gagal mendaftar!")
        # --
    # --