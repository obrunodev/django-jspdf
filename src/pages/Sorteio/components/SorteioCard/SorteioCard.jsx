import { useState } from "react";
import { Card } from "react-bootstrap"

export function SorteioCard() {
  const [number, setNumber] = useState(0);
  const sortear = () => {
    // TODO Criar método que faz 10 sorteios de números antes de definir.
    let min = Math.ceil(1);
    let max = Math.floor(50);
    setNumber(number => Math.floor(Math.random() * (max - min) + min));
    setTimeout(() => {
      for (let index = 0; index < 10; index++) {
        setNumber(number => Math.floor(Math.random() * (max - min) + min));
      }
    }, 500);
  }

  return (
    <Card>
      <Card.Body>
        <h2>Sorteio</h2>
        <p className="lead">Sorteio de rifa</p>
        <p>{ number }</p>
        <button onClick={sortear}>Contar</button>
      </Card.Body>
    </Card>
  )
}