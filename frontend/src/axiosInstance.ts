import axios, { AxiosError, AxiosRequestConfig, AxiosResponse } from "axios";
import nookies, { setCookie } from "nookies";

// Определяем интерфейс для ответа от сервера на обновление токена
interface RefreshTokenResponse {
  access: string;
  refresh?: string;
}

// Создаем axios instance
const api = axios.create({
  baseURL: "http://localhost:8000/api/",
  withCredentials: true, // Разрешаем отправку куков
});

// Интерсептор для запросов
api.interceptors.request.use(
  (config: AxiosRequestConfig) => {
    const cookies = nookies.get();
    console.log(cookies);
    const accessToken = cookies.access;

    if (accessToken && config.headers) {
      config.headers["Authorization"] = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  },
);

// Интерсептор для ответов
api.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  async (error: AxiosError) => {
    const originalRequest = error.config;

    // Проверяем, если это ошибка 401 и запрос не на обновление токена
    if (
      error.response &&
      error.response.status === 401 &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;

      try {
        const cookies = nookies.get();
        const refreshToken = cookies.refresh;

        if (!refreshToken) {
          throw new Error("Refresh token отсутствует");
        }

        // Делаем запрос на обновление токена
        const { data } = await axios.post<RefreshTokenResponse>(
          "http://localhost:8000/api/user/token/refresh/",
          {
            refresh: refreshToken,
          },
        );

        // Получаем новый токен
        const newAccessToken = data.access;

        // Обновляем accessToken в cookies
        setCookie(null, "refresh", data.refresh, {
          path: "/",
        });

        // Обновляем заголовок Authorization и повторяем оригинальный запрос
        originalRequest.headers["Authorization"] = `Bearer ${newAccessToken}`;
        return api(originalRequest); // Повторяем запрос с обновленным токеном
      } catch (refreshError) {
        console.error("Не удалось обновить токен:", refreshError);
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  },
);

export default api;
