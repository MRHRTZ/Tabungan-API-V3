import sys, traceback

from . import engine
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from model.nasabah import CreateNasabah, Nasabah
from script.utils import generateLog, LogLevel, generate_insert_sql_from_model, generate_update_sql

class NasabahData:
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.table_name = "nasabah"

    def get_next_account_no(self):
        no_rekening = ""
        try:
            sSQL = "SELECT nextval('seq_account_no') as no_rekening"
            no_rekening = self.session.execute(text(sSQL)).first()._asdict().get('no_rekening')

            self.session.commit()
            return no_rekening
        except Exception as e:
            self.session.rollback()
            generateLog(LogLevel.ERROR, "Repo Error", traceback.format_exc())

            return False

    def create_nasabah(self, nasabah: Nasabah):
        try:
            sSQL, values = generate_insert_sql_from_model(self.table_name, nasabah)
            sSQL = sSQL % values

            self.session.execute(text(sSQL))

            self.session.commit()
            self.session.close()

        except Exception as e:
            self.session.rollback()
            self.session.close()
            generateLog(LogLevel.ERROR, "Repo Error", traceback.format_exc())

            return False

    def get_phone_count(self, phone: str):
        try:
            sSQL = "select count(*) from {0} n where n.no_hp = {1!r}".format(self.table_name, phone)
            count = self.session.execute(text(sSQL)).first()._asdict().get('count')
            count = int(count)

            self.session.commit()
            self.session.close()

            return count
        except Exception as e:
            self.session.rollback()
            self.session.close()
            generateLog(LogLevel.ERROR, "Repo Error", traceback.format_exc())

            return False

    def get_nik_count(self, nik: str):
        try:
            sSQL = "select count(*) from {0} n where n.nik = {1!r}".format(self.table_name, nik)
            count = self.session.execute(text(sSQL)).first()._asdict().get('count')
            count = int(count)

            self.session.commit()
            self.session.close()

            return count
        except Exception as e:
            self.session.rollback()
            self.session.close()
            generateLog(LogLevel.ERROR, "Repo Error", traceback.format_exc())

            return False

    def get_account_no_count(self, no_rekening: str):
        try:
            sSQL = "select count(*) from {0} n where n.no_rekening = {1!r}".format(self.table_name, no_rekening)
            count = self.session.execute(text(sSQL)).first()._asdict().get('count')
            count = int(count)

            self.session.commit()
            self.session.close()

            return count
        except Exception as e:
            self.session.rollback()
            self.session.close()
            generateLog(LogLevel.ERROR, "Repo Error", traceback.format_exc())

            return False

    def get_nasabah(self, no_rekening: str):
        try:
            sSQL = "select * from {0} n where n.no_rekening = {1!r}".format(self.table_name, no_rekening)
            result = self.session.execute(text(sSQL)).first()._asdict()

            self.session.commit()
            self.session.close()

            return result
        except Exception as e:
            self.session.rollback()
            self.session.close()
            generateLog(LogLevel.ERROR, "Repo Error", traceback.format_exc())

            return False
    
    def get_nasabah_by_phone(self, phone: str):
        try:
            sSQL = "select * from {0} n where n.no_hp = {1!r}".format(self.table_name, phone)
            result = self.session.execute(text(sSQL)).first()._asdict()

            self.session.commit()
            self.session.close()

            return result
        except Exception as e:
            self.session.rollback()
            self.session.close()
            generateLog(LogLevel.ERROR, "Repo Error", traceback.format_exc())

            return False
    
    def get_saldo(self, no_rekening: str):
        try:
            sSQL = "select saldo from {0} n where n.no_rekening = {1!r}".format(self.table_name, no_rekening)
            saldo = self.session.execute(text(sSQL)).first()._asdict().get('saldo')
            saldo = int(saldo)

            self.session.commit()
            self.session.close()

            return saldo
        except Exception as e:
            self.session.rollback()
            self.session.close()
            generateLog(LogLevel.ERROR, "Repo Error", traceback.format_exc())

            return False

    def save_money(self, no_rekening: str, amount: int):
        try:
            condition = "no_rekening = {0!r}".format(no_rekening)
            sSQL, values = generate_update_sql(self.table_name, {'saldo': 'saldo+' + str(amount)}, condition)
            sSQL = sSQL % values

            self.session.execute(text(sSQL))

            self.session.commit()
            self.session.close()
        except Exception as e:
            self.session.rollback()
            self.session.close()
            generateLog(LogLevel.ERROR, "Repo Error", traceback.format_exc())

            return False

    def withdraw(self, no_rekening: str, amount: int):
        try:
            condition = "no_rekening = {0!r}".format(no_rekening)
            sSQL, values = generate_update_sql(self.table_name, {'saldo': 'saldo-' + str(amount)}, condition)
            sSQL = sSQL % values

            self.session.execute(text(sSQL))

            self.session.commit()
            self.session.close()
        except Exception as e:
            self.session.rollback()
            self.session.close()
            generateLog(LogLevel.ERROR, "Repo Error", traceback.format_exc())

            return False