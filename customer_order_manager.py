
import sqlite3


DATABASE = "orders.db"


def connect_db():
    return sqlite3.connect(DATABASE)


def initialize_database():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                product_name TEXT NOT NULL,
                quantity INTEGER NOT NULL CHECK(quantity > 0),
                unit_price REAL NOT NULL CHECK (unit_price > 0)
            )
        """)
    
    conn.commit()
    conn.close()


def show_menu():
    print("\n========== ORDER MANAGER ==========")
    print("1. Add a new order")
    print("2. View all orders")
    print("3. Search orders by customer")
    print("4. Update an order")
    print("5. Cancel an order")
    print("6. Calculate total sales")
    print("7. Exit")


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


def add_order():
    print("\n--- Add New Order ---")

    customer = get_non_empty_text("Customer name: ")
    product = get_non_empty_text("Product name: ")
    quantity = get_positive_int("Quantity: ")
    price = get_positive_float("Unit price: ")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO orders(customer_name, product_name, quantity, unit_price)
    VALUES (?, ?, ?, ?)
    """, (customer, product, quantity, price))

    conn.commit()

    order_id = cursor.lastrowid

    conn.close()


    print(f"Order added successfully. Order ID: {order_id}")


def display_order(order):
    order_total = order[3] * order[4]

    print(
        f"ID: {order[0]} | "
        f"Customer: {order[1]} | "
        f"Product: {order[2]} | "
        f"Quantity: {order[3]} | "
        f"Unit price: {order[4]:.2f} | "
        f"Order total: {order_total:.2f} EGP"
    )


def view_orders():
    conn = connect_db()
    cursore = conn.cursor()

    cursore.execute("SELECT * FROM orders")
    orders = cursore.fetchall()

    conn.close()

    if not orders:
        print("Threr are no orders")
        return

    print("\n--- All Orders ---")
    
    for order in orders:
        display_order(order)


def search_orders(customer_name):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM orders
    WHERE customer_name = ? COLLATE NOCASE
""", (customer_name,))

    matching_orders = cursor.fetchall()

    conn.close()

    return matching_orders
    

def update_order(order_id, new_quantity, new_price):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE orders 
        SET quantity = ?, unit_price = ?
        WHERE id = ?
    """, (new_quantity, new_price, order_id))

    updated = cursor.rowcount > 0

    conn.commit()
    conn.close()

    return updated


def cancel_order(order_id):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        DELETE FROM orders 
        WHERE id = ?
        """, (order_id,))

    deleted = cursor.rowcount > 0

    conn.commit()
    conn.close()

    return deleted


def calculate_total_value():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(quantity * unit_price)
        FROM orders
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total if total is not None else 0


def main():
    initialize_database()

    while True:
        show_menu()

        choice = input("\nChoose an option (1-7): ").strip()

        if choice == "1":
             add_order()

        elif choice == "2":
            view_orders()

        elif choice == "3":
            customer = get_non_empty_text("Customer name: ")
            matching_orders = search_orders(customer)

            if not matching_orders:
                print("No orders found for this customer.")
            else:
                for order in matching_orders:
                    display_order(order)

        elif choice == "4":
            order_id = get_positive_int("Enter order ID: ")
            quantity = get_positive_int("New quantity: ")
            price = get_positive_float("New unit price: ")

            if update_order(order_id, quantity, price):
                print(f"Order {order_id} was updated.")
            else:
                print("Order not found.")

        elif choice == "5":
            order_id = get_positive_int("Order ID: ")

            if cancel_order(order_id):
                print(f"Order {order_id} was cancelled.")
            else:
                    print("Order not found.")            

        elif choice == "6":
            total = calculate_total_value()
            print(f"Total sales: {total:.2f} EGP")

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please choose from 1 to 7.")


if __name__ == "__main__":
    main()
