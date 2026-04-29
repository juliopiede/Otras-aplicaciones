from pathlib import Path
import os

import asyncpg
import asyncio

MIGRATIONS_DIR = Path(__file__).resolve().parents[1] / "migrations"
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://bittacora:bittacora@localhost:5432/bittacora")


async def main() -> None:
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        for sql_file in sorted(MIGRATIONS_DIR.glob("*.sql")):
            sql = sql_file.read_text(encoding="utf-8")
            await conn.execute(sql)
            print(f"Applied {sql_file.name}")
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(main())
