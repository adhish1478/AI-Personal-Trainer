import { createContext, useState, useEffect } from "react";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [authData, setAuthData] = useState({
    isAuthenticated: false,
    user: JSON.parse(localStorage.getItem("user")) || null,
    access: localStorage.getItem("access_token") || null,
    refresh: localStorage.getItem("refresh_token") || null,
  });

  const isAuthenticated = !!authData.access;

  const login = (user, access, refresh) => {
    localStorage.setItem("user", JSON.stringify(user));
    localStorage.setItem("access_token", access);
    localStorage.setItem("refresh_token", refresh);
    setAuthData({ isAuthenticated: true, user, access, refresh });
  };

  const logout = () => {
    localStorage.removeItem("user");
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setAuthData({ user: null, access: null, refresh: null });
  };

  return (
    <AuthContext.Provider value={{ authData, isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};