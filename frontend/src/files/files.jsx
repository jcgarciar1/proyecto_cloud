import React, { useState, useRef, useEffect } from "react";
import { Link, useNavigate } from 'react-router-dom';
import "./files.css";

function Files() {
  const [file, setFile] = useState("");
  const [title, setTitle] = useState("Cargar Archivo");
  const [formattedFiles, setFormattedFiles] = useState([]);
  const [reload, setReload] = useState(1);
  const inputFile = useRef(null);
  const jwtToken = localStorage.getItem("token")
  let backend_url = 'http://3.90.123.49:8000'
  let navigate = useNavigate();


  useEffect(() => {
    if(!localStorage.getItem('token')){
      return navigate("/");
    }
    else{
      
    }
 }, [])

  useEffect(() => {
    fetch(`${backend_url}/api/tasks`, {
      method: 'GET', // *GET, POST, PUT, DELETE, etc.
      mode: 'cors', // no-cors, *cors, same-origin
      cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
      credentials: 'same-origin', // include, *same-origin, omit
      headers: { Authorization: `Bearer ${jwtToken}` },
      redirect: 'follow', // manual, *follow, error
      referrerPolicy: 'no-referrer',
    })
      .then((response) => response.json())
      .then((data) => setFormattedFiles(data))
  }, [])

  // Example POST method implementation:
  async function postData(url = '', data = {}) {
    console.log(`Bearer ${jwtToken}`)
    // Default options are marked with *
    const response = await fetch(url, {
      method: 'POST', // *GET, POST, PUT, DELETE, etc.
      mode: 'cors', // no-cors, *cors, same-origin
      cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
      credentials: 'same-origin', // include, *same-origin, omit
      headers: { Authorization: `Bearer ${jwtToken}` },
      redirect: 'follow', // manual, *follow, error
      referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
      body: data // body data type must match "Content-Type" header
    });
    return response.json(); // parses JSON response into native JavaScript objects
  }

  const handleFileUpload = (e) => {
    const { files } = e.target;
    if (files && files.length) {
      const fileName = files[0].name;
      const parts = fileName.split(".");
      const fileType = parts[parts.length - 1];

      setFile(files[0]);
      setTitle((ti) => `Transformando... ${fileName}`);

      //Aca se envia al back el archivo que se guardo en file, usar files[0]
      var data = new FormData()
      data.append('fileName', files[0])
      data.append('newFormat', 'zip')

      postData(`${backend_url}/api/tasks`, data)
        .then((response) => {
          setTitle((ti) => `Cargar Archivo`);
          setTimeout('', 5000);
          setReload(1)
        })
        .catch((err) => console.log("Solicitud fallida", err)); // Capturar errores
    }
  };

  const downloadFiles = (id) => {
    fetch(`${backend_url}/api/files/${id}`, {
      method: 'GET', // *GET, POST, PUT, DELETE, etc.
      mode: 'cors', // no-cors, *cors, same-origin
      cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
      credentials: 'same-origin', // include, *same-origin, omit
      headers: { Authorization: `Bearer ${jwtToken}` },
      redirect: 'follow', // manual, *follow, error
      referrerPolicy: 'no-referrer',
    })
    .then( res => res.blob() )
    .then( blob => {
      var file = window.URL.createObjectURL(blob);
      window.location.assign(file);
    })
  }

  const deleteFiles = (id) => {
    fetch(`${backend_url}/api/tasks/${id}`, {
      method: 'DELETE', // *GET, POST, PUT, DELETE, etc.
      mode: 'cors', // no-cors, *cors, same-origin
      cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
      credentials: 'same-origin', // include, *same-origin, omit
      headers: { Authorization: `Bearer ${jwtToken}` },
      redirect: 'follow', // manual, *follow, error
      referrerPolicy: 'no-referrer',
    })
    .then( response => response.json() )
  }

  const openFinder = () => {
    inputFile.current.click();
  };

  const logout = () => {
    localStorage.removeItem('token');
    return navigate("/");
  }

  return (
    <div className="container-fluid ">
      <div className="App">
        <h1>Welcome to CompressionInc!</h1>
        <button className="btn btn-primary" onClick={() => logout()}>Log out</button>
      </div>
      <input
        style={{ display: "none" }}
        ref={inputFile}
        onChange={handleFileUpload}
        type="file"
      />
      <div className="px-4">
        <div className="bg-dark text-light selector" onClick={openFinder}>
          <div className="py-5">{title}</div>
        </div>
        <div className="py-5"></div>
      </div>
      <table className="table">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">File Name</th>
            <th scope="col">Extension</th>
            <th scope="col">Status</th>
            <th scope="col">Download</th>
            <th scope="col">Delete</th>
          </tr>
        </thead>
        <tbody>
          {formattedFiles.length > 0
            ? formattedFiles.map((file, index) => (
              <>
                <tr><th scope="row">{formattedFiles[index].id}</th>
                  <td scope="row"><a href={`http://3.90.123.49:8000/api/files/${formattedFiles[index].id}`}>{formattedFiles[index].nombre_archivo}</a></td>
                  <td scope="row">{formattedFiles[index].extension_conversion}</td>
                  <td scope="row">{formattedFiles[index].status}</td>
                  <td scope="row"><button type="button" className="btn btn-primary" 
                  // onClick={downloadFile(formattedFiles[index].id)}
                  onClick={() => {downloadFiles(formattedFiles[index].id)}}
                  >Download</button></td>
                  <td scope="row"><button type="button" className="btn btn-danger" onClick={() => {deleteFiles(formattedFiles[index].id)}}>Delete</button></td>
                </tr>

                {/* <p className="py-3 text-light">
                  {" "}
                  {formattedFiles[index].nombre_archivo}
                </p>
                <div className="my-4"></div> */}
              </>
            ))
            : null}
          {/* <tr>
            <th scope="row">1</th>
            <td>Mark</td>
            <td>Otto</td>
          </tr>
          <tr>
            <th scope="row">2</th>
            <td>Jacob</td>
            <td>Thornton</td>
          </tr> */}
        </tbody>
      </table>
    </div>
  );
}

export default Files;
