import React, { useEffect } from 'react';
import '../css/Header.css';
import logo from '../images/Puzzle1.jpg';
import menu from '../images/MenuBar.png';
import { Link, useLocation } from "react-router-dom";

function Desktop(props) {
    const location = useLocation();

    useEffect(() => {
      // Exclude the login page from storing the previous URL
      if (location.pathname !== '/login') {
        sessionStorage.setItem('previousUrl', location.pathname);
        // Or localStorage.setItem('previousUrl', location.pathname);
      }
    }, [location]);
  
  
    return (
        <header className='header'>
        <nav className='nav'>
            {/* Add your navigation links here */}
            <ul>
                <li><Link to="/" ><img src = {logo}  className='logo' alt='Homepage'/></Link></li>
                <li className='nav-text'><Link to="/contactus">Contact Us</Link></li>
            </ul>
        </nav>
        {props.name ? 
            <div className='user-reg'>
                <p>Welcome {props.name}</p>
                <Link to='/login' onClick={props.logout}><button>Logout</button></Link>
            </div>
        : 
            <div className='user-reg'>
                <Link to="/signup"><button>Sign Up</button></Link>
                <Link to="/login"><button>Log In</button></Link>
            </div>
        }

    </header>
    )
}

function DropDown() {
    
    return (
        <header className='header'>
            <a href="/homepage"><img src={logo} className='logo' alt='Homepage'/></a>
            <div className='dropdown'>
                <img src={menu} className='menu' alt='Menu'/>
                <div className='dropdown-content'>
                    <a href="/contactus">Contact Us</a>
                </div>
            </div>
        </header>
    )
}
function NavBar(props) {
    const logout = async () => {
        await fetch('http://localhost:8000/api/logout', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            credentials: 'include',
        });
        props.setName('');
    }    
    const isMobile = window.innerWidth <= 768;
    return (
        <div>
            {isMobile ? <DropDown/> : <Desktop name={props.name} setName={props.setName} logout={logout}/>}
        </div>
    );
}

export default NavBar;