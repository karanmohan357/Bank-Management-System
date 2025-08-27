import streamlit as st

# Customer class
class Customer:
    def __init__(self, name, account_type, balance, status="Active"):
        self.name = name
        self.account_type = account_type
        self.balance = balance
        self.status = status

    def show_info(self):
        return f'''
**Customer Name:** {self.name}  
**Account Type:** {self.account_type}  
**Balance:** ₹ {self.balance}  
**Status:** {self.status}
'''

    def depositor(self, amount):
        if self.status == "Active":
            self.balance += amount
            return f"₹{amount} deposited to {self.name}'s account"
        else:
            return "Account is inactive"

    def withdrawer(self, amount):
        if self.status == "Active":
            if amount > self.balance:
                return "❌ Insufficient balance"
            else:
                self.balance -= amount
                return f"₹{amount} withdrawn from {self.name}'s account"
        else:
            return "Account is inactive"

    def acc_closer(self):
        if self.status == "Active":
            self.status = "Inactive"
            return "Account closed successfully"
        else:
            return "Account is already inactive"


# Initialize session state for persistent storage
if "bank_customers" not in st.session_state:
    st.session_state.bank_customers = {}
    st.session_state.customer_id = 1

st.title("🏦 Simple Bank Management System")

menu = st.sidebar.selectbox("📋 Menu", [
    "Create Account",
    "Deposit",
    "Withdraw",
    "Show Info",
    "Close Account",
    "Show All Accounts"
])

# 1. Create Account
if menu == "Create Account":
    st.header("➕ Create Account")
    name = st.text_input("Customer Name")
    acc_type = st.selectbox("Account Type", ["Savings", "Current"])
    balance = st.number_input("Initial Deposit (₹)", min_value=0.0, format="%.2f")
    if st.button("Create"):
        customer = Customer(name.title(), acc_type, balance)
        st.session_state.bank_customers[st.session_state.customer_id] = customer
        st.success(f"✅ Account created. Customer ID: {st.session_state.customer_id}")
        st.session_state.customer_id += 1

# 2. Deposit
elif menu == "Deposit":
    st.header("💰 Deposit Money")
    cus_id = st.number_input("Enter Customer ID", min_value=1, step=1)
    amount = st.number_input("Enter Deposit Amount", min_value=0.0, format="%.2f")
    if st.button("Deposit"):
        customer = st.session_state.bank_customers.get(cus_id)
        if customer:
            result = customer.depositor(amount)
            st.success(result)
        else:
            st.error("Invalid Customer ID")

# 3. Withdraw
elif menu == "Withdraw":
    st.header("💸 Withdraw Money")
    cus_id = st.number_input("Enter Customer ID", min_value=1, step=1)
    amount = st.number_input("Enter Withdraw Amount", min_value=0.0, format="%.2f")
    if st.button("Withdraw"):
        customer = st.session_state.bank_customers.get(cus_id)
        if customer:
            result = customer.withdrawer(amount)
            st.success(result)
        else:
            st.error("Invalid Customer ID")

# 4. Show Info
elif menu == "Show Info":
    st.header("ℹ️ Customer Info")
    cus_id = st.number_input("Enter Customer ID", min_value=1, step=1)
    if st.button("Show"):
        customer = st.session_state.bank_customers.get(cus_id)
        if customer:
            st.markdown(customer.show_info())
        else:
            st.error("Invalid Customer ID")

# 5. Close Account
elif menu == "Close Account":
    st.header("🛑 Close Account")
    cus_id = st.number_input("Enter Customer ID", min_value=1, step=1)
    if st.button("Close"):
        customer = st.session_state.bank_customers.get(cus_id)
        if customer:
            st.warning(customer.acc_closer())
        else:
            st.error("Invalid Customer ID")

# 6. Show All Accounts
elif menu == "Show All Accounts":
    st.header("📚 All Accounts Info")
    if not st.session_state.bank_customers:
        st.info("No accounts available.")
    for cid, customer in st.session_state.bank_customers.items():
        with st.expander(f"Customer ID: {cid}"):
            st.markdown(customer.show_info())
