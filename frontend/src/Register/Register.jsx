import React, { Component } from 'react';
import { useState, useEffect } from 'react';
import { useNavigate } from "react-router-dom";
import '../App.css'
import './Register.css'

let backend_url = 'http://192.168.10.17:8000/'
let validEmailRegex = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/
let incorrectEmail = <p>Incorrect email format. Please change it</p>
let usedEmailText = <p>Email in use. Please change it</p>
let emptyFieldText = <p>Empty field, please change it</p>
let notSamePasswordText = <p>Password is not the same, please change</p>
let spinner = (<div className="spinner-border text-primary" role="status">
    <span className="visually-hidden">Loading...</span>
</div>)

// Example POST method implementation:
async function postData(url = '', data = {}) {
    // Default options are marked with *
    const response = await fetch(url, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
            'Content-Type': 'application/json'
            // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        body: JSON.stringify(data) // body data type must match "Content-Type" header
    });
    return response.json(); // parses JSON response into native JavaScript objects
}

const Register = () => {
    let navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [correctEmail, setCorrectEmail] = useState(true);
    const [password, setPassword] = useState('');
    const [password2, setPassword2] = useState('');
    const [samePsswd, setSamePsswd] = useState(false);
    const [username, setUserName] = useState('');
    const [usedEmail, setUsedEmail] = useState(false);
    const [emptyField, setEmptyField] = useState(false);
    const [loading, setLoading] = useState(false);

    const passwdEffect = useEffect(() => {
        if (password === password2) {
            setSamePsswd(false)
        }
        else {
            setSamePsswd(true)
        }
    }, [password2])


    const handleEmailChange = (event) => {
        // 👇 Get input value from "event"
        setEmail(event.target.value);
        if (!event.target.value.match(validEmailRegex)) {
            setCorrectEmail(false)
        }
        else {
            setCorrectEmail(true)
        }
    };

    const handlePasswordChange = (event) => {
        // 👇 Get input value from "event"
        setPassword(event.target.value);
    };

    const handlePassword2Change = (event) => {
        // 👇 Get input value from "event"
        setPassword2(event.target.value);
    };

    const handleUserNameChange = (event) => {
        // 👇 Get input value from "event"
        setUserName(event.target.value);
    };

    const registerEvent = () => {
        // 👇 Get input value from "event"
        // Hacer una petición para un usuario con ID especifico

        if (password.length != 0 && username.length != 0 && email.length != 0 && correctEmail && !samePsswd) {
            setUsedEmail(false)
            setEmptyField(false)
            setLoading(true)
            const jsonDataLoad =  {
                "usuario":username,
                "email":email, 
                "password1": password, 
                "password2":password2
            }
            postData(`${backend_url}/api/auth/registro`, jsonDataLoad)
                .then((response) => {
                    if (response.message.includes('ya está registrado')) {
                        setUsedEmail(true)
                    }
                    else {
                        return navigate('/')
                    }
                })
                .catch(err => console.log('Solicitud fallida', err)); // Capturar errores
        }
        else {
            setEmptyField(true)
        }
        setTimeout(() => {
            setLoading(false)
        }, 2000);

    };
    return (
        <>
            <div className="App">
                <h1>Register into CompressionInc!</h1>
            </div>
            <div><div className="mb-3">
                <label htmlFor="userEmail" className="form-label">Email address:</label>
                <input type="email" className="form-control" id="userEmail" placeholder="name@example.com" onChange={handleEmailChange} />
                {(correctEmail ? null : incorrectEmail)}
            </div>
                <div className="mb-3">
                    <label htmlFor="userPassword" className="form-label">Password:</label>
                    <input type="password" className="form-control" id="userPassword" placeholder="Your Password" onChange={handlePasswordChange} />
                </div>
                <div className="mb-3">
                    <label htmlFor="userPassword" className="form-label">Insert the password again:</label>
                    <input type="password" className="form-control" id="userPassword" placeholder="Your Password" onChange={handlePassword2Change} />
                    {(samePsswd ? notSamePasswordText : null)}
                </div>
                <div className="mb-3">
                    <label htmlFor="userName" className="form-label">Username:</label>
                    <input type="text" className="form-control" id="userName" placeholder="Username" onChange={handleUserNameChange} />
                </div>
                {(loading ? spinner : (<button type="button" className="btn btn-primary" onClick={registerEvent}>Register</button>))}
                {(usedEmail ? usedEmailText : null)}
                {(emptyField ? emptyFieldText : null)}
            </div>
        </>)
}

export default Register;