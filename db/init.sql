CREATE SEQUENCE seq_account_no START 1;

CREATE TABLE IF NOT EXISTS nasabah (
    no_rekening VARCHAR(14) PRIMARY KEY,
    nama VARCHAR(60) NOT NULL,
    nik VARCHAR(16) NOT NULL,
    no_hp VARCHAR(15) NOT NULL,
    pin VARCHAR(72) NOT NULL,
    saldo int NOT NULL DEFAULT 0
);

CREATE TYPE trx_type AS ENUM ('D', 'C', 'T');

CREATE TABLE IF NOT EXISTS transaksi (
    id_transaksi SERIAL PRIMARY KEY,
    no_rekening VARCHAR(14) NOT NULL,
    jenis_transaksi trx_type NOT NULL,
    nominal int NOT NULL,
    waktu TIMESTAMP NOT NULL,
    FOREIGN KEY (no_rekening) REFERENCES nasabah (no_rekening)
);