import { useEffect,useState } from "react";
const AnalyseBody = (props) =>{
    const [sell, setSell] = useState("");
    const getBackgroundColor = (tmp) => {
      switch (tmp) {
        case "BUY":
          return "#004aad";
        case "HOLD":
          return "#9ca3af"; // neutral-400 in Tailwind is #9ca3af
        case "SELL":
          return "#b91c1c"; // red-700 in Tailwind is #b91c1c
        default:
          return "#9ca3af"; // Or any default color you want
      }
    };
    useEffect(() => {
      if (props.status === "completed") {
        setSell(props.data["final_recommendation"] || ""); // Update sell when data is available
      }
    }, [props.status]);
    if(props.status==="completed" && props.data!=null){
        return (
          <>
            <div className="w-full  flex justify-center flex-wrap">
              <div className="w-full flex justify-center">
                <span
                  style={{ backgroundColor: getBackgroundColor(sell) }}
                  className={`text-white px-12 py-2 font-bold text-xl mt-10 mx-auto border border-black rounded-lg`}
                >
                  {sell}
                </span>
              </div>
              <div className="w-[40%] flex justify-around">
                <div className="w-fit  py-2 px-4 text-center">
                  <p className=" text-lg font-medium text-black">Sell</p>
                  <p className="">{props.data.signal_counts.SELL}</p>
                </div>
                <div className="w-fit py-2 px-4 text-center">
                  <p className=" text-lg font-medium text-black">Hold</p>
                  <p className="">{props.data.signal_counts.HOLD}</p>
                </div>
                <div className="w-fit py-2 px-4 text-center">
                  <p className=" text-lg font-medium text-black">Buy</p>
                  <p className="">{props.data.signal_counts.BUY}</p>
                </div>
              </div>
            </div>
            <div className="w-[90%] mx-auto flex flex-wrap md:flex-nowrap">
              <div className="w-full pr-8">
                <p className="text-lg py-2 font-medium">Осцилатори</p>
                <table className="min-w-full overflow-auto rounded-lg ">
                  <thead className="bg-gray-100 border-y-[1px] border-black">
                    <tr>
                      <th className="px-3 py-3 text-center text-sm font-medium text-gray-700 uppercase">
                        Име
                      </th>
                      <th className="px-3 py-3 text-center text-sm font-medium text-gray-700 uppercase">
                        Вредност
                      </th>
                      <th className="px-3 py-3 text-center text-sm font-medium text-gray-700 uppercase">
                        Сигнал
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white">
                    {props.data.oscillator_summary.map((row, index) => (
                      <tr
                        key={index}
                        className="border-b border-black hover:bg-gray-50"
                      >
                        <th className="px-3 py-2.5 text-center text-xs font-medium text-gray-700 uppercase">
                          {row.text}
                        </th>
                        <th className="px-3 py-2.5 text-center text-xs font-medium text-gray-700 uppercase">
                          {row.value}
                        </th>
                        <th
                          style={{ color: getBackgroundColor(row.signal) }}
                          className="px-3 py-2.5 text-center text-sm font-bold uppercase"
                        >
                          {row.signal}
                        </th>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <div className="w-full pl-8">
                <p className="text-lg py-2 font-medium">Moving Averages</p>
                <table className="min-w-full overflow-auto rounded-lg ">
                  <thead className="bg-gray-100 border-y-[1px] border-black">
                    <tr>
                      <th className="px-3 py-3 text-center text-sm font-medium text-gray-700 uppercase">
                        Име
                      </th>
                      <th className="px-3 py-3 text-center text-sm font-medium text-gray-700 uppercase">
                        Вредност
                      </th>
                      <th className="px-3 py-3 text-center text-sm font-medium text-gray-700 uppercase">
                        Сигнал
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white">
                    {props.data.moving_average_summary.map((row, index) => (
                      <tr
                        key={index}
                        className="border-b border-black hover:bg-gray-50"
                      >
                        <th className="px-3 py-2.5 text-center text-xs font-medium text-gray-700 uppercase">
                          {row.text}
                        </th>
                        <th className="px-3 py-2.5 text-center text-xs font-medium text-gray-700 uppercase">
                          {row.value}
                        </th>
                        <th
                          style={{ color: getBackgroundColor(row.signal) }}
                          className="px-3 py-2.5 text-center text-sm font-bold uppercase"
                        >
                          {row.signal}
                        </th>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </>
        );
    }
    if (props.status === "completed" && props.error) {
      return (
        <div className="text-center font-semibold text-red-600 py-4">
          ГРЕШКА!
        </div>
      );
    }
    
}

export default AnalyseBody;