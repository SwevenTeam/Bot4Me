import {FaRegPaperPlane} from "react-icons/fa"
import {FaMicrophoneAlt} from "react-icons/fa"
import {FaUserLock} from "react-icons/fa"
import {FaSave} from "react-icons/fa"
import { FaTrashAlt } from "react-icons/fa"
import {FaUndo} from "react-icons/fa"
import {FaUserSlash} from "react-icons/fa"


const Send = () => <FaRegPaperPlane/>;
const Rec = () => <FaMicrophoneAlt/>;
const Login = () => <FaUserLock/>
const Save = () => <FaSave/>
const Trash = () => <FaTrashAlt/>
const Delete = () => <FaUndo/>
const Logout = () => <FaUserSlash/>

const CustomIcon = {
  Send,
  Rec,
  Login,
  Save,
  Trash,
  Delete,
  Logout
}
export default CustomIcon;