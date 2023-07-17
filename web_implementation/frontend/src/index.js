// import React from 'react';
// import ReactDOM from 'react-dom/client';
// import './index.css';
// import App from './App';
// import reportWebVitals from './reportWebVitals';
// import SignUp from './pages/SignUp'
// import Login from './pages/Login'
// import Puzzles from './pages/Puzzles'
// import Contests from './pages/Contests'
// import Leaderboard from './pages/Leaderboard'
// import ContactUs from './pages/ContactUs'
// import Puzzle1 from './pages/Puzzle1';
// import Puzzle2 from './pages/Puzzle2';
// import Puzzle3 from './pages/Puzzle3';
// import Puzzle4 from './pages/Puzzle4';

// import {
//   createBrowserRouter,
//   RouterProvider,
// } from "react-router-dom";

// import { BrowserRouter as Router } from 'react-router-dom';
// const router = createBrowserRouter([
//   {
//     path: "/",
//     element: <App/>,
//   },
//   {
//     path: "signup",
//     element: <SignUp/>,
//   },
//   {
//     path: "login",
//     element: <Login/>,
//   },
//   {
//     path: "puzzles",
//     element: <Puzzles/>,
//   },
//   {
//     path: "contests",
//     element: <Contests/>,
//   },
//   {
//     path: "leaderboard",
//     element: <Leaderboard/>,
//   },
//   {
//     path: "contactus",
//     element: <ContactUs/>,
//   },
//   {
//     path: "/puzzle1",
//     element: <Puzzle1/>,
//   },
//   {
//     path: "puzzle2",
//     element: <Puzzle2/>,
//   },
//   {
//     path: "puzzle3",
//     element: <Puzzle3/>,
//   },
//   {
//     path: "puzzle4",
//     element: <Puzzle4/>,
//   },    
// ]);

// ReactDOM.createRoot(document.getElementById("root")).render(
//   <React.StrictMode>
//     <Router>
//       <RouterProvider router={router} />
//     </Router>
//   </React.StrictMode>
// );

// // If you want to start measuring performance in your app, pass a function
// // to log results (for example: reportWebVitals(console.log))
// // or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
// reportWebVitals();
import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import SignUp from './pages/SignUp';
import Login from './pages/Login';
import ContactUs from './pages/ContactUs';

ReactDOM.render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path="*" element={<App />} />
        <Route path="signup" element={<SignUp />} />
        <Route path="login" element={<Login />} />
        <Route path="contactus" element={<ContactUs />} />
      </Routes>
    </Router>
  </React.StrictMode>,
  document.getElementById('root')
);

reportWebVitals();
