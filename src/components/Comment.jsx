import { Card } from 'react-bootstrap';

export function Comment({ text }) {
    return (
        <Card className='my-2'>
            <Card.Body>
                <Card.Title>Usuário X</Card.Title>
                <p>{ text }</p>
            </Card.Body>
        </Card>
    )
}