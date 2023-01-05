import { Container } from "react-bootstrap";
import { NavigationBar } from "../components/NavigationBar";

export function Home() {
  return (
    <div>
      <NavigationBar />
      <Container>
        <h1>Home page</h1>
      </Container>
    </div>
  )
}