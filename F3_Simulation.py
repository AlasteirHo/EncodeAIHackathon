# Code by Nihaar Raut (001309432) and Arber Oruci (001341361)

import random
import datetime
from F1_Lanes import Lane
from F2_Customer import Customer, generate_customer


class Simulation:
    def __init__(self, simulation_duration, number_of_lanes, customers_waiting_to_join_lane):
        self.simulation_duration = simulation_duration  # Keeping track of the simulation duration
        self.number_of_lanes = number_of_lanes  # Number of lanes generated
        self.customers_waiting_to_join_lanes = customers_waiting_to_join_lane  # Queue for customers to join lanes
        self.lanes = []  # Empty list of lanes
        self.all_customers = []  # Empty list of customers

    def setup_lanes(self):
        # Create one regular lane and a self-service lane with appropriate checkout times
        regular_lane = Lane("Regular_1", capacity=5, checkout_time=30)
        self_service_lane = Lane("Self-service", capacity=15, checkout_time=20)

        # Combine lanes into a list
        self.lanes = [self_service_lane, regular_lane]

    def start_simulation(self):
        # Start the simulation and generate initial random customers
        current_datetime = datetime.datetime.now()
        print(f"Simulation started at {current_datetime}")  # prints it with the time passed

        for _ in range(random.randint(10, 20)):
            new_customer = generate_customer()  # Generate customers, and it generates 10 to 20 customers in the start
            self.assign_customer_to_lane(new_customer)

    def award_lottery_tickets(self):
        # Identify eligible customers for lottery tickets and award one randomly
        eligible_customer = [customer for lane in self.lanes[1:] for customer in lane.customers if
                             customer.basket_size > 10]  # Logic to award if to someone with basket size above 10 only
        if eligible_customer:
            select_customer = random.choice(eligible_customer)  # Select at random from eligible ones
            lottery_message = select_customer.award_lottery_ticket()  # Display winning message right after
            return print(lottery_message)

    def assign_customer_to_lane(self, customer):
        # Assign customers to appropriate lanes based on basket size
        if customer.basket_size < 10:
            self.lanes[0].add_customer_to_lane(customer)  # Appropriate logic to put customer in self (0) lane
        else:  # Else move to regular (1) lane
            all_regular_lanes_full = all(
                len(lane.customers) == lane.capacity for lane in self.lanes[1:] if lane.lane_type.startswith("Regular"))
            #  If regular lanes are full, open a new regular lane
            if all_regular_lanes_full:
                self.open_new_regular_lane()
            else:
                # Move to a regular lane if there are fewer customers in any regular lane
                target_lane = min((lane for lane in self.lanes[1:] if lane.lane_type.startswith("Regular")),
                                  key=lambda x: len(x.customers))
                target_lane.add_customer_to_lane(customer)

        self.all_customers.append(customer)

    def get_all_customers(self):  # Retrieve data of all customers, useful to run sub-feature in GUI.
        return self.all_customers

    def open_new_regular_lane(self):
        # Find the number for the new regular lane
        new_lane_number = sum(1 for lane in self.lanes if lane.lane_type.startswith("Regular")) + 1
        new_lane = Lane(f"Regular_{new_lane_number}", capacity=5, checkout_time=30)  # New regular lane
        self.lanes.append(new_lane)
        print(f"Opened a new regular lane: {new_lane.lane_type}")  # Message shown whenever a new lane is opened.

    def run_simulation_continuously(self, time_interval):
        # Run the simulation continuously for the specified duration
        current_time = 0  # Initialise simulation time
        while current_time < self.simulation_duration:
            print(f"\nSimulation time: {current_time} seconds")  # Print simulation time passed
            self.display_lane_statuses()  # Display lane status at given simulation time right after
            # Generate new customers at regular intervals
            if current_time % 30 == 0:
                for _ in range(3):  # Generate 3 new customers every 30 seconds
                    new_customer = Customer(basket_size=0, checkout_time=30)
                    basket_size = new_customer.generate_a_shopping_basket()
                    print(f"Customer {new_customer.identifier} generated with {basket_size} items in the basket.")
                    self.assign_customer_to_lane(new_customer)
            # Process customers in self-service lanes since they're unmanned and work simultaneously
            for lane in self.lanes:
                if lane.lane_type == "Self-service":
                    # Process a limited number of customers in the self-service lane
                    num_customers_to_process = min(8, len(lane.customers))  # Process up to 8 customers
                    for _ in range(num_customers_to_process):
                        lane.process_customer_shopping_basket()
                else:
                    lane.process_customer_shopping_basket()

            current_time += time_interval  # Logic to increase current time by time interval each time

    def display_lane_statuses(self):
        # Display the status of each lane
        print("\nLane statuses:")
        for lane in self.lanes:
            lane.display_lane_status()


if __name__ == "__main__":
    # Initialise and run the simulation
    # Initialise total duration of simulation, number of lanes and waiting customers before beginning it.
    simulation = Simulation(simulation_duration=180, number_of_lanes=2, customers_waiting_to_join_lane=0)
    simulation.setup_lanes()
    simulation.start_simulation()
    simulation.run_simulation_continuously(time_interval=30)  # Display between continuous simulation time interval
    simulation.award_lottery_tickets()  # Declare lottery ticket result within simulation
