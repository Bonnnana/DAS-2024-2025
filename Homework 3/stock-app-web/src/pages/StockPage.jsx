import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Layout from "../components/Layout/Layout";
import Table from "../components/StockTable/Table";
import DropDown from "../components/StockPageComponents/DropDown";
import useHttp from "../dataStorage/use-http";
import { getCertainIssuer } from "../dataStorage/api";
import Analyse from "../components/StockPageComponents/Analyse";
import Predict from "../components/StockPageComponents/Predict";
import Fundamental from "../components/StockPageComponents/Fundamental";

function Stocks() {
  const [selectedStock, setSelectedStock] = useState(null);
  const [submitResponse, setSubmitResponse] = useState(false);
  const [technical, setTechnical] = useState(false); // State to trigger table rendering
  const [predict, setPredict] = useState(false); // State to trigger table rendering
  const[fundamental,setFundamental]=useState(false);
  const [startDate, setStartDate] = useState(""); // State for start date
  const [endDate, setEndDate] = useState(""); // State for end date
  const [stockTechnical, setstockTechnical] = useState(null);
  const [stockPredict, setstockPredict] = useState(null);
  const [stockFundamental,setstockFundamental]=useState(null);
  // Custom hook for API request
  const { sendRequest, status, data, error } = useHttp(getCertainIssuer, true);

  // const navigate = useNavigate();
  // const { stockId } = useParams();

  // Only set selected stock from URL param if it's not already set
  // useEffect(() => {
  //   if (stockId) {
  //     setSelectedStock(stockId);
  //   }
  // }, [stockId]);

  // Update selected stock only after clicking the button
  const changeSelectedValue = (selVal) => {
    const newValue = selVal[0].value;
    setSelectedStock(newValue);
  };

  // Handle button click to trigger table rendering and data fetching
  const handleButtonClick = () => {
    if (selectedStock) {
      // Reset submitResponse to false to trigger re-render of the table
      setSubmitResponse(false);
      // Log the values before calling sendRequest
      const requestData = {
        selectedStock: selectedStock,
        startDate: startDate,
        endDate: endDate,
      };
      setstockFundamental(selectedStock)
      setstockTechnical(selectedStock);
      setstockPredict(selectedStock);
      setTechnical(false);
      setFundamental(false);
      setPredict(false);
      // Trigger API request to fetch new data
      sendRequest(requestData);

      // After the API request is mad e, set submitResponse to true to display the table
      setSubmitResponse(true);
    }
  };
  const handleTechnicalButtonClick = () => {
    if (submitResponse && stockTechnical != null) {
      setPredict(false);
      setFundamental(false);
      setTechnical(true);
    }
  };
  const handlePredictButtonClick = () => {
    if (submitResponse && stockPredict != null) {
      setTechnical(false);
      setFundamental(false);
      setPredict(true);
    }
  };
  const handleFundamentalButtonClick = () => {
    if (submitResponse && stockFundamental != null) {
      setTechnical(false);
      setPredict(false);
      setFundamental(true);
    }
  };
  ;

  return (
    <Layout>
      <div className="pb-10 flex px-6 items-center ">
        <div className="rounded-md items-center mt-5 py-4 px-6 w-[80%] bg-neutral-400 shadow-md mx-auto">
          <>
            <div className="flex flex-wrap md:flex-nowrap">
              <div className="md:w-1/2 w-full px-4 pr-12">
                <p className="pb-2 font-semibold text-white">ИЗБЕРЕТЕ АКЦИЈА</p>
                <DropDown changeSelectedValue={changeSelectedValue} />
              </div>
              <div className="lg:w-1/2 font-semibold text-white">
                <p className="pb-2">ИЗБЕРЕТЕ ДАТУМ</p>
                <div className="flex items-center flex-wrap lg:flex-nowrap">
                  <label className="pr-3">ОД:</label>
                  <input
                    type="date"
                    id="startDate"
                    name="startDate"
                    className="block w-full px-2 py-1 text-gray-500 bg-gray-100 border border-gray-300 rounded-sm focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary transition duration-150 ease-in-out"
                    value={startDate}
                    onChange={(e) => setStartDate(e.target.value)}
                  />
                  <label className="pl-6 pr-3">ДО:</label>
                  <input
                    type="date"
                    id="endDate"
                    name="endDate"
                    className="block w-full px-3 py-1 text-gray-500 bg-gray-100 border border-gray-300 rounded-sm focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary transition duration-150 ease-in-out"
                    value={endDate}
                    onChange={(e) => setEndDate(e.target.value)}
                  />
                </div>
              </div>
            </div>
            <div className="w-full flex justify-end pt-3">
              <button
                className="bg-[#344c36] px-10 py-0.5 rounded-md text-white text-md"
                onClick={handleButtonClick}
              >
                ПРИКАЖИ
              </button>
            </div>
          </>
          {/* Render Table only when submitResponse is true and selectedStock is not null */}
          {submitResponse && selectedStock && (
            <div className="block mt-2 pb-6 px-2 w-full mx-auto">
              <Table
                status={status} // Pass status
                data={data} // Pass data
                error={error} // Pass error
                submitResponse={submitResponse} // Pass submitResponse to Table
                startDate={startDate}
                endDate={endDate}
              />
            </div>
          )}
        </div>
        {submitResponse &&
          selectedStock &&
          status === "completed" &&
          data != null && (
            <div className="w-[21rem] pl-4">
              <button
                onClick={handleFundamentalButtonClick}
                className=" w-full bg-[#8fb092] border-2 border-white rounded-md px-2 py-1 text-white font-semibold italic"
              >
                ФУНДАМЕНТАЛНА АНАЛИЗА
              </button>
              <button
                className="w-full bg-[#8fb092] border-2 mt-2 border-white rounded-md px-2 py-1 text-white font-semibold italic"
                onClick={handleTechnicalButtonClick}
              >
                ТЕХНИЧКА АНАЛИЗА
              </button>
              <button
                onClick={handlePredictButtonClick}
                className="w-full bg-[#8fb092] border-2 mt-2 border-white rounded-md px-2 py-1 text-white font-semibold italic"
              >
                ПРЕДВИДУВАЊЕ
              </button>
            </div>
          )}
      </div>

      {technical && stockTechnical && (
        <div className="pb-14">
          <Analyse
            analyseType={"Техничка Анализа"}
            selectedStock={stockTechnical}
          ></Analyse>
        </div>
      )}
      {predict && stockPredict && (
        <div className="pb-14">
          <Predict
            analyseType={"Предвидување"}
            selectedStock={stockPredict}
          ></Predict>
        </div>
      )}
      {fundamental && stockFundamental && (
        <div className="pb-14">
          <Fundamental
            analyseType={"Фундаментална Анализа"}
            selectedStock={stockPredict}
          ></Fundamental>
        </div>
      )}
    </Layout>
  );
}

export default Stocks;
