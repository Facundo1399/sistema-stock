import { useEffect, useState } from "react";
import styles from "../styles/StockForm.module.css";
import {
  crearProducto,
  obtenerProductos,
} from "../services/CargarProductos";
import { obtenerProveedores } from "../services/CargarProveedor";

const emptyForm = {
  codigo: "",
  nombre: "",
  precio_costo: "0",
  precio_venta: "",
  cantidad: "0",
  stock_minimo: "0",
  proveedor_id: "",
};

export default function StockForm({ token }) {
  const [formData, setFormData] = useState(emptyForm);
  const [products, setProducts] = useState([]);
  const [providers, setProviders] = useState([]);
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

    async function loadFormData() {
      setIsLoading(true);
      setError("");

      try {
        const [loadedProducts, loadedProviders] = await Promise.all([
          obtenerProductos(accessToken),
          obtenerProveedores(accessToken),
        ]);

        if (isMounted) {
          setProducts(loadedProducts);
          setProviders(loadedProviders);
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

    loadFormData();

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

    const productData = {
      codigo: formData.codigo.trim() || null,
      nombre: formData.nombre.trim(),
      precio_costo: Number(formData.precio_costo),
      precio_venta: Number(formData.precio_venta),
      cantidad: Number(formData.cantidad),
      stock_minimo: Number(formData.stock_minimo),
      proveedor_id: Number(formData.proveedor_id),
    };

    try {
      const createdProduct = await crearProducto(productData, accessToken);
      setProducts((current) => [...current, createdProduct]);
      setFormData(emptyForm);
      setSuccess("Producto cargado correctamente.");
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
          Nombre del producto
          <input
            className={styles.input}
            type="text"
            placeholder="Nombre del producto"
            name="nombre"
            value={formData.nombre}
            onChange={handleChange}
            maxLength={100}
            required
          />
        </label>

        <label className={styles.campo}>
          Código (opcional)
          <input
            className={styles.input}
            type="text"
            placeholder="Código del producto"
            name="codigo"
            value={formData.codigo}
            onChange={handleChange}
            maxLength={50}
          />
        </label>

        <label className={styles.campo}>
          Precio de costo
          <input
            className={styles.input}
            type="number"
            name="precio_costo"
            value={formData.precio_costo}
            onChange={handleChange}
            min="0"
            step="0.01"
            required
          />
        </label>

        <label className={styles.campo}>
          Precio de venta
          <input
            className={styles.input}
            type="number"
            name="precio_venta"
            value={formData.precio_venta}
            onChange={handleChange}
            min="0"
            step="0.01"
            required
          />
        </label>

        <label className={styles.campo}>
          Cantidad
          <input
            className={styles.input}
            type="number"
            name="cantidad"
            value={formData.cantidad}
            onChange={handleChange}
            min="0"
            step="1"
            required
          />
        </label>

        <label className={styles.campo}>
          Stock mínimo
          <input
            className={styles.input}
            type="number"
            name="stock_minimo"
            value={formData.stock_minimo}
            onChange={handleChange}
            min="0"
            step="1"
            required
          />
        </label>

        <label className={styles.campo}>
          Proveedor
          <select
            className={styles.input}
            name="proveedor_id"
            value={formData.proveedor_id}
            onChange={handleChange}
            required
            disabled={isLoading || providers.length === 0}
          >
            <option value="">Seleccioná un proveedor</option>
            {providers.map((provider) => (
              <option key={provider.id} value={provider.id}>
                {provider.nombre}
              </option>
            ))}
          </select>
        </label>

        {error && <p role="alert">{error}</p>}
        {success && <p role="status">{success}</p>}

        <button className={styles.boton} type="submit" disabled={isLoading || isSaving}>
          {isSaving ? "Guardando..." : "Cargar Producto"}
        </button>
      </form>

      <section aria-label="Productos existentes">
        <h2>Productos cargados</h2>
        {isLoading ? (
          <p>Cargando productos...</p>
        ) : products.length === 0 ? (
          <p>No hay productos cargados.</p>
        ) : (
          <ul>
            {products.map((product) => (
              <li key={product.id}>
                {product.nombre} — stock: {product.cantidad}
              </li>
            ))}
          </ul>
        )}
      </section>
    </main>
  );
}