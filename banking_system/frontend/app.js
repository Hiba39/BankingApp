const API_URL = "http://127.0.0.1:8000";
const PAGE_SIZE = 5;

let currentPage = 1;
let totalPages = 0;
let currentTransactions = [];

async function loadDashboard() {
    try {
        const response = await fetch(`${API_URL}/dashboard/summary`);

        if (!response.ok) {
            throw new Error("Could not load dashboard summary.");
        }

        const summary = await response.json();

        document.getElementById("totalCustomers").textContent =
            summary.total_customer_records;

        document.getElementById("totalBalance").textContent =
            new Intl.NumberFormat("en-ET", {
                style: "currency",
                currency: "ETB"
            }).format(summary.total_balance);

        document.getElementById("savingsAccounts").textContent =
            summary.savings_accounts;

        document.getElementById("currentAccounts").textContent =
            summary.current_accounts;

    } catch (error) {
        console.error(error);
    }
}

async function loadCustomers() {
    const message = document.getElementById("message");
    const table = document.getElementById("customerTable");

    const name = document.getElementById("searchName").value.trim();
    const accountType = document.getElementById("accountType").value;

    const params = new URLSearchParams({
        page: String(currentPage),
        page_size: String(PAGE_SIZE),
        sort_by: "name",
        order: "asc"
    });

    if (accountType) {
        params.set("account_type", accountType);
    }

    try {
        message.textContent = "Loading customers...";
        message.classList.remove("error");
        table.replaceChildren();

        let customers = [];

        if (name) {
            const searchParams = new URLSearchParams({
                name: name,
                page: String(currentPage),
                page_size: String(PAGE_SIZE)
            });

            if (accountType) {
                searchParams.set("account_type", accountType);
            }

            const response = await fetch(
                `${API_URL}/customers/search?${searchParams.toString()}`
            );

            if (!response.ok) {
                throw new Error("Customer search failed.");
            }

            const data = await response.json();
            const allMatches = data.customers || [];
            const matchCount = allMatches.length;

            totalPages = Math.ceil(matchCount / PAGE_SIZE);
            customers = allMatches.slice(
                (currentPage - 1) * PAGE_SIZE,
                currentPage * PAGE_SIZE
            );

            updatePagination(matchCount);

        } else {
            const response = await fetch(
                `${API_URL}/customers?${params.toString()}`
            );

            if (!response.ok) {
                throw new Error("Could not load customer records.");
            }

            const data = await response.json();
            customers = data.customers || [];
            totalPages = data.total_pages || 0;

            updatePagination(data.total_records || 0);
        }

        for (const customer of customers) {
            const row = document.createElement("tr");

            const values = [
                customer.name,
                customer.account_number,
                new Intl.NumberFormat("en-ET", {
                    style: "currency",
                    currency: "ETB"
                }).format(customer.balance),
                customer.account_type
            ];
            
            values.forEach((value, index) => {
                const cell = document.createElement("td");

                if (index === 0) {
                    const nameButton = document.createElement("button");

                    nameButton.textContent = value;
                    nameButton.className = "customer-name-button";
                    nameButton.addEventListener("click", () => {
                        openCustomerDetails(customer.account_number);
                    });

                    cell.appendChild(nameButton);
                } else {
                    cell.textContent = value;
                }

                row.appendChild(cell);
            });
            
            table.appendChild(row);
        }

        message.textContent = `${customers.length} customer record(s) on this page.`;

    } catch (error) {
        message.textContent = "Could not load customers. Check that the API is running.";
        message.classList.add("error");
        console.error(error);
    }
}

function updatePagination(totalRecords) {
    document.getElementById("pageInfo").textContent =
        `Page ${currentPage} of ${totalPages}`;

    document.getElementById("previousButton").disabled =
        currentPage <= 1;

    document.getElementById("nextButton").disabled =
        totalPages === 0 || currentPage >= totalPages;
}

document.getElementById("searchButton").addEventListener("click", () => {
    currentPage = 1;
    loadCustomers();
});

