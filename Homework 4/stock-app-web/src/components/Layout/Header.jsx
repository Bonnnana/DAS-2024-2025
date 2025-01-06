import { NavLink } from "react-router-dom";
import logo from "../../assets/logo.png";

const Header = () => {
    const spanClass =
      "text-textColor pb-2 px-4 hover:text-white hover:border-b-2 hover:border-textColor";
  return (
    <header className="bg-primary pr-4 py-4 z-10 relative ">
      <div className="flex justify-between  items-center">
        <div className="flex items-center justify-center px-4 py-0.5 rounded-tr-full rounded-br-full bg-gradient-to-r from-[#a6a6a6] to-[#ffffff]">
          <NavLink to="/" className="flex items-center relative">
            <img src={logo} className="h-10" alt="logo" />
            <span className="text-[#1c2b30] px-3 font-bold text-2xl ">
              Stock View
            </span>
          </NavLink>
        </div>
        <div className=" md:w-2/5 flex justify-evenly text-l  ">
          <NavLink to="/">
            <span className={spanClass}>Почетна</span>
          </NavLink>
          <NavLink to="/stocks">
            <span className={spanClass}>Акции</span>
          </NavLink>
          <NavLink to="/mostListedStocks">
            <span className={spanClass}>Најтргувани акции</span>
          </NavLink>
        </div>
      </div>
    </header>
  );
};

export default Header;
