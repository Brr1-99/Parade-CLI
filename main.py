import typer
from card import Card
from deck import Deck
from rich.console import Console
from rich.table import Table

colors = ['red', 'yellow', 'green', 'blue', 'purple', 'black']


all_cards = []

for i in range(0,11):
            for color in colors:
                all_cards.append(Card(i,color))
            
parade = Deck(all_cards)

score = 0

console = Console()

app = typer.Typer()

def show_cards(cards: list) -> tuple[list, list]:
    """Creates the data for the header and row of the table"""
    
    header = [f'Card: {i+1}' for i in range(len(cards))]
    row = [f'[{card.color}]{str(card.value)}[/{card.color}]' for card in cards]
    return header, row


@app.command()
def new_game() -> None:
    global hand, board, score
    parade.shuffle_deck()
    hand = parade.draw_card(5)
    board = parade.draw_card(7)
    update()
    while parade.cards:
        next = console.input('    Que carta quieres jugar a continuación?  ')
        play(int(next))
        score+= points
        console.print(f'Total de puntos tras la ronda -> {score}')
        update()

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

    hand_header, hand_row = show_cards(hand)
    table_hand = Table(*hand_header, title='Your current hand', style="bold")
    table_hand.add_row(*hand_row)
    console.print(table_hand)

    console.print('\n')

@app.command()
def play(x: int) -> None:
    global points
    removed = hand.pop(x-1)
    console.print(f'    Has jugado tu carta número {str(x)} -> un "{removed.value}" [{removed.color} ]{removed.color}[/]')

    points = 0

    if removed.value < len(board):
        for i in range(len(board) - removed.value -1, -1, -1):
            if board[i].color == removed.color or board[i].value <= removed.value:
                points += board[i].value
                board.pop(i) 

    hand.append(parade.draw_card()[0])
    board.append(removed)

    console.print(f'\n      Has obtenido {points} puntos en esta ronda.')

if __name__ == "__main__":
    app()