CREATE TABLE agg_pl (
    account_uuid UUID,
    date DATE,
    pl MONEY,
    PRIMARY KEY (account_uuid, date),
    FOREIGN KEY (account_uuid)
        REFERENCES account (uuid),
)