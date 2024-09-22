"use client";
import React, { FormEvent, useState } from "react";

const Page = () => {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    confirmPassword: "",
  });

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const { password, confirmPassword, email } = formData;

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    if (password !== confirmPassword) {
      setError("Пароли не совпадают");
      return;
    }

    setError("");

    try {
      const res = await fetch("http://localhost:8000/api/user/register/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: email,
          password: password,
          password2: confirmPassword,
        }),
      });

      const data = await res.json();
      console.log("Ответ сервера:", data);
      if (res.ok) {
        setSuccess("Регистрация прошла успешно!");
      } else {
        const errorMessages = Object.values(data).flat().join(" ");
        setError(errorMessages || "Ошибка при регистрации");
      }
    } catch (err: any) {
      console.error("Ошибка:", err);
      setError("Произошла ошибка при отправке данных");
    }
  };

  return (
    <div>
      <h1>Регистрация</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="email">Электронная почта:</label>
          <input
            type="email"
            name="email"
            id="email"
            value={email}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label htmlFor="password">Пароль:</label>
          <input
            type="password"
            name="password"
            id="password"
            value={password}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label htmlFor="confirmPassword">Подтверждение пароля:</label>
          <input
            type="password"
            name="confirmPassword"
            id="confirmPassword"
            value={confirmPassword}
            onChange={handleChange}
            required
          />
        </div>
        {error && <p style={{ color: "red" }}>Ошибка: {error}</p>}
        {success && <p style={{ color: "green" }}>{success}</p>}
        <button type="submit">Зарегистрироваться</button>
      </form>
    </div>
  );
};

export default Page;
