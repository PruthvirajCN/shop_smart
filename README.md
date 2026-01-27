# 🛒 ShopSmart - E-Commerce Website (Django)

ShopSmart is a modern, responsive, and feature-rich E-Commerce web application built using **Django**.  
It includes essential shopping features like product listing, search, sorting, cart, checkout, coupons, wishlist, reviews, and order tracking — similar to Flipkart/Amazon style UI.

---

## ✅ Features

### 🏠 Home Page
- Modern UI/UX design
- Featured products display
- Navbar with search
- Fully responsive (Mobile + Tablet + Desktop)

### 🛍️ Products Page
- Product listing with cards
- Search products by name
- Category filter
- Sorting options:
  - Newest
  - Price Low → High
  - Price High → Low
  - A → Z
  - Z → A
- Pagination for large listings
- Product hover + zoom effect

### 📄 Product Detail Page
- Full product information view
- Related products suggestion
- Product image zoom hover
- Reviews & Ratings system

### 🛒 Cart System
- Add to cart
- Update quantity
- Remove item
- Subtotal + tax calculation
- Coupon/discount support

### 🎟️ Coupon System
- Apply promo codes in cart
- Examples:
  - `SAVE10` → 10% Discount
  - `NEW50` → ₹50 Discount
- Coupon validation and total price update

### ❤️ Wishlist System
- Add/remove products from wishlist
- Wishlist page for saved items

### 🔐 Authentication
- User Registration
- Login / Logout
- Authentication required for:
  - Cart actions
  - Wishlist
  - Checkout
  - Reviews
  - Orders

### ✅ Checkout & Orders
- Checkout form (name, address, phone)
- Place order successfully
- My Orders page showing all orders
- Order Tracking Status:
  - Placed → Packed → Shipped → Delivered

### 🛠 Admin Panel
- Manage products and categories
- Manage coupons
- Manage orders and order items
- Update order status easily
- Manage reviews and wishlist

---

## 🧾 Languages Used
- **Python**
- **HTML**
- **CSS**
- **JavaScript**

---

## 🧰 Tools & Technologies Used

### Backend
- **Django (Python Framework)** – Backend logic & routing
- **Django ORM** – Database operations
- **SQLite** – Default database (local development)

### Frontend
- **HTML5** – Web structure
- **CSS3** – Styling and responsive UI
- **JavaScript** – Frontend interactions

### Development Tools
- **VS Code** – Code editor
- **Git** – Version control
- **GitHub** – Code hosting & repository management
- **Django Admin Panel** – Admin dashboard to manage data

### Environment
- **Python Virtual Environment (venv)** – Dependency isolation

---

## 📂 Project Structure

shop_smart/
│── ecommerce_project/ # Main Django project settings
│── store/ # Main app (products, cart, checkout, wishlist)
│ ├── templates/store/ # HTML templates
│ ├── static/store/ # CSS, JS, images
│ ├── models.py # Database models
│ ├── views.py # Business logic
│ ├── urls.py # Routes
│── manage.py # Django management file
│── requirements.txt # Dependencies
│── db.sqlite3 # Database (not recommended for GitHub)

<img width="1919" height="1007" alt="Screenshot 2026-01-27 202459" src="https://github.com/user-attachments/assets/ed921ed1-ef18-4c27-a4d8-1bbbe8dca1a3" />

<img width="1920" height="1080" alt="Screenshot 2026-01-27 202523" src="https://github.com/user-attachments/assets/23794c04-d312-4e4d-8498-ceffcdef78fd" />


## 🚀 Installation & Setup (Run Locally)

### ✅ 1. Clone Repository

git clone https://github.com/PruthvirajCN/shop_smart.git
cd shop_smart

✅ 2. Create & Activate Virtual Environment
Windows
python -m venv venv
.\venv\Scripts\activate

Mac/Linux
python3 -m venv venv
source venv/bin/activate

✅ 3. Install Dependencies
pip install -r requirements.txt

✅ 4. Run Migrations
python manage.py makemigrations
python manage.py migrate

✅ 5. Create Superuser (Admin Login)
python manage.py createsuperuser

✅ 6. Run Server
python manage.py runserver



