import { useEffect, useState } from "react";
import styles from "../styles/Proveedores.module.css";
import {
    crearProveedor,
    obtenerProveedores,
} from "../services/CargarProveedor";

const emptyForm = {
    nombre: '',
    telefono: '',
    email: '',
    direccion: ''
}

export default function CargarProveedores({ token }) {
    const [formData, setFormData] = useState(emptyForm);
    const [proveedores, setProveedores] = useState([])
    const [isLoading, setIsLoading] = useState(true);
    const [isSaving, setIsSaving] = useState(false);
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");
    const accessToken =
        token ?? (typeof localStorage !== "undefined"
            ? localStorage.getItem("access_token")
            : null);

    useEffect(() => {
        let isMounted = true;

        async function loadProviders() {
            setError("");
            try {
                const loadedProviders = await obtenerProveedores(accessToken);
                if (isMounted) {
                    setProveedores(loadedProviders);
                }
            } catch (loadError) {
                if (isMounted) {
                    setError(loadError.message);
                }
            } finally {
                if (isMounted) {
                    setIsLoading(false);
                }
            }
        }

        loadProviders();

        return () => {
            isMounted = false;
        };
    }, [accessToken]);

    function handleChange(event) {
        const { name, value } = event.target;
        setFormData((current) => ({ ...current, [name]: value }));
    }

    async function handleSubmit(event) {
        event.preventDefault();
        setError("");
        setSuccess("");
        setIsSaving(true);

        const providerData = {
            nombre: formData.nombre.trim(),
            telefono: formData.telefono.trim(),
            email: formData.email.trim() || null,
            direccion: formData.direccion.trim() || null,
        };

        try {
            const createdProvider = await crearProveedor(providerData, accessToken);
            setProveedores((current) => [...current, createdProvider]);
            setFormData(emptyForm);
            setSuccess("Proveedor cargado correctamente.");
        } catch (saveError) {
            setError(saveError.message);
        } finally {
            setIsSaving(false);
        }
    }

    return (
        <main className={styles.formularioCarga}>

            <form className={styles.form} onSubmit={handleSubmit}>

                <label className={styles.campo}>
                    Nombre del proveedor
                    <input
                        className={styles.input}
                        type="text"
                        placeholder="Proveedor"
                        name="nombre"
                        value={formData.nombre}
                        onChange={handleChange}
                        maxLength={100}
                        required
                    />
                </label>

                <label className={styles.campo}>
                    Telefono:
                    <input
                        className={styles.input}
                        type="tel"
                        placeholder="Telefono"
                        name="telefono"
                        value={formData.telefono}
                        onChange={handleChange}
                        required
                    />
                </label>

                <label className={styles.campo}>
                    E-Mail:
                    <input
                        className={styles.input}
                        type="email"
                        placeholder="Email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                    />
                </label>

                <label className={styles.campo}>
                    Direccion:
                    <input
                        className={styles.input}
                        type="text"
                        placeholder="Direccion"
                        name="direccion"
                        value={formData.direccion}
                        onChange={handleChange}
                    />
                </label>

                {error && <p role="alert">{error}</p>}
                {success && <p role="status">{success}</p>}

                <button className={styles.boton} type="submit" disabled={isSaving}>
                    {isSaving ? "Guardando..." : "Cargar proveedor"}
                </button>
            </form>

            <section aria-label="Proveedores existentes">
                <h2>Proveedores cargados</h2>
                {isLoading ? (
                    <p>Cargando proveedores...</p>
                ) : proveedores.length === 0 ? (
                    <p>No hay proveedores cargados.</p>
                ) : (
                    <ul>
                        {proveedores.map((proveedor) => (
                            <li key={proveedor.id}>
                                {proveedor.nombre} — {proveedor.telefono}
                            </li>
                        ))}
                    </ul>
                )}
            </section>
        </main>
    )
}