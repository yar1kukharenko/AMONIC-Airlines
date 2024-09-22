"use client";
import React, { useEffect, useState } from "react";
import { setCookie } from "nookies";

const Page = () => {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const [attempts, setAttempts] = useState(0);
  const [timer, setTimer] = useState(0); // Добавляем состояние таймера
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const { password, email } = formData;

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (timer > 0) {
      return; // Если таймер еще не завершился, блокируем дальнейшие попытки
    }

    try {
      const res = await fetch("http://localhost:8000/api/user/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          password,
        }),
      });

      const data = await res.json();
      console.log(data);

      if (res.ok) {
        setCookie(null, "accessToken", data.accessToken, {
          maxAge: 30 * 24 * 60 * 60,
          path: "/",
        });

        setCookie(null, "refreshToken", data.refreshToken, {
          maxAge: 30 * 24 * 60 * 60,
          path: "/",
        });
        setSuccess("Успешно вошли в систему");
        setAttempts(0); // Сбрасываем количество попыток при успешном входе
      } else {
        const errorMessages = Object.values(data).flat().join(" ");
        setAttempts(attempts + 1);

        if (attempts + 1 >= 3) {
          setTimer(10); // Запускаем таймер на 10 секунд при 3 неудачных попытках
        }

        setError(errorMessages || "Ошибка при входе");
      }
    } catch (err) {
      console.error(err);
      setError("Произошла ошибка при отправке данных");
    }
  };

  // Эффект для таймера, который будет отсчитывать время
  useEffect(() => {
    if (timer > 0) {
      const countdown = setInterval(() => {
        setTimer((prev) => prev - 1);
      }, 1000);

      // Очищаем интервал, когда таймер завершится
      return () => clearInterval(countdown);
    }
  }, [timer]);

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor={"email"}>Email</label>
          <input
            onChange={handleChange}
            id={"email"}
            name={"email"}
            type="email"
            required
          />
        </div>
        <div>
          <label htmlFor={"password"}>Пароль</label>
          <input
            onChange={handleChange}
            id={"password"}
            name={"password"}
            type="password"
            required
          />
        </div>
        <div>
          {error && <div style={{ color: "red" }}>{error}</div>}
          {success && <div style={{ color: "green" }}> {success}</div>}
        </div>
        <div>
          {timer > 0 && (
            <div style={{ color: "red" }}>
              Попробуйте снова через {timer} секунд
            </div>
          )}
        </div>
        <button disabled={timer > 0} type="submit">
          Войти
        </button>
      </form>
    </div>
  );
};

export default Page;
