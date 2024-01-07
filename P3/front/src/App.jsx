import { useState } from 'react'
import './App.css'
import Navigation from './components/Navigation.jsx'
import Results from './components/Results.jsx'
import { useEffect } from 'react'; // Add missing import statement

function App() {
  const [productos, setProductos] = useState([])
  const [productosF, setProductosF] = useState([])
  const [categorias, setCategorias] = useState([])

  const cambiado = (evento) => {
    if (evento.target.value !== "") {
      //usamos === para hacer una comparación exacta de la categoria, ya que sino las de men se pueden mezclar con women
      const filteredProductos = productos.filter((producto) => producto.category === evento.target.value);
      setProductosF(filteredProductos);
    } else {
      setProductosF(productos);
    }
  
    console.log(evento.target.value);
  };

  useEffect(() => {
    fetch("http://localhost:8000/etienda/api/getproducts?since=0&to=100")
      .then((response) => response.json())
      .then((prods) => {
        setProductos(prods)
        const uniqueCategorias = Array.from(new Set(prods.map((producto) => producto.category)));
        setCategorias(uniqueCategorias);
        setProductosF(prods)
      });
  }, [])

  return (
    <>
      <Navigation cambiado={cambiado} setProductosF={setProductosF} categorias={categorias}/>
      <Results productos={productosF}/>
    </>
  )
}

export default App