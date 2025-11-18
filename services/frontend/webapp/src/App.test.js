import { render, screen } from '@testing-library/react';
import App from './App';

test('renders compliance heading', () => {
  render(<App />);
  const heading = screen.getByText(/SOCI Compliance Control Room/i);
  expect(heading).toBeInTheDocument();
});
