import React, { useState} from 'react';
import NavBar from '../components/NavBar';
import { useNavigate } from 'react-router-dom';
import '../css/Signup.css'

function Login(props) {
    const previousUrl = sessionStorage.getItem('previousUrl');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [redirect, setRedirect] = useState(false);
    const navigate = useNavigate();

    const handleLogin = async(e) => {
        e.preventDefault();

        const response = await fetch('http://localhost:8000/api/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            credentials: 'include',
            body: JSON.stringify({
                email,
                password
            })
        });
        
        // const content = await response.json();
        // props.setName(content.name);
        setRedirect(true);
        // props.setName(content.name);
    }

    if (redirect) {
        if (previousUrl && previousUrl !== '/login') {
            navigate(previousUrl);
          } else {
            navigate('/');
          }
    }

    return (
        <div>
            <NavBar></NavBar>
            <div className='sign-up'>
                <h1>Login</h1>
                <form onSubmit={handleLogin}>
                    <input 
                        type='email'
                        placeholder='Email'
                        value={email}
                        required
                        onChange={(e) => setEmail(e.target.value)}
                    />
                    <input 
                        type='password'
                        placeholder='Password'
                        value={password}
                        required
                        onChange={(e) => setPassword(e.target.value)}
                    />
                    <button type='submit'>Submit</button>
                </form>
            </div>
        </div>
    );
}

export default Login;       