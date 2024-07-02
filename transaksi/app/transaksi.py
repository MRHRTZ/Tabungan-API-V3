from typing_extensions import Annotated
from fastapi import Depends
from model.nasabah import Nasabah 
from model.transaksi import CreateTransaction, Transaction 
from datastore.nasabah import NasabahData
from datastore.transaksi import TransaksiData
from script.utils import (
    generateLog, LogLevel, 
    setSuccess, setError, setFailed, 
    encrypt_string, 
    get_random, RandomType, 
    getCurrentTime,
    svc_mutasi
)

class TransaksiApp:
    def __init__(self):
        self.nasabah_data = NasabahData()
        self.transaksi_data = TransaksiData()

    def tabung(self, data):
        try:
            response = setSuccess("", "Berhasil menambahkan tabungan")
            
            if data.no_rekening in [None, "", 0]:
                response = setFailed('field no_rekening masih kosong!')
                return response
            
            if data.nominal in [None, "", 0]:
                response = setFailed('field nominal masih kosong!')
                return response

            count_acc_no = self.nasabah_data.get_account_no_count(data.no_rekening)
            if count_acc_no == 0:
                response = setFailed('(999) No Rekening tidak dikenali.')
                return response

            self.nasabah_data.save_money(data.no_rekening, data.nominal)

            saldo_nasabah = self.nasabah_data.get_saldo(data.no_rekening)
            if saldo_nasabah == False and (saldo_nasabah != 0):
                response = setFailed('(999) Gagal mengambil data saldo.')
                return response

            response['result'] = {'saldo': saldo_nasabah}

            transactionObj = {}
            transactionObj['no_rekening'] = data.no_rekening
            transactionObj['jenis_transaksi'] = 'C'
            transactionObj['nominal'] = data.nominal
            transactionObj['tanggal_transaksi'] = getCurrentTime()
            transaction = CreateTransaction(**transactionObj)

            resp_api = svc_mutasi('/api/v1/mutasi', transaction.json())
            if not resp_api or resp_api.get('status', 400) != 200:
                response = setFailed('(990) Gagal membuat mutasi')

            return response
        except Exception as e:
            return setError("(99) Gagal menambah tabungan!")
        # --

    def tarik(self, data):
        try:
            response = setSuccess("", "Berhasil tarik tabungan")
            
            if data.no_rekening in [None, "", 0]:
                response = setFailed('field no_rekening masih kosong!')
                return response
            
            if data.nominal in [None, "", 0]:
                response = setFailed('field nominal masih kosong!')
                return response

            count_acc_no = self.nasabah_data.get_account_no_count(data.no_rekening)
            if count_acc_no == 0:
                response = setFailed('(999) No Rekening tidak dikenali.')
                return response
            
            saldo_nasabah = self.nasabah_data.get_saldo(data.no_rekening)
            if saldo_nasabah < data.nominal:
                response = setFailed('(999) Saldo anda kurang.')
                return response

            self.nasabah_data.withdraw(data.no_rekening, data.nominal)

            saldo_nasabah = self.nasabah_data.get_saldo(data.no_rekening)
            if saldo_nasabah == False and (saldo_nasabah != 0):
                response = setFailed('(999) Gagal mengambil data saldo.')
                return response

            response['result'] = {'saldo': saldo_nasabah}

            transactionObj = {}
            transactionObj['no_rekening'] = data.no_rekening
            transactionObj['jenis_transaksi'] = 'D'
            transactionObj['nominal'] = data.nominal
            transactionObj['tanggal_transaksi'] = getCurrentTime()
            transaction = CreateTransaction(**transactionObj)

            resp_api = svc_mutasi('/api/v1/mutasi', transaction.json())
            if not resp_api or resp_api.get('status', 400) != 200:
                response = setFailed('(990) Gagal membuat mutasi')

            return response
        except Exception as e:
            return setError("(99) Gagal tarik tabungan!")
        # --
    # --
# --