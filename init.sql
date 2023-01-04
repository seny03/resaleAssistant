CREATE TABLE IF NOT EXISTS "OFFERS" (
  "link" text(128) PRIMARY KEY NOT NULL,
  "description" text(2048),
  "buy_price" real(128) NOT NULL,
  "sell_price" real(128) NOT NULL,
  "desired_price" real(128)
) WITHOUT ROWID;
