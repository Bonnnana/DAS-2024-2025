import { StockUp,StockDown } from "../../assets/icons/icons";

const PredictBody = (props) => {
  const getBackgroundColor = (tmp) => {
    switch (tmp) {
      case "UP":
        return "#008000";
      case "DOWN":
        return "#b91c1c"; // red-700 in Tailwind is #b91c1c
      default:
        return "#9ca3af"; // Or any default color you want
    }
  };
  const getText = (value) =>{
    if (value === "UP") {
      return "расте";
    }
    if (value === "DOWN") {
      return "опаѓа";
    }
  }
  const getArrow = (value) =>{
    if (value === "UP") {
          return (
              <StockUp width="90" height="90" />
          );
        }
        if (value === "DOWN") {
          return <StockDown width="90" height="90" />;
        }
  }
  if (props.status === "pending") {
    return <div className="text-center py-4">Loading data...</div>;
  }

  if (props.status === "completed" && props.error!=null) {
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
  if (props.status === "completed" && props.data!=null) {
    console.log(props.data);
    return (
      <div className="text-center">
        <div className="text-center py-4">
          <p className={` font-semibold text-2xl `}>
            Во следниот период акцијата ќе{" "}
            <span
              className="font-bold text-3xl"
              style={{ color: getBackgroundColor(props.data.prediction) }}
            >
              {getText(props.data.prediction)}
            </span>
          </p>
        </div>
        <p className={` font-semibold text-xl`}>
          Историјат на движење на цената на акцијата
        </p>
        <img
          src={`data:image/png;base64,${props.data.image}`}
          className="w-fit mx-auto px-28"
          alt="Stock Price Trends"
        />
      </div>
    );
  }
  
};

export default PredictBody;
