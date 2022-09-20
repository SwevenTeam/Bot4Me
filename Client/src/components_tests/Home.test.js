import { fireEvent, render, screen } from "@testing-library/react";
import Home from "../components/Home";

test("test Home render", () => {
  render(<Home />);
  const linkElement = screen.getByText(/Ciao sono il tuo assistente Bot4Me/i);
  expect(linkElement).toBeInTheDocument();
});

describe("test Integration Messagge", () => {
  it("dovrebbe mostrare il messaggio scritto", async () => {
    render(<Home />);
    const inputApiKey = screen.getByPlaceholderText(
      /Scrivi qui la tua ApiKey.../i
    );
    const buttonElement = screen.getByTestId(/SALVA API-KEY/i);

    fireEvent.change(inputApiKey, {
      target: { value: "12345678-1234-1234-1234-123456789012" },
    });

    fireEvent.click(buttonElement);

    const inputElement = screen.getByPlaceholderText(
      /Scrivi qui il tuo messaggio.../i
    );

    const buttonSendElement = screen.getByTestId(/INVIA MESSAGGIO/i);

    fireEvent.change(inputElement, {
      target: { value: "Prova Messaggio" },
    });
    fireEvent.click(buttonSendElement);

    const divElement = screen.getByText(/Prova Messaggio/i);
    expect(divElement).toBeInTheDocument();
  });
});
