# -*- coding: utf-8 -*-
"""Homework 1_Bhagyashri Patil
### MIS-515 Homework 1: Stock Market - Random Walk
"""

"""
* MIS-515 : Assignment 1
* Problem Statement:
Create a Python program that performs a “random walk” stock market simulation. The random walk hypothesis argues that the stock prices randomly 
increase or decrease each day relative to their prices the previous day, and these changes in price cannot be predicted.
To perform the simulation, first ask the user for:
(1) the initial price of the stock and
(2) how many days they would like to simulate.
Then, each day, assume that the change in stock price will be random and range from a 2 percent increase to a 2 percent decrease relative to the
previous day. Ensure that your program captures the daily change in stock price. In addition, also keep track of how many days the stock price 
increased and how many days the stock price decreased. At the end of the simulation, report (print) the new stock price and the number of days 
that the stock price increased and decreased.
Once a simulation is complete, the program should ask the user if they would like to run the simulation again and allow the user to run the 
simulation an unlimited number of times. Each time the user runs a simulation, also write the results of that simulation to an output CSV file 
called randomwalk.csv. Each time a simulation is run, create a new row in your CSV file containing the initial price, number of days simulated, 
and final price for that simulation.
"""

# Homework - 1: Solution
# Code Indent used : 4

# Importing the required libraries
import csv, google.colab.files
import random

# Writing the output to the csv file
with open('randomwalk.csv','a') as file:
    writer = csv.writer(file, lineterminator = '\n')

    # Writing a header row to the csv file
    header = ['initial price','number of days simulated', 'final price for simulation']
    writer.writerow(header)

    ###################################################
    # Initiating the problem statement code from below:
    ###################################################

    # Welcome message to user
    print("\n*** Welcome to the 'STOCK MARKET' Random Walk - Analysis! ***")

    # By-default start of the first simulation
    repeat = 'yes'

    # Run the simulation for an unlimited number of times, until user stops.
    while repeat.lower().strip() == 'yes':
        """
        (1) .lower() = for handling lower case letters
        (2) .strip() = for removing extra spaces added before/after the string
        """

        # Variable to store the simulated new_stock_price generated every day, to check if new_stock_price > initial_stock_price OR vice-versa. 
        simulated_stock_values = []
        
        # User input for the initial stock price and the days to simulate.
        initial_stock_price = int(input('\nWhat is the initial price of the stock? = $'))
        """
        Here, I am assuming stock price in dollar ($) currency.
        """
        simulate_days = int(input('How many days would you like to simulate? = '))

        # Initializing new_stock_price variable to store the initial_stock_price value at first.
        new_stock_price = initial_stock_price
        """
        Here, as we proceed ahead in the 'for' loop, new_stock_price variable will keep iterating and storing the latest calculated value of 
        new_stock_price in itself, with every single 'for' loop iteration. In this way, we get new_stock_value relative to the previous day.
        """

        # Generating loop equal to as that of total number of days to simulate.
        # This will calculate new_stock_price for every new day of simulation.
        for i in range(0, simulate_days, 1):

            # Generating random % increase/decrease using random.uniform module
            random_percent = random.uniform(0.98, 1.02)
            """
            Here I have considered 2% as my increase/decrease - upper/lower bound
            """
            # Calculating new simulated stock price using random % value generated
            new_stock_price = new_stock_price * random_percent

            # Storing the simulated stock prices as a list, for comparing with base value of initial_stock_value.
            simulated_stock_values.append(new_stock_price)

            # EXIT of For-loop


        # Displaying the simulation result.
        print(f"\nAfter {simulate_days} days, ${ round(new_stock_price, 5) } is the new stock price.")

        # Calculating the stock values above/below the initial stock value
        rised_stock_values = [i for i in simulated_stock_values if i >= initial_stock_price]
        dropped_stock_values = [i for i in simulated_stock_values if i < initial_stock_price]
        """
        Here, if the new simulated stock value "equals/is greater than" the initial stock value, then I have considered it as "rised_stock_values".
        """
        # Displaying the simulation result using above variables
        print(f"The stock price increased '{len(rised_stock_values)}' time(s) and decreased '{len(dropped_stock_values)}' time(s).")

        # Ask the user if they would like to run the simulation again
        repeat = str(input('\n -> Would you like to perform another simulation (yes/no)? = '))

        # Writing the data rows to the csv file, on every simulation.
        row = [initial_stock_price, simulate_days, new_stock_price]
        writer.writerow(row)

        # EXIT of While-loop


# Exit message to user
print("\n*** Thank you for using Stock Market - Random Walk Analysis *")

# Generating and printing output CSV file (automatically gets downloaded)
google.colab.files.download('randomwalk.csv')
