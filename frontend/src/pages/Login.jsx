import { useState } from "react";
import styles from "../styles/Login.module.css";
import { iniciarSesion } from "../services/CargarProductos";

export function LoginForm({ className = "", onLogin, ...props }) {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormData((current) => ({
      ...current,
      [name]: value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setIsSubmitting(true);

    try {
      const data = await iniciarSesion(formData.email, formData.password);
      onLogin(data.access_token);
    } catch (loginError) {
      setError(loginError.message);
    } finally {
      setIsSubmitting(false);
    }
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

          {error && <p role="alert">{error}</p>}

          <button
            type="submit"
            className={styles.primaryButton}
            disabled={isSubmitting}
          >
            {isSubmitting ? "Ingresando..." : "Entrar"}
          </button>

        </form>
      </div>
    </div>
  );
}

export default LoginForm;
