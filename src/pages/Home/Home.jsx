import { Container } from "react-bootstrap";
import { Heading } from "../../components/Heading";
import { Button } from "./components/Button";

export function Home() {
  return (
    <>
      <Heading />
      <Container>
        <h1>Home page</h1>
        <Button />
      </Container>
    </>
  );
}