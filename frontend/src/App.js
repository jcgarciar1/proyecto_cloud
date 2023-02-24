import { useState, useId } from 'react'
import './App.css'
import { Link, useNavigate } from 'react-router-dom';
import { ReactSession } from 'react-client-session';
//import { SessionContext } from './Session.jsx';
//import { EventPage } from './EventsPage/EventPage';


let incorrectEmail = <p>Incorrect email format. Please change it</p>
let validEmailRegex = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/
let emptyFieldText = <p>Empty field, please change it</p>
let backend_url = 'http://192.168.10.17:8000/'
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

function App() {
  const [email, setEmail] = useState('');
  const [correctEmail, setCorrectEmail] = useState(true);
  const [password, setPassword] = useState('');
  const [emptyField, setEmptyField] = useState(false);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState(false);
  const [showError, setShowError] = useState(false);

  let navigate = useNavigate();
  ReactSession.setStoreType("localStorage");

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

  const login = () => {
    if (password.length != 0 && email.length != 0 && correctEmail) {
      setEmptyField(false)
      const jsonDataLoad = {
        "email":email,
        "password":password
    }
      postData(`${backend_url}/api/auth/login`, jsonDataLoad)
        .then((response) => {
          if(response.message === "Sesion iniciada"){
            ReactSession.set("token", response.access_token);
          }
          else{
            setShowError(true)
            setErrorMessage(response.message)
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
  }
  return (
    <>
      <div className="App">
        <h1>Welcome to CompressionInc!</h1>
      </div>
      <div><div className="mb-3">
        <label htmlFor="userEmail" className="form-label">Email address:</label>
        <input type="email" className="form-control" id='userEmail' placeholder="name@example.com" onChange={handleEmailChange} />
        {(correctEmail ? null : incorrectEmail)}
      </div>
        <div className="mb-3">
          <label htmlFor="exampleFormControlInput1" className="form-label">Password:</label>
          <input type="password" className="form-control" id="userPassword" placeholder="Your Password" onChange={handlePasswordChange} />
        </div>
        {(loading ? spinner : <button type="button" className="btn btn-primary" onClick={login}>Login</button>)}
        {(showError ? <p>{errorMessage}</p> : null)}
        <br></br>
        {(emptyField ? emptyFieldText : null)}
        <Link to="/register">Not registered? What are you waiting?</Link></div>
    </>

  )
}

export default App