import Select from "react-dropdown-select";
import React, { useState, useEffect } from "react";
import useHttp from "../../dataStorage/use-http";
import { getAllIssuers } from "../../dataStorage/api";

const DropDown = (props) => {
  const { sendRequest, status, data, error } = useHttp(getAllIssuers, true);

  useEffect(() => {
    sendRequest(); // Send request on component mount
  }, [sendRequest]); // Empty dependency array to ensure it only runs once

  if(status=="pending"){
    return(
    <div className="text-center py-4">Loading data...</div>
    );
  };
  if(status == "completed" && data!=null && data.length>0){
     return (
       <Select
         className="px-4 py-2 text-gray-700 bg-gray-100 focus:none border-gray-300 rounded-lg focus:outline-none focus:ring-0.5 focus:ring-primary focus:border-primary transition duration-150 ease-in-out"
         options={data}
         onChange={props.changeSelectedValue}
         placeholder="Избери акција"
       />
     );
  };
  

 
};

export default DropDown;
