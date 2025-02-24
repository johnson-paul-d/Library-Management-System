# 📚 Library Management System

This is a **Library Management System** built using **Flask (Python), MySQL, HTML, CSS, and JavaScript (AJAX)**. The application allows a librarian to efficiently manage books, members, and transactions (issuing and returning books).

---

## 🚀 Features

- 📖 **Manage Books** (Add, Delete, Search, and Display Books)
- 👥 **Manage Members** (Add, Delete, and View Members)
- 🔄 **Issue and Return Books** (Maintains Transactions with Rent Fee Calculation)
- 📅 **Automatic Date & Time Handling** for Issuing and Returning Books
- 🎨 **Professional UI Design** (Clean and Responsive Layout)
- 🔍 **Search Functionality** (Filter Books and Members Dynamically)
- ⚡ **AJAX for Dynamic Updates** (Fast and Seamless UI Interactions)

---

## 🛠️ Tech Stack

- **Backend:** Flask (Python) 🐍
- **Database:** MySQL 🛢️
- **Frontend:** HTML, CSS, JavaScript (AJAX) 🎨
- **Version Control:** Git & GitHub

---

## 📂 Project Structure

```
📦 library-management-system
├── 📁 static
│   ├── 📁 css
│   │   ├── styles.css
│   ├── 📁 js
│   │   ├── scripts.js
├── 📁 templates
│   ├── index.html
│   ├── books.html
│   ├── members.html
│   ├── transactions.html
├── app.py  # Flask Application
├── db.py   # Database Connection
├── requirements.txt  # Dependencies
├── README.md  # Documentation
```

---

## 🔧 Installation & Setup

1️⃣ **Clone the Repository**
```sh
git clone https://github.com/yourusername/library-management-system.git
cd library-management-system
```

2️⃣ **Set Up a Virtual Environment (Optional but Recommended)**
```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3️⃣ **Install Dependencies**
```sh
pip install -r requirements.txt
```

4️⃣ **Configure the Database**
- Create a MySQL database: `library_db`
- Import the `schema.sql` file into MySQL
- Update `db.py` with your MySQL credentials

5️⃣ **Run the Application**
```sh
python app.py
```

6️⃣ **Open in Browser**
```
http://127.0.0.1:5000/
```

---

## 📜 API Endpoints

| Endpoint             | Method | Description                          |
|----------------------|--------|--------------------------------------|
| `/api/books`        | GET    | Fetch all books                     |
| `/api/books/add`    | POST   | Add a new book                      |
| `/api/books/delete/<id>` | DELETE | Delete a book               |
| `/api/members`      | GET    | Fetch all members                   |
| `/api/members/add`  | POST   | Add a new member                    |
| `/api/members/delete/<id>` | DELETE | Delete a member               |
| `/api/issue`        | POST   | Issue a book                        |
| `/api/return`       | POST   | Return a book and calculate rent fee|
| `/api/transactions` | GET    | Fetch all transactions              |

---

## 📌 Future Enhancements

- 📊 **Dashboard with Insights**
- 🛡️ **Authentication & User Roles**
- 📅 **Due Date Reminder System**
- 📑 **Export Reports (CSV/PDF)**

