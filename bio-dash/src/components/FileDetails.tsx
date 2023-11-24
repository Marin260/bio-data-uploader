import { Card, CardContent, Typography } from "@mui/material";
import "./../styles/FileDetails.css";

export const FileDetails = ({ file }: { file: File }) => {
  const size =
    file.size < 1000000
      ? (file.size / 1000).toFixed(1) + "kb"
      : (file.size / 100000).toFixed(1) + "Mb";

  return (
    <div
      style={{
        marginBlock: "1rem",
      }}
    >
      <Card className="file-card">
        <CardContent sx={{ padding: 0 }}>
          <Typography className="file-card-title" gutterBottom>
            Uploaded file
          </Typography>
          <Typography sx={{ paddingLeft: "0.5rem" }}>{file.name}</Typography>
          <Typography
            variant="body2"
            sx={{ color: "gray", paddingLeft: "0.5rem" }}
          >
            size: {size}
          </Typography>
        </CardContent>
      </Card>
    </div>
  );
};
