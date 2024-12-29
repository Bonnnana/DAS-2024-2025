import useHttp from "../../dataStorage/use-http";
import { getMostLiquid } from "../../dataStorage/api";
import { useEffect } from "react";
import { StockUp, StockDown } from "../../assets/icons/icons";

function Table(props) {
  const { sendRequest, status, data, error } = useHttp(getMostLiquid, true);

  const getChangeIndicator = (percentChange) => {
    const value = parseFloat(percentChange?.replace(",", "."));
    if (isNaN(value)) return null;

    if (value > 0) {
      return (
        <div className="w-5 h-5">
          <StockUp width="30" height="30" />
        </div>
      );
    }
    if (value < 0) {
      return (
        <div className="w-5 h-5">
          <StockDown width="30" height="30" />
        </div>
      );
    }
    if (value === 0.0) {
      return (
        <div className="w-5 mx-auto h-0.5 block bg-gray-500 rounded-lg"></div>
      );
    }
  };

  useEffect(() => {
    sendRequest();
  }, [props]); // Trigger request whenever props change

  useEffect(() => {
    if (data) {
      console.log(data); // Log the data separately
    }
  }, [data]);

  return (
    <>
      <p className="font-semibold text-xl text-white py-2">
        Најликвидни акции 
      </p>
      {status==="pending" && (
        <div className="text-center py-4">Loading data...</div>)}
        
      {status === "completed" && data != null && (
        <div className="shadow-lg overflow-hidden border border-gray-200 rounded-lg block">
          <table className="min-w-full overflow-auto rounded-lg ">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-3 py-3 text-center text-xs font-medium text-gray-500 uppercase">
                  Шифра
                </th>
                <th className="px-3 py-3 text-center text-xs font-medium text-gray-500 uppercase">
                  Просечна цена
                </th>
                <th className="px-3 py-3 text-center text-xs font-medium text-gray-500 uppercase">
                  Промена во %
                </th>
                <th></th>
                <th className="px-3 py-3 text-center text-xs font-medium text-gray-500 uppercase">
                  Промет во БЕСТ
                </th>
              </tr>
            </thead>
            <tbody className="bg-white">
              {data.map((row, index) => (
                <tr key={index} className="border-b hover:bg-gray-50">
                  <td className="px-3 py-4 text-xs text-center font-medium text-gray-900">
                    {row.ISSUER}
                  </td>
                  <td className="px-3 py-4 text-xs text-center font-medium text-gray-900">
                    {row.AVG_PRICE}
                  </td>
                  <td className="px-3 py-4 text-xs text-center">
                    {row.PERCENT_CHANGE}
                  </td>
                  <td className="px-3 py-4 text-xs text-center">
                    {getChangeIndicator(row.PERCENT_CHANGE)}
                  </td>
                  <td className="px-3 py-4 text-xs text-center text-gray-500">
                    {row.TOTAL_TURNOVER}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </>
  );
}

export default Table;
