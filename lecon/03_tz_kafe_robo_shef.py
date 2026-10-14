
#кафе «Робо-шеф»


print("Кафе «Робо-шеф»")

dishes = ("чай", "сок", "сэндвич")

prices = {
    "чай": 10,
    "сок": 15,
    "сэндвич": 25
}

stock = {
    "чай": 3,
    "сок": 3,
    "сэндвич": 3
}

cart = []
served_clients = set()

revenue = 0
is_running = True
current_client = ""


def show_menu():
    print("\nМеню:")
    for dish in dishes:
        print(f"{dish} - {prices[dish]} сомони. Осталось: {stock[dish]} шт.")


def show_help():
    print("\nДоступные команды:")
    print("добавить <блюдо>, <количество> - добавить блюдо")
    print("оплатить <сумма> - оплатить заказ")
    print("отмена - отменить текущий заказ")
    print("помощь - показать команды")
    print("выход - выйти из игры")


def calculate_total():
    total = 0

    for dish in cart:
        total += prices[dish]

    return total


def show_cart() :
    if not cart:
        print("Корзина пуста.")
        return

    print("\nКорзина:")

    for dish in dishes:
        quantity = cart.count(dish)

        if quantity > 0:
            price = prices[dish] * quantity
            print(f"{dish} x {quantity} = {price} сомони.")

    print(f"Сумма: {calculate_total()} сомони.")


def get_cart_quantity(dish: str):
    return cart.count(dish)


def add_to_cart(dish: str, quantity: int):
    if dish not in dishes:
        print("Такого блюда нет в меню.")
        return

    if quantity < 1 or quantity > 3:
        print("Количество должно быть от 1 до 3.")
        return

    current_quantity = get_cart_quantity(dish)
    available = stock[dish] - current_quantity

    if quantity > available:
        print(f"Недостаточно блюда на складе. Доступно: {available} шт.")
        return

    for _ in range(quantity):
        cart.append(dish)

    print(f"{dish} x {quantity} добавлено в корзину.")
    show_cart()


def checkout(payment: int) :
    global revenue

    total = calculate_total()

    if not cart:
        print("Корзина пуста.")
        return False

    if payment <= 0:
        print("Сумма оплаты должна быть больше нуля.")
        return False

    if payment < total:
        print(f"Недостаточно денег. Сумма заказа: {total} сомони.")
        print("Заказ остаётся открытым.")
        return False

    change = payment - total

    print(f"Оплата принята. Сдача: {change} сомони.")

    print("\nЧек:")
    for dish in dishes:
        quantity = cart.count(dish)

        if quantity > 0:
            price = prices[dish] * quantity
            print(f"{dish} x {quantity} = {price} сомони.")

            stock[dish] -= quantity

    revenue += total
    served_clients.add(current_client)

    print(f"Итого: {total} сомони.")
    print(f"Клиент {current_client} обслужен.")

    return True


show_menu()

cashier = input("Введите имя кассира: ").strip()

print(f"Здравствуйте, {cashier}!")
print("Введите 'помощь', чтобы увидеть список команд.")


while is_running:

    if current_client == "":
        current_client = input("\nВведите имя клиента: ").strip().lower()

        if not current_client:
            print("Имя клиента не может быть пустым.")
            current_client = ""

        elif current_client in served_clients:
            print(f"Клиент {current_client} уже обслужен.")
            current_client = ""

        else:
            print(f"Начинаем заказ клиента: {current_client}")

    else:
        choice = input("> ").strip() .lower()# убирает пробелы # и делает все буквы маленькими

        if choice == "помощь":
            show_help()

        elif choice == "выход":
            print(f"\nТекущая выручка: {revenue} сомони.")
            is_running = False

        elif choice == "отмена":
            cart.clear()
            current_client = ""
            print("Заказ отменён. Клиент не засчитан.")

        elif choice.startswith("добавить"):

            parts = choice.split(",")

            if len(parts) != 2:
                print("Используйте формат: добавить чай, 2")

            else:
                dish_part = parts[0]
                quantity_part = parts[1]

                dish = dish_part.replace("добавить", "").strip()

                try:
                    quantity = int(quantity_part.strip())
                    add_to_cart(dish, quantity)

                except ValueError:
                    print("Количество должно быть целым числом.")

        elif choice.startswith("оплатить"):

            parts = choice.split()

            if len(parts) != 2:
                print("Используйте формат: оплатить 30")

            else:
                try:
                    payment = int(parts[1])

                    if checkout(payment):
                        cart.clear()
                        current_client = ""

                        if len(served_clients) == 3:
                            print("\n=== ИТОГ ИГРЫ ===")
                            print(f"Выручка: {revenue} сомони.")
                            print(f"Количество клиентов: {len(served_clients)}")

                            print("Остатки:")
                            for dish in dishes:
                                print(f"{dish}: {stock[dish]} шт.")

                            is_running = False

                except ValueError:
                    print("Оплата должна быть целым числом.")

        else:
            print("Неизвестная команда. Введите 'помощь'.")