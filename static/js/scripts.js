document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('booksTable')) loadBooks();
    if (document.getElementById('membersTable')) loadMembers();
    if (document.getElementById('transactionsTable')) loadTransactions();

    const addBookForm = document.getElementById('addBookForm');
    if (addBookForm) {
        addBookForm.addEventListener('submit', function(e) {
            e.preventDefault();
            addBook();
        });
    }

    const addMemberForm = document.getElementById('addMemberForm');
    if (addMemberForm) {
        addMemberForm.addEventListener('submit', function(e) {
            e.preventDefault();
            addMember();
        });
    }
});

function loadBooks() {
    fetch('/api/books')
    .then(response => response.json())
    .then(data => {
        const tableBody = document.querySelector('#booksTable tbody');
        tableBody.innerHTML = data.length ? data.map(book => `
            <tr>
                <td>${book.title}</td>
                <td>${book.author}</td>
                <td>${book.genre}</td>
                <td>${book.stock}</td>
                <td>₹${book.rent_fee}</td>
                <td><button onclick="deleteBook(${book.book_id})">🗑️ Delete</button></td>
            </tr>`).join('') : `<tr><td colspan="6" style="text-align:center; color:red;">No books found</td></tr>`;
    })
    .catch(error => console.error('Error loading books:', error));
}

function addBook() {
    const bookData = {
        title: document.getElementById('title').value.trim(),
        author: document.getElementById('author').value.trim(),
        genre: document.getElementById('genre').value.trim(),
        stock: parseInt(document.getElementById('stock').value.trim(), 10),
        rent_fee: parseFloat(document.getElementById('rent_fee').value.trim())
    };

    if (Object.values(bookData).some(value => !value)) {
        alert("Please fill in all fields correctly.");
        return;
    }

    fetch('/api/books/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(bookData)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        if (!data.error) {
            loadBooks();
            document.getElementById('addBookForm').reset();
        }
    })
    .catch(error => console.error('Error adding book:', error));
}

function deleteBook(bookId) {
    if (!confirm("Are you sure you want to delete this book?")) return;
    fetch(`/api/books/delete/${bookId}`, { method: 'DELETE' })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        loadBooks();
    })
    .catch(error => console.error('Error deleting book:', error));
}

function loadMembers() {
    fetch('/api/members')
    .then(response => response.json())
    .then(data => {
        const tableBody = document.querySelector("#membersTable tbody");
        tableBody.innerHTML = data.map(member => `
            <tr>
                <td>${member.name}</td>
                <td>${member.email}</td>
                <td>${member.phone}</td>
                <td><button onclick="deleteMember(${member.member_id})">🗑️ Delete</button></td>
            </tr>`).join('');
    })
    .catch(error => console.error("Error loading members:", error));
}

function deleteMember(memberId) {
    if (!confirm("Are you sure you want to delete this member?")) return;
    fetch(`/api/members/delete/${memberId}`, { method: "DELETE" })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        loadMembers();
    })
    .catch(error => console.error("Error deleting member:", error));
}

function addMember() {
    const memberData = {
        name: document.getElementById('name').value.trim(),
        email: document.getElementById('email').value.trim(),
        phone: document.getElementById('phone').value.trim()
    };

    if (Object.values(memberData).some(value => !value)) {
        alert("Please fill in all fields.");
        return;
    }

    fetch('/api/members/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(memberData)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        loadMembers();
        document.getElementById('addMemberForm').reset();
    })
    .catch(error => console.error('Error adding member:', error));
}

function formatDateTime(dateString) {
    if (!dateString) return '<span style="color:red;">Not Returned</span>';
    const date = new Date(dateString);
    return date.toLocaleString();  // Converts to local time format
}

function loadTransactions() {
    fetch('/api/transactions')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector('#transactionsTable tbody');
            tableBody.innerHTML = '';

            data.forEach(transaction => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${transaction.transaction_id}</td>
                    <td>${transaction.title}</td>
                    <td>${transaction.member_name}</td>
                    <td>${formatDateTime(transaction.issue_date)}</td>
                    <td>${formatDateTime(transaction.return_date)}</td>
                    <td>${transaction.rent_fee !== null ? `₹${transaction.rent_fee}` : '<span style="color:orange;">Pending</span>'}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error loading transactions:', error));
}
