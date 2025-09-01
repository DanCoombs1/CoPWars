# Aiimi CoP Wars - Coding Challenge Platform

A competitive coding platform where users solve monthly challenges and compete on a leaderboard. Code is executed and evaluated using the Judge0 CE API.

## Features

- 🏆 **Monthly Coding Challenges** - New challenges every month
- ⚡ **Real-time Code Execution** - Powered by Judge0 CE API
- 🎯 **Performance Scoring** - Based on execution time and memory usage
- 🏅 **Leaderboard** - Track scores and rankings
- 🔐 **User Authentication** - Email/password signup and anonymous guest access
- 💻 **Multi-language Support** - JavaScript, Python, Java, C#, SQL
- 🎨 **Cyberpunk UI** - Modern, themed interface

## Tech Stack

- **Frontend**: React, Vite, Tailwind CSS
- **Backend**: Node.js, Express
- **Database**: Firebase Firestore
- **Authentication**: Firebase Auth
- **Code Execution**: Judge0 CE API (RapidAPI)

## Setup Instructions

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Firebase project with Firestore enabled

### 1. Clone and Install Dependencies

```bash
# Install backend dependencies
cd backend
npm install

# Install frontend dependencies
cd ../frontend
npm install
```

### 2. Firebase Configuration

1. Create a Firebase project at [Firebase Console](https://console.firebase.google.com/)
2. Enable Authentication (Email/Password and Anonymous)
3. Enable Firestore Database
4. Get your Firebase config and update it in `frontend/src/App.jsx`

### 3. Judge0 API Configuration

1. Get a Judge0 CE API key from [RapidAPI](https://rapidapi.com/judge0-official/api/judge0-ce/)
2. Create a `.env` file in the backend directory:
   ```
   JUDGE0_API_KEY=your_judge0_api_key_here
   ```

### 4. Start the Application

```bash
# Start the backend server (Terminal 1)
cd backend
npm start

# Start the frontend development server (Terminal 2)
cd frontend
npm run dev
```

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000

### 5. Add a Sample Challenge

1. Run the sample challenge script:
   ```bash
   node sample-challenge.js
   ```

2. Copy the JSON output and add it to your Firestore database:
   - Collection: `artifacts/cop-codewars/public/data/challenges/`
   - Document ID: `2024-12` (or current month)
   - Paste the JSON content

## Usage

### For Users

1. **Sign Up/In**: Create an account or sign in with email/password, or continue as a guest
2. **Select Challenge**: View the current month's coding challenge
3. **Write Code**: Use the built-in code editor with syntax highlighting
4. **Test Code**: Click "Test Program" to run your code without submitting
5. **Submit Solution**: Click "Submit" to submit your solution to the leaderboard
6. **View Results**: See your score, execution time, and memory usage
7. **Check Leaderboard**: View rankings and compare with other users

### For Administrators

1. **Create Challenges**: Add new challenges to Firestore with the following structure:
   ```javascript
   {
     title: "Challenge Title",
     description: "Challenge description...",
     testCases: [
       {
         name: "Test Case Name",
         input: "input string",
         expectedOutput: "expected output"
       }
     ],
     starterCode: {
       javascript: "// starter code",
       python: "# starter code",
       // ... other languages
     }
   }
   ```

2. **Monitor Submissions**: View user submissions in Firestore
3. **Update Leaderboard**: Scores are automatically calculated and updated

## API Endpoints

### Backend API (`http://localhost:8000`)

- `POST /execute` - Execute code using Judge0 API
  - Body: `{ language, code, testCases }`
  - Returns: Execution results with score, time, and memory usage

## Scoring System

The scoring system awards up to 1000 points based on:

- **Time Performance** (700 points max):
  - Perfect time: 100ms = 700 points
  - Maximum time: 2 seconds = 0 points
  - Linear interpolation between

- **Memory Efficiency** (300 points max):
  - Perfect memory: 16MB = 300 points
  - Maximum memory: 128MB = 0 points
  - Linear interpolation between

- **Test Cases**: All tests must pass to receive any points

## File Structure

```
├── backend/
│   ├── server.js          # Express server with Judge0 integration
│   ├── package.json       # Backend dependencies
│   └── node_modules/
├── frontend/
│   ├── src/
│   │   ├── App.jsx        # Main React application
│   │   ├── main.jsx       # React entry point
│   │   └── index.css      # Global styles
│   ├── package.json       # Frontend dependencies
│   └── vite.config.js     # Vite configuration
├── sample-challenge.js    # Sample challenge for testing
└── README.md             # This file
```

## Troubleshooting

### Common Issues

1. **Backend Connection Error**:
   - Ensure the backend server is running on port 8000
   - Check that the Judge0 API key is valid

2. **Firebase Connection Issues**:
   - Verify Firebase configuration in `App.jsx`
   - Ensure Firestore rules allow read/write access

3. **Code Execution Fails**:
   - Check that the language is supported by Judge0
   - Verify test case format matches expected structure

### Debug Mode

To enable debug logging, add console.log statements in the backend server.js file.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for internal use at Aiimi.

## Support

For issues or questions, contact the development team or create an issue in the repository.