document.getElementById("resetButton").addEventListener("click", () => {
    document.getElementById("searchName").value = "";
    document.getElementById("accountType").value = "";
    currentPage = 1;
    loadCustomers();
});

document.getElementById("searchName").addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        currentPage = 1;
        loadCustomers();
    }
});

document.getElementById("previousButton").addEventListener("click", () => {
    if (currentPage > 1) {
        currentPage--;
        loadCustomers();
    }
});

document.getElementById("nextButton").addEventListener("click", () => {
    if (currentPage < totalPages) {
        currentPage++;
        loadCustomers();
    }
});

loadDashboard();
loadCustomers();

const navLinks = document.querySelectorAll(".nav-link");

navLinks.forEach((link) => {
    link.addEventListener("click", (event) => {
        const sectionName = link.dataset.section;

        if (sectionName !== "dashboard" && sectionName !== "customers") {
            event.preventDefault();
            alert(
                sectionName.charAt(0).toUpperCase() +
                sectionName.slice(1) +
                " will be added in a future lesson."
            );
            return;
        }

        navLinks.forEach((item) => {
            item.classList.remove("active");
        });

        link.classList.add("active");

        document.getElementById(sectionName).scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    });
});

async function openCustomerDetails(accountNumber) {
    const detailsPanel = document.getElementById("customerDetails");
    const transactionTable = document.getElementById("transactionTable");
    const transactionMessage = document.getElementById("transactionMessage");

    detailsPanel.hidden = false;
    transactionTable.replaceChildren();

    document.getElementById("detailName").textContent = "Loading...";
    document.getElementById("detailAccount").textContent = accountNumber;
    document.getElementById("detailType").textContent = "Loading...";
    document.getElementById("detailBalance").textContent = "Loading...";

    transactionMessage.textContent = "Loading transactions...";

    detailsPanel.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });

    try {
        const customerResponse = await fetch(
            `${API_URL}/customers/${encodeURIComponent(accountNumber)}`
        );

        if (!customerResponse.ok) {
            throw new Error("Could not load customer details.");
        }

        const customer = await customerResponse.json();

        document.getElementById("detailName").textContent = customer.name;
        document.getElementById("detailAccount").textContent = customer.account_number;
        document.getElementById("detailType").textContent = customer.account_type;
        document.getElementById("detailBalance").textContent =
            new Intl.NumberFormat("en-ET", {
                style: "currency",
                currency: "ETB"
            }).format(customer.balance);

        const transactionResponse = await fetch(
            `${API_URL}/customers/${encodeURIComponent(accountNumber)}/transactions`
        );

        if (!transactionResponse.ok) {
            throw new Error("Customer loaded, but transaction history could not be retrieved.");
        }

        const transactionData = await transactionResponse.json();
        const transactions = transactionData.transactions || [];
        currentTransactions = transactions;
        renderTransactionReport();

        if (!Array.isArray(transactions)) {
            throw new Error("The transaction response has an unexpected format.");
        }

        if (transactions.length === 0) {
            transactionMessage.textContent =
                `No transactions found for ${transactionData.customer_name}. ` +
                `Total recorded: ${transactionData.transaction_count}.`;
            return;
        }

        renderTransactions();

    } catch (error) {
        transactionMessage.textContent = error.message;
        console.error(error);
    }
}

