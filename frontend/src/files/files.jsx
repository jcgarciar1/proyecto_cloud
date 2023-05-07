import React, { useState, useRef, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./files.css";

function Files() {
  const [file, setFile] = useState("");
  const [title, setTitle] = useState("Cargar Archivo");
  const [formattedFiles, setFormattedFiles] = useState([]);
  const [reload, setReload] = useState(1);
  const [type, setType] = useState(1);
  const inputFile = useRef(null);
  const jwtToken = localStorage.getItem("token");
  let backend_url = "http://34.160.47.154";
  //var backend_url   = process.env.BACKEND_URL;
  let navigate = useNavigate();

  useEffect(() => {
    if (!localStorage.getItem("token")) {
      return navigate("/");
    } else {
    }
  }, []);

  useEffect(() => {
    fetch(`${backend_url}/api/tasks`, {
      method: "GET", // *GET, POST, PUT, DELETE, etc.
      mode: "cors", // no-cors, *cors, same-origin
      cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
      credentials: "same-origin", // include, *same-origin, omit
      headers: { Authorization: `Bearer ${jwtToken}` },
      redirect: "follow", // manual, *follow, error
      referrerPolicy: "no-referrer",
    })
      .then((response) => response.json())
      .then((data) => setFormattedFiles(data));
  }, []);

  // Example POST method implementation:
  async function postData(url = "", data = {}) {
    console.log(`Bearer ${jwtToken}`);
    // Default options are marked with *
    const response = await fetch(url, {
      method: "POST", // *GET, POST, PUT, DELETE, etc.
      mode: "cors", // no-cors, *cors, same-origin
      cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
      credentials: "same-origin", // include, *same-origin, omit
      headers: { Authorization: `Bearer ${jwtToken}` },
      redirect: "follow", // manual, *follow, error
      referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
      body: data, // body data type must match "Content-Type" header
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
      var data = new FormData();
      data.append("fileName", files[0]);
      data.append("newFormat", type);

      postData(`${backend_url}/api/tasks`, data)
        .then((response) => {
          setTitle((ti) => `Cargar Archivo`);
          setTimeout("", 5000);
          setReload(1);
        })
        .catch((err) => console.log("Solicitud fallida", err)); // Capturar errores
    }
  };

  const downloadFiles = (id) => {
    fetch(`${backend_url}/api/files/${id}`, {
      method: "GET", // *GET, POST, PUT, DELETE, etc.
      mode: "cors", // no-cors, *cors, same-origin
      cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
      credentials: "same-origin", // include, *same-origin, omit
      headers: { Authorization: `Bearer ${jwtToken}` },
      redirect: "follow", // manual, *follow, error
      referrerPolicy: "no-referrer",
    })
      .then((res) => res.blob())
      .then((blob) => {
        var file = window.URL.createObjectURL(blob);
        window.location.assign(file);
      });
  };

  const deleteFiles = (id) => {
    fetch(`${backend_url}/api/tasks/${id}`, {
      method: "DELETE", // *GET, POST, PUT, DELETE, etc.
      mode: "cors", // no-cors, *cors, same-origin
      cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
      credentials: "same-origin", // include, *same-origin, omit
      headers: { Authorization: `Bearer ${jwtToken}` },
      redirect: "follow", // manual, *follow, error
      referrerPolicy: "no-referrer",
    }).then((response) => response.json());
  };

  const openFinder = () => {
    inputFile.current.click();
  };

  const logout = () => {
    localStorage.removeItem("token");
    return navigate("/");
  };

  const onChangeValue = (e) => {
    setType(e.target.value);
  };

  return (
    <div className="container-fluid ">
      <div className="App">
        <div className="sombra">
          <div>
            <div className="navbar-mia">
              <img
                className="logo-mia"
                src={require("../img/zip-folder.png")}
                alt="logo"
              />
              <ul>
                <li>
                  <a href="/" onClick={() => logout()}>
                    Cerrar Sesión
                  </a>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <h1>Bienvenido a CompressionInc!</h1>
      </div>
      <input
        style={{ display: "none" }}
        ref={inputFile}
        onChange={handleFileUpload}
        type="file"
      />
      <div onChange={onChangeValue}>
        <h5>Selecciona el tipo de compresión que deseas:</h5>
        <div className="center-button">
          <label className="block">
            <input type="radio" value="zip" name="gender" /> zip{" "}
          </label>
          <label className="block">
            <input type="radio" value="tar.gz" name="gender" /> tar.gz
          </label>
          <label className="block">
            <input type="radio" value="tar.bz2" name="gender" /> tar.bz2
          </label>
        </div>
      </div>
      <br />
      <div className="boton" onClick={openFinder}>
        <div>{title}</div>
      </div>
      <br />
      <br />
      <link
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css"
        rel="stylesheet"
        integrity="sha384-gH2yIJqKdNHPEq0n4Mqa/HGKIhSkIHeL5AyhkYV8i59U5AR6csBvApHHNl/vI1Bx"
        crossorigin="anonymous"
      />

      <i class="bi bi-trash"></i>

      <table className="table">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">Nombre</th>
            <th scope="col">Extensión</th>
            <th scope="col">Status</th>
            <th scope="col">Descargar</th>
            <th scope="col">Eliminar</th>
          </tr>
        </thead>
        <tbody>
          {formattedFiles.length > 0
            ? formattedFiles.map((file, index) => (
                <>
                  <tr>
                    <th scope="row">{formattedFiles[index].id}</th>
                    <td scope="row">
                      <a
                        href={`http://3.90.123.49:8000/api/files/${formattedFiles[index].id}`}
                      >
                        {formattedFiles[index].nombre_archivo}
                      </a>
                    </td>
                    <td scope="row">
                      {formattedFiles[index].extension_conversion}
                    </td>
                    <td scope="row">{formattedFiles[index].status}</td>
                    <td scope="row">
                      <button
                        type="button"
                        className="btn btn-primary"
                        // onClick={downloadFile(formattedFiles[index].id)}
                        onClick={() => {
                          downloadFiles(formattedFiles[index].id);
                        }}
                      >
                        Descargar
                      </button>
                    </td>
                    <td scope="row">
                      <button
                        type="button"
                        className="btn btn-danger"
                        onClick={() => {
                          deleteFiles(formattedFiles[index].id);
                        }}
                      >
                        Eliminar
                      </button>
                    </td>
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
