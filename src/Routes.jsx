import {
  BrowserRouter as Router,
  Routes,
  Route
} from 'react-router-dom';
import { Comments } from './pages/Comments';
import { Home } from './pages/Home';
import { Sorteio } from './pages/Sorteio';

export function AppRoutes() {
  return (
    <Router>
      <Routes>
        <Route path='/' element={<Home />}></Route>
        <Route path='/comments' element={<Comments />}></Route>
        <Route path='/sorteio' element={<Sorteio />}></Route>
      </Routes>
    </Router>
  )
}