document.getElementById("backToCustomers").addEventListener("click", () => {
    document.getElementById("customerDetails").hidden = true;

    document.getElementById("customers").scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
});
function renderTransactionReport() {
    let totalDeposits = 0;
    let totalWithdrawals = 0;
    let totalTransfers = 0;

    for (const transaction of currentTransactions) {
        const type = String(
            transaction.transaction_type ??
            transaction.type ??
            ""
        ).toUpperCase();

        const amount = Number(transaction.amount) || 0;

        if (type === "DEPOSIT") {
            totalDeposits += amount;
        } else if (type === "WITHDRAWAL") {
            totalWithdrawals += amount;
        } else if (type === "TRANSFER") {
            totalTransfers += amount;
        }
    }

    const totalVolume =
        totalDeposits + totalWithdrawals + totalTransfers;

    const formatETB = amount =>
        new Intl.NumberFormat("en-ET", {
            style: "currency",
            currency: "ETB"
        }).format(amount);

    document.getElementById("reportDeposits").textContent =
        formatETB(totalDeposits);

    document.getElementById("reportWithdrawals").textContent =
        formatETB(totalWithdrawals);

    document.getElementById("reportTransfers").textContent =
        formatETB(totalTransfers);

    document.getElementById("reportVolume").textContent =
        formatETB(totalVolume);

    document.getElementById("reportCount").textContent =
        `Total transactions: ${currentTransactions.length}`;
}

function renderTransactions() {
    const transactionTable = document.getElementById("transactionTable");
    const transactionMessage = document.getElementById("transactionMessage");
    const filter = document.getElementById("transactionFilter").value;
    const sort = document.getElementById("transactionSort").value;

    transactionTable.replaceChildren();

    let filteredTransactions = [...currentTransactions];

    // FILTER
    if (filter !== "ALL") {
        filteredTransactions = filteredTransactions.filter(transaction => {
            const type = transaction.transaction_type ?? transaction.type ?? "";
            return String(type).toUpperCase() === filter;
        });
    }

    // SORT
    filteredTransactions.sort((a, b) => {
        if (sort === "HIGH_AMOUNT" || sort === "LOW_AMOUNT") {
            const amountA = Number(a.amount) || 0;
            const amountB = Number(b.amount) || 0;

            return sort === "HIGH_AMOUNT" ? amountB - amountA : amountA - amountB;
        }

        const dateA = new Date(a.timestamp ?? a.date ?? 0).getTime();
        const dateB = new Date(b.timestamp ?? b.date ?? 0).getTime();

        return sort === "NEWEST" ? dateB - dateA : dateA - dateB;
    });

    if (filteredTransactions.length === 0) {
        transactionMessage.textContent = "No transactions match the selected filter.";
        return;
    }

    transactionMessage.textContent = `${filteredTransactions.length} transaction(s) found.`;

    for (const transaction of filteredTransactions) {
        const row = document.createElement("tr");

        const type = transaction.transaction_type ?? transaction.type ?? "—";
        const amount = Number(transaction.amount);

        const formattedAmount = Number.isFinite(amount)
            ? new Intl.NumberFormat("en-ET", {
                style: "currency",
                currency: "ETB"
            }).format(amount)
            : "—";

        const status = transaction.status ?? "UNKNOWN";
        const description = transaction.description ?? "—";
        const timestamp = transaction.timestamp ?? transaction.date ?? null;

        let formattedDate = "—";
        if (timestamp) {
            const date = new Date(timestamp);
            if (!Number.isNaN(date.getTime())) {
                formattedDate = date.toLocaleString();
            }
        }

        // Type
        const typeCell = document.createElement("td");
        const typeSpan = document.createElement("span");
        typeSpan.className = "transaction-type";
        typeSpan.textContent = type;
        typeCell.appendChild(typeSpan);

        // Amount
        const amountCell = document.createElement("td");
        const amountSpan = document.createElement("span");
        amountSpan.className = "transaction-amount";
        amountSpan.textContent = formattedAmount;
        amountCell.appendChild(amountSpan);

        // Status
        const statusCell = document.createElement("td");
        const statusBadge = document.createElement("span");
        const normalizedStatus = String(status).toLowerCase();

        statusBadge.className = "transaction-badge";
        if (normalizedStatus === "success") {
            statusBadge.classList.add("success");
        } else if (normalizedStatus === "failed") {
            statusBadge.classList.add("failed");
        } else if (normalizedStatus === "pending") {
            statusBadge.classList.add("pending");
        }

        statusBadge.textContent = status;
        statusCell.appendChild(statusBadge);

        // Description
        const descriptionCell = document.createElement("td");
        descriptionCell.textContent = description;

        // Date
        const dateCell = document.createElement("td");
        dateCell.textContent = formattedDate;

        row.appendChild(typeCell);
        row.appendChild(amountCell);
        row.appendChild(statusCell);
        row.appendChild(descriptionCell);
        row.appendChild(dateCell);

        transactionTable.appendChild(row);
    }
}

