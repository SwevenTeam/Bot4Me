import { render, screen } from '@testing-library/react';
import AudioRecorder from '../components/AudioRecorder';

test('test AudioRecorder render', () => {
  render(<AudioRecorder />);
  const linkElement = screen.getByText(/Registra/i);
  expect(linkElement).toBeInTheDocument();
});
