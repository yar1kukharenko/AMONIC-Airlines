"use client";
import axios from "axios";
import { useEffect, useState } from "react";

import styles from "./test.module.scss";

export default function Home() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    axios
      .get("http://localhost:8000/api/items/")
      .then((response) => {
        setItems(response.data);
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

  return (
    <div>
      <h1 className={styles.heading}> Список предметов</h1>
      <ul>
        {items.map((item) => (
          <li key={item.id}>
            {item.name}: {item.description}
          </li>
        ))}
      </ul>
    </div>
  );
}
