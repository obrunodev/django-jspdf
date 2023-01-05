import { useState } from 'react'
import { Button, Alert, Container } from 'react-bootstrap';
import { Comment } from './components/Comment';
import './App.css'

function App() {
  const variants = ['primary', 'warning', 'danger'];
  const comments = ['Conteúdo muito bacana', 'Me ajudou demais'];

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

      <h3 className='mt-5'>Comentários:</h3>
      {comments.map(comment => (
        <Comment text={comment} />
      ))}
    </Container>
  )
}

export default App
