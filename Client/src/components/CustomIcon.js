import {FaRegPaperPlane} from "react-icons/fa"
import {FaMicrophoneAlt} from "react-icons/fa"
import {FaUserCog} from "react-icons/fa"
import {FaSave} from "react-icons/fa"
import { FaTrashAlt } from "react-icons/fa"
import {FaUndo} from "react-icons/fa"


const Send = () => <FaRegPaperPlane/>;
const Rec = () => <FaMicrophoneAlt/>;
const UserConf = () => <FaUserCog/>
const Save = () => <FaSave/>
const Trash = () => <FaTrashAlt/>
const Delete = () => <FaUndo/>

const CustomIcon = {
  Send,
  Rec,
  UserConf,
  Save,
  Trash,
  Delete
}
export default CustomIcon;