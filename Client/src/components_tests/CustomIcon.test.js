import { render, screen } from "@testing-library/react";
import CustomIcon from "../components/CustomIcon";

test("test CustonIcon render", () => {
  const ButtonIcon = CustomIcon["Rec"];
  render(<ButtonIcon />);
  const linkElement = screen.getByTitle("Icon");
  expect(linkElement).toBeInTheDocument();
});
