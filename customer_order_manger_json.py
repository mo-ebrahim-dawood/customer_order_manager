import json

def main():
    try:
        with open("orders.json", "r") as file:
             orders = json.load(file)

    except FileNotFoundError:
        orders = []
    
    if orders: 
        next_order_id = max(order["id"] for order in orders) + 1

    else:
        next_order_id = 1

    while True:
        show_menu()
        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            next_order_id = add_order(orders, next_order_id)

        elif choice == "2":
            view_orders(orders)

        elif choice == "3":
            customer_name = get_non_empty_text("Customer name: ")
            matching_orders = search_orders(orders, customer_name)

            if not matching_orders:
                print("No orders found for this customer.")
            else:
                for order in matching_orders:
                    display_order(order)

        elif choice == "4":
            order_id = get_positive_int("Enter order ID: ")
            cancelled_order = cancel_order(orders, order_id)

            if cancelled_order is None:
                print("Order not found.")
            else:
                print(f"Order {order_id} was cancelled.")
                update_orders_file(orders)

        elif choice == "5":
            total = calculate_total_value(orders)
            print(f"Total sales: {total:.2f} EGP")

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please choose from 1 to 6.")

        print()


def show_menu():
    print("========== ORDER MANAGER ==========")
    print("1. Add a new order")
    print("2. View all orders")
    print("3. Search orders by customer")
    print("4. Cancel an order")
    print("5. Calculate total sales")
    print("6. Exit")
    print()


def get_non_empty_text(prompt):
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("This field cannot be empty.")


def get_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))

            if value > 0:
                return value

            print("Please enter a number greater than zero.")

        except ValueError:
            print("Please enter a valid whole number.")


def get_positive_float(prompt):
    while True:
        try:
            value = float(input(prompt))

            if value > 0:
                return value

            print("Please enter a price greater than zero.")

        except ValueError:
            print("Please enter a valid price.")


def update_orders_file(orders):
    with open("orders.json", "w") as file:
        json.dump(orders, file, indent = 4)


def add_order(orders, next_order_id):
    print("\n--- Add New Order ---")

    customer_name = get_non_empty_text("Customer name: ")
    product_name = get_non_empty_text("Product name: ")
    quantity = get_positive_int("Quantity: ")
    unit_price = get_positive_float("Unit price: ")

    order = {
        "id": next_order_id,
        "customer_name": customer_name,
        "product_name": product_name,
        "quantity": quantity,
        "unit_price": unit_price
    }

    orders.append(order)

    update_orders_file(orders)

    print(f"Order added successfully. Order ID: {next_order_id}")

    return next_order_id + 1


def display_order(order):
    order_total = order["quantity"] * order["unit_price"]

    print(
        f"ID: {order['id']} | "
        f"Customer: {order['customer_name']} | "
        f"Product: {order['product_name']} | "
        f"Quantity: {order['quantity']} | "
        f"Unit price: {order['unit_price']:.2f} | "
        f"Order total: {order_total:.2f} EGP"
    )


def view_orders(orders):
    if not orders:
        print("There are no orders.")
        return

    print("\n--- All Orders ---")

    for order in orders:
        display_order(order)


def search_orders(orders, customer_name):
    matching_orders = []

    for order in orders:
        if order["customer_name"].casefold() == customer_name.casefold():
            matching_orders.append(order)

    return matching_orders


def cancel_order(orders, order_id):
    for index, order in enumerate(orders):
        if order["id"] == order_id:
            return orders.pop(index)

    return None


def calculate_total_value(orders):
    total = 0

    for order in orders:
        total += order["quantity"] * order["unit_price"]

    return total


if __name__ == "__main__":
    main()
