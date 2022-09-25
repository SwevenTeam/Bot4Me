import { FaRegPaperPlane } from "react-icons/fa";
import { FaMicrophoneAlt } from "react-icons/fa";
import { FaUserLock } from "react-icons/fa";
import { FaSave } from "react-icons/fa";
import { FaTrashAlt } from "react-icons/fa";
import { FaUndo } from "react-icons/fa";
import { FaUserSlash } from "react-icons/fa";

const Send = () => <FaRegPaperPlane title="Icon" />;
const Rec = () => <FaMicrophoneAlt title="Icon" />;
const Login = () => <FaUserLock title="Icon" />;
const Save = () => <FaSave title="Icon" />;
const Trash = () => <FaTrashAlt title="Icon" />;
const Delete = () => <FaUndo title="Icon" />;
const Logout = () => <FaUserSlash title="Icon" />;

const CustomIcon = {
  Send,
  Rec,
  Login,
  Save,
  Trash,
  Delete,
  Logout,
};
export default CustomIcon;
