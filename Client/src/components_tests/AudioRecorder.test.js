import AudioRecorder from "../components/AudioRecorder";
import { fireEvent, render, screen } from "@testing-library/react";
import { act } from "react-dom/test-utils";
import { AudioContext } from "standardized-audio-context-mock";
global.AudioContext = AudioContext;
const mediaDevicesMock = {
  enumerateDevices: jest.fn().mockImplementation(() => Promise.resolve()),
  getUserMedia: jest
    .fn()
    .mockImplementation(async () =>
      Promise.resolve(availabilitySuccessMockData)
    ),
};
global.navigator.mediaDevices = mediaDevicesMock; // here

test("test AudioRecorder render", () => {
  render(<AudioRecorder />);
  const linkElement = screen.getByText(/Registra/i);
  expect(linkElement).toBeInTheDocument();
});

describe("test Integration Messagge", () => {
  it("test per verificare avvio registrazione", async () => {
    /*const mockCallback = jest.fn(() => Promise.resolve());

    act(() => {
      render(<AudioRecorder changeMessage={mockCallback} hidden={!true} />);
    });

    const buttonElement = screen.getByTestId(/Registra/i);
    expect(buttonElement).toHaveClass("msger-rec-start");
    act(() => {
      buttonElement.dispatchEvent(new MouseEvent("click", { bubbles: true }));
    });*/
  });
});
