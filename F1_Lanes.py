# Code by Nihaar Raut (001309432) and subclasses check by Arber Oruci (001341361)


class Lane:
    def __init__(self, lane_type, capacity, checkout_time):
        self.lane_type = lane_type
        self.capacity = capacity  # Max capacity a lane can withhold
        self.checkout_time = checkout_time
        self.customers = []  # Empty list to keep track of customers

    def add_customer_to_lane(self, customer):
        # Add a customer to the lane if there is available space else display a rejection message
        if len(self.customers) < self.capacity:
            self.customers.append(customer)
            print(f"Customer {customer.identifier} just joined {self.lane_type} lane")
        else:
            print(f"The {self.lane_type} queue is full. Cannot add more customers.")

    def process_customer_shopping_basket(self):
        # Process the shopping basket of the first customer in the lane
        if self.customers:
            customer = self.customers[0]  # Retrieves the first customer in lane
            checkout_time = customer.check_out(self.lane_type)
            print(f"Processing customer number {customer.identifier}'s basket in {self.lane_type} lane")
            self.customers.pop(0)  # Remove the customer (pop) out of lane
            return checkout_time

    def process_all_customers(self):
        # Process the shopping baskets of all customers in the lane (esp. used for self-checkout lane)
        if self.customers:
            print(f"Processing all customers' baskets in {self.lane_type} lane")
            for customer in self.customers:
                customer.check_out(self.lane_type)
            self.customers.clear()  # Clear after fully processing customer's basket
        else:
            # Avoid printing the "Self-service queue is closed" message
            if not self.lane_type.startswith("Self-service"):  # Self-service lane cannot be closed
                print(f"{self.lane_type} queue is closed." if not self.lane_type.startswith("regular") else
                      f"{self.lane_type} queue ({self.capacity}): Closed.")  # Close regular lanes if unoccupied

    def remove_customer_from_lane(self, customer):
        # Remove a customer from the lane
        if customer in self.customers:
            self.customers.remove(customer)
            print(f"Customer {customer.identifier} removed from the queue successfully")
        else:  # If customer not found
            print(f"Customer {customer.identifier} has not finished or was not found in the queue")

    def close_lane(self):
        # Close the lane if there are no customers
        if not self.customers:
            print(f"{self.lane_type} queue is closed.")
        else:  # If customers are in queue
            print(f"{self.lane_type} queue cannot be closed. Customers in the queue.")

    def open_lane(self):
        # Open the lane if there are extra customers
        if not self.customers:
            print(f"{self.lane_type} queue is open.")
        else:  # If lane is already opened with busy customers
            print(f"{self.lane_type} queue cannot be opened. Customers in the queue.")

    def display_lane_status(self):
        # Display the status of the lane with asterisks representing customers
        status = '*' * len(self.customers)
        if not self.customers:  # If there are no customers, return empty
            print(f"{self.lane_type.capitalize()} queue ({self.capacity}): Empty.")
        else:  # Print simulation time status
            print(f"{self.lane_type.capitalize()} queue ({self.capacity}): {status}.")


class RegularLane(Lane):
    def __init__(self, capacity, checkout_time):
        super().__init__("Regular", capacity, checkout_time)  # Inheriting from the lane class
        self.checkout_time = checkout_time

    def process_customer_shopping_basket(self):
        # Process the shopping basket of the first customer in the lane
        if self.customers:
            customer = self.customers[0]  # For first customer in lane
            # Increase the checkout time for regular lanes
            checkout_time = customer.check_out(self.lane_type) * 1.2
            print(f"Processing customer number {customer.identifier}'s basket in {self.lane_type} lane")
            self.customers.pop(0)  # Remove the customer from the front after processing
            return checkout_time


class SelfServiceLane(Lane):
    def __init__(self, capacity, checkout_time):
        super().__init__("Self-service", capacity, checkout_time)  # Inheriting from the lane class
        self.checkout_time = checkout_time

    def process_customer_shopping_basket(self):
        # Process the shopping basket of the first customer in the lane
        if self.customers:
            customer = self.customers[0]  # For first customer in lane
            # Increase the checkout time for self-service lanes
            checkout_time = customer.check_out(self.lane_type) * 1.5
            print(f"Processing customer number {customer.identifier}'s basket in {self.lane_type} lane")
            self.customers.pop(0)  # Remove the customer at front after processing is finished
            return checkout_time

    def close_lane(self):
        # Raise an error if someone tries to close a self-service lane, it always needs to stay open.
        raise NotImplementedError("Self-service lanes cannot be closed.")
