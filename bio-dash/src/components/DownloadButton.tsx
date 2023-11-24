import { Button } from "@mui/material";
import { ZipEndpoints } from "../utils/send-file";

export const DownloadButton = ({
  zipEndpoint,
}: {
  zipEndpoint: ZipEndpoints;
}) => {
  return (
    <>
      <Button
        sx={{ marginTop: "0.5rem" }}
        variant="contained"
        onClick={() => {
          const link = document.createElement("a");
          link.download = `download.txt`;
          link.href = zipEndpoint.zip;
          link.click();
        }}
      >
        Download Results
      </Button>
    </>
  );
};
