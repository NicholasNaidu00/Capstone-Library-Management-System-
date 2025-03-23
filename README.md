# Library Management System

A modern and efficient system for managing library operations including book management, member management, and lending services.

## Features

- Book Management (add, update, delete, search)
- Member Management (registration, updates, removal)
- Lending System (borrow, return, reserve books)
- Fine Calculation for overdue books
- Search and Filter capabilities
- User-friendly interface

## Tech Stack

- Python
- SQLite for database
- Flask for web framework
- HTML/CSS/JavaScript for frontend
- Bootstrap for styling

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize the database:
```bash
python init_db.py
```

4. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Project Structure

```
library_management_system/
├── app.py              # Main application file
├── init_db.py         # Database initialization
├── requirements.txt   # Project dependencies
├── static/           # Static files (CSS, JS)
├── templates/        # HTML templates
└── models/          # Database models
```

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

MIT License
