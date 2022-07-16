import typer, random
from card import Card
from deck import Deck
from player import Player
from rich.console import Console
from rich.table import Table

colors = ['red', 'yellow', 'green', 'blue', 'purple', 'black']


all_cards = []

for i in range(0,5):
            for color in colors:
                all_cards.append(Card(i,color))
            
parade = Deck(all_cards)


console = Console()

app = typer.Typer()

def show_cards(cards: list, heading: str) -> None:
    """Creates the data for the header and row of the table"""
    
    header = [f'Card: {i+1}' for i in range(len(cards))]
    row = [f'[{card.color}]{str(card.value)}[/{card.color}]' for card in cards]
    table = Table(*header, title=f'{heading}', style="bold")
    table.add_row(*row)
    console.print(table)


@app.command()
def new_game() -> None:
    global hand, board, players, finished
    num_players = console.input('    Cuántos jugadores quieres que haya?  ')
    parade.shuffle_deck()

    finished = [False] * int(num_players)
    players = []

    for i in range(1, int(num_players) + 1):
        players.append(Player(f'Player {i}', parade.draw_card(5), []))

    random.shuffle(players)
    board = parade.draw_card(7)
    update()
    while not all(finished):
        for idx,player in enumerate(players):
            show_cards(player.hand, 'Your current hand')
            next = console.input(f'    Qué carta quieres jugar a continuación {player.name}?  ')
            play(int(next), idx)

            console.print(f'Total de cartas obtenidas de {player.name} tras la ronda -> {len(player.cards)} ')
            show_cards(player.cards, 'Your current cards obtained')

            update()
            if all(finished):
                console.print('Juego terminado')
                for player in players:
                    console.print(f'Total de cartas obtenidas de {player.name} -> {len(player.cards)} ')
                    show_cards(player.cards, 'Your current cards obtained')

                    console.print('      ' +'------------------------------'*2, style="bold blink white")

                    show_cards(player.hand, 'Your current hand')
                break

    for idx,player in enumerate(players):
            console.print(f'Total de cartas obtenidas de {player.name}')
            show_cards(player.cards, 'Your current cards obtained')

            console.print('      ' +'------------------------------'*2, style="bold blink white")

            show_cards(player.hand, 'Your current hand')

            one, two = console.input(f'    Qué dos cartas quieres jugar {player.name}? -> x,y ').split(',')
            final_round(int(one), int(two), idx)

    score = final_results(players)

    for color in colors:
        maximo = -1 
        id_color = -1
        for idx,player in enumerate(score):
            if player[color]['number'] > maximo:
                maximo = player[color]['number']
                id_color = idx
            elif player[color]['number'] == maximo and maximo > 0 and id_color != -1:
                id_color = -1
        if id_color != -1:
            score[idx][color]['score'] = score[idx][color]['number'] 

    min_score = 50
    id = -1
    for idx,player in enumerate(score):
        pointos = list(player.values())
        total = sum(int(color['score']) for color in pointos)
        if total < min_score:
            min_score = total
            id = idx

    console.print(f'      The winner is player {id+1} with {min_score} points.')

@app.command()
def update() -> None:

    console.print('\n')

    show_cards(board, 'Board')

    console.print('\n')
    console.print('      ' +'------------------------------'*2, style="bold blink white")
    console.print('\n' + '\n')

@app.command()
def play(x: int, idx: int) -> None:
    global points
    removed = players[idx].hand.pop(x-1)
    console.print(f'    Has jugado tu carta número {str(x)} -> un "{removed.value}" [{removed.color} ]{removed.color}[/]')
    points = 0

    if removed.value < len(board):
        for i in range(len(board) - removed.value -1, -1, -1):
            if board[i].color == removed.color or board[i].value <= removed.value:
                card_get = board.pop(i) 
                players[idx].cards.append(card_get)
    try:
        players[idx].hand.append(parade.draw_card()[0])
    except IndexError:
        finished[idx] = True
    board.append(removed)

    console.print(f'\n      El jugador {players[idx].name} ha terminado su ronda.')

@app.command()
def final_round(one: int, two: int, idx: int):
    players[idx].cards.append(players[idx].hand[one-1])
    players[idx].cards.append(players[idx].hand[two-1])


def final_results(players: list[Player]) -> list[dict]:
    scoreboard = []
    for player in players:
        cards = {
            'red': {
                'number': 0,
                'score': 0,
            },
            'yellow': {
                'number': 0,
                'score': 0,
            },
            'green': {
                'number': 0,
                'score': 0,
            },
            'blue': {
                'number': 0,
                'score': 0,
            },
            'black': {
                'number': 0,
                'score': 0,
            },
            'purple': {
                'number': 0,
                'score': 0,
            },
        }
        for card in player.cards:
            cards[card.color]['number'] +=1
            cards[card.color]['score'] += card.value
        scoreboard.append(cards)
    return scoreboard

if __name__ == "__main__":
    app()