import { render, screen } from "@testing-library/react";
import CustomButton from "../components/CustomButton";

test("test CustomButton render", () => {
  render(<CustomButton text={"Ciao"} />);
  const linkElement = screen.getByText(/Ciao/i);
  expect(linkElement).toBeInTheDocument();
});
