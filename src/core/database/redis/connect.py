import asyncio
from redis.asyncio import Redis


sessions = Redis(host='localhost', port=6379, db=0)
cart = Redis(host='localhost', port=6379, db=1)
check = Redis(host='localhost', port=6379, db=2)
