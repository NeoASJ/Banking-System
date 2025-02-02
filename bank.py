class bank:
    b = {}
    def __init__(self,accno,accname,bal=0):
        self.accno = accno
        self.accname = accname
        self.bal = bal
        bank.b[self.accno]= self
    def deposit(self,am):
        self.am = am
        self.bal +=self.am
        self.update()
    def withdraw(self,am):
        self.am =am
        if (self.bal -self.am)>=0:
            self.bal -=self.am
            self.update()
        else:
            print("insufficient funds")
    @staticmethod
    def check_account(st):
        return st in bank.b
    @staticmethod
    def display():
        if len(bank.b)<1:
            print('no  records found')
        else:
            print("Accno  Accname  Balance")
            for i in bank.b.values():
                print(f"{i.accno}    {i.accname}     {i.bal}") 
    @staticmethod
    def remove(st):
        if st in bank.b:
            del bank.b[st]
        else:
            print(f"no records found with accno {st}")
    def update(self):
        bank.b[self.accno] = self
    
if __name__ == "__main__":
    while True:
        print("\nMenu:")
        print("1. Create new account")
        print("2. Withdraw")
        print("3. Deposit")
        print("4. Delete account")
        print("5. Display all records")
        print("6. Exit")
        action = int(input("Choose an action: "))
        if action == 1:
            accno = int(input("Enter account ID: "))
            name = input("Enter name: ").title()
            balance = input("Enter initial balance (or leave empty this set balance to 0): ")
            if not bank.check_account(accno):
                if balance == "":
                    bank(accno, name) 
                else:
                    balance = int(balance)
                    bank(accno, name, balance)
            else:
                print(f"The Account ID {accno}  already exits try with different Acc ID ")
        elif action == 2:
            accno = int(input("Enter account ID: "))
            amount = int(input("Enter amount to withdraw: "))
            if accno in bank.b:
                bank.b[accno].withdraw(amount)
            else:
                print(f"Account with ID {accno} not found.")
        elif action == 3:
            accno = int(input("Enter account ID: "))
            amount = int(input("Enter amount to deposit: "))
            if accno in bank.b:
                bank.b[accno].deposit(amount)
            else:
                print(f"Account with ID {accno} not found.")
        elif action == 4:
            accno = int(input("Enter account ID to remove: "))
            bank.remove(accno)
        elif action == 5:
            bank.display()
        elif action == 6:
            print("Exiting program.")
            break
        else:
            print("Invalid . Please try again and enter a valid option given in menu.")

    
            
            
        
