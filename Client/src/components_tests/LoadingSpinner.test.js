import { render, screen } from "@testing-library/react";
import LoadingSpinner from "../components/LoadingSpinner";

test("test CustomButton render", () => {
  render(<LoadingSpinner />);
  const element = screen.getByTestId(/Loading Spinner/i);
  expect(element).toBeInTheDocument();
});
