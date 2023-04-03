import json
import requests
import sys


def check_for_market_inefficiency(event, book1, book2, market_type):
    market1 = next((m1 for m1 in book1.get('markets', []) if m1['key'] == market_type), None)
    market2 = next((m2 for m2 in book2.get('markets', []) if m2['key'] == market_type), None)
    # Performing simple arbitrage for now, meaning that the odds are only analyzed if the event has 2 outcomes (typically a win and loss)
    if (market1 is not None and len(market1.get('outcomes', [])) == 2) and (market2 is not None and len(market2.get('outcomes', [])) == 2):
        for o1 in market1['outcomes']:
            for o2 in market2['outcomes']:
                if (
                    # Not betting on same outcome in different books
                    (o1['name'] != o2['name'])
                    # H2H market won't have point fields, but the other markets will and the point fields need to match.
                    # For instance, Team A's spread is +1.5 on one sportsbook and Team B's spread is -1.5 on the other.
                    and ((o1.get('point') is None and o2.get('point') is None) or o1.get('point') == -(o2.get('point')))
                    # Arbitrage condition: the return on the plus money needs to be greater than the inverse
                    # return on the minus money.
                    and (o1.get('price') + o2.get('price') > 0)
                ):
                    event_type = event['sport_title']
                    home = event['home_team']
                    away = event['away_team']
                    bookTitle1 = book1['title']
                    bookTitle2 = book2['title']
                    name1 = o1['name']
                    name2 = o2['name']
                    price1 = o1['price']
                    price2 = o2['price']
                    point1 = o1.get('point', '')
                    point2 = o2.get('point', '')
                    print('\n-------------------------------------------------')
                    print(f'Discovered arbitrage opportunity for the {event_type} event between the {home} and {away}:')
                    print(f'{bookTitle1} {market_type} --> {name1} {price1} {point1}')
                    print(f'{bookTitle2} {market_type} --> {name2} {price2} {point2}')
                    print('-------------------------------------------------\n')
                    

def check_response(response, resource):
    if response.status_code != 200:
        print(f'\n\n[ERROR] Failed to get {resource}:\nstatus code {response.status_code}\nresponse body {response.text}')
        sys.exit()

def get_active_sport_keys(config):
    sports_response = requests.get(
        'https://api.the-odds-api.com/v4/sports', 
        params={
            'api_key': config['apiKey']
        }
    )
    check_response(sports_response, 'sports')
    # Sports with outrights don't offer the markets required for arbitrage
    return [sport['key'] for sport in sports_response.json() if not sport['has_outrights']]

def get_config():
    data = {}
    with open('config.json') as f:
        data = json.load(f)
    return data

def process_event_odds_matrix(event):
    for book1 in event.get('bookmakers', []):
        for book2 in event.get('bookmakers', []):
            # Odds will be an exact match when comparing sportsbook to itself, no opportunity for arbitrage
            if book1['key'] != book2['key']:
                check_for_market_inefficiency(event, book1, book2, 'h2h')
                check_for_market_inefficiency(event, book1, book2, 'spreads')
                check_for_market_inefficiency(event, book1, book2, 'totals')

def scan_for_arbitrage_opportunities(config, sport):
    odds_response = requests.get(
        f'https://api.the-odds-api.com/v4/sports/{sport}/odds',
        params={
            'api_key': config['apiKey'],
            'regions': config['regions'],
            'markets': config['markets'],
            'oddsFormat': config['oddsFormat'],
            'dateFormat': config['dateFormat'],
            'bookmakers': config['bookmakers']
        }
    )
    check_response(odds_response, 'odds')
    odds_json = odds_response.json()
    for event in odds_json:
        process_event_odds_matrix(event)

def detect_arbitrage():
    print('\nINITIATING ARBITRAGE DETECTION...')
    config_data = get_config()
    sport_keys = get_active_sport_keys(config_data)
    print(f'Found {len(sport_keys)} sports listed as active.\n')
    for sport in sport_keys:
        print(f'Scanning odds packages for sport: {sport}')
        scan_for_arbitrage_opportunities(config_data, sport)

if __name__ == '__main__':
    detect_arbitrage()
