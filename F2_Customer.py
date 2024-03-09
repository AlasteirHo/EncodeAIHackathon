# Code by Arber Oruci (001341361)

import random


class Customer:
    customer_counter = 0  # To keep track of total customers throughout the simulation

    def __init__(self, basket_size, checkout_time):
        Customer.customer_counter += 1
        self.identifier = Customer.customer_counter
        self.basket_size = basket_size
        self.checkout_time = checkout_time
        self.lottery_tickets = None  # initially set to None
        self.lane = []  # Initialised as empty list

    def generate_a_shopping_basket(self):
        # Generate a random shopping basket size for the customer
        self.basket_size = random.randint(1, 30)
        return self.basket_size  # Return the basket size

    def check_out(self, lane_type):
        # Calculate the total checkout time based on basket size and lane type
        if lane_type == "regular":
            checkout_time = self.basket_size * 4  # For regular lane its calculated as 4x where x is the basket size
        else:
            checkout_time = self.basket_size * 6  # For self lane its calculated as 6x where x is the basket size
        return checkout_time

    def award_lottery_ticket(self):
        # Award a lottery ticket to the customer if eligible
        if self.basket_size > 10:  # To allow ticket to be given to people who are in regular lane only.
            self.lottery_tickets = True  # If they win
            return f"Customer {self.identifier} has won a lottery ticket"
        else:
            return f"Customer {self.identifier} is not eligible for a lottery ticket"

    def display_basket_and_time(self):
        # Display customer's basket and processing time, specifically used for ease of access for the GUI.
        return f"Customer {self.identifier}'s Basket Size: {self.basket_size}, Time to process: {self.checkout_time}"


def generate_customer():  # Independent method not inside previous class
    # Generate a random customer with a shopping basket
    new_customer = Customer(basket_size=0, checkout_time=30)
    basket_size = new_customer.generate_a_shopping_basket()
    print(f"Customer {new_customer.identifier} generated with {basket_size} items in the basket.")
    return new_customer
