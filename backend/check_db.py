import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

async def check():
    engine = create_async_engine('postgresql+asyncpg://postgres.lkwhqaiqzdutsxgeggko:AgriShield%40svh1@aws-0-ap-northeast-1.pooler.supabase.com:5432/postgres')
    async with engine.begin() as conn:
        print('User count:', (await conn.execute(text('SELECT COUNT(*) FROM users'))).scalar())
        print('Farm count:', (await conn.execute(text('SELECT COUNT(*) FROM farms'))).scalar())
        print('Policy count:', (await conn.execute(text('SELECT COUNT(*) FROM insurance_policies'))).scalar())
        print('Claim count:', (await conn.execute(text('SELECT COUNT(*) FROM claims'))).scalar())

if __name__ == '__main__':
    asyncio.run(check())
