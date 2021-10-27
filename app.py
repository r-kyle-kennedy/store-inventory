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
    try:
        if price_str[0] == '$':
            price_float = float(price_str[1:])
            return int((price_float * 1000) / 10)
        else:
            raise ValueError
    except:
        input(f'{price_str} is not a valid price. press enter to try again.')
        return clean_price(input('Product price(ie: $19.99):  '))


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


def get_valid_id(list):
    choice = input(f'Enter product id (1-{len(list)}) :  ')
    try:
        choice = int(choice)
        if choice in list:
            return session.query(Product).filter(Product.product_id==choice).first()
        else:
            raise ValueError
    except:
        input(f'{choice} is not a valid input, press enter to try again')
        return get_valid_id(list)


def get_valid_quantity():
    quantity = input('Product quantity: ')
    try:
        quantity = int(quantity)
        return quantity
    except:
        input(f'{quantity} is not a valid input. Press enter to try again')
        return get_valid_quantity()


def update_or_add(new_product):
    product_in_db = session.query(Product).filter(Product.product_name==new_product.product_name).one_or_none()
    if product_in_db:
        edit = session.query(Product).filter(Product.product_name==new_product.product_name).first()
        edit.product_quantity = new_product.product_quantity
        edit.product_price = new_product.product_price
        edit.date_updated = new_product.date_updated
    else:
        session.add(new_product)


def add_product():
    not_correct = True
    while not_correct:
        print('Add Product')
        name = input('Product name:  ')
        quantity = get_valid_quantity()
        price = clean_price(input('Product price(ie: $19.99):  '))
        date = datetime.date.today()
        correct_input = input(f'''
            \nName: {name}
            \rQuantity: {quantity}
            \rPrice: ${"{:.2f}".format(float(price)/100)}
            \rLast Updated: {date}
            \rIs this correct(y/n)?  ''')
        if correct_input.lower() == 'y':
            not_correct=False
            new_product = Product(product_name=name, product_quantity=quantity, product_price=price, date_updated=date)
            update_or_add(new_product)
            session.commit()


def backup():
    with open('backup.csv', 'w') as csvfile:
        csvfile.write('product_name,product_price,product_quantity,date_updated')
        for product in session.query(Product):
            csvfile.write(f'\n{product.product_name},${"{:.2f}".format(float(product.product_price)/100)},{product.product_quantity},{product.date_updated.month}/{product.date_updated.day}/{product.date_updated.year}')


def app():
    app_running = True
    while app_running:
        choice = menu().lower()
        if choice == 'v':
            #look product up by ID#
            id_list = []
            for item in session.query(Product):
                id_list.append(item.product_id)
            id_choice = get_valid_id(id_list)
            print()
            print(f'Name: {id_choice.product_name}')
            print(f'Quantity: {id_choice.product_quantity}')
            print(f'Price: ${"{:.2f}".format(float(id_choice.product_price)/100)}')
            print(f'Last Updated: {id_choice.date_updated}')
        elif choice == 'a':
            print()
            add_product()
        elif choice == 'b':
            #backup database to .csv file
            print('Creating Backup')
            backup()
            print('Backup saved to backup.csv')
        elif choice == 'q':
            #quit program
            app_running = False
            print()
            print('Exiting Program. Goodbye.')
            print()
        else:
            input(f'{choice} is not a valid input, press enter to return to the menu.')


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()
