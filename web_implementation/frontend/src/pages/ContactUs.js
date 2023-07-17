import React, { useEffect, useState } from 'react';
import NavBar from '../components/NavBar';
import '../css/ContactUs.css'
import Footer from '../components/Footer';
function ContactUs() {
    const [name, setName] = useState('');
    
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
            <div className='contact-us'>
                <h1>Contact Us</h1>
                <p>Kaustubh Gupta</p>
                <p>+91 8982255359</p>
                <p>es21btech11016@iith.ac.in</p>
            </div>
            <Footer/>
        </div>
     );
}


export default ContactUs;