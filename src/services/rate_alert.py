import asyncio
import datetime
from datetime import UTC

import aiohttp

from constants.rate_alert import (
    GATE_SYMBOLS_LIST,
    BINANCE_SYMBOLS_LIST,
    BYBIT_SYMBOLS_LIST,
    KUCOIN_SYMBOLS_LIST,
    BTC_AMOUNT,
    COINS,
    INITIAL_RATES,
)

from configs.config import crypto_api_settings


async def get_initial_data():
    result = {}
    async with aiohttp.ClientSession() as session:
        # команда для отправки запроса к API
        url = 'https://api.gateio.ws/api/v4/spot/tickers'
        # задаем параметры передачи запроса
        params = {}
        async with session.get(url, params=params) as response:
            pairs_json = await response.json()
        for pair in pairs_json:
            symbol = pair.get('currency_pair').replace('_', '')
            if symbol in GATE_SYMBOLS_LIST:
                if symbol.endswith('BTC'):
                    new_symbol = f'BTC{symbol.replace("BTC", "")}'
                    result[new_symbol] = 1 / float(pair.get('last'))
                else:
                    result[symbol] = float(pair.get('last'))
    result['BTCSOL'] = result.get('BTCUSDT') / result.get('SOLUSDT')
    result['BTCRUB'] = result.get('BTCUSDT') / result.get('RUBYUSDT') / 10
    del result['SOLUSDT']
    del result['RUBYUSDT']

    return result


async def get_binance_data():
    result = {}
    async with aiohttp.ClientSession() as session:
        # команда для отправки запроса к API
        url = 'https://api3.binance.com/api/v3/ticker/price'
        # задаем параметры передачи запроса
        params = {}
        async with session.get(url, params=params) as response:
            pairs_json = await response.json()
        for pair in pairs_json:
            symbol = pair.get('symbol')
            if symbol in BINANCE_SYMBOLS_LIST:
                if symbol.endswith('BTC'):
                    new_symbol = f'BTC{symbol.replace("BTC", "")}'
                    result[f'BINANCE-{new_symbol}'] = 1 / float(pair.get('price'))
                else:
                    result[f'BINANCE-{symbol}'] = float(pair.get('price'))

    return result


async def get_coinmarketcap_data():
    result = {}
    async with aiohttp.ClientSession() as session:
        # команда для отправки запроса к API
        url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
        # задаем параметры передачи запроса
        params = {
            'symbol': 'BTC,USDT,ETH,XMR,SOL,DOGE',
            'convert': 'RUB'
        }
        headers = {
            'Accept': 'application/json',
            'X-CMC_PRO_API_KEY': crypto_api_settings.X_CMC_PRO_API_KEY
        }
        session.headers.update(headers)
        async with session.get(url, params=params) as response:
            pairs_json = await response.json()
        usdt_rub = pairs_json.get('data').get('USDT')[0].get('quote').get('RUB').get('price')
        etc_rub = pairs_json.get('data').get('ETH')[0].get('quote').get('RUB').get('price')
        xmr_rub = pairs_json.get('data').get('XMR')[0].get('quote').get('RUB').get('price')
        sol_rub = pairs_json.get('data').get('SOL')[0].get('quote').get('RUB').get('price')
        btc_rub = pairs_json.get('data').get('BTC')[0].get('quote').get('RUB').get('price')
        doge_rub = pairs_json.get('data').get('DOGE')[0].get('quote').get('RUB').get('price')

        result['CMC-BTCUSDT'] = btc_rub / usdt_rub
        result['CMC-BTCETH'] = btc_rub / etc_rub
        result['CMC-BTCXMR'] = btc_rub / xmr_rub
        result['CMC-BTCSOL'] = btc_rub / sol_rub
        result['CMC-BTCRUB'] = btc_rub
        result['CMC-BTCDOGE'] = btc_rub / doge_rub

    return result


async def get_bybit_data():
    result = {}
    async with aiohttp.ClientSession() as session:
        # команда для отправки запроса к API
        url = 'https://api.bybit.com/spot/v3/public/quote/ticker/price'
        # задаем параметры передачи запроса
        params = {}
        async with session.get(url, params=params) as response:
            pairs_json = await response.json()
        for pair in pairs_json.get('result').get('list'):
            symbol = pair.get('symbol')
            if symbol in BYBIT_SYMBOLS_LIST:
                if symbol.endswith('BTC'):
                    new_symbol = f'BTC{symbol.replace("BTC", "")}'
                    result[f'BYBIT-{new_symbol}'] = 1 / float(pair.get('price'))
                else:
                    result[f'BYBIT-{symbol}'] = float(pair.get('price'))
    result['BYBIT-BTCDOGE'] = result.get('BYBIT-BTCUSDT') / result.get('BYBIT-DOGEUSDT')
    result['BYBIT-BTCRUB'] = result.get('BYBIT-BTCUSDT') / result.get('BYBIT-RUBYUSDT') / 10
    del result['BYBIT-DOGEUSDT']
    del result['BYBIT-RUBYUSDT']

    return result


