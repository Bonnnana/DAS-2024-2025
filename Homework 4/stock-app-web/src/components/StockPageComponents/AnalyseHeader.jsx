// Header.jsx
import React from "react";

const Header = React.memo(function Header({ analyseType, selectedStock }) {
  return (
    <div className="flex justify-between">
      <h2
        className="bg-gradient-to-r from-[rgba(255,255,255,0.36)] to-[#71a383] 
                     w-fit text-lg font-semibold rounded-3xl px-10 py-1"
      >
        {analyseType}
      </h2>
      <h2
        className="w-fit text-lg tracking-wider font-semibold px-8 py-1 
                     border-2 border-black"
      >
        {selectedStock}
      </h2>
    </div>
  );
});

export default Header;
