import useHttp from "../../dataStorage/use-http";
import { getCertainIssuer } from "../../dataStorage/api";
import { useEffect } from "react";


function Table(props) {
  const { sendRequest, status, data, error } = useHttp(getCertainIssuer, true);

  useEffect(() => {
    if(props.selectedValue!=null){
        sendRequest(props.selectedValue);
    }
  }, [props.selectedValue]);
  return (
    <div className="overflow-x-auto shadow-lg rounded-lg border border-gray-200">
      <table className="min-w-full table-auto">
        <thead className="bg-gray-100">
          <tr>
            <th className="px-3 py-3 text-center text-sm font-medium text-gray-500 uppercase">
              #
            </th>
            <th className="px-3 py-3 text-center text-sm font-medium text-gray-500 uppercase">
              Датум
            </th>
            <th className="px-3 py-3 text-center text-sm font-medium text-gray-500 uppercase">
              Цена на последна трансакција
            </th>
            <th className="px-3 py-3 text-center text-sm font-medium text-gray-500 uppercase">
              Максимална цена
            </th>
            <th className="px-3 py-3 text-center text-sm font-medium text-gray-500 uppercase">
              Минимална цена
            </th>
            <th className="px-3 py-3 text-center text-sm font-medium text-gray-500 uppercase">
              Просечна цена
            </th>
            <th className="px-3 py-3 text-center text-sm font-medium text-gray-500 uppercase">
              Промена во %
            </th>
            <th className="px-3 py-3 text-center text-sm font-medium text-gray-500 uppercase"></th>
            <th className="px-3 py-3 text-center text-sm font-medium text-gray-500 uppercase">
              Волумен
            </th>
            <th className="px-3 py-3 text-center text-sm font-medium text-gray-500 uppercase">
              Промет
            </th>
          </tr>
        </thead>
        {props.selectedValue != null &&
          status === "completed" &&
          data.length > 0 && (
            <tbody className="bg-white">
              {data.map((row, index) => (
                <tr key={index} className="border-b hover:bg-gray-50">
                  <td className="px-3 py-4 text-sm text-center font-medium text-gray-900">
                    {row.line_number}
                  </td>
                  <td className="px-3 py-4 text-sm text-center font-medium text-gray-900">
                    {row.DATE}
                  </td>
                  <td className="px-3 py-4 text-sm text-center text-gray-500">
                    {row.LAST_TRADE_PRICE}
                  </td>
                  <td className="px-3 py-4 text-sm text-center text-gray-500">
                    {row.MAX_PRICE}
                  </td>
                  <td className="px-3 py-4 text-sm text-center text-gray-500">
                    {row.MIN_PRICE}
                  </td>
                  <td className="px-3 py-4 text-sm text-center text-gray-500">
                    {row.AVG_PRICE}
                  </td>
                  <td className="px-3 py-4 text-sm text-center text-gray-500">
                    {row.PERCENT_CHANGE}
                  </td>
                  <td className="px-3 py-4 text-sm text-center text-gray-500">
                    {
                      parseFloat(row.PERCENT_CHANGE.replace(",", ".")) > 0.0 ? (
                        <span className="block w-12 h-4 text-xs font-medium text-green-800 border-2 border-green-800 bg-green-200 rounded-full"></span>
                      ) : parseFloat(row.PERCENT_CHANGE.replace(",", ".")) <
                        0.0 ? (
                        <span className=" block w-12 h-4 text-xs font-medium text-red-800 border-2 border-red-800 bg-red-200 rounded-full"></span>
                      ) : (
                        <span></span>
                      )
                      //(
                      //   <span className="block w-12 h-5 text-xs font-medium text-gray-800 bg-gray-200  border-2 border-red-800 rounded-full">
                      //     Not Changed
                      //   </span>
                      //)
                    }
                  </td>
                  <td className="px-3 py-4 text-sm text-center text-gray-500">
                    {row.VOLUME}
                  </td>
                  <td className="px-3 py-4 text-sm text-center text-gray-500">
                    {row.TOTAL_TURNOVER}
                  </td>
                </tr>
              ))}
            </tbody>
          )}
      </table>
    </div>
  );
}

export default Table;
