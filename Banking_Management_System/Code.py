def banking_system():
    print(('\t'* 7 +'--------------------------'))
    print('\t'*7 +'Welcome to Banking system')
    print('\t'*7 +'--------------------------')
    print('For your account information.')
    pin = {'36745988' : 5639, '25477865' : 5518, '13244564' : 5560} # storing pin as keys with Bank Identification Number BIN as values
    balance = {'36745988' : 200000, '25477865' : 10000000, '13244564' : 50000} # storing Bank Identification Number (BIN) as keys and balances as values

    #using BIN as keys to a list that contains the date and amount of the deposit
    deposits = {'36745988' : [{'date' : "01/05/2024", 'amount' : 100000} , {'date' : "19/06/2024", 'amount' : 50000}],
                '25477865' : [{'date' : "15/05/2024", 'amount' : 300000} , {'date' : "30/08/2024", 'amount' : 400000}],
                '13244564' : [{'date' : "16/03/2024", 'amount' : 15000}]}

    # Using BIN as keys to a list that contains the date and amount of the withdrawals
    withdrawals = {'36745988' : [{'date' : "10/05/2024", 'amount' : 50000}], '25477865' : [{'date' : "25/05/2024", 'amount' : 30000} , {'date' : "15/09/2024", 'amount' : 100000}]}


    for tries in range(3): # To continue the loop and give the user 3 tries to enter into their account number
        account_number = input("Enter your account number: ")
        if account_number in balance:
            break # exit from the loop
        print("Account doesn't exist.") #if invalid acc number, it will give indication and the loop will run again until the user reaches the limit i.e. three tries
    else:
        print("Unfortunately! You have reached the limit. Access denied.\nCase has been submitted to management.\nFor more details, contact the bank.") #if the user reached the limit of tries and didn't input correct pin, access will be blocked by management.
        return # stop the entire function, 'cause of invalid and suspicious input

    i = 0
    while i < 3: # To continue the loop and give the user 3 tries to enter into their account pin
        user_pin = int(input("Enter your 4-digit PIN: "))
        if user_pin == pin[account_number]:
            print("Access granted!")

            while True:
                request = int(input("---- Select an option ----\n"
                                    "For money deposit press- 1 \n"
                                    "For money withdrawal press- 2 \n"
                                    "To find your account balance press- 3 \n"
                                    "To exit press- 4\nEnter option number: "))

                if request == 1:
                    user_amount = int(input("Enter the amount: "))  # Ask user for the amount to deposit
                    date = input("Enter the date: ")
                    # Use the account number to access the key and append the deposit entry as a new dictionary in the list

                    if user_amount > 0:
                        deposits[account_number].append({'date': date, 'amount': user_amount})

                        # Access the current balance in the balance dictionary and add the new deposit
                        new_amount = user_amount + balance.pop(account_number)
                        # Update the new amount in the balance of the account
                        balance[account_number] = new_amount
                        print("Deposit Successful!")  # print a message to confirm the deposit was successful
                    else:
                        print("Invalid Amount! Enter a positive value")


                elif request == 2:
                    user_withdrawal = int(
                        input("Enter the amount you would like to withdraw: "))  # Ask for the amount for withdrawal
                    date = input("Enter the date: ")
                    # Use the account number entered by the user to access the list and enter the withdrawal entry
                    if user_withdrawal > 0 and user_withdrawal < balance[account_number]:
                        withdrawals[account_number].append({'date': date, 'amount': user_withdrawal})
                        # Access the current balance and deduct the withdrawal
                        new_amount = balance.pop(account_number) - user_withdrawal
                        # Update the new amount
                        balance[account_number] = new_amount
                        print("Withdrawal Successful!")  # print a message to confirm the withdrawal was successful

                    else:
                        print("Invalid Amount! Your account balance is insufficient")

                elif request == 3:
                    print("Your balance is:", balance[account_number])

                elif request == 4:
                    print("\n🏦 Thank you for banking with us.")
                    print("We appreciate your trust and look forward to serving you again!")
                    print("Have a wonderful day! 😊")

                    return

                else:
                    print("Invalid option. Try again.")

        else:
            i += 1
            if i == 3:
                print("You have entered the incorrect PIN three times. Your card is temporarily blocked. Kindly contact customer service for assistance.")
                return
            print("Incorrect PIN, Try Again.")


banking_system()
