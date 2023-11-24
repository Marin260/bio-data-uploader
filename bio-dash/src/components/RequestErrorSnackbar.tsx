import { Alert, Snackbar } from "@mui/material";
import React from "react";

export const RequestErrorSnackbar = ({
  open,
  setOpen,
}: {
  open: boolean;
  setOpen: (value: React.SetStateAction<boolean>) => void;
}) => {
  const handleClose = (_?: React.SyntheticEvent | Event, reason?: string) => {
    if (reason === "clickaway") return;

    setOpen(false);
  };

  return (
    <>
      <Snackbar open={open} autoHideDuration={5000} onClose={handleClose}>
        <Alert severity="error">
          An error ocured, try again or contact support!
        </Alert>
      </Snackbar>
    </>
  );
};