document.getElementById("transactionFilter").addEventListener("change", renderTransactions);
document.getElementById("exportTransactions").addEventListener("click", function () {
console.log("EXPORT BUTTON CLICKED");    
    if (currentTransactions.length === 0) {
        alert("No transaction records available to export.");
        return;
    }

    const headers = [
        "Transaction Type",
        "Amount",
        "Status",
        "Description",
        "Date"
    ];

    const rows = currentTransactions.map(transaction => [
        transaction.transaction_type ?? transaction.type ?? "",
        transaction.amount ?? "",
        transaction.status ?? "",
        transaction.description ?? "",
        transaction.timestamp ?? transaction.date ?? ""
    ]);

    const csvContent = [
        headers,
        ...rows
    ].map(row =>
        row.map(value =>
            `"${String(value).replace(/"/g, '""')}"`
        ).join(",")
    ).join("\n");

    const blob = new Blob(
        ["\uFEFF" + csvContent],
        { type: "text/csv;charset=utf-8;" }
    );

    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = "transaction_history.csv";

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    URL.revokeObjectURL(url);

    alert("Transaction history exported successfully!");
});
document.getElementById("transactionSort").addEventListener("change", renderTransactions);

const depositForm = document.getElementById("depositForm");

depositForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const accountNumber = document.getElementById("depositAccount").value.trim();
    const amount = Number(document.getElementById("depositAmount").value);
    const message = document.getElementById("depositMessage");

    if (!/^\d{8}$/.test(accountNumber)) {
        message.textContent = "Enter a valid 8-digit account number.";
        return;
    }

    if (!Number.isFinite(amount) || amount <= 0 || amount > 1000000) {
        message.textContent = "Enter a valid deposit amount.";
        return;
    }

    message.textContent = "Processing deposit...";

    try {
        const response = await fetch(`${API_URL}/accounts/deposit`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                account_number: accountNumber,
                amount: amount
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                typeof data.detail === "string"
                    ? data.detail
                    : "Deposit failed. Check the account and try again."
            );
        }

        message.textContent =
            `Deposit successful! ${data.customer_name}: ` +
            `ETB ${Number(data.deposit_amount).toFixed(2)} deposited. ` +
            `New balance: ETB ${Number(data.new_balance).toFixed(2)}.`;

        depositForm.reset();

        await loadDashboard();
        await loadCustomers();

        const detailsPanel = document.getElementById("customerDetails");
        if (
            !detailsPanel.hidden &&
            document.getElementById("detailAccount").textContent.trim() === accountNumber
        ) {
            await openCustomerDetails(accountNumber);
        }
    } catch (error) {
        message.textContent = error.message || "Could not connect to the banking API.";
    }
});

const withdrawForm = document.getElementById("withdrawForm");

withdrawForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const accountNumber = document.getElementById("withdrawAccount").value.trim();
    const amount = Number(document.getElementById("withdrawAmount").value);
    const message = document.getElementById("withdrawMessage");

    if (!/^\d{8}$/.test(accountNumber)) {
        message.textContent = "Enter a valid 8-digit account number.";
        return;
    }

    if (!Number.isFinite(amount) || amount <= 0 || amount > 1000000) {
        message.textContent = "Enter a valid withdrawal amount.";
        return;
    }

    message.textContent = "Processing withdrawal...";

    try {
        const response = await fetch(`${API_URL}/accounts/withdraw`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                account_number: accountNumber,
                amount: amount
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                typeof data.detail === "string"
                    ? data.detail
                    : "Withdrawal failed."
            );
        }

        message.textContent =
            `Withdrawal successful! ${data.customer_name}: ` +
            `ETB ${Number(data.withdrawal_amount).toFixed(2)} withdrawn. ` +
            `New balance: ETB ${Number(data.new_balance).toFixed(2)}.`;

        withdrawForm.reset();

        await loadDashboard();
        await loadCustomers();

        const detailsPanel = document.getElementById("customerDetails");
        if (
            !detailsPanel.hidden &&
            document.getElementById("detailAccount").textContent.trim() === accountNumber
        ) {
            await openCustomerDetails(accountNumber);
        }

    } catch (error) {
        message.textContent = error.message || "Could not connect to the banking API.";
        console.error(error);
    }
});

