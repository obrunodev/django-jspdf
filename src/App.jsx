import { useState } from 'react'
import './App.css'

function App() {
  const [contador, setContador] = useState(0)

  const handleContador = () => setContador(contador => contador + 1);

  return (
    <div>
      <p>Contador: {contador}</p>
      <button onClick={handleContador}>Incrementar</button>
    </div>
  )
}

export default App
