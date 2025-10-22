import axios from "axios";

const baseURL = import.meta.env.VITE_API_BASE || "http://localhost:8000/";

const axiosInstance = axios.create({
  baseURL,
});

axiosInstance.interceptors.request.use(
  (config) => {
    const access = localStorage.getItem("access_token");
    if (access) {
      config.headers["Authorization"] = `Bearer ${access}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If 401 Unauthorized and we haven't retried yet
    if (
      error.response &&
      error.response.status === 401 &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;

      const refresh = localStorage.getItem("refresh_token");
      if (!refresh) {
        // No refresh token, force logout
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        window.location.href = "/"; 
        return Promise.reject(error);
      }

      try {
        // Get new access token
        const { data } = await axios.post(
          `${baseURL.replace(/\/$/, "")}/accounts/token/refresh/`,
          { refresh }
        );

        const newAccess = data.access;

        // Save new access token
        localStorage.setItem("access_token", newAccess);
        localStorage.setItem("refresh_token", refresh); // Optionally update refresh token if provided
        axiosInstance.defaults.headers["Authorization"] = `Bearer ${newAccess}`;
        originalRequest.headers["Authorization"] = `Bearer ${newAccess}`;

        // Retry original request
        return axiosInstance(originalRequest);
      } catch (refreshError) {
        // Refresh failed, logout
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        window.location.href = "/";
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default axiosInstance;