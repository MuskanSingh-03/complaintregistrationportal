import { Router, Route } from 'wouter'
import Home from './pages/Home'
import NotFound from './pages/NotFound'

export default function App() {
  return (
    <Router>
      <Route path="/" component={Home} />
      <Route component={NotFound} />
    </Router>
  )
}
