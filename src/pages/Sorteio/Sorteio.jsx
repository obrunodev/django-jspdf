import { SorteioCard } from "./components/SorteioCard";
import { Heading } from "../../components/Heading";
import { Container } from "react-bootstrap";

export function Sorteio() {
  return (
    <>
      <Heading />
      <Container>
        <SorteioCard />
      </Container>
    </>
  )
}