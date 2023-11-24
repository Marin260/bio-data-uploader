import { useMemo, useState } from "react";
import { useDropzone } from "react-dropzone";
import { ZipEndpoints, sendFile } from "../utils/send-file";
import { readFile } from "../utils/read-file";
import { Button, CircularProgress } from "@mui/material";
import { FileDetails } from "./FileDetails";
import { DateInput } from "./DateInput";
import FileUploadIcon from "@mui/icons-material/FileUpload";
import { DownloadButton } from "./DownloadButton";
import { RequestErrorSnackbar } from "./RequestErrorSnackbar";
import "./../styles/FileUpload.css";

const baseStyle = {
  flex: 1,
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  padding: "80px",
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
  const [zipEndpoint, setZipEndpoint] = useState({} as ZipEndpoints);
  const [startDate, setStartDate] = useState(new Date());
  const [endDate, setEndDate] = useState(new Date());
  const [loadingState, setLoadingState] = useState(false);
  const [open, setOpen] = useState(false);

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
    <div
      className="container"
      style={{ backgroundColor: "white", padding: "1rem" }}
    >
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
      {files.length > 0 && (
        <>
          <div className="file-upload">
            <FileDetails file={acceptedFiles[0]} />
            <DateInput
              startDate={startDate}
              endDate={endDate}
              setStartDate={setStartDate}
              setEndDate={setEndDate}
            />
          </div>
          <Button
            variant="contained"
            endIcon={<FileUploadIcon />}
            onClick={() =>
              sendFile(
                acceptedFiles[0],
                setZipEndpoint,
                setLoadingState,
                setOpen,
                {
                  startDate: startDate.toLocaleDateString("en-UK"),
                  endDate: endDate.toLocaleDateString("en-UK"),
                }
              )
            }
          >
            Upload
          </Button>
        </>
      )}

      {zipEndpoint.zip && (
        <>
          <br />
          <DownloadButton zipEndpoint={zipEndpoint} />
        </>
      )}

      {loadingState && (
        <>
          <br />
          <CircularProgress sx={{ marginTop: "0.5rem" }} />
        </>
      )}
      {open && <RequestErrorSnackbar open={open} setOpen={setOpen} />}
    </div>
  );
};

// TODO: get zip by fetch to avoid one time download
