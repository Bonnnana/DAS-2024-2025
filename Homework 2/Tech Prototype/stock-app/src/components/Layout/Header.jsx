import { NavLink } from "react-router-dom";
// import logo from "../../assets/logo.png";

const Header = () => {
    const spanClass =
      "text-textColor pb-2 px-4 hover:text-white hover:border-b-2 hover:border-textColor";
  return (
    <header className="bg-primary top-0 pr-4 py-4">
      <div className="flex justify-between  items-center">
        <div className="flex items-center px-10 justify-center rounded-tr-full py-1 rounded-br-full bg-gradient-to-r from-gray-300 to-gray-500">
          <NavLink to="/">
            {/* <img src="" className="h-[4.5rem] pl-3 md:pl-14" alt="logo" /> */}
            <span className="text-[#1c2b30] font-bold text-[22px]">
              Stock View
            </span>
          </NavLink>
        </div>
        <div className=" md:w-2/5 flex justify-evenly md:text-xl text-l  ">
          <NavLink to="/">
            <span className={spanClass}>Почетна</span>
          </NavLink>
          <NavLink to="/stocks">
            <span className={spanClass}>Акции</span>
          </NavLink>
          <NavLink to="/mostListedStocks">
            <span className={spanClass} >Најтргувани акции</span>
          </NavLink>
        </div>
      </div>
    </header>
  );
};

export default Header;
