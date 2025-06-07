# 🏨 Technovista Hotel Reservation System

**Technovista** is a modern web-based hotel reservation system designed for efficient room booking and seamless mobile payments. Integrated with the **Safaricom M-Pesa Daraja API**, it allows users to pay using STK Push directly from their phones.

---

## 🚀 Features

- User registration and login system
- Dynamic room browsing and availability checks
- Real-time hotel room booking
- M-Pesa **STK Push** integration via **Daraja API**
- Admin dashboard for room, user, and booking management
- Email confirmation for successful bookings
- Responsive and mobile-friendly design

---

## 🛠️ Technologies Used

| Category       | Tech Stack                         |
|----------------|------------------------------------|
| **Frontend**   | HTML5, CSS3, JavaScript            |
| **Backend**    | Django, Flask (modular use)        |
| **API Layer**  | Django REST Framework (DRF)        |
| **Database**   | SQLite / PostgreSQL (customizable) |
| **Payment API**| M-Pesa Daraja API (STK Push)       |

---

## 💳 M-Pesa Daraja API Integration

### STK Push Workflow:
1. User selects a room and proceeds to payment.
2. System collects the user's phone number.
3. STK Push is initiated using Daraja API credentials.
4. User receives M-Pesa prompt and confirms.
5. Callback confirms payment, and booking is finalized.

> ✅ Sandbox tested and ready for production with valid credentials and public callback URL.

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/melau-eddy/TechnoVista-Project
cd technovista-hotel-reservation
