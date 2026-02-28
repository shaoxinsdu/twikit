#!/usr/bin/env python3
"""
Twikit 快速启动脚本
用法:
    python run.py login          # 首次登录，保存cookies
    python run.py search <关键词>  # 搜索推文
    python run.py trend          # 获取热门趋势
    python run.py user <用户名>   # 查看用户信息
    python run.py tweet <内容>    # 发推文
    python run.py timeline       # 查看自己的时间线
"""

import asyncio
import sys
import json
from twikit import Client

COOKIES_FILE = 'cookies.json'

async def login():
    from config import USERNAME, EMAIL, PASSWORD, LANGUAGE
    client = Client(LANGUAGE)
    await client.login(
        auth_info_1=USERNAME,
        auth_info_2=EMAIL,
        password=PASSWORD
    )
    client.save_cookies(COOKIES_FILE)
    print('Login successful! Cookies saved.')
    return client

async def get_client():
    from config import LANGUAGE
    client = Client(LANGUAGE)
    try:
        client.load_cookies(COOKIES_FILE)
    except FileNotFoundError:
        print('No cookies found. Run: python run.py login')
        sys.exit(1)
    return client

async def search_tweets(query, count=20):
    client = await get_client()
    tweets = await client.search_tweet(query, 'Latest', count=count)
    for i, tweet in enumerate(tweets, 1):
        print(f'\n--- Tweet {i} ---')
        print(f'@{tweet.user.screen_name}: {tweet.text}')
        print(f'  Likes: {tweet.favorite_count} | RT: {tweet.retweet_count}')
        print(f'  ID: {tweet.id} | {tweet.created_at}')

async def get_trends():
    client = await get_client()
    trends = await client.get_trends('trending')
    for i, trend in enumerate(trends, 1):
        print(f'{i}. {trend}')

async def get_user(screen_name):
    client = await get_client()
    user = await client.get_user_by_screen_name(screen_name)
    print(f'Name: {user.name} (@{user.screen_name})')
    print(f'Bio: {user.description}')
    print(f'Followers: {user.followers_count}')
    print(f'Following: {user.following_count}')
    print(f'Tweets: {user.statuses_count}')
    print(f'\nRecent tweets:')
    tweets = await user.get_tweets('Tweets')
    for i, tweet in enumerate(tweets[:5], 1):
        print(f'  {i}. {tweet.text[:100]}')

async def post_tweet(text):
    client = await get_client()
    tweet = await client.create_tweet(text)
    print(f'Tweet posted! ID: {tweet.id}')

async def get_timeline():
    client = await get_client()
    tweets = await client.get_timeline()
    for i, tweet in enumerate(tweets[:20], 1):
        print(f'\n--- {i} ---')
        print(f'@{tweet.user.screen_name}: {tweet.text[:200]}')
        print(f'  Likes: {tweet.favorite_count} | RT: {tweet.retweet_count}')

async def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1]

    if cmd == 'login':
        await login()
    elif cmd == 'search':
        query = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else input('Search: ')
        await search_tweets(query)
    elif cmd == 'trend':
        await get_trends()
    elif cmd == 'user':
        name = sys.argv[2] if len(sys.argv) > 2 else input('Username: ')
        await get_user(name)
    elif cmd == 'tweet':
        text = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else input('Tweet: ')
        await post_tweet(text)
    elif cmd == 'timeline':
        await get_timeline()
    else:
        print(f'Unknown command: {cmd}')
        print(__doc__)

if __name__ == '__main__':
    asyncio.run(main())
