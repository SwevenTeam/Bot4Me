import { fireEvent, render, screen } from "@testing-library/react";
import Home from "../components/Home";

test("test Home render", () => {
  render(<Home />);
  const linkElement = screen.getByText(/Ciao sono il tuo assistente Bot4Me/i);
  expect(linkElement).toBeInTheDocument();
});

describe("test Integration Messagge", () => {
  it("test per mostrare il messaggio scritto", async () => {
    render(<Home />);
    const inputApiKey = screen.getByTestId(/apikeyInput/i);
    const buttonElement = screen.getByTestId(/SALVA API-KEY/i);
    fireEvent.change(inputApiKey, {
      target: { value: "" },
    });
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

  it("test per cancellare API-KEY scritta", async () => {
    render(<Home />);
    const inputApiKey = screen.getByTestId(/apikeyInput/i);
    fireEvent.change(inputApiKey, {
      target: { value: "" },
    });
    fireEvent.change(inputApiKey, {
      target: { value: "12345678-1234-1234-1234-123456789012" },
    });
    const buttonElement = screen.getByTestId(/CANCELLA API-KEY/i);

    fireEvent.change(inputApiKey, {
      target: { value: "12345678-1234-1234-1234-123456789012" },
    });

    fireEvent.click(buttonElement);

    const inputElement = screen.getByPlaceholderText(
      /Scrivi qui la tua ApiKey.../i
    );

    expect(inputElement).toBeInTheDocument();
  });

  it("test per cancellare il messaggio scritto", async () => {
    render(<Home />);
    const inputApiKey = screen.getByTestId(/apikeyInput/i);
    const buttonElement = screen.getByTestId(/SALVA API-KEY/i);
    fireEvent.change(inputApiKey, {
      target: { value: "" },
    });
    fireEvent.change(inputApiKey, {
      target: { value: "12345678-1234-1234-1234-123456789012" },
    });

    fireEvent.click(buttonElement);

    const inputElement = screen.getByPlaceholderText(
      /Scrivi qui il tuo messaggio.../i
    );

    const buttonSendElement = screen.getByTestId(/CANCELLA MESSAGGIO/i);

    fireEvent.change(inputElement, {
      target: { value: "Prova Messaggio Da Cancellare" },
    });

    fireEvent.click(buttonSendElement);

    const divElement = screen.getByPlaceholderText(
      /Scrivi qui il tuo messaggio.../i
    );
    expect(divElement).toBeInTheDocument();
  });

  it("test per effettuare il logout", async () => {
    render(<Home />);
    const inputApiKey = screen.getByTestId(/apikeyInput/i);
    const buttonElement = screen.getByTestId(/SALVA API-KEY/i);
    fireEvent.change(inputApiKey, {
      target: { value: "" },
    });
    fireEvent.change(inputApiKey, {
      target: { value: "12345678-1234-1234-1234-123456789012" },
    });

    fireEvent.click(buttonElement);

    const buttonSendElement = screen.getByTestId(/LOGOUT/i);

    fireEvent.click(buttonSendElement);

    const divElement = screen.getByTestId(/API KEY/i);
    expect(divElement).toBeInTheDocument();
  });

  it("test per verificare la trascrizione di un messaggio", async () => {
    render(<Home />);
    functionToMock = jest.fn().mockReturnValue("messaggio tradotto");

    const inputApiKey = screen.getByTestId(/apikeyInput/i);
    const buttonElement = screen.getByTestId(/SALVA API-KEY/i);

    fireEvent.change(inputApiKey, {
      target: { value: "" },
    });

    fireEvent.change(inputApiKey, {
      target: { value: "12345678-1234-1234-1234-123456789012" },
    });

    fireEvent.click(buttonElement);

    const inputElement = screen.getByPlaceholderText(
      /Scrivi qui il tuo messaggio.../i
    );

    fireEvent.change(inputElement, {
      target: { value: functionToMock() },
    });

    const buttonSendElement = screen.getByTestId(/INVIA MESSAGGIO/i);

    fireEvent.click(buttonSendElement);

    const elementToFind = screen.getByText("messaggio tradotto");
    expect(elementToFind).toBeInTheDocument();
  });
});
