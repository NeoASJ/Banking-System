import maskpass
from datetime import datetime
import sys


if sys.stdout.encoding != 'utf-8':
    sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
if sys.stdin.encoding != 'utf-8':
    sys.stdin = open(sys.stdin.fileno(), mode='r', encoding='utf-8', buffering=1)

class Bank():
    bank = {}
    _account_counter = 0

    def __init__(self, user, age, password, bal=0, account_type='Generic'):
        Bank._account_counter += 1
        self.__accid = Bank._account_counter
        self.user = user
        self.age = age
        self.__bal = bal
        self.type = account_type
        self.__password = password
        Bank.bank[self.__accid] = self
        self.transactions = []
        print(f"\n🎉 Success! Account created with ID: {self.__accid} for {self.user}.")

    def calculate_interest(self):
        return 0

    def __repr__(self):
        return f"BankAccount(accid={self.__accid}, user='{self.user}', age={self.age}, bal={self.__bal}, type='{self.type}')"

    def deposit_amount(self, amount):
        if amount <= 0:
            return 'Deposit failed: Amount must be positive.'
        self.__bal += amount
        self.transactions.append(f"{datetime.now()}: Deposit of {amount}, balance: {self.__bal}")
        return f'The current balance {self.__bal}'

    def withdraw(self, amount):
        if amount <= 0:
            return 'Withdrawal failed: Amount must be positive.'
        if self.__bal - amount >= 0:
            self.__bal -= amount
            self.transactions.append(f"{datetime.now()}: Withdrawal of {amount}, balance: {self.__bal}")
            return f'The current balance {self.__bal}'
        else:
            self.transactions.append(f"{datetime.now()}: Failed withdrawal of {amount}, insufficient funds")
            return 'No sufficient funds'

    @staticmethod
    def transfer_amount(transfer_id, receiver_id, amount, passwd):
        sender = Bank.bank.get(transfer_id)
        receiver = Bank.bank.get(receiver_id)
        if sender is None:
            return 'Sender not found'
        if not sender.verify(passwd):
            return 'INCORRECT PASSWORD'
        if receiver is None:
            return 'Receiver not found'
        if amount <= 0:
            return 'Transfer failed: Amount must be positive.'
            
        result = sender.withdraw(amount)
        if result == 'No sufficient funds':
            return result
            
        receiver.deposit_amount(amount)
        sender.transactions.append(
            f"{datetime.now()}: Transfer of {amount} to {receiver.user} (Acc ID: {receiver_id})"
        )
        receiver.transactions.append(
            f"{datetime.now()}: Transfer of {amount} from {sender.user} (Acc ID: {transfer_id})"
        )
        return f'{sender.user} sent {amount} to {receiver.user}'

    @property
    def balance(self):
        return f"Balance left {str(self.__bal)}"

    def verify(self, passw):
        return passw == self.__password
    

    def get_account_num(self):
        return self.__accid

    def display(self, passwored):
        if self.verify(passwored):
            return (f"Account Number: {self.__accid} - The user {self.user} "
                      f"opened {self.type} account with balance {self.__bal}.")
        else:
            return None

    def show_transactions(self):
        return '\n'.join(self.transactions)

    @staticmethod
    def viewdetails(accid):
        # We replace the hardcoded prompt with a better one for humanization
        passw = maskpass.askpass(prompt="Security Check: Please enter your account password: ", mask="*")
        account = Bank.bank.get(accid)
        if not account:
            return "Account not found"
        if account.verify(passw):
            return account
        else:
            return "Incorrect password"

class Savings_Acc(Bank):
    def __init__(self, user, age, password, bal=0):
        super().__init__(user, age, password, bal, account_type='Savings')
    def calculate_interest(self):
        interest = self._Bank__bal * 0.05
        self._Bank__bal += interest
        self.transactions.append(
            f"{datetime.now()}: Interest gained {interest}, balance: {self._Bank__bal}")
        return f'the interest gained is {interest} the current balance is {self._Bank__bal}'

class Checking_Acc(Bank):
    def __init__(self, user, age, password, bal=0):
        super().__init__(user, age, password, bal, account_type='Checking')
    def calculate_interest(self, fee):
        self.fee = fee
        self._Bank__bal -= fee
        self.transactions.append(
            f"{datetime.now()}: Fee {fee} charged, balance: {self._Bank__bal}")
        return f'the fee imposed on the account is -{self.fee} current bal {self._Bank__bal}'

