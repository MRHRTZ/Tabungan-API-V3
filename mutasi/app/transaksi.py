from model.transaksi import CreateTransaction, Transaction 
from datastore.transaksi import TransaksiData
from script.utils import generateLog, LogLevel, setSuccess, setError, setFailed, encrypt_string, get_random, RandomType, getCurrentTime

class TransaksiApp:
    def __init__(self):
        self.transaksi_data = TransaksiData()

    def mutasi(self, data):
        try:
            response = setSuccess("", "Berhasil membuat mutasi")
            
            trx = {}
            trx['no_rekening'] = data.no_rekening
            trx['jenis_transaksi'] = data.jenis_transaksi
            trx['nominal'] = data.nominal
            trx['waktu'] = data.tanggal_transaksi

            transaction = CreateTransaction(**trx)
            data_mutasi = self.transaksi_data.create_transaction(transaction)

            response['result'] = data_mutasi

            return response

        except Exception as e:
            
            return setError("(99) Gagal mendapatkan mutasi!")
        # --
    # --