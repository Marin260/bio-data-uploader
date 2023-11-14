import { BACKEND_URL } from "../constants/env-development";

export type ImgEndpoints = {
  sleep: string;
  activity: string;
};

export const sendFile = (
  file: File,
  setImgEndpoint: (value: React.SetStateAction<ImgEndpoints>) => void
) => {
  const formData = new FormData();
  formData.append("file", file);

  fetch(BACKEND_URL + "/file-upload", {
    method: "post",
    body: formData,
  }).then(async (val) => {
    const response: { fileName: string } = await val.json();
    setImgEndpoint({
      sleep: BACKEND_URL + "/img/sleep/" + response.fileName,
      activity: BACKEND_URL + "/img/activity/" + response.fileName,
    });
  });
};
