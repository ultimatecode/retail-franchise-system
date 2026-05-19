from sqlalchemy import create_engine, text
from datetime import datetime, timedelta

engine = create_engine('mysql+pymysql://amb:86fHPpcSGxSHnfri@192.168.2.88:3306/amb')
db = engine.connect()

now = datetime.now()
today_start = int(now.replace(hour=0, minute=0, second=0, microsecond=0).timestamp())
yesterday_start = int((now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)).timestamp())

print(f'Today start: {today_start}')
print(f'Yesterday start: {yesterday_start}')

# 查询昨天销售额
query = text('SELECT COALESCE(SUM(totalmoney), 0) as sales FROM order_user WHERE type = 1 AND status >= 9 AND reg_date >= :ys AND reg_date < :ts')
result = db.execute(query, {'ys': yesterday_start, 'ts': today_start}).first()
print(f'Yesterday result: {result}')
if result:
    print(f'Yesterday sales: {result[0]}')

db.close()
