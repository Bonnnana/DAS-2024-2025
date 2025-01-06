import React, { memo, useState, useEffect } from "react";
import { StockDown, StockUp } from "../../assets/icons/icons";

const Table = (props) => {
  const [currentPage, setCurrentPage] = useState(1); // Current page state
  const [loading, setLoading] = useState(true); // Loading state
  const [data, setData] = useState([]); // Local data state to manage the data after fetching
  const rowsPerPage = 10; // Number of rows per page

  // Helper function to determine change indicator style
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

  // Function to change the current page
  const handlePageChange = (newPage) => {
    if (newPage > 0 && newPage <= totalPages) {
      setCurrentPage(newPage);
    }
  };

  // Calculate pagination info after data is fetched
  const totalPages = Math.ceil(data.length / rowsPerPage);
  const startIndex = (currentPage - 1) * rowsPerPage;
  const currentPageData = data.slice(startIndex, startIndex + rowsPerPage);

  // Handle API data fetching
  useEffect(() => {
    if (props.data && props.data.length > 0) {
      setData(props.data); // Set the fetched data once available
      setLoading(false); // Set loading to false once data is fetched
    } else {
      setLoading(true); // Keep loading state true if no data
    }
  }, [props.data]); // This will trigger every time `props.data` changes

  // Reset currentPage to 1 whenever the component is re-rendered or data changes
  useEffect(() => {
    setCurrentPage(1);
  }, [props.data]);

  // Render based on status
  if (loading && props.status==="pending") {
    return <div className="text-center py-4">Loading data...</div>;
  }

  if (props.status === "completed" && props.error) {
    return (
      <div className="text-center font-semibold text-red-600 py-4">ГРЕШКА! ЗА ВНЕСЕНИТЕ ДАТИ НЕМАМЕ НИКАКВИ ПОДАТОЦИ!</div>
    );
  }

  if (
    props.status === "completed" &&
    (!props.data || props.data.length === 0)
  ) {
    return <div className="text-center py-4">No data available.</div>;
  }

  return (
    <>
        {props.data && props.data.length > 0 && (
          <p className="font-semibold text-white py-2">
            ИЗБЕРЕНА АКЦИЈА:{" "}
            <span className="font-bold pl-1 text-xl text-primary">
              {props.data[0].ISSUER}
            </span>
          </p>
        )}
      <div className="shadow-lg overflow-hidden border border-gray-200 rounded-lg block">
        <table className="min-w-full  overflow-auto rounded-lg ">
          <thead className="bg-gray-100">
            <tr>
              <th className="px-3 py-2 text-center text-xs font-medium text-gray-500 uppercase">
                #
              </th>
              <th className="px-3 py-2 text-center text-xs font-medium text-gray-500 uppercase">
                Датум
              </th>
              <th className="px-3 py-2 text-center text-xs font-medium text-gray-500 uppercase">
                Цена на последна трансакција
              </th>
              <th className="px-3 py-2 text-center text-xs font-medium text-gray-500 uppercase">
                Максимална цена
              </th>
              <th className="px-3 py-2 text-center text-xs font-medium text-gray-500 uppercase">
                Минимална цена
              </th>
              <th className="px-3 py-2 text-center text-xs font-medium text-gray-500 uppercase">
                Просечна цена
              </th>
              <th className="px-3 py-2 text-center text-xs font-medium text-gray-500 uppercase">
                Промена во %
              </th>
              <th></th>
              <th className="px-3 py-2 text-center text-xs font-medium text-gray-500 uppercase">
                Волумен
              </th>
              <th className="px-3 py-2 text-center text-xs font-medium text-gray-500 uppercase">
                Промет
              </th>
            </tr>
          </thead>
          <tbody className="bg-white">
            {currentPageData.map((row, index) => (
              <tr key={index} className="border-b hover:bg-gray-50">
                <td className="px-3 py-2 text-xs text-center font-medium text-gray-900">
                  {row.line_number}
                </td>
                <td className="px-3 py-2 text-xs text-center font-medium text-gray-900">
                  {row.DATE}
                </td>
                <td className="px-3 py-2 text-xs text-center text-gray-500">
                  {row.LAST_TRADE_PRICE}
                </td>
                <td className="px-3 py-2 text-xs text-center text-gray-500">
                  {row.MAX_PRICE}
                </td>
                <td className="px-3 py-2 text-xs text-center text-gray-500">
                  {row.MIN_PRICE}
                </td>
                <td className="px-3 py-2 text-xs text-center text-gray-500">
                  {row.AVG_PRICE}
                </td>
                <td className="px-3 py-2 text-xs text-center">
                  {row.PERCENT_CHANGE}
                </td>
                <td className="px-3 py-2 text-xs text-center">
                  {getChangeIndicator(row.PERCENT_CHANGE)}
                </td>
                <td className="px-3 py-2 text-xs text-center text-gray-500">
                  {row.VOLUME}
                </td>
                <td className="px-3 py-2 text-xs text-center text-gray-500">
                  {row.TOTAL_TURNOVER}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination Controls */}
      <div
        className={`flex justify-between items-center py-4 ${
          totalPages === 1 ? "hidden" : ""
        }`}
      >
        <button
          onClick={() => handlePageChange(currentPage - 1)}
          disabled={currentPage === 1}
          className="px-4 py-2 text-white bg-primary rounded-md disabled:bg-gray-400"
        >
          Previous
        </button>
        <div className="text-sm text-white">
          Page {currentPage} of {totalPages}
        </div>
        <button
          onClick={() => handlePageChange(currentPage + 1)}
          disabled={currentPage === totalPages}
          className="px-4 py-2 text-white bg-primary rounded-md disabled:bg-gray-400"
        >
          Next
        </button>
      </div>
    </>
  );
};

export default memo(Table);
