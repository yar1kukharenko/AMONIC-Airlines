"use client"; // Обязательно для клиентского компонента
import React, { useEffect, useState } from "react";
import {
  Button,
  Grid2,
  MenuItem,
  Select,
  Table,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@mui/material";
import styles from "./dashboard.module.scss";
import api from "@/axiosInstance";
import classNames from "classnames";
import AddUserPopup from "@/components/AddUserPopup/AddUserPopup";

const Page = () => {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState("");
  const [selectedCell, setSelectedCell] = useState<string | null>(null);
  const [offices, setOffices] = useState([]);
  const [office, setOffice] = useState("all");
  const [openPopup, setOpenPopup] = useState(false);

  const handleOfficeChange = async (e) => {
    setOffice(e.target.value);
    if (e.target.value === "all") {
      const res = await api.get("/user/users/");
      setUsers(res.data);
      return;
    }

    const res = await api.get("/user/users/?office=" + e.target.value);
    setUsers(res.data);
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await api.get("/user/users/");
        setUsers(res.data);
        console.log(res.data);
        const officesRes = await api.get("/user/offices/");
        setOffices(officesRes.data);
      } catch (error: any) {
        console.error("Ошибка:", error.message);
        setError("Ошибка при загрузке данных.");
      }
    };

    fetchData().then((r) => console.log(r));
  }, []);

  const handleCellClick = (id: number) => {
    if (selectedCell === id) {
      setSelectedCell(null); // Если строка уже выбрана, убираем выделение
    } else {
      setSelectedCell(id); // Выделяем строку
    }
  };

  const calculateAge = (birthday: string) => {
    const birthDate = new Date(birthday);
    const ageDifMs = Date.now() - birthDate.getTime();
    const ageDate = new Date(ageDifMs); // Конвертируем разницу в дату
    return Math.abs(ageDate.getUTCFullYear() - 1970); // Вычитаем 1970 год, так как это базовый год в JavaScript
  };
  return (
    <>
      <AddUserPopup onClose={() => setOpenPopup(false)} open={openPopup} />
      <div className={styles.container}>
        <Grid2 container spacing={2}>
          <Grid2>
            <Button onClick={() => setOpenPopup(true)}>
              Добавить пользователя
            </Button>
          </Grid2>
          <Grid2>
            <Button>Выход</Button>
          </Grid2>
          <Grid2 size={12}>
            <Select
              labelId="demo-simple-select-label"
              id="demo-simple-select"
              value={office}
              onChange={handleOfficeChange}
              autoWidth={true}
            >
              <MenuItem value={"all"}>
                <em>Все офисы</em>
              </MenuItem>
              {offices.map((office, index) => {
                return (
                  <MenuItem key={office.id} value={office.id}>
                    {office.title}
                  </MenuItem>
                );
              })}
            </Select>
          </Grid2>
          <Grid2 size={12}>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Имя</TableCell>
                    <TableCell>Фамилия</TableCell>
                    <TableCell>Возраст</TableCell>
                    <TableCell>Роль</TableCell>
                    <TableCell>Email</TableCell>
                    <TableCell>Офис</TableCell>
                  </TableRow>
                </TableHead>
                <tbody>
                  {users.map((user) => (
                    <TableRow
                      onClick={() => handleCellClick(user.id)}
                      className={classNames(
                        user.id === selectedCell && styles.rowSelected,
                        styles.row,
                      )}
                      key={user.id}
                    >
                      <TableCell>{user.firstname}</TableCell>
                      <TableCell>{user.lastname}</TableCell>
                      <TableCell>{calculateAge(user.birthdate)}</TableCell>
                      <TableCell>{user.role}</TableCell>
                      <TableCell>{user.email}</TableCell>
                      <TableCell>{user.office}</TableCell>
                    </TableRow>
                  ))}
                </tbody>
              </Table>
            </TableContainer>
          </Grid2>
          <Grid2 size={4}>
            <Button disabled={!selectedCell}>Сменить роль</Button>
          </Grid2>
          <Grid2 size={4}>
            <Button disabled={!selectedCell}> Включить/Выключить Вход</Button>
          </Grid2>
        </Grid2>
        {error && <p>{error}</p>}
      </div>
    </>
  );
};

export default Page;
