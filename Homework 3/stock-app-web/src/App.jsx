import React, { useContext, Suspense } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
// import LoadingSpinner from "./components/UI/LoadingSpinner";

import "./App.css";

function App() {
  // const Cart = React.lazy(() => import("./pages/Cart"));
  // const NotFound = React.lazy(() => import("./pages/NotFound"));
  const Main = React.lazy(() => import("./pages/MainPage"));
  const Stocks=React.lazy(() => import("./pages/StockPage"))
  const MostLiquid=React.lazy(()=> import("./pages/MostLiquid"))
  return (
    <>
      <BrowserRouter>
        <Suspense
          fallback={
            <div className="w-full h-screen pt-[20%]">
              {/* <LoadingSpinner /> */}
            </div>
          }
        >
          <Routes>
            <Route path="/" element={<Main />} />
            <Route path="/stocks" element={<Stocks />}>
              <Route path="/stocks/:stockId" element={<Stocks />}></Route>
            </Route>
            <Route path="/mostListedStocks" element={<MostLiquid />} />
            {/* <Route path="*" element={<NotFound />} /> */}
          </Routes>
        </Suspense>
      </BrowserRouter>
    </>
  );
}

export default App;
