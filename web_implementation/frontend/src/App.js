import './css/App.css';
import React, { useEffect, useState } from 'react'
import NavBar from './components/NavBar'
import Footer from './components/Footer';
// import Puzzles from './pages/Puzzles';
import sudoku from './images/Sudoku.png'
import bacon from './images/Question 2.png'
import q3 from './images/Question 3.png'
import Login from './pages/Login'
import {Routes, Route, useLocation}  from 'react-router-dom'


function Puzzle({ puzzle, index }) {
  return (
    <div className="puzzle-showcase">
      {index % 2 === 0 ? (
        <>
          <div className="puzzle-description">
            <h3>{puzzle.title}</h3>
            <p>{puzzle.description}</p>
            <p>{puzzle.description2}</p>
          </div>
          <div className="puzzle-image">
            <img src={puzzle.imageUrl} alt="Puzzle" />
          </div>
        </>
      ) : (
        <>
          <div className="puzzle-image">
            <img src={puzzle.imageUrl} alt="Puzzle" />
          </div>        
          <div className="puzzle-description">
            <h3>{puzzle.title}</h3>
            <p>{puzzle.description}</p>
            <p>{puzzle.description2}</p>
          </div>

        </>
      )
    }

    </div>
  );
}
function Homepage(props) {
  const puzzles = [
  {
    title:  'Dot Dot Dottie Dot',
    description: 'You see a perfectly normal Sudoku board over here, but wait something is wrong for sure :). Look at the title of the image first of all, it is Dot Dot Dottie Dot and it has been striked through. This suggests that Dashes and Dots are involved here for sure hinting us to use Morse Code to solve this. Further the symbols in the centre row, they mean something, but this you can figure out after you have already the solved the Morse Code.',
    description2: ' Puzzles are all about looking at your surroundings and then trying to figure out what they could imply. So just be attentive and notice the minute details provided all around you.',
    imageUrl: sudoku,
  },
  {
    title: 'Bold Pigs',
    description: 'Not everything needs to be hidden for them to be hard. Every single information you need to solve this puzzle is given on the image and the title. If you look at the image inside this question, you see a little something, hinting you further towards the answer.',
    description2: '',
    imageUrl: bacon,
  },
  {
    title: 'The Unimportant Order',
    description: 'This one is quite straight forward, it is what you see in the image, just to test your math skills at best :). Do you have enough math power to be able to solve this question, only time will tell.',
    description2: '',
    imageUrl: q3,
  },
];
  return (
    <div>
    <div className="welcome-message">
      <h1>The Trio Treasure Hunt!</h1>
      <p>Get ready for an exciting adventure filled with puzzles, challenges, and rewards.</p>
    </div>
    {puzzles.map((puzzle, index) => (
        <Puzzle key={index} puzzle={puzzle} index={index} />
      ))}
  </div>
  );
}


function App() {
  const location = useLocation();
  console.log(location)
  const [name, setName] = useState('');

  useEffect(() => {
    document.title = 'Puzzler - The Puzzling Place';
  }, []);

  useEffect(() => {
    (async () => {
      try {
        const response = await fetch('http://localhost:8000/api/user', {
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
        });
  
        if (response.ok) {
          const content = await response.json();
          setName(content.name);
        } else {
          // Handle non-successful response
          throw new Error('Failed to fetch user data');
        }
      } catch (error) {
        // Handle fetch error
        console.error(error);
      }
    })();
  }, []);
  
  return (
    <div className="App">
      <Routes>
        {/* <Switch> */}
        <Route path="/login" component={() => <Login setName={setName}/>} />
        <Route path="/" component={App} />          
        {/* </Switch> */}
      </Routes>
      <NavBar name={name} setName={setName}/>
      <Homepage/>
      <Footer />
    </div>
  );
}

export default App;
