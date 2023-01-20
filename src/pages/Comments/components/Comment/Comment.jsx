import { Button, Card } from 'react-bootstrap';

export function Comment({ text }) {
  return (
    <Card className='my-2'>
      <Card.Body>
        <Card.Title>Usuário X</Card.Title>
        <p>{ text }</p>
        <Button variant='dark'>Responder</Button>
      </Card.Body>
    </Card>
  )
}