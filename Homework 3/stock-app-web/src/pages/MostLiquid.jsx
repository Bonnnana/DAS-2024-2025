import Layout from "../components/Layout/Layout";
import MostLiquidTable from "../components/StockTable/MostLiquidTable";

function Main() {
  return (
    <Layout>
      <div className="pb-16">
        <div className="rounded-md block mt-5 pt-2 pb-8 sm:px-8 px-2 w-[75%] bg-neutral-400 shadow-md mx-auto">
          <MostLiquidTable />
        </div>
      </div>
    </Layout>
  );
}

export default Main;
