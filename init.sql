CREATE TABLE IF NOT EXISTS "OFFERS" (
  "id" integer(8) PRIMARY KEY NOT NULL,
  "description" text(2048) NOT NULL,
  "cur_price" real(8) NOT NULL,
  "desired_price" real(8)
) WITHOUT ROWID;
