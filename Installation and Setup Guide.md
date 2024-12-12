# Company Email Account Registration System

## Prerequisites
- Python 3.8+
- Node.js 14+
- pip
- npm or yarn

## Backend Setup
1. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. Install Python dependencies
```bash
pip install flask flask-cors cryptography pandas sqlite3
```

3. Run Backend
```bash
python app.py
```

## Frontend Setup
1. Create React Project
```bash
npx create-react-app email-registration
cd email-registration
npm install axios tailwindcss
```

2. Replace src/App.js with provided React component

3. Run Frontend
```bash
npm start
```

## Configuration
- Modify backend settings in `app.py`
- Adjust frontend in React component
- Set up secure environment variables

## Running Application
1. Start Backend: `python app.py`
2. Start Frontend: `npm start`
3. Access at `http://localhost:3000`

## Security Notes
- Use in controlled environments
- Implement additional security layers
- Regularly update dependencies