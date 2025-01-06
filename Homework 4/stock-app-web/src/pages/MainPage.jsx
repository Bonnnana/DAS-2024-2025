import Layout from "../components/Layout/Layout"
import picture from "../assets/stockdata.png"

function Main() {


    return (
      <Layout>
        <div className="flex text-center z-10 text-[#e9e9e9] ">
          <div className="w-[50%]  px-10  h-full  mt-24  ml-[2%]">
            <h1 className="mx-auto text-3xl font-bold">
              МАКЕДОНСКАТА БЕРЗА НА ДОФАТ НА ВАШИОТ ЕКРАН
            </h1>
            <hr className=" bg-[#bbbbbb] mx-auto w-5/6 h-[2px] mt-3 border-none" />
            <p className="mt-3 ">АНАЛИЗА, ПРЕДВИДУВАЊЕ, УСПЕХ!</p>
          </div>
          <img
            src={picture}
            className="w-[65%] absolute right-0 top-6 z-0"
            alt="stockdata-image"
          />
        </div>
      </Layout>
    );
}

export default Main;
