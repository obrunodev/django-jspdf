import {
  BrowserRouter as Router,
  Routes,
  Route
} from 'react-router-dom';
import { Comments } from './pages/Comments';
import { Home } from './pages/Home';

export function AppRoutes() {
  return (
    <Router>
      <Routes>
        <Route path='/' element={<Home />}></Route>
        <Route path='/comments' element={<Comments />}></Route>
      </Routes>
    </Router>
  )
}