import { LocalizationProvider, DatePicker } from "@mui/x-date-pickers";
import { AdapterDateFns } from "@mui/x-date-pickers/AdapterDateFns";

export const DateInput = ({
  startDate,
  endDate,
  setStartDate,
  setEndDate,
}: {
  startDate: Date;
  endDate: Date;
  setStartDate: (value: React.SetStateAction<Date>) => void;
  setEndDate: (value: React.SetStateAction<Date>) => void;
}) => {
  return (
    <div>
      <LocalizationProvider dateAdapter={AdapterDateFns}>
        <DatePicker
          sx={{ marginBottom: "0.25rem" }}
          minDate={startDate}
          maxDate={endDate}
          value={startDate}
          onChange={(date: Date | null) => {
            if (date !== null) setStartDate(new Date(date));
          }}
        />
        <br />
        <DatePicker
          minDate={startDate}
          maxDate={endDate}
          value={endDate}
          onChange={(date: Date | null) => {
            if (date !== null) setEndDate(new Date(date));
          }}
        />
      </LocalizationProvider>
    </div>
  );
};
