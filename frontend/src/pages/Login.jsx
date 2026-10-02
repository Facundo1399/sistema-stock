import { useState } from "react";

import styles from "../styles/Login.module.css";

export function LoginForm({ className = "", ...props }) {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormData((current) => ({
      ...current,
      [name]: value,
    }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log("Login attempt:", formData);
  };

  return (
    <div className={`${styles.wrapper} ${className}`.trim()} {...props}>
      <div className={styles.card}>
        <div className={styles.header}>
          <p className={styles.eyebrow}>Bienvenido</p>
          <h1>Iniciar sesión</h1>
        </div>

        <form className={styles.form} onSubmit={handleSubmit}>
          <label className={styles.field}>
            <span>Email</span>
            <input
              name="email"
              type="email"
              placeholder="tu@email.com"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </label>

          <label className={styles.field}>
            <span>Contraseña</span>
            <input
              name="password"
              type="password"
              placeholder="••••••••"
              value={formData.password}
              onChange={handleChange}
              required
            />
          </label>

          <button type="submit" className={styles.primaryButton}>
            Entrar
          </button>

        </form>
      </div>
    </div>
  );
}

export default LoginForm;
