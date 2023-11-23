export const readFile = (
  file: File,
  setStartDate: (value: React.SetStateAction<Date>) => void,
  setEndDate: (value: React.SetStateAction<Date>) => void
) => {
  const reader = new FileReader();
  reader.onload = () => {
    const fileData = reader.result;
    if (typeof fileData === "string") {
      let data = fileData.split(/\r?\n/);
      data = [data[0], data[data.length - 2]];
      data = data.map((line) => {
        console.log(line);
        const columns = line.split(/\t/);
        return columns[1];
      });
      setStartDate(new Date(data[0]));
      setEndDate(new Date(data[1]));
    }
  };
  reader.readAsText(file);
};