const transferForm = document.getElementById("transferForm");

transferForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const senderAccount = document.getElementById("senderAccount").value.trim();
    const recipientAccount = document.getElementById("recipientAccount").value.trim();
    const amount = Number(document.getElementById("transferAmount").value);
    const message = document.getElementById("transferMessage");

    // 1. Validation checks run FIRST
    if (senderAccount === recipientAccount) {
        message.textContent = "Sender and recipient must be different accounts.";
        return;
    }

    if (
        !/^\d{8}$/.test(senderAccount) ||
        !/^\d{8}$/.test(recipientAccount) ||
        !Number.isFinite(amount) ||
        amount <= 0 ||
        amount > 1000000
    ) {
        message.textContent = "Enter valid account numbers and a valid amount.";
        return;
    }

    // 2. Confirmation dialog prompts AFTER successful validation
    const confirmed = confirm(
        `Please confirm this transfer:\n\n` +
        `From account: ${senderAccount}\n` +
        `To account: ${recipientAccount}\n` +
        `Amount: ${amount.toFixed(2)} ETB\n\n` +
        `Do you want to continue?`
    );

    if (!confirmed) {
        message.textContent = "Transfer cancelled.";
        return;
    }

    message.textContent = "Processing transfer...";

    try {
        const response = await fetch(`${API_URL}/accounts/transfer`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                sender_account: senderAccount,
                recipient_account: recipientAccount,
                amount: amount
            })
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Transfer failed.");
        }

        const reference = result.reference || `TRF-${Date.now()}`;
        document.getElementById("receiptReference").textContent = reference;
        document.getElementById("receiptSender").textContent = result.sender_account;
        document.getElementById("receiptRecipient").textContent = result.recipient_account;
        document.getElementById("receiptAmount").textContent = `${Number(result.amount).toFixed(2)} ETB`;
        document.getElementById("receiptSenderBalance").textContent = `${Number(result.sender_new_balance).toFixed(2)} ETB`;
        document.getElementById("receiptRecipientBalance").textContent = `${Number(result.recipient_new_balance).toFixed(2)} ETB`;
        document.getElementById("receiptStatus").textContent = result.status || "SUCCESS";
        document.getElementById("receiptDate").textContent = result.timestamp || new Date().toLocaleString();
        document.getElementById("transferReceipt").hidden = false;
        console.log("Receipt immediately after display:",
            document.getElementById("transferReceipt").hidden);

        message.textContent =
            `Success! Transferred ${Number(result.amount).toFixed(2)} ETB. ` +
            `Sender balance: ${Number(result.sender_new_balance).toFixed(2)} ETB. ` +
            `Recipient balance: ${Number(result.recipient_new_balance).toFixed(2)} ETB.`;

        transferForm.reset();

        await loadDashboard();
        await loadCustomers();

        const detailsPanel = document.getElementById("customerDetails");
        const detailAccount = document.getElementById("detailAccount");

        if (
            detailsPanel &&
            detailAccount &&
            detailsPanel.offsetParent !== null
        ) {
            const openAccount = detailAccount.textContent.trim();
            if (openAccount === senderAccount || openAccount === recipientAccount) {
                await openCustomerDetails(openAccount);
            }
        }
    } catch (error) {
        message.textContent = error.message || "Unable to complete transfer.";
    }
});

document.getElementById("showRecipientBalance").addEventListener("change", function () {
    document.getElementById("recipientBalanceRow").hidden = !this.checked;
});