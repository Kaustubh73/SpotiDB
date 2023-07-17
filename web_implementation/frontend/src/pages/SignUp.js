import React, { useState} from 'react';
import {useNavigate} from 'react-router-dom';
import NavBar from '../components/NavBar';
import '../css/Signup.css'
import Footer from '../components/Footer';

function SignUp(props) { 
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [redirect, setRedirect] = useState(false);

    const handleSignUp = async(e) => {
        e.preventDefault();

        await fetch('http://localhost:8000/api/register', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                name,
                email,
                password
            })
        });
        setRedirect(true);
    };
    const navigate = useNavigate();

    if (redirect) {
        navigate('/login');
    }
    return (
        <div>
            <NavBar></NavBar>
            <div className='sign-up'>
                <h1>Sign Up</h1>
                <form onSubmit={handleSignUp}>
                    <input 
                        placeholder='Name' 
                        required 
                        onChange={e => setName(e.target.value)}
                    />
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
            <Footer/>
        </div>
    );
}

export default SignUp;