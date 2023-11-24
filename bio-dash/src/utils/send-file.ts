import React from "react";

export type ZipEndpoints = {
  zip: string;
};

export const sendFile = (
  file: File,
  setImgEndpoint: (value: React.SetStateAction<ZipEndpoints>) => void,
  setLoadingState: (value: React.SetStateAction<boolean>) => void,
  setOpen: (value: React.SetStateAction<boolean>) => void,
  timeFrame: {
    startDate: string;
    endDate: string;
  }
) => {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("start", timeFrame.startDate);
  formData.append("end", timeFrame.endDate);

  console.log(formData);

  const BACKEND = import.meta.env.PROD
    ? import.meta.env.VITE_BACKEND_URL
    : "http://localhost:8080";

  setLoadingState(true);

  fetch(BACKEND + "/file-upload", {
    method: "post",
    body: formData,
  })
    .then(async (val) => {
      const response: { fileName?: string; error?: string; status?: number } =
        await val.json();
      if (response.fileName)
        setImgEndpoint({
          zip: BACKEND + "/zip/" + response.fileName,
        });
      else if (response.error) {
        setOpen(true);
      }
      setLoadingState(false);
    })
    .catch((err) => {
      console.log(err);
    });
};
