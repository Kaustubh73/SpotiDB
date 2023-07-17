import React, { useEffect, useState } from 'react';
import NavBar from '../components/NavBar';
import '../css/Leaderboard.css'
import Footer from '../components/Footer';


function Leaderboard() {
    const [name, setName] = useState('');
    const [leaderboard, setLeaderboard] = useState([]);

    useEffect(() => {
        (
          async () => {
            try {
            const response = await fetch('http://localhost:8000/api/leaderboard', {
                headers: {'Content-Type': 'application/json'},
                credentials: 'include',
            });
            
            const content = await response.json();
            try {
                setLeaderboard(content);
            } catch {
                console.error('Error fetching leaderboard');
            }
          } catch (error) {
                console.error(error);
          }
        }
        )(); 
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
        <div>
            <NavBar name={name} setName={setName}></NavBar>
            <div className='leaderboard-container'>
                <h1>Leaderboard</h1>
                {leaderboard.length === 0 ? (
                    <div>No users found in the leaderboard.</div>
                ) : (
                    <table className='leaderboard-table'>
                        <thead>
                            <tr>
                            <th>Name</th>
                            <th>Solved Count</th>
                            <th>Solved Puzzles</th>
                            </tr>
                        </thead>
                        <tbody>
                            {leaderboard.map((user, index) => (
                            <tr key={index}>
                                <td>{user.name}</td>
                                <td>{user.solved_count}</td>
                                <td>{user.solved_puzzles.split(',').join(', ')}</td>
                            </tr>
                            ))}
                        </tbody>
                    </table>
                )}              
            </div>
            <Footer/>
        </div>
     );
}


export default Leaderboard;