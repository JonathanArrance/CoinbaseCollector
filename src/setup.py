import psycopg2
import logging
import settings

# Configure logging
logging.basicConfig(level=logging.INFO)

def init_db():
    try:
        # 🔹 Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname=settings.PGSQL_DB,
            user=settings.PGSQL_USER,
            password=settings.PGSQL_PASSWORD,
            host=settings.PGSQL_HOST,
            port=settings.PGSQL_PORT
        )
        cursor = conn.cursor()

        '''
        # 🔹 Create tables
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS validCoins (
            ID SERIAL PRIMARY KEY,
            CoinName TEXT NOT NULL,
            CoinAbv TEXT UNIQUE NOT NULL,
            CoinTicker TEXT
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cryptoHistory (
            ID SERIAL PRIMARY KEY,
            coin TEXT NOT NULL,
            timestamp TIMESTAMPTZ NOT NULL,
            price NUMERIC
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS portfolios (
            ID SERIAL PRIMARY KEY,
            PortfolioName TEXT UNIQUE NOT NULL
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS portfolioCoins (
            ID SERIAL PRIMARY KEY,
            CoinName TEXT NOT NULL,
            PortfolioName TEXT NOT NULL,
            UNIQUE (CoinName, PortfolioName)
        );
        """)
        '''


        # 🔹 Insert seed data
        cursor.execute("""
        INSERT INTO "validcoins" ("coinname", "coinabv", "cointicker")
        VALUES ('Bitcoin','btc','btc-usd')
        ON CONFLICT ("coinabv") DO NOTHING;
        """)
        cursor.execute("""
        INSERT INTO "validcoins" ("coinname", "coinabv", "cointicker")
        VALUES ('Ethereum','eth','eth-usd')
        ON CONFLICT ("coinabv") DO NOTHING;
        """)
        cursor.execute("""
        INSERT INTO "validcoins" ("coinname", "coinabv", "cointicker")
        VALUES ('Dogecoin','doge','doge-usd')
        ON CONFLICT ("coinabv") DO NOTHING;
        """)
        cursor.execute("""
        INSERT INTO "validcoins" ("coinname", "coinabv", "cointicker")
        VALUES ('Chainlink','link','link-usd')
        ON CONFLICT ("coinabv") DO NOTHING;
        """)

        cursor.execute("""
        INSERT INTO "portfolios" ("portfolioname")
        VALUES ('Default')
        ON CONFLICT ("portfolioname") DO NOTHING;
        """)

        # 🔹 Commit changes
        conn.commit()
        logging.info("Database initialized successfully ✅")

    except Exception as e:
        logging.error(f"Error initializing database: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    init_db()