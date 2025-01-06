import React, { useState, useCallback } from "react";
import { getTechnical } from "../../dataStorage/api";
import useHttp from "../../dataStorage/use-http";

import AnalyseHeader from './AnalyseHeader'
import AnalyseButtons from "./AnalyseButtons";
import AnalyseBody from './AnalyseBody';

const Analyse = (props) => {
  const { sendRequest, status, data, error } = useHttp(getTechnical, true);
  const [submitResponse, setSubmitResponse] = useState(false);

  // Memoize the button click handler so that
  // it doesn't get re-created on every render
  const handleButtonClick = useCallback(
    (timeframe) => {
      setSubmitResponse(false);
      const requestData = {
        selectedStock: props.selectedStock,
        days: timeframe,
      };
      sendRequest(requestData);
      setSubmitResponse(true);
    },
    [props.selectedStock, sendRequest]
  );

  return (
    <div className="rounded-md items-center py-6 px-6 w-[90%] bg-white shadow-md mx-auto">
      <AnalyseHeader
        analyseType={props.analyseType}
        selectedStock={props.selectedStock}
      />

      <AnalyseButtons onButtonClick={handleButtonClick} />

      <AnalyseBody
        submitResponse={submitResponse}
        data={data}
        status={status}
        error={error}
      />
    </div>
  );
};

export default Analyse;
