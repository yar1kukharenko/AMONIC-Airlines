import React, { useEffect, useState } from "react";
import {
  Box,
  Button,
  Dialog,
  DialogTitle,
  FormHelperText,
  InputLabel,
  MenuItem,
  Select,
  Stack,
  TextField,
} from "@mui/material";
import api from "@/axiosInstance";
import { DatePicker, LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import dayjs from "dayjs"; // Импортируем dayjs для работы с датами
import "dayjs/locale/ru";

interface AddUserPopupProps {
  onClose: () => void;
  open: boolean;
}

interface AddUserData {
  email: string;
  password: string;
  firstname: string;
  lastname: string;
  office: number;
  birthdate: string;
}

const AddUserPopup: React.FC<AddUserPopupProps> = ({ onClose, open }) => {
  const [formData, setFormData] = useState<AddUserData>({
    email: "",
    password: "",
    firstname: "",
    lastname: "",
    office: 0,
    birthdate: "",
  });

  const [offices, setOffices] = useState([]);
  const [office, setOffice] = useState("all");

  const [lastname, setLastname] = useState("");
  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [selectedDate, setSelectedDate] = React.useState(dayjs()); // Устанавливаем начальное значение как dayjs объект
  const [password, setPassword] = useState("");

  const [helperText, setHelperText] = useState("");

  const handleDateChange = (newDate) => {
    console.log(newDate.format("DD-MM-YYYY"));
    setSelectedDate(newDate);
  };

  const handleOfficeChange = async (e) => {
    setOffice(e.target.value);
  };

  const onSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const data = {
      ...formData,
      office: office,
      birthdate: selectedDate.format("YYYY-MM-DD"),
      password: password,
      firstname: name,
      email: email,
      lastname: lastname,
    };

    const res = await api.post("/user/add-user/", data);

    if (res.status === 201) {
      onClose();
    } else {
      setHelperText("Ошибка при добавлении пользователя");
      console.log(res.data);
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const officesRes = await api.get("/user/offices/");
        setOffices(officesRes.data);
        setOffice(officesRes.data[0].id);
      } catch (error) {
        console.error("Ошибка:", error.message);
      }
    };

    fetchData();
  }, []);

  return (
    <Dialog open={open}>
      <DialogTitle>Добавить пользователя</DialogTitle>
      <form onSubmit={onSubmit}>
        <Box sx={{ padding: 2 }}>
          <Stack spacing={2}>
            <TextField
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              label="Email"
            ></TextField>
            <TextField
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              label="Имя"
            ></TextField>
            <TextField
              value={lastname}
              onChange={(e) => setLastname(e.target.value)}
              required
              label="Фамилия"
            ></TextField>
            <InputLabel id="demo-simple-select-label">Офис</InputLabel>
            <Select
              labelId="demo-simple-select-label"
              id="demo-simple-select"
              value={office}
              onChange={handleOfficeChange}
              autoWidth={true}
            >
              {offices.map((office) => {
                return (
                  <MenuItem key={office.id} value={office.id}>
                    {office.title}
                  </MenuItem>
                );
              })}
            </Select>
            <LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale="ru">
              <DatePicker
                label="Выберите дату"
                value={selectedDate}
                onChange={handleDateChange}
                renderInput={(params) => (
                  <TextField {...params} helperText={null} />
                )}
              />
            </LocalizationProvider>
            <TextField
              required
              label="Пароль"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <FormHelperText></FormHelperText>
            <Stack direction="row" spacing={2}>
              <Button type={"submit"} variant={"contained"}>
                Добавить
              </Button>
              <Button onClick={onClose} type={"button"} variant={"text"}>
                Закрыть
              </Button>
            </Stack>
          </Stack>
        </Box>
      </form>
    </Dialog>
  );
};

export default AddUserPopup;
