from models import Base, session, Product, engine
import datetime
import csv
import time

def menu():
    while True:
        print('''
            \nMain Menu
            \rv) Search product
            \ra) Add product
            \rb) Backup database
            \rq) Quit''')
        return input('\nWhat would you like to do?  ')



def app():
    app_running = True
    while app_running:
        choice = menu().lower()
        if choice == 'v':
            #look product up by # ID
            print(f'choice was: {choice}')
        elif choice == 'a':
            #add new product
            print(f'choice was: {choice}')
        elif choice == 'b':
            #backup database to .csv file
            print(f'choice was: {choice}')
        elif choice == 'q':
            #quit program
            app_running = False
            print('Exiting Program. Goodbye.')
        else:
            input(f'{choice} is not a valid input, press enter to return to the menu.')


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    #add_csv()
    app()
