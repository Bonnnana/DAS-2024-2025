import React, {useEffect} from "react";
import {getPrediction} from "../../dataStorage/api";
import useHttp from "../../dataStorage/use-http";
import AnalyseHeader from './AnalyseHeader';
import PredictBody from "./PredictBody";

const Predict = (props) => {
    const {sendRequest, status, data, error} = useHttp(getPrediction, true);
    useEffect(() => {
        sendRequest(props.selectedStock); // Pass the selected stock to the API request
    }, [sendRequest, props.selectedStock]);


    return (
        <div className="rounded-md items-center py-6 px-6 w-[90%] bg-white shadow-md mx-auto">
            <AnalyseHeader
                analyseType={props.analyseType}
                selectedStock={props.selectedStock}
            ></AnalyseHeader>
            <PredictBody
                data={data}
                status={status}
                error={error}
            />
        </div>
    );
};

export default Predict;
