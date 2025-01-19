import {StockUp, StockDown} from "../../assets/icons/icons";

const FundamentalBody = (props) => {
    const getBackgroundColor = (tmp) => {
        switch (tmp) {
            case "BUY":
                return "#008000";
            case "SELL":
                return "#b91c1c"; // red-700 in Tailwind is #b91c1c
            default:
                return "#9ca3af"; // Or any default color you want
        }
    };
    if (props.status === "pending") {
        return <div className="text-center py-4">Loading data...</div>;
    }

    if (props.status === "completed" && props.data.error != null) {
        return (
            <div className="text-center font-semibold text-red-600 py-4">
                ГРЕШКА! НЕМАМЕ НИКАКВИ ПОДАТОЦИ!
            </div>
        );
    }
    if (
        props.status === "completed" &&
        (!props.data || props.data.length === 0)
    ) {
        return <div className="text-center py-4">No data available.</div>;
    }
    if (props.status === "completed" && props.data != null) {
        console.log(props.data);
        return (
            <div>
                <div className="w-full flex justify-center">
          <span
              style={{backgroundColor: getBackgroundColor(props.data.signal)}}
              className={`text-white px-12 py-2 font-bold text-xl mt-10 mx-auto border border-black rounded-lg`}
          >
            {props.data.signal}
          </span>
                </div>
                <div className="flex w-full pt-10">
                    <div className=" w-full flex items-center px-20">
                        <img
                            src={`data:image/png;base64,${props.data.image}`}
                            className="w-full"
                            alt="Stock Price Trends"
                        />
                    </div>
                    <div className="w-full flex items-center px-10">
                        <img
                            src={`data:image/png;base64,${props.data.image2}`}
                            className="w-full"
                            alt="Stock Price Trends"
                        />
                    </div>
                </div>
            </div>
        );
    }
};

export default FundamentalBody;
