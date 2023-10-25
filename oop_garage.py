'''
Your parking garage class should have the following methods:
- takeTicket
- This should decrease the amount of tickets available by 1
- This should decrease the amount of parkingSpaces available by 1

- payForParking
- Display an input that waits for an amount from the user and store it in a variable
- If the payment variable is not empty then (meaning the ticket has been paid) -> display 
    a message to the user that their ticket has been paid and they have 15mins to leave
- This should update the "currentTicket" dictionary key "paid" to True

-leaveGarage
- If the ticket has been paid, display a message of "Thank You, have a nice day"
- If the ticket has not been paid, display an input prompt for payment
- Once paid, display message "Thank you, have a nice day!"
- Update parkingSpaces list to increase by 1 (meaning add to the parkingSpaces list)
- Update tickets list to increase by 1 (meaning add to the tickets list)

You will need a few attributes as well:
- tickets -> list
- parkingSpaces -> list
- currentTicket -> dictionary
'''

'''
I have some questions about specs:
self.tickets are: a list of closed out tickets? or a list of tickets currently in circulation?
create a ticket class? store date, time_in, parking space, time_out, paid_time
    dictionary of ticket objects? keys = ticket_number : value = ticket object


'''

from datetime import datetime
from datetime import timedelta
import random
import json

def is_float(num: str) -> bool :
    '''
    num is expected to be a string
    '''
    try:
        float(num)
    except ValueError:
        return False
    return True


class Garage():
    '''
    The class maintains a virtual parking garage. Keeps information on 

    tickets = 
        {ticket_nunmber: {parking_space: int, 
                                in_time: xx:xx, 
                               out_time: xx:xx,
                                   paid: bool]}
    and maintains a dictionary of ALL tickets from the day. At EOD, the dictionary is
    dumped to JSON file

    parking_spaces = the number of spaces in the lot. Triggers lot_full status
    lot_full = No vacancies if TRUE
    occupied_spaces = a set of spaces that have been assigned (and should be occupied)
    current_tickets = the set of currently outstanding/open tickets (should match len(occupied_spaces))
    ticket


    HOURLY RATE:
    0-2 hrs : $3
    2-12 hrs : $2 / hr
    Day : $25 / day
    
    WEEKLY RATE:
    $75 / wk

    MONTHLY RATE:
    $200 / mo
    '''

    def __init__(self) -> None:
        self.parking_spaces = 25        # Number of spaces available in lot
        self.occupied_spaces = set()    # Currently occupied spaces
        self.current_tickets = set()    # Current outstanding tickets
        self.tickets = {}               # All tickets issued, dump to JSON daily
        self.lot_full = False
        self.hourly_rate = 3
        self.max_daily = 25
        self.last_ticket_number = 1001

    def get_ticket(self):
        # Assign parking space
        parking_space = random.randint(100, 125)
        while parking_space in self.occupied_spaces:
            parking_space = random.randint(100, 125)
        self.occupied_spaces.add(parking_space)

        # Assign ticket number
        while self.last_ticket_number in self.ticket:
            self.last_ticket_number += 1
        ticket_number = self.last_ticket_number
        self.current_tickets.add(ticket_number)
        
        # Store ticket info
        self.tickets[ticket_number] = {'parking_space': parking_space,
                                                'in_time': datetime.now(),
                                                'out_time': -1,
                                                'paid' : False
                                               }
        return ticket_number

    def take_ticket(self):
        if self.lot_full == True:
            return 'Sorry, the lot is currently full.'
        ticket_number  = self.get_ticket()
        print(f'Please take your ticket and park in spot {self.tickets[ticket_number]["parking_space"]}')
        self.parking_spaces -= 1
        if self.parking_spaces == 0:
            self.lot_full = True
        
    def rate_formula(self, ticket_number):
        self.tickets[ticket_number]['time_out'] = datetime.now()
        time_parked = (self.tickets[ticket_number]['time_out'] - self.tickets[ticket_number]['time_in']) // 1   # to get a whole number
        # Check for multiple days
        if time_parked.days > 0:
            result = time_parked.days * self.max_daily
            time_parked -= timedelta(days = time_parked.days)

        # Deal with less than day amount, // 3600 to yield hours floored
        temp = (time_parked.seconds // 3600) * self.hourly_rate
        if temp > self.max_daily:
            result += self.max_daily
        else:
            result += temp
        
        return result

    def pay_for_parking(self, ticket_number = -1):
        
        # Get ticket number
        valid = False
        while valid == False and ticket_number == -1:
            valid = True
            ticket_number = input('Please enter your ticket number: ')
            if ticket_number.isnumeric() == False:
                print('Invalid input.')
                valid = False
            elif int(ticket_number) not in self.current_tickets:
                print('Invalid ticket number, try again')
                valid = False
            
        # Pay bill
        bill = self.rate_formula(ticket_number)
        while bill > 0:
            valid = False
            while valid == False:
                valid = True
                pay = input('Ticket not yet paid, please pay ${bill} \n'
                            'Insert money: $')
                if is_float(pay) == False:
                    print('Invalid input, please enter a decimal number')
                    valid = False
            
            if float(pay) > 0:
                pay = "{:.2f}".format(float(pay))
                bill -= float(pay)
                print(f'${pay} paid')
                if bill < 0:
                    bill *= -1
                    print(f'{bill} is your change.')

        # Make it Official            
        print('Thank you, have a nice day!')
        self.current_tickets[ticket_number]['paid'] = True


    def leave_garage(self, ticket):
        if self.tickets[ticket]['paid'] == False:
            self.pay_for_parking(ticket)
        
        elif self.tickets[ticket]['time_out'] - datetime.now() > 15:
                print('Sorry, exit time limit exceeded')
                self.pay_for_parking(ticket)
        else:
            print('Thank you, have a nice day!')
        

        self.lot_full = False
        print('')



        self.parking_spaces += 1
        self.current_tickets.remove(ticket)
    
thing = '1,236,634.10'
print(thing.split('.'))
print(thing.replace(',', '').split('.'))

num = '{:.2f}'.format(float(thing.replace(',', '')))
print(float(num))



now = datetime.now()
then = now - timedelta(days=2, hours= 4, minutes= 12, seconds= 34)
change = now - then
change -= timedelta(days = change.days)

print(now)
print(then)
print(change.days)