# Textile ERP

A modular **ERP system** built with **Django**, designed for managing textile industry workflows.  
Each app is independent, with its own CRUD operations, ensuring scalability and maintainability.

---

## 📦 Included Apps

- **Users** → Manage users, roles, and permissions.
- **Colors** → Handle textile color palettes.
- **Companies** → Register and manage related companies.
- **Demand** → Track demands and purchase requests.
- **Fabrics** → Catalog fabrics and materials.
- **Garments** → Manage garments and finished products.
- **Inventory** → Control stock levels and inventory movements.
- **POs (Purchase Orders)** → Issue and track purchase orders.

---

## ⚙️ Key Features

- Full CRUD functionality in each module.
- Selection flow:
  1. The user selects a **Demand**.
  2. Available **Vendors** are displayed based on that demand.
  3. Corresponding **Fabrics** are shown once a vendor is chosen.
- When a **PO** is issued, the linked demand row automatically moves to the **Closed** table.
- Modular interface prepared for future integrations.

---

## 🚀 Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** PostgreSQL / SQLite (configurable)
- **Version Control:** Git & GitHub

---

## 📂 Project Structure
- textile_erp/
- ├── users/ 
- ├── colors/ 
- ├── companies/ 
- ├── demand/ 
- ├── fabrics/ 
- ├── garments/ 
- ├── inventory/ 
- └── pos/


Each app contains its own **models.py**, **views.py**, **forms.py**, and **templates** to maintain modularity.

---

## 📌 Roadmap
- [ ] Pull Request (use fabric).
- [ ] PDF report generation. (PO)
- [ ] Inventory dashboards with metrics.
- [ ] User validations.

