import asyncio
import datetime
from datetime import UTC
from typing import Dict, Tuple
import aiohttp

from constants.rate_alert import (
    GATE_SYMBOLS_LIST,
    BINANCE_SYMBOLS_LIST,
    BYBIT_SYMBOLS_LIST,
    KUCOIN_SYMBOLS_LIST,
    BTC_AMOUNT,
    COINS,
)
from configs.config import crypto_api_settings
from constants.email_contexts import USER_EMAIL
from crud.initial_rate import crud_initial_rate
from crud.rate_alert import crud_rate_alert
from schemas.rate_alert import RateAlertCreate
from services.email import send_new_rate_alert_email
from services.initial_rate import create_initial_rate, update_initial_rate


async def get_initial_data() -> Dict:
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


async def get_binance_data() -> Dict:
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


async def get_coinmarketcap_data() -> Dict:
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


async def get_bybit_data() -> Dict:
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


async def get_gate_data() -> Dict:
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


async def get_kucoin_data() -> Dict:
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


async def retry_task(task_func, max_retries=3) -> Dict:
    for attempt in range(max_retries):
        try:
            result = await asyncio.create_task(task_func())
            return result
        except Exception as e:
            print(f"Task {task_func.__name__} failed on attempt {attempt + 1}: {e}")
            await asyncio.sleep(5)


async def get_markets_data() -> Dict:
    result = {}
    tasks = await asyncio.gather(
        retry_task(get_binance_data),
        retry_task(get_coinmarketcap_data),
        retry_task(get_bybit_data),
        retry_task(get_gate_data),
        retry_task(get_kucoin_data)
    )
    for data in tasks:
        if data:
            result.update(data)

    return result


async def find_min_max(
        markets_data: Dict, initial_rates: Dict
) -> Dict:
    result = {}
    min_rate = float('inf')
    min_rate_pair = ''
    max_rate = -float('inf')
    max_rate_pair = ''
    target_pair = ''

    for key, value in markets_data.items():
        pair = key.split('-')[1]
        rate = value / initial_rates[pair]

        if rate >= 1.0003:
            if rate > max_rate:
                max_rate = rate
                max_rate_pair = key
                target_pair = pair
            stored_pair = await crud_initial_rate.get_by_name(pair)
            if stored_pair.value < value:
                await update_initial_rate(
                    pair, markets_data.get(key)
                )

    for key, value in markets_data.items():
        pair = key.split('-')[1]
        if pair == target_pair:
            rate = value / initial_rates[pair]
            if rate < min_rate:
                min_rate = rate
                min_rate_pair = key

    if max_rate_pair:
        result = {
            'min_price': markets_data.get(min_rate_pair),
            'max_price': markets_data.get(max_rate_pair),
            'max_rate': max_rate,
            'max_rate_pair': max_rate_pair,
            'price': initial_rates.get(target_pair)
        }

    return result


async def get_initial_rates() -> Dict:
    initial_data = await crud_initial_rate.get_multi()
    if initial_data:
        initial_rates = {item.name: item.value for item in initial_data}
    else:
        initial_rates = await retry_task(get_initial_data)

        for key, value in initial_rates.items():
            await create_initial_rate({
                'name': key,
                'value': value
            })

    return initial_rates


async def get_new_data() -> Dict:
    result = {}
    initial_rates = await get_initial_rates()
    markets_data = await get_markets_data()

    if markets_data:
        minmax = await find_min_max(markets_data, initial_rates)
        if minmax:
            result = {
                'max_rate_pair': minmax.get('max_rate_pair'),
                'max_rate': minmax.get('max_rate'),
                'min_price': minmax.get('min_price'),
                'max_price': minmax.get('max_price'),
                'price': minmax.get('price'),
                'date': datetime.datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            }

    return result


async def get_final_data() -> Tuple:
    new_data = await get_new_data()
    final_data = {}
    currency_pair = ''
    market_name = ''
    if new_data:
        market_name, currency_pair = new_data.get('max_rate_pair').split('-')
        final_data = {
            'key_json':  {
                'title': f'{currency_pair[:3]}/{currency_pair[3:]} Rate Alert',
                'kash': [
                    {
                        'price': new_data.get('price'),
                        'minmax': [
                            {
                                'min_price': new_data.get('min_price'),
                                'max_price': new_data.get('max_price'),
                            }
                        ],
                    }
                ],
                'difference': (new_data.get('max_rate') - 1) * 100,
                'total_amount': BTC_AMOUNT * new_data.get('max_price'),
                'coins': COINS,
                'date': new_data.get('date')
            }
        }

    return final_data, market_name, currency_pair


async def perform_scheduled_tasks() -> None:
    final_data, market_name, currency_pair = await get_final_data()
    if final_data:
        await create_rate_alert(final_data)
        await send_new_rate_alert_email(
            to_email=USER_EMAIL,
            market_name=market_name,
            total_amount=f"{final_data.get('key_json').get('total_amount')} {currency_pair[3:]}",
            difference=f"+{final_data.get('key_json').get('difference')} %",
        )


async def create_rate_alert(create_data: Dict) -> None:
    try:
        schema = RateAlertCreate(
            **create_data,
        )
        await crud_rate_alert.create(
            create_schema=schema
        )
    except Exception:
        raise
