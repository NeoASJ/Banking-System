# 🏦 Neo Bank CLI Application

A simple, object-oriented command-line interface (CLI) application for managing bank accounts, built with Python. This application demonstrates basic banking operations like creating accounts, depositing, withdrawing, transferring funds, and viewing transaction history.

## ✨ Features

* **Account Types:** Supports **Savings** (with interest) and **Checking** (with maintenance fees).
* **Security:** Uses `maskpass` for secure, hidden password entry.
* **Transaction Logging:** Detailed history is logged for every major action (deposit, withdrawal, transfer, interest/fee).
* **Encapsulation:** Uses private attributes (like `__bal`, `__password`, `__accid`) to protect sensitive account data.
* **Polymorphism:** The `calculate_interest` method behaves differently for `Savings_Acc` and `Checking_Acc`.

## 🛠️ Prerequisites

Before running the application, you need to have **Python 3** installed.

This application uses the `maskpass` library for securely accepting passwords without displaying them on the screen.

### Installation

1.  **Install the required library:**
    ```bash
    pip install maskpass
    ```

## 🚀 Getting Started

1.  **Save the code:** Save the provided Python code into a file named `bank_cli.py`.
2.  **Run the application:**
    ```bash
    python bank.py
    ```

### Using the Application

The main menu provides a list of actions:

| Option | Description |
| :---: | :--- |
| **1** | **Open a New Account:** Choose between Savings or Checking. |
| **2** | **Withdraw Funds:** Requires Account ID and password verification. |
| **3** | **Deposit Funds:** Requires Account ID and password verification. |
| **4** | **Transfer Money:** Transfers money between two accounts. Requires Sender ID, Recipient ID, amount, and Sender's password. |
| **5** | **Close Account:** Permanently removes an account after verification. |
| **6** | **View Account Details & History:** Check balance and see all past transactions. |
| **7** | **Account Maintenance:** Applies interest (Savings) or charges a fee (Checking). |
| **8** | **Display All Accounts (Admin View):** Lists all created accounts and their current state. |
| **9** | **Exit Application:** Closes the CLI. |

***

## ⚙️ Core Class Structure

The application is built around three main classes:

### 1. `Bank` (Base Class)

* **Purpose:** Handles generic account creation, basic deposit/withdrawal logic, account identification (`__accid`), and secure password management.
* **Key Methods:**
    * `deposit_amount(amount)`: Adds funds to the account.
    * `withdraw(amount)`: Removes funds if balance is sufficient.
    * `transfer_amount(transfer_id, receiver_id, amount, passwd)`: A `staticmethod` to facilitate transfers between accounts.
    * `viewdetails(accid)`: A `staticmethod` used for secure password-protected access to an account.

### 2. `Savings_Acc` (Subclass)

* **Inherits from:** `Bank`
* **Special Feature:** Overrides `calculate_interest()` to apply a **5% interest** (0.05) directly to the account balance.

### 3. `Checking_Acc` (Subclass)

* **Inherits from:** `Bank`
* **Special Feature:** Overrides `calculate_interest(fee)` to be used for charging a **service fee** deducted from the balance.


* **Admin Access (Option 8):** The Admin View accesses the private balance attribute using **name mangling** (`account._Bank__bal`), which is a specific Python mechanism for accessing private members of a class hierarchy.
