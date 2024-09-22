"use client";
import React, { useState } from "react";
import { setCookie } from "nookies";

const Page = () => {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

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
        setSuccess("Успешно зарегистрированы");
      } else {
        const errorMessages = Object.values(data).flat().join(" ");

        setError(errorMessages || "Ошибка при регистрации");
      }
    } catch (err) {
      console.error(err);
      setError("Произошла ошибка при отправке данных");
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor={"email"}>Username</label>
          <input
            onChange={handleChange}
            id={"email"}
            name={"email"}
            type="email"
            required
          />
        </div>
        <div>
          <label htmlFor={"password"}>Password</label>
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
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default Page;
