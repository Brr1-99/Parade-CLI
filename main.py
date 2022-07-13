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

def show_cards(cards: list) -> tuple[list, list]:
    """Creates the data for the header and row of the table"""
    
    header = [f'Card: {i+1}' for i in range(len(cards))]
    row = [f'[{card.color}]{str(card.value)}[/{card.color}]' for card in cards]
    return header, row


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
            hand_header, hand_row = show_cards(player.hand)
            table_hand = Table(*hand_header, title='Your current hand', style="bold")
            table_hand.add_row(*hand_row)
            console.print(table_hand)
            next = console.input(f'    Qué carta quieres jugar a continuación {player.name}?  ')
            play(int(next), idx)

            console.print(f'Total de cartas obtenidas de {player.name} tras la ronda -> {len(player.cards)} ')
            cards_header, cards_row = show_cards(player.cards)
            table_cards = Table(*cards_header, title='Your current cards obtained', style="bold")
            table_cards.add_row(*cards_row)
            console.print(table_cards)
            update()
            if all(finished):
                console.print('Juego terminado')
                for player in players:
                    console.print(f'Total de cartas obtenidas de {player.name} -> {len(player.cards)} ')
                    cards_header, cards_row = show_cards(player.cards)
                    table_cards = Table(*cards_header, title='Your current cards obtained', style="bold")
                    table_cards.add_row(*cards_row)
                    console.print(table_cards)

                    console.print('      ' +'------------------------------'*2, style="bold blink white")

                    hand_header, hand_row = show_cards(player.hand)
                    table_hand = Table(*hand_header, title='Your current hand', style="bold")
                    table_hand.add_row(*hand_row)
                    console.print(table_hand)
                break

@app.command()
def update() -> None:

    console.print('\n')

    board_header, board_row = show_cards(board)
    table_board = Table(*board_header, title='Board', style="bold")
    table_board.add_row(*board_row)
    console.print(table_board)

    console.print('\n')
    console.print('      ' +'------------------------------'*2, style="bold blink white")
    console.print('\n')


    console.print('\n')

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

if __name__ == "__main__":
    app()