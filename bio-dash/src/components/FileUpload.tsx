import { useMemo, useState } from "react";
import { useDropzone } from "react-dropzone";
import { LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";
import { ImgEndpoints, sendFile } from "../utils/send-file";

const baseStyle = {
  flex: 1,
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  padding: "20px",
  borderWidth: 2,
  borderRadius: 2,
  borderColor: "#eeeeee",
  borderStyle: "dashed",
  backgroundColor: "#fafafa",
  color: "#bdbdbd",
  outline: "none",
  transition: "border .24s ease-in-out",
};

const focusedStyle = {
  borderColor: "#2196f3",
};

const acceptStyle = {
  borderColor: "#00e676",
};

const rejectStyle = {
  borderColor: "#ff1744",
};

export const FileUpload = () => {
  const [imgEndpoint, setImgEndpoint] = useState({} as ImgEndpoints);

  const {
    getRootProps,
    getInputProps,
    isFocused,
    isDragAccept,
    isDragReject,
    isDragActive,
    acceptedFiles,
  } = useDropzone({
    accept: { "text/plain": [".txt"] },
    maxFiles: 1,
    maxSize: 1000000,
  });

  const style = useMemo(
    () => ({
      ...baseStyle,
      ...(isFocused ? focusedStyle : {}),
      ...(isDragAccept ? acceptStyle : {}),
      ...(isDragReject ? rejectStyle : {}),
    }),
    [isFocused, isDragAccept, isDragReject]
  );

  const files = acceptedFiles.map((file) => <p key={file.name}>{file.name}</p>);
  //if (files.length === 1) sendFile(acceptedFiles[0], setImgEndpoint);
  // TODO: parse file to get dates
  return (
    <div className="container" style={{ backgroundColor: "white" }}>
      <div {...getRootProps({ style })}>
        <input {...getInputProps()} />
        {isDragActive ? (
          <p>Drop the files here...</p>
        ) : (
          <p>Drag and drop some files here, or click to select files</p>
        )}
      </div>

      {files.length > 0 ? (
        <>
          <div style={{ color: "black" }}>
            <h4>File</h4>
            <p>{files}</p>
          </div>
          <LocalizationProvider dateAdapter={AdapterDayjs}>
            <DatePicker />
            <DatePicker />
          </LocalizationProvider>
          <button onClick={() => sendFile(acceptedFiles[0], setImgEndpoint)}>
            upload
          </button>
        </>
      ) : (
        <></>
      )}

      {imgEndpoint.activity ? (
        <>
          <img src={imgEndpoint.activity} alt="activity img" />
          <img src={imgEndpoint.sleep} alt="sleep img" />
        </>
      ) : (
        <p style={{ backgroundColor: "black" }}>ne dela</p>
      )}
    </div>
  );
};
