import asyncio
import asyncpg

async def main():
    conn = await asyncpg.connect("postgresql://postgres.lkwhqaiqzdutsxgeggko:AgriShield%40svh1@aws-0-ap-northeast-1.pooler.supabase.com:5432/postgres")
    await conn.execute("DROP TABLE IF EXISTS claims, farms, users, alembic_version CASCADE;")
    await conn.close()

if __name__ == "__main__":
    asyncio.run(main())
