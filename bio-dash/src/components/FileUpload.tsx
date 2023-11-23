import { useMemo, useState } from "react";
import { useDropzone } from "react-dropzone";
import { LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDateFns } from "@mui/x-date-pickers/AdapterDateFns";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";
import { ZipEndpoints, sendFile } from "../utils/send-file";
import { readFile } from "../utils/read-file";
import { CircularProgress } from "@mui/material";

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
  const [imgEndpoint, setImgEndpoint] = useState({} as ZipEndpoints);
  const [startDate, setStartDate] = useState(new Date());
  const [endDate, setEndDate] = useState(new Date());
  const [loadingState, setLoadingState] = useState(false);

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
    onDrop: (files: File[]) => {
      files.forEach((file) => {
        readFile(file, setStartDate, setEndDate);
      });
    },
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

  return (
    <div className="container" style={{ backgroundColor: "white" }}>
      {
        //@ts-ignore
        <div {...getRootProps({ style })}>
          <input {...getInputProps()} />
          {isDragActive ? (
            <p>Drop the files here...</p>
          ) : (
            <p>Drag and drop some files here, or click to select files</p>
          )}
        </div>
      }
      {files.length > 0 ? (
        <>
          <div style={{ color: "black" }}>
            <h4>File</h4>
            <p>{files}</p>
          </div>
          <LocalizationProvider dateAdapter={AdapterDateFns}>
            <DatePicker
              minDate={startDate}
              maxDate={endDate}
              value={startDate}
              onChange={(date: Date | null) => {
                if (date !== null) setStartDate(new Date(date));
              }}
            />
            <DatePicker
              minDate={startDate}
              maxDate={endDate}
              value={endDate}
              onChange={(date: Date | null) => {
                if (date !== null) setEndDate(new Date(date));
              }}
            />
          </LocalizationProvider>
          <br />
          <button
            onClick={() =>
              sendFile(acceptedFiles[0], setImgEndpoint, setLoadingState, {
                startDate: startDate.toLocaleDateString("en-UK"),
                endDate: endDate.toLocaleDateString("en-UK"),
              })
            }
          >
            upload
          </button>
        </>
      ) : (
        <></>
      )}

      {imgEndpoint.zip && (
        <>
          <br />
          <a href={imgEndpoint.zip} download="aljo">
            Download Results
          </a>
        </>
      )}

      {loadingState && (
        <>
          <br />
          <CircularProgress />
        </>
      )}
    </div>
  );
};

// TODO: get zip by fetch to avoid one time download
// TODO: clean up the frontend (styles, generalize code, etc...)
