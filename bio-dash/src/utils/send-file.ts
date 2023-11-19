import { BACKEND_URL } from "../constants/env-development";

export type ImgEndpoints = {
  sleep: string;
  activity: string;
  zip?: string;
};

export const sendFile = (
  file: File,
  setImgEndpoint: (value: React.SetStateAction<ImgEndpoints>) => void,
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

  fetch(BACKEND_URL + "/file-upload", {
    method: "post",
    body: formData,
  }).then(async (val) => {
    const response: { fileName: string } = await val.json();
    setImgEndpoint({
      sleep: BACKEND_URL + "/img/sleep/" + response.fileName,
      activity: BACKEND_URL + "/img/activity/" + response.fileName,
      zip: BACKEND_URL + "/zip/" + response.fileName,
    });
  });
};
