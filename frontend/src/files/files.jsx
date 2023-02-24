import React, { useState, useRef, useEffect } from "react";
import "./files.css";

function Files() {
  const [file, setFile] = useState("");
  const [title, setTitle] = useState("Cargar Archivo");
  const [formattedFiles, setFormattedFiles] = useState([]);
  const inputFile = useRef(null);

  const handleDownloadFile = (e) => {
    // Implementar descarga con la respuesta del back
    console.log("se descarga");
  };

  const handleFileUpload = (e) => {
    const { files } = e.target;
    if (files && files.length) {
      const fileName = files[0].name;
      const parts = fileName.split(".");
      const fileType = parts[parts.length - 1];

      setFile(files[0]);
      setTitle((ti) => `Transformando... ${fileName}`);

      //Aca se envia al back el archivo que se guardo en file, usar files[0]

      //Al recibir la respuesta
      setFormattedFiles([...formattedFiles, files[0]]);
      console.log(formattedFiles);
    }
  };

  const openFinder = () => {
    inputFile.current.click();
  };

  return (
    <div className="container-fluid ">
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
        <div>
          {formattedFiles.length > 0
            ? formattedFiles.map((file, index) => (
                <div
                  className="bg-dark text-light selector"
                  onClick={handleDownloadFile}
                  key={`file ${index}`}
                >
                  <p className="py-3 text-light">
                    {" "}
                    {formattedFiles[index].name}
                  </p>
                  <div className="my-4"></div>
                </div>
              ))
            : null}
        </div>
      </div>
    </div>
  );
}

export default Files;
