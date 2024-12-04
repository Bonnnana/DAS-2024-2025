import React, { useState } from "react";
import Layout from "../components/Layout/Layout";
import Select from "react-dropdown-select";
import useHttp from "../dataStorage/use-http";
import { getAllIssuers } from "../dataStorage/api";
import { useEffect } from "react";
import Table from "../components/StockTable/Table";
function Stocks() {

  const [selectedStock, setSelectedStock] = useState(null);
  const { sendRequest, status, data, error } = useHttp(getAllIssuers, true);
  
  useEffect(() => {
    sendRequest();
  }, []);
  
  const changeSelectedValue = (selVal) => {
    setSelectedStock(selVal[0].value);
  };


  return (
    <div className="bg-neutral-200 min-h-screen">
      <Layout>
        <div className="rounded-md block mt-5 py-4 sm:px-8 px-2 w-[95%] bg-white shadow-md mx-auto">
          {/* {status === "pending" && <span>...</span>} */}
          {status === "completed" &&
            data != null &&
            data.length > 0 &&
            !error && (
              <div>
                <Select
                  options={data}
                  onChange={(selectedValue) =>
                    changeSelectedValue(selectedValue)
                  }
                />
              </div>
            )}
        </div>

        <div className="rounded-md block mt-5 py-4 min-h-[60vh] sm:px-8 px-2 w-[95%] bg-white shadow-md mx-auto">
          <Table selectedValue={selectedStock} ></Table>
        </div>
      </Layout>
    </div>
  );
}

export default Stocks;
