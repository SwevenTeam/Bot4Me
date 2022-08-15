import { render, screen } from '@testing-library/react';
import Home from '../components/Home';

test('test Home render', () => {
  render(<Home />);
  const linkElement = screen.getByText(/Ciao sono il tuo assistente Bot4Me/i);
  expect(linkElement).toBeInTheDocument();
});