if __name__ == "__main__":
    while True:
        print("\n" + "🏛️")
        print("    Welcome to the Neo Bank ")
        print("💰"*10)
        print("How can we help you today? Please choose an option:")
        print("1. Open a New Account")
        print("2. Withdraw Funds")
        print("3. Deposit Funds")
        print("4. Transfer Money")
        print("5. Close Account")
        print("6. View Account Details & History")
        print("7. Account Maintenance (Apply Interest/Fee)")
        print("8. Display All Accounts (Admin View)")
        print("9. Exit Application")
        
        try:
            action = int(input("\nYour choice (1-9): "))
        except ValueError:
            print("🚨 That's not a valid number. Please enter an option from 1 to 9.")
            continue

        
        if action == 1:
            print("\n--- New Account Setup ---")
            name = input("What is the account holder's full name ?: ").title()
            try:
                age = int(input("How old  are you ?: "))
            except ValueError:
                print("🚨 Age must be a number. Please try again.")
                continue

            password = maskpass.askpass(prompt="🔑 Set a secure password for this account: ", mask="*")
            
            balance_input = input("Enter your initial deposit (or press Enter for $0): ")
            try:
                balance = float(balance_input) if balance_input else 0.0
            except ValueError:
                print("🚨 Invalid balance amount. Please enter a number.")
                continue
            
            print("\nAccount Types:")
            print(" (S) Savings Account")
            print(" (C) Checking Account")
            acc_type_choice = input("Which account type do you want? (S/C): ").upper()
            
            if acc_type_choice == 'S':
                Savings_Acc(name, age, password, balance)
            elif acc_type_choice == 'C':
                Checking_Acc(name, age, password, balance)
            else:
                print("❌ Invalid type selected. Account creation cancelled.")
        
        
        elif action in [2, 3, 5, 6, 7]:
            try:
                accno = int(input("Enter your 🆔 Account ID: "))
            except ValueError:
                print("🚨 Invalid ID format. Please enter a number.")
                continue

            account = Bank.viewdetails(accno)
            if isinstance(account, str):
                print(f"❌ {account}")
                continue

           
            if action == 2:
                try:
                    amount = float(input("How much are you taking out today?: "))
                    print(f"✅ Withdrawal result: {account.withdraw(amount)}")
                except ValueError:
                    print("🚨 Invalid amount entered.")

            
            elif action == 3:
                try:
                    amount = float(input("How much are you putting in today?: "))
                    print(f"✅ Deposit result: {account.deposit_amount(amount)}")
                except ValueError:
                    print("🚨 Invalid amount entered.")

            
            elif action == 5:
                confirm = input(f"Are you sure you want to permanently close account {accno} for {account.user}? (yes/no): ").lower()
                if confirm == 'yes':
                    if accno in Bank.bank:
                        del Bank.bank[accno]
                        print(f"🗑️ Account {accno} has been permanently closed.")
                    else:
                         print("❌ Account not found (shouldn't happen after verification).")
                else:
                    print("Account closure cancelled. We're glad you stayed!")
                    
            
            elif action == 6:
                print("\n--- 👁️ Account Details ---")
                print(f"Name: {account.user} | Account ID: {account.get_account_num()} | Type: {account.type}")
                # Using the balance property for a formatted view
                print(f"Current Balance: {account.balance}") 
                print("\n--- 📜 Transaction History ---")
                print(account.show_transactions())
                    
            
            elif action == 7:
                print("\n--- ⚙️ Applying Maintenance Action ---")
                if account.type == 'Savings':
                    print("Applying interest to your Savings account...")
                    print(account.calculate_interest())
                elif account.type == 'Checking':
                    try:
                        fee = float(input("Enter the service fee amount to charge: $: "))
                        print(account.calculate_interest(fee))
                    except ValueError:
                        print("🚨 Invalid fee amount entered.")
                else:
                    print(f"Action not applicable. Interest/Fee is not defined for {account.type} accounts.")

        
        elif action == 4:
            print("\n--- ➡️ Funds Transfer ---")
            try:
                sender_id = int(input("Enter YOUR 🆔 Account ID (Sender): "))
                receiver_id = int(input("Enter the Recipient's 🆔 Account ID: "))
                amount = float(input("Enter the amount you wish to send: $: "))
                password = maskpass.askpass(prompt="🔑 Enter your password to authorize the transfer: ", mask="*")
                
                result = Bank.transfer_amount(sender_id, receiver_id, amount, password)
                print(f"✅ Transfer Status: {result}")
            except ValueError:
                print("🚨 Invalid ID or amount entered.")
        
        # --- Option 8: Display All Accounts (Admin View) ---
        elif action == 8:
            print("\n--- 🔒 Admin Access: All Accounts ---")
            if not Bank.bank:
                print("No accounts registered yet.")
                continue
                
            for accid, account in Bank.bank.items():
                # Accessing private attribute via name mangling as the user did in the original classes
                print(f"ID: {accid} | Name: {account.user} | Type: {account.type} | Balance: {account._Bank__bal}")

        # --- Option 9: Exit ---
        elif action == 9:
            print("👋 Thank you for banking with us. Goodbye!")
            break

        # --- Invalid Option ---
        else:
            print("❓ Hmm, I didn't catch that. Please choose a number from the menu.")
