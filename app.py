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


def clean_price(price_str):
    price_float = float(price_str[1:])
    return int((price_float * 1000) / 10)


def clean_date(date_str):
    split_date = date_str.split('/')
    month = int(split_date[0])
    day = int(split_date[1])
    year = int(split_date[2])
    return datetime.date(year, month, day)


def add_csv():
    with open('inventory.csv') as csvfile:
        data = csv.reader(csvfile)
        iter_data = iter(data)
        next(iter_data)
        for row in iter_data:
            product_in_db = session.query(Product).filter(Product.product_name==row[0]).one_or_none()
            if not product_in_db:
                name = row[0]
                price = clean_price(row[1])
                quantity = int(row[2])
                date = clean_date(row[3])
                new_product = Product(product_name=name, product_quantity=quantity, product_price=price, date_updated=date)
                session.add(new_product)
            else:
                item = session.query(Product).filter(Product.product_name==row[0]).first()
                new_product_date = clean_date(row[3])
                if item.date_updated < new_product_date:
                    item.product_price = clean_price(row[1])
                    item.product_quantity = int(row[2])
                    item.date_updated = new_product_date
        session.commit()


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
    add_csv()
    app()