async def get_gate_data():
    result = {}
    async with aiohttp.ClientSession() as session:
        # команда для отправки запроса к API
        url = 'https://api.gateio.ws/api/v4/spot/tickers'
        # задаем параметры передачи запроса
        params = {}
        async with session.get(url, params=params) as response:
            pairs_json = await response.json()
        for pair in pairs_json:
            symbol = pair.get('currency_pair').replace('_', '')
            if symbol in GATE_SYMBOLS_LIST:
                if symbol.endswith('BTC'):
                    new_symbol = f'BTC{symbol.replace("BTC", "")}'
                    result[f'GATE-{new_symbol}'] = 1 / float(pair.get('last'))
                else:
                    result[f'GATE-{symbol}'] = float(pair.get('last'))
    result['GATE-BTCSOL'] = result.get('GATE-BTCUSDT') / result.get('GATE-SOLUSDT')
    result['GATE-BTCRUB'] = result.get('GATE-BTCUSDT') / result.get('GATE-RUBYUSDT') / 10
    del result['GATE-SOLUSDT']
    del result['GATE-RUBYUSDT']

    return result


async def get_kucoin_data():
    result = {}
    async with aiohttp.ClientSession() as session:
        # команда для отправки запроса к API
        url = 'https://api.kucoin.com/api/v1/market/allTickers'
        # задаем параметры передачи запроса
        params = {}
        async with session.get(url, params=params) as response:
            pairs_json = await response.json()
        for pair in pairs_json.get('data').get('ticker'):
            symbol = pair.get('symbol').replace('-', '')
            if symbol in KUCOIN_SYMBOLS_LIST:
                if symbol.endswith('BTC'):
                    new_symbol = f'BTC{symbol.replace("BTC", "")}'
                    result[f'KUCOIN-{new_symbol}'] = 1 / float(pair.get('last'))
                else:
                    result[f'KUCOIN-{symbol}'] = float(pair.get('last'))
    result['KUCOIN-BTCSOL'] = result.get('KUCOIN-BTCUSDT') / result.get('KUCOIN-SOLUSDT')
    del result['KUCOIN-SOLUSDT']

    return result


async def retry_task(task_func, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = await asyncio.create_task(task_func)
            return result
        except Exception as e:
            print(f"Task {task_func.__name__} failed on attempt {attempt + 1}: {e}")
            await asyncio.sleep(1)


async def main():
    try:
        tasks = await asyncio.gather(
            retry_task(get_binance_data()),
            retry_task(get_coinmarketcap_data()),
            retry_task(get_bybit_data()),
            retry_task(get_gate_data()),
            retry_task(get_kucoin_data())
        )
    except Exception as e:
        print(f'Exception: {e}')
    return tuple(tasks)


async def get_new_data():
    new_data = {}
    binance_data, cmc_data, bybit_data, gate_data, kucoin_data = await main()
    data = binance_data
    data.update(cmc_data)
    data.update(bybit_data)
    data.update(gate_data)
    data.update(kucoin_data)
    for key, value in data.items():
        pair = key.split('-')[1]
        rate = value / INITIAL_RATES[pair]
        if rate >= 1.0003:
            new_data[key] = {
                'price': value,
                'rate': rate,
                'date': datetime.datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            }
    return new_data


async def get_final_data():
    new_data = await get_new_data()
    max_rate_pair = max(new_data, key=lambda x: new_data[x]['rate'])
    max_rate = new_data[max_rate_pair]['rate']
    currency_pair = max_rate_pair.split('-')[1]
    min_rate_pair = None
    min_rate = float('inf')
    for pair, info in new_data.items():
        if currency_pair in pair:
            if info['rate'] < min_rate:
                min_rate = info['rate']
                min_rate_pair = pair

    final_data = {
        'key_json':  {
            'title': f'{currency_pair[:3]}/{currency_pair[3:]} Rate Alert',
            'kash': [
                {
                    'price': round(INITIAL_RATES[currency_pair], 2),
                    'minmax': [
                        {
                            'min_price': round(new_data[min_rate_pair]['price'], 2),
                            'max_price': round(new_data[max_rate_pair]['price'], 2),
                        }
                    ],
                }
            ],
            'difference': round(((max_rate - 1) * 100), 2),
            'total_amount': round(BTC_AMOUNT * new_data[max_rate_pair]['price'], 2),
            'coins': COINS,
            'date': new_data[max_rate_pair]['date']
        }
    }
    return final_data
