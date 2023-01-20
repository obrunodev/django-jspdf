import { useState } from 'react'
import { Button, Alert, Container, Card } from 'react-bootstrap';
import { Comment } from './components/Comment';
import { Heading } from '../../components/Heading';

export function Comments() {
  const variants = ['primary', 'warning', 'danger'];

  const [comments, setComments] = useState([
    'Conteúdo muito bacana',
    'Me ajudou demais',
    'Era exatamente o que eu procurava'
  ]);
  const createComment = () => {
    const commentInput = document.getElementById('commentInput');
    setComments([...comments, commentInput.value]);
    commentInput.value = '';
  }

  const [contador, setContador] = useState(0);
  const handleContador = () => setContador(contador => contador + 1);

  return (
    <div>
      <Heading />
      <Container className='my-3'>
        <Card style={{
          background: "#222",
          color: "#f8f8f8"
        }}>
          <Card.Body>
            <p>Contador: {contador}</p>
            <Button variant='primary' onClick={handleContador}>Incrementar</Button>
          </Card.Body>
        </Card>
        
        <div className="my-2">
          {variants.map(variant => (
            <Alert key={variant} variant={variant}>Esse é um alerta de {variant}</Alert>
          ))}
        </div>

        <h3 className='mt-5'>Comentários:</h3>
        {comments.map(comment => (
          <Comment key={comment} text={comment} />
        ))}

        <Card>
          <Card.Body>
            <textarea name="commentInput" id="commentInput" cols="30" rows="3" className="form-control mb-2"></textarea>
            <Button variant="dark" onClick={createComment}>Adicionar comentário</Button>
          </Card.Body>
        </Card>
      </Container>

    </div>
  )
}