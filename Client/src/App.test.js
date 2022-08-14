import { render, screen } from '@testing-library/react';
import App from './App';

test('test main chat render', () => {
  render(<App />);
  const linkElement = screen.getByText(/Benvenuto su Bot4Me, sarò il tuo assistente personale 😄/i);
  expect(linkElement).toBeInTheDocument();
});

test('test main chat info 1 render', () => {
  render(<App />);
  const linkElement = screen.getByText(/Posso aiutarti a semplificare i tuoi compiti aziendali come:/i);
  expect(linkElement).toBeInTheDocument();
});

test('test main chat info 3 render', () => {
  render(<App />);
  const linkElement = screen.getByText(/Registrare la tua presenza in sede/i);
  expect(linkElement).toBeInTheDocument();
});

test('test main chat info 2 render', () => {
  render(<App />);
  const linkElement = screen.getByText(/Inserire rendiconto ore/i);
  expect(linkElement).toBeInTheDocument();
});

test('test main chat info 4 render', () => {
  render(<App />);
  const linkElement = screen.getByText(/Aprire il cancello aziendale/i);
  expect(linkElement).toBeInTheDocument();
});

test('test main chat info 5 render', () => {
  render(<App />);
  const linkElement = screen.getByText(/E molto altro .../i);
  expect(linkElement).toBeInTheDocument();
});

test('test main chat info 6 render', () => {
  render(<App />);
  const linkElement = screen.getByText(/Mettimi alla prova!/i);
  expect(linkElement).toBeInTheDocument();
});

