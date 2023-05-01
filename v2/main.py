import importlib
import json
from books.Sportsbook import Sportsbook


def get_book_inst(class_name: str, url: str, username: str, password: str) -> Sportsbook:
    mod = importlib.import_module(f'books.{class_name}')
    book_class = getattr(mod, class_name)
    return book_class(url, username, password)

def get_config():
    data = {}
    with open('v2/config.json') as f:
        data = json.load(f)
    return data

def get_enabled_books(config_data: dict) -> 'list[Sportsbook]':
    books = []
    for book_config in config_data['books']:
        book_name = book_config['name']
        if book_config['enabled']:
            book = get_book_inst(book_name, book_config['url'], book_config['username'], book_config['password'])
            books.append(book)
    return books

def get_authenticated_books(config_data: dict) -> 'list[Sportsbook]':
    enabled_books = get_enabled_books(config_data)
    books = []
    for book in enabled_books:
        print(f'Logging into {book.name}...')
        login_success = book.login()
        if login_success:
            books.append(book)
            print(f'Successfully logged into {book.name}.\n')
        else:
            book.quit_session()
            print(f'Failed to log into {book.name}! Skipping it in arbitrage detection.\n')
    return books

def compare_odds_data(book1: Sportsbook, book2: Sportsbook, sport: str):
    odds1 = book1.get_moneyline_odds(sport)
    odds2 = book2.get_moneyline_odds(sport)
    for team in odds1.keys():
        odds_obj = odds1[team]
        opponent = odds_obj['opponent']
        # Arbitrage opportunity possible if plus money for team A on book A is greater than
        # inverse minus money for team B on book B.
        if opponent in odds2 and odds_obj['odds'] + odds2[opponent]['odds'] > 0:
            price1 = odds_obj['odds']
            price2 = odds2[opponent]['odds']
            current_plus_money = price1 > 0
            minus_odds = price1 if not current_plus_money else price2
            # If odds are +150 and -130, bet 1 unit on plus money for every 1.3 units on minus money
            # Currently betting $0.50 (minimum possible), but position size should eventually be calculated as percentage of balance
            plus_bet = 0.5
            minus_bet = 0.5 * (abs(minus_odds) / 10)
            bet1 = plus_bet if current_plus_money else minus_bet
            bet2 = minus_bet if current_plus_money else plus_bet
            book1_placed = book1.place_moneyline_bet(team, opponent, price1, bet1)
            book2_placed = book2.place_moneyline_bet(opponent, team, price2, bet2)
            print('\n[SUCCESS] ---------------------------------------')
            print(f'Discovered arbitrage opportunity for the event between the {team} and {opponent}:')
            print(f'{book1.name} --> {team} {price1} (betting ${bet1:.2f})')
            print(f'{book2.name} --> {opponent} {price2} (betting ${bet2:.2f})')
            if not book1_placed:
                print(f'\nFailed to place bet for ${book1.name}! It\'s likely that the odds moved.')
            elif not book2_placed:
                print(f'\nFailed to place bet for ${book2.name}! It\'s likely that the odds moved.')
            else:
                print(f'\nSuccessfully placed bet!')
            print('-------------------------------------------------\n')

def detect_arbitrage():
    print('\nINITIATING ARBITRAGE DETECTION...\n')
    config_data = get_config()
    books = get_authenticated_books(config_data)
    for sport in config_data['sports']:
        print(f'\nAnalyzing {sport} odds...')
        for i, book_i in enumerate(books):
            for j, book_j in enumerate(books):
                # No use comparing book to itself
                if i != j:
                    compare_odds_data(book_i, book_j, sport)
    # Spin down drivers for books
    for book in books:
        book.quit_session()

if __name__ == '__main__':
    detect_arbitrage()
