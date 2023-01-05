import { useState } from 'react'
import { Button, Alert, Container } from 'react-bootstrap';
import './App.css'

function App() {
  const variants = ['primary', 'warning', 'danger'];

  const [contador, setContador] = useState(0);
  const handleContador = () => setContador(contador => contador + 1);

  return (
    <Container>
      <p>Contador: {contador}</p>
      <Button variant='primary' onClick={handleContador}>Incrementar</Button>
      <div className="my-2">
        {variants.map(variant => (
          <Alert variant={variant}>Esse é um alerta de {variant}</Alert>
        ))}
      </div>
    </Container>
  )
}

export default App
